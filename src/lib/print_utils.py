from typing import List, Dict
from collections import defaultdict


def print_dataset_overview(datasets_info: List[Dict]):
    """ Prints an overview of datasets in the DataStore."""
    print('Dataset Overview:')
    for dataset in datasets_info:
        print(f"- '{dataset['name']}': {dataset['size']:8d}")


def print_run_overview(runs_info: List[Dict], metric: str):
    """ Prints an overview of runs."""
    print('Runs:')
    header = ['Label', 'Date', 'Dataset', 'Preprocessing', 'Model', 'Metric']
    rows = [header, [''] * len(header)]
    for run_info in runs_info:
        run = run_info['run']
        if run is None:
            continue
        columns = [
            run_info['label'],
            f'{run.timestamp:%Y-%m-%d}',
            run.dataset_name,
            run.preprocessing_cfg['name'],
            run.model_type,
            f'{run.metric_scores[metric]:.2f}',
        ]
        rows.append(columns)
    max_widths = defaultdict(int)
    for row in rows:
        for i, column in enumerate(row):
            max_widths[i] = max([max_widths[i], len(column)])
    total_width = sum([val + 3 for val in max_widths.values()])
    print('-' * total_width)
    for row in rows:
        for i, column in enumerate(row):
            print(f'{column:<{max_widths[i]}}', end='')
            print(' | ', end='')
        print()
    print('-' * total_width)
