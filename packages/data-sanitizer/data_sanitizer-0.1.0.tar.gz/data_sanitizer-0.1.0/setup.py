# setup.py

from setuptools import setup, find_packages

setup(
    name='data_sanitizer',
    version='0.1.0',
    description='Data-Sanitizer is a comprehensive Python package designed to streamline the process of cleaning and preprocessing tabular data using pandas. Whether you are dealing with missing values, duplicates, outliers, or need to encode categorical variables and scale numerical features, DataSanitizer provides a suite of easy-to-use tools to prepare your data for analysis and machine learning.',
    author='Balwant Gorad',
    author_email='goradbj@gmail.com',
    packages=find_packages(),
    install_requires=[
        'pandas>=1.0.0',
        'scikit-learn>=0.22.0',
    ],
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.6',
)
