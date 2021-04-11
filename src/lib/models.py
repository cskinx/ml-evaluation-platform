from lib.config import Config
from tensorflow import keras
from tensorflow.keras.layers.experimental import preprocessing
import tensorflow as tf


def regression(config: Config, normalizer: preprocessing.Normalization)\
        -> keras.Sequential:
    # build model
    model = keras.Sequential([
        normalizer,
        tf.layers.Dense(units=1)
    ])
    # compile model
    learning_rate = config.get('model.hyperparameters.learning_rate')
    loss = config.get('model.hyperparameters.loss')
    model.compile(
        optimizer=tf.optimizers.Adam(learning_rate=learning_rate),
        loss=loss)
    return model


def dnn(config: Config, normalizer: preprocessing.Normalization)\
        -> keras.Sequential:
    # get layer sizes and check validity
    layer_sizes = config.get('model.hyperparameters.layer_sizes')
    if len(layer_sizes) != 2:
        raise ValueError('model.hyperparameters.layer_sizes requires two'
            ' values for dnn')
    if not all(isinstance(size, int) for size in layer_sizes):
        raise TypeError('model.hyperparameters.layer_sizes need to be'
            ' integer values')
    # build model
    model = keras.Sequential([
        normalizer,
        tf.layers.Dense(layer_sizes[0], activation='relu'),
        tf.layers.Dense(layer_sizes[1], activation='relu'),
        tf.layers.Dense(1)
    ])
    # compile model
    learning_rate = config.get('model.hyperparameters.learning_rate')
    loss = config.get('model.hyperparameters.loss')
    model.compile(
        optimizer=tf.optimizers.Adam(learning_rate=learning_rate),
        loss=loss)
    return model
