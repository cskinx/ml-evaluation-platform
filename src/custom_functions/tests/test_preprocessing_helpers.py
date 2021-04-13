import pytest
from src.custom_functions import preprocessing_helpers
import pandas as pd
import numpy as np


def test_drop_missing():
    df = pd.DataFrame({
        'A': [0, 1], 
        'B': [2, np.nan],
    })
    df_dropped = preprocessing_helpers.drop_missing(df)
    assert len(df.index) > len(df_dropped.index)
    assert len(df_dropped.index) == 1


def test_fuel_dummies_full():
    df = pd.DataFrame({'Origin': [1, 3, 2, 3, 1]})
    df_dummies = preprocessing_helpers.fuel_efficiency_dummies(df)
    assert len(df.columns) < len(df_dummies.columns)
    assert len(df_dummies.columns) == 3


def test_fuel_dummies_part():
    df = pd.DataFrame({'Origin': [1]})
    df_dummies = preprocessing_helpers.fuel_efficiency_dummies(df)
    assert len(df.columns) == len(df_dummies.columns)
    assert len(df_dummies.columns) == 1


def test_keep_horsepower():
    df = pd.DataFrame({
        'Horsepower': [130.0],
        'Cylinders': [8],
        'MPG': [18.0]}
    )
    df_horse = preprocessing_helpers.keep_horsepower_only(df)
    assert len(df.columns) > len(df_horse.columns)
    assert len(df_horse.columns) == 2
