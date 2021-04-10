import pandas as pd
import numpy as np
from tensorflow.keras.layers.experimental import preprocessing
import logging
from typing import Tuple

from lib.data_model import DataSet
from lib.data_store import DataStore
from lib.config import Config
from operators.preprocessing import custom_functions


def split_dataset(dataset_df: pd.DataFrame, trainset_ratio: float)\
        -> Tuple[pd.DataFrame, pd.DataFrame]:
    train_dataset = dataset_df.sample(frac=trainset_ratio, random_state=0)
    test_dataset = dataset_df.drop(train_dataset.index)
    return (train_dataset, test_dataset)


def preprocess(dataset_df: pd.DataFrame, config: Config) -> DataSet:
    # first, apply custom functions pipeline
    custom_fct_names = config.get('dataset.preprocessing.custom_functions')
    for function_name in custom_fct_names:
        try:
            callable_fct = getattr(custom_functions, function_name)
            callable_fct(dataset_df)
        except AttributeError:
            # raise Exception with more explicit error message
            raise AttributeError('Could not find preprocessing function '
                f'{function_name} in operators.preprocessing.custom_functions')

    split_ratio = config.get('dataset.preprocessing.trainset_ratio')
    train_dataset, test_dataset = split_dataset(dataset_df, split_ratio)

    target_column = config.get('dataset.preprocessing.target_column')
    train_labels = train_dataset.pop(target_column)
    test_labels = test_dataset.pop(target_column)

    normalizer = preprocessing.Normalization()
    normalizer.adapt(np.array(train_dataset))

    dataset = DataSet(
        training_set=train_dataset,
        training_labels=train_labels,
        test_set=test_dataset,
        test_labels=test_labels,
        normalizer=normalizer
    )
    return dataset


def generate_dataset(config: Config) -> DataSet:
    """ Loads the complete dataset, processes it and returns a more
    complex DataSet object which can then directly be used for training
    and evaluation."""
    # load dataset from data store
    data_store = DataStore(config)
    dataset_name = config.get('dataset.name')
    dataset_df = data_store.load_dataset(dataset_name)
    dataset = preprocess(dataset_df, config)
    return dataset
