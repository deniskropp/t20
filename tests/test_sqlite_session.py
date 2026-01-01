import pytest
import os
import shutil
import tempfile
import sqlite3
from t20.core.core import Session
from t20.core.db import SessionDB

@pytest.fixture
def temp_project_root():
    # Reset SessionDB before and after
    SessionDB._reset_instance()
    
    # Create a temporary directory for the project root
    temp_dir = tempfile.mkdtemp()
    yield temp_dir
    
    # Cleanup
    SessionDB._reset_instance()
    shutil.rmtree(temp_dir)

def test_session_db_initialization(temp_project_root):
    # Test that SessionDB initializes correctly
    db_path = os.path.join(temp_project_root, "sessions.db")
    db = SessionDB(db_path)
    
    assert os.path.exists(db_path)
    
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    
    # Check tables exist
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='sessions'")
    assert cursor.fetchone() is not None
    
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='artifacts'")
    assert cursor.fetchone() is not None
    
    conn.close()

def test_session_creation(temp_project_root):
    # Test creating a session via Session class
    session = Session(project_root=temp_project_root)
    
    # Check if session is in DB
    db_path = os.path.join(temp_project_root, "sessions", "sessions.db")
    assert os.path.exists(db_path)
    
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    cursor.execute("SELECT id FROM sessions WHERE id=?", (session.session_id,))
    row = cursor.fetchone()
    assert row is not None
    assert row[0] == session.session_id
    conn.close()

def test_artifact_persistence(temp_project_root):
    # Test saving and retrieving artifacts
    session = Session(project_root=temp_project_root)
    
    # Save string artifact
    session.add_artifact("test.txt", "Hello World")
    content = session.get_artifact("test.txt")
    assert content == "Hello World"
    
    # Save JSON artifact
    data = {"key": "value", "list": [1, 2, 3]}
    session.add_artifact("data.json", data)
    retrieved_data = session.get_artifact("data.json")
    assert retrieved_data == data

def test_artifact_persistence_check_db(temp_project_root):
    # Verify directly in DB
    session = Session(project_root=temp_project_root)
    session.add_artifact("direct.txt", "Direct Content")
    
    db_path = os.path.join(temp_project_root, "sessions", "sessions.db")
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    
    cursor.execute("SELECT content FROM artifacts WHERE session_id=? AND name=?", (session.session_id, "direct.txt"))
    row = cursor.fetchone()
    assert row is not None
    assert row[0] == "Direct Content"
    conn.close()
