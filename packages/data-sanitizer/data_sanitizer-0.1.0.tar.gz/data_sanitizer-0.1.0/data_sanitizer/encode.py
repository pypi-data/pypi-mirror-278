# data_sanitizer/encode.py

import pandas as pd

def encode_categorical(df, columns):
    """
    Encode categorical features using one-hot encoding.
    
    Parameters:
    - df: pandas DataFrame
    - columns: list of columns to encode
    
    Returns:
    - DataFrame with encoded categorical features
    """
    return pd.get_dummies(df, columns=columns)
