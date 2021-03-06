from datetime import datetime

from tensorflow import keras

from lib.data_model import PreppedDataset, Run
from lib.config import Config
from lib.data_store import DataStore
from lib.print_utils import print_run_overview


def evaluate(model: keras.Sequential, dataset: PreppedDataset, config: Config):
    model_result = model.evaluate(
        dataset.test_set,
        dataset.test_labels,
        verbose=0,
        return_dict=True
    )
    # we could handle multiple metrics here but we are only measuring the
    # model loss (mean abs error) for now.
    metrics = {
        config.get('model.hyperparameters.loss'): model_result['loss']
    }
    run = Run(
        timestamp=datetime.now(),
        dataset_name=config.get('dataset.name'),
        preprocessing_cfg=config.get(
            'dataset.preprocessing',
            as_primitive=True),
        model_type=config.get('model.type'),
        model_hyperparameters=dict(config.get(
            'model.hyperparameters',
            as_primitive=True)),
        metric_scores=metrics
    )
    # store run and compare it to previous best runs
    metric = config.get('model.hyperparameters.loss')
    data_store = DataStore(config)
    best_run = data_store.get_best_run(run.dataset_name, metric)
    data_store.save_run(run)
    runs_info = []
    if best_run:
        runs_info.append({'label': 'Previous best', 'run': best_run})
    runs_info.append({'label': 'New run', 'run': run})
    print_run_overview(runs_info, metric)
