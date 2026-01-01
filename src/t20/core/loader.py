import os
import importlib.util
import inspect
from typing import Dict, Type
from t20.core.agent import Agent

def load_agent_classes(directory: str) -> Dict[str, Type[Agent]]:
    """
    Dynamically loads Agent subclasses from Python files in a given directory.

    Args:
        directory (str): The path to the directory containing agent Python files.

    Returns:
        Dict[str, Type[Agent]]: A dictionary mapping class names to agent classes.
    """
    agent_classes: Dict[str, Type[Agent]] = {}
    for filename in os.listdir(directory):
        if filename.endswith('.py') and not filename.startswith('__'):
            module_name = filename[:-3]
            module_path = os.path.join(directory, filename)
            spec = importlib.util.spec_from_file_location(module_name, module_path)
            if spec and spec.loader:
                module = importlib.util.module_from_spec(spec)
                spec.loader.exec_module(module)
                for name, obj in inspect.getmembers(module, inspect.isclass):
                    if issubclass(obj, Agent) and obj is not Agent:
                        agent_classes[name] = obj
    return agent_classes
