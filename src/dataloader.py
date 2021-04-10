import pandas as pd
from typing import Dict
import argparse

from lib.config import get_config, get_value
import lib.database as db


def read_dataset(dataset_config: Dict):
    """ Reads the dataset with the given configuration and stores
    it in the database."""
    dataset_df = pd.read_csv(**dataset_config['pandas_args'])
    db.store_dataset(dataset_config['name'], dataset_df)


def check_config(config):
    """ Sanity check to catch missing fields in the configuration."""
    mandatory_fields = [
        'dataset',
        'dataset.name',
        'dataset.pandas_args',
        'dataset.pandas_args.filepath_or_buffer',
    ]
    for field in mandatory_fields:
        if not get_value(config, field):
            raise KeyError(f'Required configuration field "{field}" not found')


def main(config_path: str):
    config = get_config(config_path)
    check_config(config)
    read_dataset(config['dataset'])


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--config', default='',
        help='name of the configuration file to use (e.g. \'default\')')
    args = parser.parse_args()
    main(args.config)
