import pandas as pd

from lib.config import Config, config_prompt
from lib.data_store import DataStore


def store_dataset(config: Config):
    """ Reads the dataset with the given configuration and stores
    it in the database."""
    dataset_name = config.get('dataset.name')
    pandas_config = config.get('dataset.pandas_args')
    dataset_df = pd.read_csv(**pandas_config)
    data_store = DataStore(config)
    data_store.store_dataset(dataset_name, dataset_df)


if __name__ == '__main__':
    config = config_prompt()
    store_dataset(config)
