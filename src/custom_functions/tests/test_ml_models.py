import pytest
from src.custom_functions import ml_models
from src.lib.config import Config
import numpy as np
from tensorflow.keras.layers.experimental.preprocessing import Normalization


@pytest.fixture
def regression_config():
    config_data = {
        'model': {
            'hyperparameters': {
                'learning_rate': 0.1,
                'loss': 'mean_absolute_error',
            }
        }
    }
    return Config.from_dict(config_data)


@pytest.fixture
def dnn_config():
    config_data = {
        'model': {
            'hyperparameters': {
                'learning_rate': 0.1,
                'loss': 'mean_absolute_error',
            }
        }
    }
    return Config.from_dict(config_data)


@pytest.fixture
def min_normalizer():
    """ Normalizer with minimalistic data."""
    adapt_data = np.array([[1., 2.], [2., 3.], ], dtype=np.float32)
    normalizer = Normalization()
    normalizer.adapt(adapt_data)
    return normalizer


def test_regression(regression_config, min_normalizer):
    model = ml_models.regression(regression_config, min_normalizer)
