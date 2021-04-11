from lib.config import Config, config_prompt
from operators.preprocessing import generate_dataset
from operators.training import train
from operators.evaluation import evaluate


def run_pipeline(config: Config):
    dataset = generate_dataset(config)
    model = train(dataset, config)
    evaluate(model, dataset, config)


if __name__ == '__main__':
    config = config_prompt()
    run_pipeline(config)
