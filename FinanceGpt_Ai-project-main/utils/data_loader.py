import pandas as pd
import os
from utils.helpers import logger

def load_csv(filepath):
    """
    Loads a CSV file into a Pandas DataFrame.
    
    Args:
        filepath (str): The path to the CSV file.
        
    Returns:
        pd.DataFrame or None: The loaded data, or None if the file doesn't exist.
    """
    if not os.path.exists(filepath):
        logger.error(f"File not found: {filepath}")
        return None
        
    try:
        df = pd.read_csv(filepath)
        logger.info(f"Successfully loaded data from {filepath} with shape {df.shape}")
        return df
    except Exception as e:
        logger.error(f"Error loading {filepath}: {e}")
        return None
