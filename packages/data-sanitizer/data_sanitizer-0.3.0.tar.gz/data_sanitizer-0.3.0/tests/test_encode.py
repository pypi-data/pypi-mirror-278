# tests/test_encode.py

import unittest
import pandas as pd
from data_sanitizer.encode import encode_categorical

class TestEncoding(unittest.TestCase):
    
    def test_encode_categorical(self):
        df = pd.DataFrame({'A': ['a', 'b', 'a'], 'B': [1, 2, 3]})
        result = encode_categorical(df, columns=['A'])
        self.assertIn('A_a', result.columns)
        self.assertIn('A_b', result.columns)
        self.assertEqual(result['A_a'].iloc[0], 1)
        self.assertEqual(result['A_b'].iloc[1], 1)

if __name__ == '__main__':
    unittest.main()
