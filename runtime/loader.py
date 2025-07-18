# runtime/loader.py
import os
import yaml
from glob import glob

def load_config(config_path):
    """Lädt die Runtime-Konfiguration."""
    print(f"Lade Konfiguration von: {config_path}")
    with open(config_path, 'r', encoding='utf-8') as f:
        return yaml.safe_load(f)

def load_agent_templates(agents_dir):
    """Lädt alle Agenten-Spezifikationen aus einem Verzeichnis."""
    print(f"Lade Agenten-Templates von: {agents_dir}")
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
    print(f"{len(templates)} Agenten-Templates geladen.")
    return templates

def load_prompts(prompts_dir):
    """Lädt alle System-Prompts aus einem Verzeichnis."""
    print(f"Lade Prompts von: {prompts_dir}")
    prompt_files = glob(os.path.join(prompts_dir, '*.txt'))
    prompts = {}
    for prompt_file in prompt_files:
        with open(prompt_file, 'r', encoding='utf-8') as f:
            # Use the absolute path as the key for reliable lookup
            prompts[os.path.basename(prompt_file)] = f.read()
    print(f"{len(prompts)} Prompts geladen.")
    return prompts
