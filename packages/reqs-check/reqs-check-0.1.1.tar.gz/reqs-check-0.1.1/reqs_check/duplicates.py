import os
import re

def parse_requirements_for_duplicates(file_path):
    """
    Parse a requirements file and return a dictionary of packages and versions.

    Args:
        file_path (str): The path to the requirements file.

    Returns:
        dict: A dictionary where the keys are package names and the values are lists of version strings.
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
                    if pkg not in requirements:
                        requirements[pkg] = []
                    requirements[pkg].append(ver.strip())
    return requirements

def find_duplicates(files):
    """
    Find duplicate packages in multiple requirements files.
    
    Args:
        files (list): A list of file paths to requirements files.
        
    Returns:
        dict: A dictionary where the keys are file paths and the values are dictionaries of duplicate packages and versions.
    """
    all_duplicates = {}
    
    for file in files:
        requirements = parse_requirements_for_duplicates(file)
        duplicates = {pkg: vers for pkg, vers in requirements.items() if len(vers) > 1}
        if duplicates:
            all_duplicates[file] = duplicates
    
    return all_duplicates
