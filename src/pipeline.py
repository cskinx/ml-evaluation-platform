from lib.config import Config, config_prompt
from operators.preprocessing.preprocessing import generate_dataset


def run_pipeline(config: Config):
    generate_dataset(config)


if __name__ == '__main__':
    config = config_prompt()
    run_pipeline(config)
