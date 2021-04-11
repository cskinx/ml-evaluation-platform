from typing import Dict
from dataclasses import dataclass
from datetime import datetime

import pandas as pd
from tensorflow.keras.layers.experimental import preprocessing


# TODO: this should be renamed because it has the same name as datasets in the DB
# but they refer to different concepts.
@dataclass
class Dataset:
    """ Representation of a dataset containing a training and test set,
    which are each split into features and labels. Also contains a normalizer
    based on the training set to properly transform instances outside of
    the training set."""
    training_set: pd.DataFrame
    training_labels: pd.DataFrame
    test_set: pd.DataFrame
    test_labels: pd.DataFrame
    normalizer: preprocessing.Normalization


@dataclass
class Run:
    """ Representation of a single run on a specific dataset with a specific
    model and set of results, i.e. metrics with their  scores, at a specific
    time and date."""
    timestamp: datetime
    dataset_name: str
    preprocessing_cfg: Dict
    model_type: str
    model_hyperparameters: Dict
    metric_scores: Dict
