import pytest
from src.lib.config import Config


@pytest.fixture
def min_config():
    parameters = {
        'dataset': {
            'name': 'test',
            'columns': [
                'colA',
                'colB',
            ]
        }
    }
    return Config.from_dict(parameters)


def test_creation(min_config):
    assert type(min_config) == Config


def test_merge(min_config):
    new_data_dict = {
        'dataset': {
            'name': 'new_test'
        }
    }
    new_config = Config.from_dict(new_data_dict)
    min_config.absorb(new_config)
    assert min_config.get('dataset.name') == 'new_test'


def test_missing(min_config):
    with pytest.raises(KeyError):
        min_config.get('preprocessing')


def test_paths(min_config):
    assert min_config.get('dataset.name') == 'test'
    columns = min_config.get('dataset.columns')
    assert len(columns) == 2
    assert columns[1] == 'colB'
