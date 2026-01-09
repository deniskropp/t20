"""
This module provides the SQLite3 database manager for the multi-agent runtime.
It handles session and artifact persistence.
"""
import sqlite3
import logging
import json
import os
from typing import Any, Optional, Dict, List
from threading import Lock

logger = logging.getLogger(__name__)

class SessionDB:
    """
    Manages SQLite3 connection and operations for sessions and artifacts.
    """
    _instance = None
    _lock = Lock()

    def __init__(self, db_path: str):
        self.db_path = db_path
        self._init_db()

    @classmethod
    def get_instance(cls, db_path: str = "sessions.db") -> 'SessionDB':
        with cls._lock:
            if cls._instance is None:
                cls._instance = cls(db_path)
            elif cls._instance.db_path != db_path:
                logger.warning(f"SessionDB requested with new path '{db_path}' but already initialized with '{cls._instance.db_path}'. Re-initializing.")
                cls._instance = cls(db_path)
            return cls._instance

    @classmethod
    def _reset_instance(cls):
        """For testing purposes only."""
        with cls._lock:
            if cls._instance:
                try:
                    cls._instance._get_conn().close()
                except:
                    pass
            cls._instance = None

    def _get_conn(self) -> sqlite3.Connection:
        return sqlite3.connect(self.db_path, check_same_thread=False)

    def _init_db(self):
        """Initialize the database schema."""
        conn = self._get_conn()
        try:
            cursor = conn.cursor()
            # Sessions table
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS sessions (
                    id TEXT PRIMARY KEY,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    metadata TEXT
                )
            ''')
            # Artifacts table
            # Content is stored as TEXT (JSON or strings).
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS artifacts (
                    session_id TEXT,
                    name TEXT,
                    content TEXT,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    PRIMARY KEY (session_id, name),
                    FOREIGN KEY(session_id) REFERENCES sessions(id)
                )
            ''')
            conn.commit()
        except sqlite3.Error as e:
            logger.error(f"Database initialization error: {e}")
            raise
        finally:
            conn.close()

    def create_session(self, session_id: str, metadata: Optional[Dict[str, Any]] = None) -> None:
        """Creates a new session record."""
        conn = self._get_conn()
        try:
            cursor = conn.cursor()
            meta_str = json.dumps(metadata) if metadata else "{}"
            cursor.execute(
                "INSERT INTO sessions (id, metadata) VALUES (?, ?)",
                (session_id, meta_str)
            )
            conn.commit()
            logger.debug(f"Session {session_id} created in DB.")
        except sqlite3.IntegrityError:
            logger.warning(f"Session {session_id} already exists.")
        except sqlite3.Error as e:
            logger.error(f"Error creating session {session_id}: {e}")
        finally:
            conn.close()

    def save_artifact(self, session_id: str, name: str, content: Any) -> None:
        """Saves or updates an artifact."""
        conn = self._get_conn()
        try:
            cursor = conn.cursor()
            
            # Ensure session exists (mild safety check, or we could rely on FK constraints if enforced)
            # SQLite doesn't enforce FK by default unless PRAGMA foreign_keys = ON; 
            # We'll just upsert the artifact.
            
            content_str = ""
            if isinstance(content, (dict, list)):
                content_str = json.dumps(content)
            else:
                content_str = str(content)

            cursor.execute('''
                INSERT OR REPLACE INTO artifacts (session_id, name, content)
                VALUES (?, ?, ?)
            ''', (session_id, name, content_str))
            
            conn.commit()
            logger.debug(f"Artifact {name} saved for session {session_id}.")
        except sqlite3.Error as e:
            logger.error(f"Error saving artifact {name} in session {session_id}: {e}")
        finally:
            conn.close()

    def get_artifact(self, session_id: str, name: str) -> Optional[Any]:
        """Retrieves an artifact's content."""
        conn = self._get_conn()
        try:
            cursor = conn.cursor()
            cursor.execute(
                "SELECT content FROM artifacts WHERE session_id = ? AND name = ?",
                (session_id, name)
            )
            row = cursor.fetchone()
            if row:
                content_str = row[0]
                # Try to parse as JSON, otherwise return string
                try:
                    return json.loads(content_str)
                except json.JSONDecodeError:
                    return content_str
            return None
        except sqlite3.Error as e:
            logger.error(f"Error retrieving artifact {name} for session {session_id}: {e}")
            return None
        finally:
            conn.close()

    def list_artifacts(self, session_id: str) -> List[str]:
        """Lists all artifact names for a session."""
        conn = self._get_conn()
        try:
            cursor = conn.cursor()
            cursor.execute(
                "SELECT name FROM artifacts WHERE session_id = ?",
                (session_id,)
            )
            rows = cursor.fetchall()
            return [row[0] for row in rows]
        except sqlite3.Error as e:
            logger.error(f"Error listing artifacts for session {session_id}: {e}")
            return []
        finally:
            conn.close()
