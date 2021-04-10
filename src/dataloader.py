import pandas as pd
import argparse

from lib.config import Config
from lib.data_store import DataStore


def store_dataset(config: Config):
    """ Reads the dataset with the given configuration and stores
    it in the database."""
    dataset_name = config.get('dataset.name')
    pandas_config = config.get('dataset.pandas_args')
    dataset_df = pd.read_csv(**pandas_config)
    data_store = DataStore(config)
    data_store.store_dataset(dataset_name, dataset_df)


def main(config_path: str):
    config = Config(config_path)
    store_dataset(config)


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--config', default='',
        help='name of the configuration file to use (e.g. \'default\')')
    args = parser.parse_args()
    main(args.config)
