from lib.config import Config, config_prompt
from operators.preprocessing import preprocess


def run_pipeline(config: Config):
    preprocess(config)


if __name__ == '__main__':
    config = config_prompt()
    run_pipeline(config)
