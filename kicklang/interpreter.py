"""
KickLang Interpreter
--------------------
Executes parsed KickLang commands.
"""

import logging
from typing import List, Dict, Any
from kicklang.parser import KickLangParser

logger = logging.getLogger(__name__)

class KickLangInterpreter:
    def __init__(self):
        self.parser = KickLangParser()

    def execute(self, script_content: str, context: Any = None):
        """
        Parses and executes a KickLang script.
        
        Args:
           script_content (str): The script to execute.
           context (Any): Optional context object (e.g., System or KnowledgeGraph) to operate on.
        """
        commands = self.parser.parse(script_content)
        for command in commands:
            self._execute_command(command, context)

    def _execute_command(self, command: Dict[str, Any], context: Any):
        """
        Executes a single command.
        """
        action = command.get("action")
        params = command.get("params", {})
        
        logger.info(f"Executing KickLang action: {action} with params: {params}")
        
        # Placeholder for actual command logic mapping
        # In the future, this will map to context.kg.add_component, etc.
        if action == "log":
            print(f"KickLang Log: {params.get('message')}")
        else:
            logger.warning(f"Unknown KickLang action: {action}")
