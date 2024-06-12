import os

def lint_requirements(file_path) -> list[str]:
    """
    Lint a requirements file and return a list of warnings.
    
    Args:
        file_path (str): The path to the requirements file.
        
    Returns:
        list: A list of lint warnings.
    """
    if not os.path.isfile(file_path):
        raise FileNotFoundError(f"The file {file_path} does not exist.")

    warnings = []
    with open(file_path, 'r') as file:
        for line_num, line in enumerate(file, 1):
            line = line.strip()
            if line and not line.startswith('#'):
                if '==' not in line and '>=' not in line and '<=' not in line and '~=' not in line:
                    warnings.append(f"Line {line_num}: '{line}' does not specify a version.")
                if line.startswith('-e ') or line.startswith('--editable'):
                    warnings.append(f"Line {line_num}: '{line}' uses editable installs, which are not recommended for production.")
    return warnings
