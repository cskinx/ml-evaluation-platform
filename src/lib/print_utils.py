from typing import List, Dict


def print_dataset_overview(datasets_info: List[Dict]):
    """ Prints an overview of datasets in the DataStore."""
    print('Dataset Overview:')
    for dataset in datasets_info:
        print(f"- '{dataset['name']}': {dataset['size']:8d}")


def print_run_overview(runs_info: List[Dict], metric: str):
    """ Prints an overview of runs."""
    print('Runs:')
    for run_info in runs_info:
        run = run_info['run']
        columns = [
            run_info['label'],
            run.dataset_name,
            run.preprocessing_cfg['name'],
            run.model_name,
            f'{run.metric_scores[metric]:.2f}',
        ]
        print('\t'.join(columns))
