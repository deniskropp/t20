# Handles CLI argument parsing and integration

import argparse

def parse_gui_args(args):
    # Parser for arguments specific to launching the GUI itself.
    # These are distinct from the arguments passed to the 't20-system' subprocess.
    parser = argparse.ArgumentParser(add_help=False) # Prevent argparse from interfering with t20-system args if passed directly
    parser.add_argument('--theme', type=str, default='dark', help='Set the UI theme (e.g., dark, light)')
    # Add other GUI-specific arguments here if needed, e.g., --config-file
    
    # Parse only the arguments we recognize as GUI arguments.
    # This assumes GUI arguments are passed like '--theme dark' and runtime arguments
    # are handled by the 't20-system' call itself when launched via subprocess.
    gui_args, _ = parser.parse_known_args(args)
    return gui_args

def get_runtime_args_for_subprocess(ui_config):
    """Constructs the command line arguments for the t20-system subprocess
       based on the UI configuration.
    """
    args = []
    # Task goal is handled separately by the executor
    
    args.append("-o")
    args.append(ui_config.get("orchestrator", "LaCogito"))
    args.append("-m")
    args.append(ui_config.get("model", "gemini-1.5-flash-latest"))
    args.append("-r")
    args.append(str(ui_config.get("rounds", 5)))
    
    files = ui_config.get("files", [])
    if files:
        args.append("-f")
        args.extend(files)
        
    return args

# Note: The primary parsing of 't20-system' arguments happens within the 't20-system'
# command itself when executed via subprocess. This module mainly helps structure
# the arguments collected from the GUI config into the format expected by 't20-system'.
