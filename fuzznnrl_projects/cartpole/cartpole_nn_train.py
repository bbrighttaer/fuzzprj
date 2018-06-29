# project: fuzzprj
# Copyright (C) 6/25/18 - 3:22 PM
# Author: bbrighttaer


import logging as log

import matplotlib.pyplot as plt
import numpy as np
import tensorflow as tf

from fuzznnrl_projects.cartpole.cartpole_nn import neural_net, LossHistory

np.random.seed(1)
tf.set_random_seed(1)

model_path = "cartpole_model.h5"

LOG_FORMAT = "%(asctime)s - %(levelname)s - %(message)s"
log.basicConfig(level=log.INFO, format=LOG_FORMAT)

EPOCHS = 5
BATCH_SIZE = 128


def batch_generator(path, batch_size):
    with open(path, mode='r') as f:
        read = True
        while read:
            data = []
            for i in range(batch_size):
                line = f.readline()
                if len(line) > 0:
                    row = eval('[{}]'.format(line))
                    data.append(row)
                else:
                    read = False
            data = np.array(data).squeeze()
            if len(data) > 0:
                X = data[:, :4]
                Y = data[:, 4:6]
                yield (X, Y)
    log.debug("file closed")


def generator_eval():
    count = 0
    for X, Y in batch_generator(path="data/dev_set.csv", batch_size=128):
        count += 1
        print(str(X), str(Y), count)


def train_net():
    params = [10, 50, 30, 2]
    model = neural_net(num_inputs=4, params=params, lr=0.1)
    hist = LossHistory()
    loss = []
    num_batches_train = None
    num_batches_dev = None
    num_batches_test = None
    for i in range(EPOCHS):
        num_batches_train = len_batches("data/training_set.csv",
                                        BATCH_SIZE) if num_batches_train is None else num_batches_train
        model.fit_generator(generator=batch_generator("data/training_set.csv", BATCH_SIZE),
                            epochs=1, callbacks=[hist],
                            verbose=1,
                            steps_per_epoch=num_batches_train)
        # dev set evaluation
        log.info("Dev set evaluation")
        num_batches_dev = len_batches("data/dev_set.csv", BATCH_SIZE) if num_batches_dev is None else num_batches_dev
        eval_stats = model.evaluate_generator(generator=batch_generator("data/dev_set.csv", BATCH_SIZE),
                                              steps=num_batches_dev)
        print(model.metrics_names, "\n", eval_stats)

        # test set evaluation
        log.info("Test set evaluation")
        num_batches_test = len_batches("data/test_set.csv",
                                       BATCH_SIZE) if num_batches_test is None else num_batches_test
        eval_stats = model.evaluate_generator(generator=batch_generator("data/test_set.csv", BATCH_SIZE),
                                              steps=num_batches_test)
        print(model.metrics_names, "\n", eval_stats)

        for l, acc in hist.losses_acc:
            loss.append(l)

    plt.figure(0)
    plt.plot(loss)
    plt.xlabel("iteration")
    plt.ylabel("loss")
    plt.show()

    # save model weights
    model.save_weights(model_path, overwrite=True)


def len_batches(path, batch_size):
    count = 0
    for _ in batch_generator(path, batch_size):
        count += 1
    return count


if __name__ == '__main__':
    train_net()
