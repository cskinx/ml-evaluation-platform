from typing import List, Dict
import logging
import json
import datetime as dt

from sqlalchemy import create_engine
from sqlalchemy_utils import database_exists, create_database
from sqlalchemy.engine.result import RowProxy
import pandas as pd

from lib.config import Config
from lib.data_model import Run


def row_to_run(row: RowProxy) -> Run:
    # add column names as keys
    run_dict = dict(row)
    run_dict['metric_scores'] = {
        run_dict.pop('metric'): run_dict.pop('score')
    }
    return Run(**run_dict)


class DataStore:
    """ A wrapper for accessing the database in the desired way.
    Sets up a database connection with the given configuration and hides
    the exact implementation of the queries etc."""

    def __init__(self, config: Config):
        """ Reads the database configuration and sets up the database."""
        # connection details
        self.username = config.get('database.username')
        self.password = config.get('database.password')
        self.host = config.get('database.host')
        self.port = config.get('database.port')
        self.db_name = config.get('database.name')
        # table names and prefix
        self.dataset_prefix = config.get('database.dataset_prefix')
        self.scores_table = 'metric_scores'
        self.runs_table = 'runs'
        self.setup()

    def setup(self):
        """ Create database and necessary metadata tables, if they
        don't already exist."""
        connection_str = f"postgresql://{self.username}:{self.password}" \
            f"@{self.host}:{self.port}/{self.db_name}"
        self.engine = create_engine(connection_str)
        # https://stackoverflow.com/a/61885943
        if not database_exists(connection_str):
            create_database(connection_str)
        # necessary tables
        runs_table_query = f"""
            CREATE TABLE IF NOT EXISTS {self.runs_table} (
                run_id                 SERIAL PRIMARY KEY,
                timestamp              TIMESTAMP,
                dataset_name           VARCHAR(128),
                preprocessing_cfg      JSON,
                model_type             VARCHAR(128),
                model_hyperparameters  JSON
            );
        """
        self.engine.execute(runs_table_query)
        scores_table_query = f"""
            CREATE TABLE IF NOT EXISTS {self.scores_table} (
                run_id  INTEGER REFERENCES {self.runs_table} (run_id),
                metric  VARCHAR(128),
                score   FLOAT,
                PRIMARY KEY(run_id, metric)
            );
        """
        self.engine.execute(scores_table_query)

    def load_best_run(self, dataset_name: str, metric: str) -> Run:
        query = f"""
            WITH runs_scores AS (
                SELECT  timestamp,
                        dataset_name,
                        preprocessing_cfg,
                        model_type,
                        model_hyperparameters,
                        metric,
                        score
                FROM    {self.runs_table}, {self.scores_table}
                WHERE   {self.runs_table}.run_id = {self.scores_table}.run_id
                    AND {self.runs_table}.dataset_name = '{dataset_name}'
                    AND {self.scores_table}.metric = '{metric}'
            ),
            best_score AS (
                SELECT MIN(score) AS value
                FROM runs_scores
            )
            SELECT runs_scores.*
            FROM   runs_scores, best_score
            WHERE runs_scores.score = best_score.value
            ORDER BY runs_scores.timestamp ASC
            LIMIT 1;
        """
        result = self.engine.execute(query)
        run_row = result.fetchone()
        return row_to_run(run_row)

    def load_runs(self, conditions: List[str] = []) -> List[Run]:
        """ Loads a list of runs, filtered by the given condition."""
        condition_str = ''
        if len(conditions) >= 1:
            condition_str = 'AND ' + ' AND '.join(conditions)
        query = f"""
            SELECT  timestamp,
                    dataset_name,
                    preprocessing_cfg,
                    model_type,
                    model_hyperparameters,
                    metric,
                    score
            FROM    {self.runs_table}, {self.scores_table}
            WHERE   {self.runs_table}.run_id = {self.scores_table}.run_id
                    {condition_str};
        """
        results = self.engine.execute(query)
        runs = []
        for row in results:
            runs.append(row_to_run(row))
        return runs

    def load_recent_good_runs(
            self, dataset_name: str, metric: str, max_score: float)\
            -> List[Run]:
        """ Loads all runs from the last 7 days which have a score below
        the max_score for the given metric."""
        seven_days_ago = dt.date.today() - dt.timedelta(days=7)
        conditions = [
            f"{self.runs_table}.dataset_name = '{dataset_name}'",
            f"{self.scores_table}.metric = '{metric}'",
            f"{self.scores_table}.score < {max_score}",
            f"{self.runs_table}.timestamp >= '{seven_days_ago}'",
        ]
        runs = self.load_runs(conditions)
        return runs

    def save_run(self, run: Run):
        """ Saves the given run into the database."""
        # save run metadata
        query = f"""
            INSERT INTO {self.runs_table} (timestamp, dataset_name,
                preprocessing_cfg, model_type, model_hyperparameters)
            VALUES (
                '{run.timestamp}',
                '{run.dataset_name}',
                '{json.dumps(run.preprocessing_cfg)}',
                '{run.model_type}',
                '{json.dumps(run.model_hyperparameters)}'
            )
            RETURNING run_id;
        """
        # returns the run_id for the next insert
        run_id = self.engine.execute(query).scalar()
        # save run results
        metric_rows = []
        for metric, score in run.metric_scores.items():
            metric_rows.append(f"({run_id}, '{metric}', {score})")
        value_rows = ', '.join(metric_rows)
        query = f"""
            INSERT INTO {self.scores_table} (run_id, metric, score)
            VALUES {value_rows};
        """
        self.engine.execute(query)

    def get_table_count(self, table_name: str) -> int:
        query = f'SELECT COUNT(*) FROM "{table_name}"'
        count = self.engine.execute(query).scalar()
        return count

    def store_dataset(self, name: str, dataset_df: pd.DataFrame):
        table_name = f'{self.dataset_prefix}{name}'
        try:
            dataset_df.to_sql(table_name, self.engine)
        except ValueError:
            logging.error(f'dataset {name} already exists;'
                          ' please choose a different name.')

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
