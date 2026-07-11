import pandas as pd
from utils.helpers import logger

def clean_data(df):
    """
    Performs basic data cleaning: removing nulls and duplicates.
    
    Args:
        df (pd.DataFrame): The input dataframe.
        
    Returns:
        pd.DataFrame: The cleaned dataframe.
    """
    if df is None:
        return None
        
    # Drop rows with missing values
    initial_shape = df.shape
    df_clean = df.dropna()
    
    # Drop duplicate rows
    df_clean = df_clean.drop_duplicates()
    
    logger.info(f"Cleaned data. Shape went from {initial_shape} to {df_clean.shape}")
    return df_clean

def prepare_stock_features(df):
    """
    Prepares features for our simple stock prediction model.
    We will use 'Open', 'High', 'Low', 'Volume' to predict 'Close'.
    
    Args:
        df (pd.DataFrame): Stock dataframe.
        
    Returns:
        X (pd.DataFrame), y (pd.Series): Features and target variable.
    """
    features = ['Open', 'High', 'Low', 'Volume']
    target = 'Close'
    
    if not all(col in df.columns for col in features + [target]):
        logger.error("Missing required columns for stock prediction.")
        return None, None
        
    X = df[features]
    y = df[target]
    
    return X, y
