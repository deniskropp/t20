"""
Prompt Store
------------
Manages the loading and retrieval of system prompts.
"""

import os
import logging
from glob import glob
from typing import Dict

logger = logging.getLogger(__name__)

class PromptStore:
    def __init__(self, prompts_dir: str):
        self.prompts_dir = prompts_dir
        self.prompts: Dict[str, str] = {}
        self.load_prompts()

    def load_prompts(self) -> None:
        """
        Loads all system prompts from text files within the specified directory.
        """
        logger.info(f"Loading prompts from: {self.prompts_dir}")
        if not os.path.isdir(self.prompts_dir):
            logger.warning(f"Prompts directory not found: {self.prompts_dir}")
            return

        prompt_files = glob(os.path.join(self.prompts_dir, '*.txt'))
        for prompt_file in prompt_files:
            try:
                with open(prompt_file, 'r', encoding='utf-8') as f:
                    self.prompts[os.path.basename(prompt_file)] = f.read()
            except Exception as e:
                logger.error(f"Error loading prompt {prompt_file}: {e}")
        
        logger.info(f"{len(self.prompts)} prompts loaded.")

    def get_prompt(self, name: str) -> str:
        """
        Retrieves a prompt by its filename/key.
        """
        return self.prompts.get(name, "")
