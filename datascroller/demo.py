import os
import pandas as pd


DATA_DIR = os.path.join(os.path.dirname(__file__), 'demo_data')


def read_titanic_csv():
    return pd.read_csv(os.path.join(DATA_DIR, 'titanic.csv'))

def read_titanic_parquet():
    return pd.read_parquet(os.path.join(DATA_DIR, 'titanic.parquet'))
