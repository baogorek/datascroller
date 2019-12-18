import os
import pandas as pd


DATA_DIR = os.path.join(os.path.dirname(__file__), 'demo_data')


def read_titanic():
    return pd.read_csv(os.path.join(DATA_DIR, 'titanic.csv'))
