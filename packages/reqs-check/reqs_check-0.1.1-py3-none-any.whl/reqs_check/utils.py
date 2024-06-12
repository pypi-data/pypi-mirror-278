import os
import re 

def parse_requirements(file_path) -> dict:
    """
    Parse a requirements file and return a dictionary of packages and versions.
    
    Args:
        file_path (str): The path to the requirements file.
        
    Returns:
        dict: A dictionary where the keys are package names and the values are version strings.
    """
    if not os.path.isfile(file_path):
        raise FileNotFoundError(f"The file {file_path} does not exist.")

    requirements = {}
    with open(file_path, 'r') as file:
        for line in file:
            line = line.strip()
            if line and not line.startswith('#'):
                match = re.match(r'([a-zA-Z0-9_-]+)([>=<~!]+[a-zA-Z0-9._-]+)?', line)
                if match:
                    pkg = match.group(1)
                    ver = match.group(2) if match.group(2) else 'Any'
                    requirements[pkg.strip()] = ver.strip()
    return requirements



