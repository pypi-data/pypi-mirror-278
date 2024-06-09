# tests/test_cleaning.py

import unittest
import pandas as pd
import numpy as np
from data_sanitizer.clean import handle_missing_values, remove_duplicates, remove_outliers, convert_types

class TestCleaning(unittest.TestCase):
    
    def test_handle_missing_values_mean(self):
        df = pd.DataFrame({'A': [1, 2, None, 4], 'B': [None, 2, 3, 4]})
        result = handle_missing_values(df, strategy='mean')
        self.assertEqual(result['A'].iloc[2], 2.3333333333333335)  # mean of [1, 2, 4]
        self.assertEqual(result['B'].iloc[0], 3.0)  # mean of [2, 3, 4]
    
    def test_remove_duplicates(self):
        df = pd.DataFrame({'A': [1, 2, 2, 4], 'B': [1, 2, 2, 4]})
        result = remove_duplicates(df)
        self.assertEqual(len(result), 3)  # duplicates removed

    def test_remove_outliers_iqr(self):
        df = pd.DataFrame({'A': [1, 2, 3, 1000], 'B': [2, 3, 4, 5]})
        result = remove_outliers(df, columns=['A'], method='IQR')
        self.assertEqual(len(result), 3)  # outlier removed
    
    def test_convert_types(self):
        df = pd.DataFrame({'A': [1, 2, 3], 'B': ['1', '2', '3']})
        result = convert_types(df, columns=['B'], dtypes=[int])
        self.assertTrue(result['B'].dtype == int)
    
if __name__ == '__main__':
    unittest.main()
