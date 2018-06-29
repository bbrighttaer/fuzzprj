# project: fuzzprj
# Copyright (C) 6/25/18 - 1:19 PM
# Author: bbrighttaer

import keras.metrics as metrics
from keras.models import Sequential
from keras.layers.core import Dense, Activation, Dropout
from keras.optimizers import Adam
from keras.layers import BatchNormalization
from keras.callbacks import Callback


# callback implementation to monitor training cost
class LossHistory(Callback):
    def __init__(self):
        super().__init__()
        self.__losses_acc = []

    @property
    def losses_acc(self):
        return self.__losses_acc

    def on_batch_end(self, batch, logs=None):
        self.__losses_acc.append((logs.get("loss"), logs.get("acc")))

    def on_train_begin(self, logs=None):
        self.__losses_acc = []


def neural_net(num_inputs, params, lr=0.001, loss="mean_squared_error", load=''):
    # create model
    model = Sequential()

    # input layer
    model.add(Dense(units=params[0], kernel_initializer='he_uniform', input_shape=(num_inputs,)))
    model.add(BatchNormalization())
    model.add(Activation('relu'))

    # hidden layer
    model.add(Dense(units=params[1], kernel_initializer='he_uniform'))
    model.add(BatchNormalization())
    model.add(Activation('relu'))

    # hidden layer
    model.add(Dense(units=params[2], kernel_initializer='he_uniform'))
    model.add(BatchNormalization())
    model.add(Activation('relu'))

    # output layer
    model.add(Dense(units=params[3], kernel_initializer='he_uniform'))
    model.add(BatchNormalization())
    model.add(Activation('softmax'))

    # finalize model creation
    opt = Adam(lr)
    model.compile(loss=loss, optimizer=opt, metrics=['accuracy', metrics.mae])

    # pre-trained weights have been specified
    if len(load) > 0:
        model.load_weights(load)
        print("weights loaded")

    return model
