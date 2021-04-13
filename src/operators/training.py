from tensorflow import keras
import tensorflow as tf

from lib.config import Config
from lib.data_model import PreppedDataset
from custom_functions import ml_models


def train(dataset: PreppedDataset, config: Config)\
        -> keras.Sequential:
    # determine model type and get respective function
    model_type = config.get('model.type')
    try:
        build_model = getattr(ml_models, model_type)
    except AttributeError:
        # raise Exception with more explicit error message
        raise AttributeError('Could not find model function '
                             f'"{model_type}" in lib.models')
    # build
    model = build_model(config, dataset.normalizer)
    # compile
    learning_rate = config.get('model.hyperparameters.learning_rate')
    loss = config.get('model.hyperparameters.loss')
    model.compile(
        optimizer=tf.optimizers.Adam(learning_rate=learning_rate),
        loss=loss)
    # train
    epochs = config.get('model.hyperparameters.epochs')
    validation_split = config.get('model.hyperparameters.validation_split')
    model.fit(
        dataset.training_set, dataset.training_labels,
        epochs=epochs, validation_split=validation_split, verbose=0)
    return model
