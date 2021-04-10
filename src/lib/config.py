from omegaconf import OmegaConf
import os


def get_config(name: str = '', config_dir: str = './configs'):
    """ Load the configuration files properly; always reads the default.yml
    but overwrites its values if a more specific file is given."""
    # load default config
    default_cfg_path = os.path.join(config_dir, 'default.yml')
    config = OmegaConf.load(default_cfg_path)
    # load more specific config
    specific_cfg_path = os.path.join(config_dir, name, '.yml')
    if os.path.exists(specific_cfg_path):
        specific_config = OmegaConf.load(specific_cfg_path)
        config = OmegaConf.merge(config, specific_config)
    return config


def get_value(config, path):
    """ Returns the value at the given path of the config;
    just a wrapper to hide the OmegaConf library."""
    return OmegaConf.select(config, path)
