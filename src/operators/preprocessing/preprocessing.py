import pandas as pd
from tensorflow.keras.layers.experimental import preprocessing
import logging

from lib.data_model import DataSet
from lib.data_store import DataStore
from lib.config import Config
from operators.preprocessing import custom_functions


def preprocess(dataset_df: pd.DataFrame, config: Config) -> DataSet:
    # first, apply custom functions pipeline
    custom_fct_names = config.get('dataset.preprocessing.custom_functions')
    for function_name in custom_fct_names:
        try:
            callable_fct = getattr(custom_functions, function_name)
            callable_fct(dataset_df)
        except AttributeError:
            # raise Exception with more explicit error message
            raise AttributeError('Could not find preprocessing function {function_name}'\
                ' in operators.preprocessing.custom_functions')
    normalizer = preprocessing.Normalization()
    pass
    # ...


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
