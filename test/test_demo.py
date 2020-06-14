import os
import unittest

import pandas as pd

from datascroller import demo

class DataTests(unittest.TestCase):
    """Tests for ensuring that data can be correctly loaded"""

    def test_read_csv(self):
        csv_path = os.path.join(os.getcwd(), 'datascroller/demo_data/titanic.csv')
        control_df = pd.read_csv(csv_path)
        test_df = demo.read_titanic_csv()
        self.assertTrue(control_df.equals(test_df))

    def test_read_parquet(self):
        parquet_path = os.path.join(os.getcwd(), 'datascroller/demo_data/titanic.parquet')
        control_df = pd.read_parquet(parquet_path)
        test_df = demo.read_titanic_parquet()
        self.assertTrue(control_df.equals(test_df))


if __name__ == '__main__':
    unittest.main()
