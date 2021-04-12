""" Contains custom functions for preprocessing a dataset;
these functions can then be referenced in the configuration files and applied
only to specific datasets.
This seems necessary because it would be very tedious to map all functionality
to the structure in the configuration file, especially if the preprocessing
contains very dataset-specific steps such as renaming variables."""
import pandas as pd
pd.options.mode.chained_assignment = None


def drop_missing(dataset_df: pd.DataFrame) -> pd.DataFrame:
    dataset_df = dataset_df.dropna()
    return dataset_df


def fuel_efficiency_dummies(dataset_df: pd.DataFrame) -> pd.DataFrame:
    origin_map = {
        1: 'USA',
        2: 'Europe',
        3: 'Japan'
    }
    dataset_df['Origin'] = dataset_df['Origin'].map(origin_map)
    dataset_df = pd.get_dummies(
        dataset_df,
        columns=['Origin'],
        prefix='',
        prefix_sep='')
    return dataset_df


def keep_horsepower_only(dataset_df: pd.DataFrame) -> pd.DataFrame:
    dataset_df = dataset_df[['Horsepower', 'MPG']]
    return dataset_df
