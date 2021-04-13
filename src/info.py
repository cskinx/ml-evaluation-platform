""" Main entry point to print various information."""
import argparse

from lib.config import Config
from lib.data_store import DataStore
from lib.print_utils import print_run_overview, print_dataset_overview

# modes
PRINT_DATASETS = 'datasets'
PRINT_RELEVANT_RUNS = 'relevant_runs'
PRINT_ALL_RUNS = 'all_runs'


def main(info_type: str, config: Config):
    data_store = DataStore(config)
    dataset_selected = config.get('dataset.name')
    metric_selected = config.get('model.hyperparameters.loss')
    if info_type == PRINT_DATASETS:
        overview = data_store.get_dataset_overview()
        print_dataset_overview(overview)
    elif info_type in [PRINT_RELEVANT_RUNS, PRINT_ALL_RUNS]:
        if info_type == PRINT_RELEVANT_RUNS:
            runs = data_store.load_recent_good_runs(
                dataset_selected,
                metric_selected,
                max_score=2.5)
        elif info_type == PRINT_ALL_RUNS:
            runs = data_store.load_runs()
        runs_info = [
            {'label': str(i + 1), 'run': run} for i, run in enumerate(runs)
        ]
        print_run_overview(runs_info, metric_selected)


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument(
        '--config',
        default='',
        help='name of the configuration file to use (e.g. \'default\')')
    parser.add_argument(
        '--type',
        required=True,
        choices=[PRINT_DATASETS, PRINT_RELEVANT_RUNS, PRINT_ALL_RUNS],
        help='choose type for what to print')
    args = parser.parse_args()
    config = Config.from_file(args.config)
    main(args.type, config)
