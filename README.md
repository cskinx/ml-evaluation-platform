# ML Evaluation Platform
This project is based on the Keras example for predicting fuel efficiency found [here](https://www.tensorflow.org/tutorials/keras/regression). The purpose is to reproduce the steps from that notebook with more sound engineering. Specifically, results for particular models with certain configurations should be tracked and made easy to reproduce. 

Ideally, this platform can also be used for any other similar problems and models, i.e., Keras models on tabular data. However, the intention is definitely not to produce production-level code but rather to explore how this problem could be modeled so that it becomes a lot more sustainable and scalable to train and evaluate ML approaches.   
For actual solutions to that problem, platforms such as [Kubeflow](https://www.kubeflow.org) ([metadata management](https://www.kubeflow.org/docs/components/metadata/) and [pipelines](https://www.kubeflow.org/docs/components/pipelines/)) and [DVC](https://dvc.org) ([experiment tracking](https://dvc.org/doc/start/experiments) and [pipelines](https://dvc.org/doc/start/data-pipelines)) are a lot more powerful and most of all they are specifically designed to properly handle each of these steps and requirements. 


## Requirements
Only Docker is required to run the project.

If you want to run some of the Python scripts outside of a Docker image we recommend using Python 3.8. All required packages are contained in `requirements.txt` (`pip install -r requirements.txt`).

Note that the latest official Tensorflow release does not support Apple's M1 chip yet. [Here is a guide](https://github.com/apple/tensorflow_macos/issues/153) on how to install it in a way so that one can still use Tensorflow on newer Macbooks.

## Setup
### Launch SQL database
We are using a PostgreSQL database with their [official Docker image](https://hub.docker.com/_/postgres):

`docker run --name data-store -e POSTGRES_PASSWORD=<password> -p 5432:5432 -d postgres:latest`


## Extensions
This is just a first, very plain implementation of a model evaluation platform. There are a lot of potential extensions which hopefully would be fairly straight forward to add with the current modular structure. A few ideas:

- The configuration files could be even more powerful if any number of configuration files could be loaded; currently only 2 are supported, but one could easily support an arbitrary number with the latest config file overwriting the previous ones. This way, one could for example combine any preprocessing methods with any model parameters and quickly generate results for different combinations. It would also be nice to load a config from the database and save it directly as a .yml file to reproduce this run.
