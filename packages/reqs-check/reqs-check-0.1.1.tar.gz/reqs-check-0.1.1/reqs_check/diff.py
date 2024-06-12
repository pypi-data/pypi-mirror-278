import pandas as pd
from termcolor import colored
from .utils import parse_requirements

def highlight_differences(df):
    """
    Highlight differing versions in a DataFrame.
    
    Args:
        df (DataFrame): A DataFrame where the columns are file paths and the rows are packages with their versions.
        
    Returns:
        DataFrame: A DataFrame where differing versions are highlighted in red.
    """
    df_highlighted = df.copy()
    for idx, row in df.iterrows():
        versions = row[1:]
        if len(set(versions)) > 1:
            df_highlighted.loc[idx, row.index[1:]] = [colored(ver, 'red') if ver != 'Not Present' else colored(ver, 'blue') for ver in versions]
        elif 'Not Present' in versions.values:
            df_highlighted.loc[idx, row.index[1:]] = [colored(ver, 'blue') if ver == 'Not Present' else ver for ver in versions]
    return df_highlighted

def filter_differences(df):
    """
    Filter a DataFrame to only show rows with differing versions.
    
    Args:
        df (DataFrame): A DataFrame where the columns are file paths and the rows are packages with their versions.
    
    Returns:
        DataFrame: A filtered DataFrame where only rows with differing versions are shown.
    """
    df_filtered = df[df.apply(lambda row: len(set(row[1:])) > 1, axis=1)]
    return df_filtered
    
def compare_requirements(files) -> pd.DataFrame:
    """
    Compare multiple requirements files and return a DataFrame of the differences.
    
    Args:
        files (list): A list of file paths to requirements files.
        
    Returns:
        DataFrame: A DataFrame where the columns are the file paths and the rows are packages with their versions.
    """
    all_requirements = {}
    
    for file in files:
        requirements = parse_requirements(file)
        all_requirements[file] = requirements
    
    df = pd.DataFrame(all_requirements).fillna('Not Present')
    df.index.name = 'Package'
    df.reset_index(inplace=True)
    return df
