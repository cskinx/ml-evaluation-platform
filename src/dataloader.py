import pandas as pd

from lib.config import Config, config_prompt
from lib.data_store import DataStore
from lib.print_utils import print_dataset_overview


def store_dataset(config: Config):
    """ Reads the dataset with the given configuration and stores
    it in the database."""
    # load data
    dataset_name = config.get('dataset.name')
    pandas_config = config.get('dataset.loading')
    dataset_df = pd.read_csv(**pandas_config)
    # store dataset
    data_store = DataStore(config)
    data_store.store_dataset(dataset_name, dataset_df)
    # print overview
    overview = data_store.get_dataset_overview()
    print_dataset_overview(overview)


if __name__ == '__main__':
    config = config_prompt()
    store_dataset(config)
