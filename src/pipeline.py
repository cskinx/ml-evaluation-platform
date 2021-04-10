from lib.config import Config, config_prompt
from operators.preprocessing.preprocessing import generate_dataset


def run_pipeline(config: Config):
    dataset = generate_dataset(config)
    print(dataset.training_set)
    print(dataset.test_set)


if __name__ == '__main__':
    config = config_prompt()
    run_pipeline(config)
