from typing import List, Dict
from pydantic import BaseModel
import json
import os

# Updated Pydantic model for ARA configuration
class ARAconfig(BaseModel):
    ext_code_dirs: List[Dict[str, str]] = [{"source_dir_1": "./src"}, {"source_dir_2": "./tests"}] # names should not be used in application code, only the path should be relevant to avoid brittle application behavior
    glossary_dir: str = "./glossary"
    doc_dir: str = "./docs"
    local_prompt_templates_dir: str = "./ara/.araconfig/prompt-modules"
    local_ara_templates_dir: str = "./ara/.araconfig/templates/"
    ara_prompt_given_list_includes: List[str] = [
        "*.businessgoal", "*.vision", "*.capability", "*.keyfeature", 
        "*.epic", "*.userstory", "*.example", "*.feature", "*.task", "*.py", "*.md"
    ]

# Function to ensure the necessary directories exist
def ensure_directory_exists(directory: str):
    if not os.path.exists(directory):
        os.makedirs(directory)
        print(f"New directory created at {directory}")
    return directory

# Function to read the JSON file and return an ARAconfig model
def read_data(filepath: str) -> ARAconfig:
    if not os.path.exists(filepath):
        # If file does not exist, create it with default values
        default_config = ARAconfig()
        with open(filepath, 'w') as file:
            json.dump(default_config.dict(), file, indent=4)
        print(f"ara-tool configuration file '{filepath}' created with default configuration. Please modify it as needed and re-run your command")
        exit()  # Exit the application

    with open(filepath, 'r') as file:
        data = json.load(file)
    return ARAconfig(**data)

# Function to save the modified configuration back to the JSON file
def save_data(filepath: str, config: ARAconfig):
    with open(filepath, 'w') as file:
        json.dump(config.dict(), file, indent=4)

# Singleton for configuration management
class ConfigManager:
    _config_instance = None

    @classmethod
    def get_config(cls, filepath='./ara/.araconfig/ara_config.json'):
        if cls._config_instance is None:
            cls._config_instance = read_data(filepath)
        return cls._config_instance
