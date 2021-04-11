import pandas as pd
import numpy as np
from tensorflow.keras.layers.experimental import preprocessing

from lib.data_model import Dataset
from lib.data_store import DataStore
from lib.config import Config
from lib import preprocessing_helpers


def apply_custom_functions(dataset_df: pd.DataFrame, config: Config)\
        -> pd.DataFrame:
    """ It looks a bit hacky but we are just taking the function names
    from the config and loading the actual Callable functions from
    the preprocessing.custom_functions file.
    See https://stackoverflow.com/a/3071
    """
    custom_fct_names = config.get('dataset.preprocessing.custom_functions')
    for function_name in custom_fct_names:
        try:
            preprocess_fct = getattr(preprocessing_helpers, function_name)
            dataset_df = preprocess_fct(dataset_df)
        except AttributeError:
            # raise Exception with more explicit error message
            raise AttributeError('Could not find preprocessing function '
                f'"{function_name}" in lib.preprocessing_helpers')
    return dataset_df


def preprocess(dataset_df: pd.DataFrame, config: Config) -> Dataset:
    # apply custom functions pipeline
    dataset_df = apply_custom_functions(dataset_df, config)
    # split by rows
    split_ratio = config.get('dataset.preprocessing.trainset_ratio')
    train_dataset = dataset_df.sample(frac=split_ratio, random_state=0)
    test_dataset = dataset_df.drop(train_dataset.index)
    # split by column
    target_column = config.get('dataset.preprocessing.target_column')
    train_labels = train_dataset.pop(target_column)
    test_labels = test_dataset.pop(target_column)
    # fit normalizer to training features
    normalizer = preprocessing.Normalization(
        input_shape=[len(train_dataset.columns),]
    )
    normalizer.adapt(np.array(train_dataset))

    dataset = Dataset(
        training_set=train_dataset,
        training_labels=train_labels,
        test_set=test_dataset,
        test_labels=test_labels,
        normalizer=normalizer
    )
    return dataset


def generate_dataset(config: Config) -> Dataset:
    """ Loads the complete dataset, processes it and returns a more
    complex DataSet object which can then directly be used for training
    and evaluation."""
    # load dataset from data store
    data_store = DataStore(config)
    dataset_name = config.get('dataset.name')
    dataset_df = data_store.load_dataset(dataset_name)
    dataset = preprocess(dataset_df, config)
    return dataset
