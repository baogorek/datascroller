import os

import pandas as pd

from datascroller import demo


def test_read_titanic():

    csv_path = os.path.join(os.getcwd(), 'datascroller/demo_data/titanic.csv')
    control_df = pd.read_csv(csv_path)
    test_df = demo.read_titanic()
    assert control_df.equals(test_df)
