# data_sanitizer/clean.py
import numpy as np
import pandas as pd

def handle_missing_values(df, strategy='mean', columns=None):
    """
    Handle missing values in the DataFrame.
    
    Parameters:
    - df: pandas DataFrame
    - strategy: 'mean', 'median', 'mode', or 'drop'
    - columns: list of columns to apply the strategy on, default is all columns
    
    Returns:
    - DataFrame with handled missing values
    """
    if columns is None:
        columns = df.columns
    
    for column in columns:
        if strategy == 'mean':
            df[column].fillna(df[column].mean(), inplace=True)
        elif strategy == 'median':
            df[column].fillna(df[column].median(), inplace=True)
        elif strategy == 'mode':
            df[column].fillna(df[column].mode()[0], inplace=True)
        elif strategy == 'drop':
            df.dropna(subset=[column], inplace=True)
    
    return df

def remove_duplicates(df):
    """
    Remove duplicate rows from the DataFrame.
    
    Parameters:
    - df: pandas DataFrame
    
    Returns:
    - DataFrame with duplicates removed
    """
    return df.drop_duplicates()

def remove_outliers(df, columns, method='IQR'):
    """
    Remove outliers from the DataFrame.
    
    Parameters:
    - df: pandas DataFrame
    - columns: list of columns to check for outliers
    - method: 'IQR' or 'Z-score'
    
    Returns:
    - DataFrame with outliers removed
    """
    if method == 'IQR':
        Q1 = df[columns].quantile(0.25)
        Q3 = df[columns].quantile(0.75)
        IQR = Q3 - Q1
        df = df[~((df[columns] < (Q1 - 1.5 * IQR)) | (df[columns] > (Q3 + 1.5 * IQR))).any(axis=1)]
    elif method == 'Z-score':
        from scipy import stats
        df = df[(np.abs(stats.zscore(df[columns])) < 3).all(axis=1)]
    
    return df

def convert_types(df, columns, dtypes):
    """
    Convert data types of specified columns.
    
    Parameters:
    - df: pandas DataFrame
    - columns: list of columns to convert
    - dtypes: list of target data types
    
    Returns:
    - DataFrame with converted data types
    """
    for column, dtype in zip(columns, dtypes):
        df[column] = df[column].astype(dtype)
    
    return df