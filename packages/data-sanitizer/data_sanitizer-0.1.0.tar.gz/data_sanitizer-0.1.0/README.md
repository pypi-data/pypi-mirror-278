Data-Sanitizer
Data-Sanitizer is a comprehensive Python package designed to streamline the process of cleaning and preprocessing tabular data using pandas. Whether you're dealing with missing values, duplicates, outliers, or need to encode categorical variables and scale numerical features, DataSanitizer provides a suite of easy-to-use tools to prepare your data for analysis and machine learning.

Features
1. Handle Missing Values: Easily fill missing values with mean, median, mode, or drop them entirely.
2. Remove Duplicates: Effortlessly identify and remove duplicate rows from your dataset.
3. Remove Outliers: Detect and remove outliers using Interquartile Range (IQR) or Z-score methods.
4. Convert Data Types: Seamlessly convert data types of specified columns to ensure consistency.
5. Encode Categorical Variables: Perform one-hot encoding on categorical features to prepare them for machine learning models.
6. Scale Numerical Features: Standardize or normalize numerical features to improve the performance of your algorithms.

Installation
Install DataSanitizer easily using pip: pip install datasanitizer

Usage

Data-Sanitizer integrates smoothly with pandas DataFrames, making it intuitive for users familiar with pandas.

Example

import pandas as pd
from datasanitizer import handle_missing_values, remove_duplicates, remove_outliers, convert_types, encode_categorical, scale_features

# Sample DataFrame
df = pd.DataFrame({
    'A': [1, 2, None, 4],
    'B': [None, 2, 3, 4],
    'C': ['cat', 'dog', 'cat', 'mouse'],
    'D': [10, 20, 30, 1000]
})

# Handling missing values
df = handle_missing_values(df, strategy='mean')

# Removing duplicates
df = remove_duplicates(df)

# Removing outliers
df = remove_outliers(df, columns=['D'], method='IQR')

# Converting data types
df = convert_types(df, columns=['A'], dtypes=[float])

# Encoding categorical variables
df = encode_categorical(df, columns=['C'])

# Scaling numerical features
df = scale_features(df, columns=['D'], strategy='standard')

print(df)

Contributing
We welcome contributions to improve Data-Sanitizer.

Contact
For any questions or issues, please contact the package maintainer at goradbj@gmail.com