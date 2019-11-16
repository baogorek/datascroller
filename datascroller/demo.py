import os
import pandas as pd


DATA_DIR = os.path.dirname(__file__)

def read_titanic():
    return pd.read_csv(os.path.join(DATA_DIR, 'demo_data/titanic.csv'))
