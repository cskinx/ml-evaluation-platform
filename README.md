# ML Evaluation Platform
(... or: _Weights&Biases on a Budget_)

This project is based on the Keras example for predicting fuel efficiency found [here](https://www.tensorflow.org/tutorials/keras/regression). The purpose is to reproduce the steps from this notebook with more sound engineering. Specifically, results for particular models with certain configurations should be tracked and made easy to reproduce.

Ideally, this platform can also be used for any other similar problems and models, i.e., Keras models on tabular data. However, the intention is definitely not to produce production-level code but rather to explore how this problem could be modeled so that it becomes a lot more sustainable and scalable to train and evaluate ML approaches.   
For actual solutions to that problem, platforms such as [Kubeflow](https://www.kubeflow.org) ([metadata management](https://www.kubeflow.org/docs/components/metadata/), [pipelines](https://www.kubeflow.org/docs/components/pipelines/)), [DVC](https://dvc.org) ([experiment tracking](https://dvc.org/doc/start/experiments), [pipelines](https://dvc.org/doc/start/data-pipelines)) or [Weights&Biases](https://wandb.ai/site) are a lot more powerful and most of all they are specifically designed to properly handle these steps and requirements.

## Requirements
Only Docker is required to run the project.

If you want to run the Python scripts outside of a Docker image, Python 3.8 is required. All required packages can be installed with `requirements.txt` (`pip install -r requirements.txt`).

Note that the latest official Tensorflow release does not support Apple's M1 chip yet. [Here is a guide](https://github.com/apple/tensorflow_macos/issues/153) on how to install it in a way so that one can still use Tensorflow on newer Macbooks.

## Setup
### Fill out configuration
The central part to set the behavior of the pipeline is the configuration folder. The `default.yml` file contains example settings for our specific workflow to predict the fuel efficiency, and it should be very straight-forward to replace these arguments to change any of the steps in the pipeline. This includes the specific dataset (URL or file path), dataset characteristics, preprocessing steps, model hyperparameters, and also database connection details. If you only want to test a single different parameter, you can simply create a new configuration file in the same folder and add only this parameter. In that case, the values from the `default.yml` file will be taken and only this specific parameter is overwritten.

### Launch SQL database
We are using a PostgreSQL database based on the [official Docker image](https://hub.docker.com/_/postgres):

`docker run --name data-store -e POSTGRES_PASSWORD=<password> -p 5432:5432 --network="host" -d postgres:latest`

Note that you can use any other database as well, you simply have to fill out the right details in the configuration file under `database`.

### Build Docker image
We only use a single Dockerfile for all different script calls. To build it locally, in the main folder run:

`docker build -t ml-evaluation-platform .`

### Load dataset
To load the dataset, fill out the `dataset` parameters in the configuration file and run:

`docker run --network="host" ml-evaluation-platform python ./src/dataloader.py`

This will load the dataset specified in the `default.yml`; if you were to add the dataset details into a config file called `datasetB.yml`, you need to add `--config datasetB` to the end of script call.

### Run pipeline
To run the pipeline with all three steps (preprocessing, training, evaluation) as described in a specific configuration file, run:

`docker run --network="host" ml-evaluation-platform python ./src/pipeline.py --config dnn`

### Print information
You can also print various overviews:

- All loaded datasets:
`docker run --network="host" ml-evaluation-platform python ./src/info.py --type datasets`
- All runs:
`docker run --network="host" ml-evaluation-platform python ./src/info.py --type datasets`
- All recent good runs (from the last 7 days with an error of less than 2.5):
`docker run --network="host" ml-evaluation-platform python ./src/info.py --type relevant_runs`

## Extensions
This is just a first, very plain implementation of a model evaluation platform. There are a lot of potential extensions which hopefully would be fairly straight forward to add with the current modular structure. A few ideas:

- The configuration files could be even more powerful if any number of configuration files could be loaded; currently only 2 are supported, but one could easily support an arbitrary number with the latest config file overwriting the previous ones. This way, one could for example combine any preprocessing methods with any model parameters and quickly generate results for different combinations. It would also be nice to load a config from the database and save it directly as a .yml file to reproduce this run.
- It would be quite easy to generalize the model definitions even more; for example one could create a generic model which takes an arbitrary number of layers with specific sizes and activations functions. It would also be fairly straight-forward to also support other models such as PyTorch; one would just need to create generic `Model` and `Normalizer` classes which are used in the operator modules, and simply create the specific sub-classes of that type for the specific frameworks. This level of abstraction is definitely not needed for this notebook and this example.
- Currently, only the loss metric is supported for the evaluation; it would make a lot of sense to extend this to other metrics such as recall and precision. This also requires a change in the `DataStore` functions however, because it currently always sees lower scores as better ones.
- The pipeline is closely coupled from a user perspective, currently, even though they are different Python modules. It's not possible to e.g. only preprocess a dataset and then load that dataset later to train a model on it, and we also cannot store models currently. For large datasets and more complex models, this would definitely be an issue but for this problem we would simply be over-engineering it.
- It would also be nice if we could train a new model with a new configuration without having to re-build the Docker image. E.g. one could also add the possibility to pass a configuration as JSON dictionary via the command line interface.