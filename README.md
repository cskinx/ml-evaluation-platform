# ML Evaluation Platform
This project is based on the Keras example for predicting fuel efficiency found [here](https://www.tensorflow.org/tutorials/keras/regression). The purpose is to reproduce the steps from that notebook with more sound engineering. Specifically, results for particular models with certain configurations should be tracked and made easy to reproduce. 

Ideally, this platform can also be used for any other similar problems and models, i.e., Keras models on tabular data. However, the intention is definitely not to produce production-level code but rather to explore how this problem could be modeled so that it becomes a lot more sustainable and scalable to train and evaluate ML approaches.   
For actual solutions to that problem, platforms such as [Kubeflow](https://www.kubeflow.org) ([metadata management](https://www.kubeflow.org/docs/components/metadata/) and [pipelines](https://www.kubeflow.org/docs/components/pipelines/)) and [DVC](https://dvc.org) ([experiment tracking](https://dvc.org/doc/start/experiments) and [pipelines](https://dvc.org/doc/start/data-pipelines)) are a lot more powerful and most of all they are specifically designed to properly handle each of these steps and requirements. 


## Requirements
Only Docker is required to run the project.

If you want to run some of the Python scripts outside of a Docker image we recommend using Python 3.8. All required packages are contained in `requirements.txt` (`pip install -r requirements.txt`).


## Setup
### Launch SQL database
We are using a PostgreSQL database with their [official Docker image](https://hub.docker.com/_/postgres):

`docker run --name data-store -e POSTGRES_PASSWORD=<password> -p 5432:5432 -d postgres:latest`