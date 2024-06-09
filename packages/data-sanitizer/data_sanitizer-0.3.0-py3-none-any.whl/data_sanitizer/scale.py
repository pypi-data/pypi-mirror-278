# data_sanitizer/scaling.py

from sklearn.preprocessing import StandardScaler, MinMaxScaler

def scale_features(df, columns, strategy='standard'):
    """
    Scale numerical features.
    
    Parameters:
    - df: pandas DataFrame
    - columns: list of columns to scale
    - strategy: 'standard' or 'minmax'
    
    Returns:
    - DataFrame with scaled features
    """
    scaler = StandardScaler() if strategy == 'standard' else MinMaxScaler()
    
    df[columns] = scaler.fit_transform(df[columns])
    
    return df
