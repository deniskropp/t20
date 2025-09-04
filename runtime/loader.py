# runtime/loader.py
import os
import yaml
from glob import glob
import logging

logger = logging.getLogger(__name__)

def load_config(config_path):
    """
    Loads the runtime configuration from a YAML file.

    Args:
        config_path (str): The absolute path to the configuration file.

    Returns:
        dict: The loaded configuration as a dictionary.
    """
    logger.info(f"Loading configuration from: {config_path}")
    with open(config_path, 'r', encoding='utf-8') as f:
        return yaml.safe_load(f)

def load_agent_templates(agents_dir):
    """
    Loads all agent specifications from YAML files within a specified directory.

    Args:
        agents_dir (str): The absolute path to the directory containing agent YAML files.

    Returns:
        list: A list of dictionaries, where each dictionary represents an agent's specification.
    """
    logger.info(f"Loading agent templates from: {agents_dir}")
    agent_files = glob(os.path.join(agents_dir, '*.yaml'))
    templates = []
    for agent_file in agent_files:
        with open(agent_file, 'r', encoding='utf-8') as f:
            template = yaml.safe_load(f)
            # Resolve prompt path relative to the agent file's directory
            if 'system_prompt' in template and template['system_prompt']:
                base_dir = os.path.dirname(agent_file)
                prompt_path = os.path.abspath(os.path.join(base_dir, template['system_prompt']))
                template['system_prompt_path'] = prompt_path
            templates.append(template)
    logger.info(f"{len(templates)} agent templates loaded.")
    return templates

def load_prompts(prompts_dir):
    """
    Loads all system prompts from text files within a specified directory.

    Args:
        prompts_dir (str): The absolute path to the directory containing prompt text files.

    Returns:
        dict: A dictionary where keys are prompt filenames (e.g., 'agent_instructions.txt')
              and values are the content of the prompt files.
    """
    logger.info(f"Loading prompts from: {prompts_dir}")
    prompt_files = glob(os.path.join(prompts_dir, '*.txt'))
    prompts = {}
    for prompt_file in prompt_files:
        with open(prompt_file, 'r', encoding='utf-8') as f:
            # Use the absolute path as the key for reliable lookup
            prompts[os.path.basename(prompt_file)] = f.read()
    logger.info(f"{len(prompts)} prompts loaded.")
    return prompts