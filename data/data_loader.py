import pandas as pd

def load_data(path):
    df = pd.read_csv(path)
    df.info()
    df.describe()
    df.head()
    return df
