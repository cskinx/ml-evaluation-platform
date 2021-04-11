from typing import List, Dict
import logging

from sqlalchemy import create_engine
from sqlalchemy_utils import database_exists, create_database
import pandas as pd

from lib.config import Config
from lib.data_model import Run


class DataStore:
    """ A wrapper for accessing the database in the desired way.
    Sets up a database connection with the given configuration and hides
    the exact implementation of the queries etc."""

    def __init__(self, config: Config):
        self.username = config.get('database.username')
        self.password = config.get('database.password')
        self.host = config.get('database.host')
        self.port = config.get('database.port')
        self.db_name = config.get('database.name')
        self.dataset_prefix = config.get('database.dataset_prefix')
        connection_str = f"postgresql://{self.username}:{self.password}" \
            f"@{self.host}:{self.port}/{self.db_name}"
        self.engine = create_engine(connection_str)
        # https://stackoverflow.com/a/61885943
        if not database_exists(connection_str):
            create_database(connection_str)

    def load_best_run(self, dataset_name: str, metric: str) -> Run:
        pass

    def load_recent_good_runs(
            self, dataset_name: str, metric: str, max_score: float = None)\
            -> List[Run]:
        """ Loads all runs from the last 7 days which have a score below
        the max_score for the given metric."""
        pass

    def save_run(self, run: Run):
        """ Saves the given run into the database."""
        pass

    def get_table_count(self, table_name: str) -> int:
        query = f'SELECT COUNT(*) FROM "{table_name}"'
        count = self.engine.execute(query).scalar()
        return count

    def store_dataset(self, name: str, dataset_df: pd.DataFrame):
        table_name = f'{self.dataset_prefix}{name}'
        try:
            dataset_df.to_sql(table_name, self.engine)
        except ValueError:
            logging.error(f'dataset {name} already exists;'\
                ' please choose a different name.')
        self.print_datasets()

    def load_dataset(self, name: str) -> pd.DataFrame:
        """ Loads the complete dataset with the given name."""
        table_name = f'{self.dataset_prefix}{name}'
        dataset_df = pd.read_sql(table_name, self.engine)
        return dataset_df

    def get_dataset_overview(self) -> List[Dict]:
        """ Returns datasets with number of observations (rows)."""
        datasets = []
        table_names = self.engine.table_names()
        for table_name in table_names:
            if table_name.startswith(self.dataset_prefix):
                dataset_name = table_name.replace(self.dataset_prefix, '')
                table_count = self.get_table_count(table_name)
                datasets.append({
                    'name': dataset_name,
                    'size': table_count,
                })
        return datasets
