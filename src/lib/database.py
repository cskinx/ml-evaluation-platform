import pandas as pd
from typing import List
from lib.data_model import Run


def load_best_run(dataset_name: str) -> Run:
    pass


def load_relevant_runs(dataset_name: str) -> List[Run]:
    pass


def save_run(run: Run):
    pass


def store_dataset(name: str, dataset: pd.DataFrame):
    pass


def load_dataset(name: str) -> pd.DataFrame:
    pass
