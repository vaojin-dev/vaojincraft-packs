import os
from core.file_utils import load_json

def load(config_path):
    """
    Loads the global configuration file.
    """
    if not os.path.exists(config_path):
        raise FileNotFoundError(f"Critical Error: Global configuration file missing at {config_path}")
    
    return load_json(config_path)