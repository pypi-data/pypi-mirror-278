# tests/test_scale.py

import unittest
import pandas as pd
from data_sanitizer.scale import scale_features

class TestScaling(unittest.TestCase):
    
    def test_scale_features_standard(self):
        df = pd.DataFrame({'A': [1, 2, 3], 'B': [4, 5, 6]})
        result = scale_features(df, columns=['A', 'B'], strategy='standard')
        self.assertAlmostEqual(result['A'].mean(), 0)
        self.assertAlmostEqual(result['B'].mean(), 0)

if __name__ == '__main__':
    unittest.main()
