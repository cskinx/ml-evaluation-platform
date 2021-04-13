from __future__ import annotations
import os
from typing import Any, Dict
import argparse

from omegaconf import OmegaConf, DictConfig


class Config:
    """ A wrapper for the functionality from omegaconfg.
    Basically just reads the 'configs/default.yml' file plus one optional other
    config file and makes the values accessible by path strings."""

    def __init__(self, config: DictConfig):
        self.config = config

    @classmethod
    def from_file(cls, name: str = '', config_dir: str = './configs'):
        """ Load the configuration files properly; always reads the default.yml
        but overwrites its values if a more specific file is given."""
        # load default config
        default_cfg_path = os.path.join(config_dir, 'default.yml')
        config = OmegaConf.load(default_cfg_path)
        # load more specific config
        specific_cfg_path = os.path.join(config_dir, f'{name}.yml')
        if os.path.exists(specific_cfg_path):
            specific_config = OmegaConf.load(specific_cfg_path)
            config = OmegaConf.merge(config, specific_config)
        return cls(config)

    @classmethod
    def from_dict(cls, config_dict: Dict):
        """ Takes a configuration as dictionary and creates a Config object."""
        config = OmegaConf.create(config_dict)
        return cls(config)

    def absorb(self, new_config: Config):
        """ Absorbs the other config and overwrites the values
        in this config."""
        OmegaConf.merge(self.config, new_config)

    def get(self, path: str, throw_exception: bool = True,
            as_primitive: bool = False) -> Any:
        """ Returns the value at the given path of the config;
        if field is mandatory, an Exception should be thrown."""
        value = OmegaConf.select(self.config, path)
        if not value and throw_exception:
            raise KeyError(f'Required configuration field "{path}" not found')
        if as_primitive:
            value = OmegaConf.to_container(value)
        return value


def config_prompt() -> Config:
    """ Add a prompt solely to ask for a config path; then create and return
    the Config object."""
    parser = argparse.ArgumentParser()
    parser.add_argument(
        '--config',
        default='',
        help='name of the configuration file to use (e.g. \'default\')')
    args = parser.parse_args()
    config = Config.from_file(args.config)
    return config
