import os
from typing import Any
import argparse

from omegaconf import OmegaConf


class Config:
    """ A wrapper for the functionality from omegaconfg.
    Basically just reads the 'configs/default.yml' file plus one optional other
    config file and makes the values accessible by path strings."""

    def __init__(self, name: str = '', config_dir: str = './configs'):
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
        self.config = config

    def get(self, path, throw_exception=True) -> Any:
        """ Returns the value at the given path of the config;
        if field is mandatory, an Exception should be thrown."""
        value = OmegaConf.select(self.config, path)
        if not value and throw_exception:
            raise KeyError(f'Required configuration field "{path}" not found')
        return value


def config_prompt() -> Config:
    """ Add a prompt solely to ask for a config path; then create and return
    the Config object."""
    parser = argparse.ArgumentParser()
    parser.add_argument('--config', default='',
        help='name of the configuration file to use (e.g. \'default\')')
    args = parser.parse_args()
    config = Config(args.config)
    return config
