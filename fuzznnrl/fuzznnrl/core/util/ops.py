# project: fuzznnrl
# Copyright (C) 6/6/18 - 11:00 AM
# Author: bbrighttaer

import numpy as np


def softmax(x, axis=0):
    """
    Compute softmax values for each sets of scores in x.

    Parameters
    -----------
    :param x: The vector/matrix for the sotfmax operation
    :param axis:
    :return:
    """

    e_x = np.exp(x - np.max(x))
    return e_x / e_x.sum(axis=axis)


def boltzmanexp(probs, tau):
    probs = np.exp(probs / tau)
    probs = probs / np.sum(probs)
    return probs


def normalize(x, dl, dh, nl, nh):
    """
    Performs a range normalization operation.

    Parameters
    -----------
    :param x: The number/vector to be normalized
    :param dl: The minimum possible value of x.
    :param dh: The maximum possible value of x.
    :param nl: The minimum possible value of the normalized range.
    :param nh: The maximum possible value of the normalized range.
    :return: The normalized value(s).
    """
    return (((x - dl) * (nh - nl)) / (dh - dl)) + nl


def denormalize(x, dl, dh, nl, nh):
    """
    An inverse function of the range normalize operation.

    Parameters
    -----------
    :param x: The number/vector to be normalized
    :param dl: The minimum possible value of x.
    :param dh: The maximum possible value of x.
    :param nl: The minimum possible value of the normalized range.
    :param nh: The maximum possible value of the normalized range.
    :return: The de-normalized value(s).
    """
    return ((dl - dh) * x - (nl * dl) + dh * nl) / (nl - nh)


# Get The Current Date Or Time - credit: Richie Bendall [https://www.richie-bendall.ml/]
def getdatetime(timedateformat='complete'):
    from datetime import datetime
    timedateformat = timedateformat.lower()
    if timedateformat == 'day':
        return ((str(datetime.now())).split(' ')[0]).split('-')[2]
    elif timedateformat == 'month':
        return ((str(datetime.now())).split(' ')[0]).split('-')[1]
    elif timedateformat == 'year':
        return ((str(datetime.now())).split(' ')[0]).split('-')[0]
    elif timedateformat == 'hour':
        return (((str(datetime.now())).split(' ')[1]).split('.')[0]).split(':')[0]
    elif timedateformat == 'minute':
        return (((str(datetime.now())).split(' ')[1]).split('.')[0]).split(':')[1]
    elif timedateformat == 'second':
        return (((str(datetime.now())).split(' ')[1]).split('.')[0]).split(':')[2]
    elif timedateformat == 'millisecond':
        return (str(datetime.now())).split('.')[1]
    elif timedateformat == 'yearmonthday':
        return (str(datetime.now())).split(' ')[0]
    elif timedateformat == 'daymonthyear':
        return ((str(datetime.now())).split(' ')[0]).split('-')[2] + '-' + \
               ((str(datetime.now())).split(' ')[0]).split('-')[1] + '-' + \
               ((str(datetime.now())).split(' ')[0]).split('-')[0]
    elif timedateformat == 'hourminutesecond':
        return ((str(datetime.now())).split(' ')[1]).split('.')[0]
    elif timedateformat == 'secondminutehour':
        return (((str(datetime.now())).split(' ')[1]).split('.')[0]).split(':')[2] + ':' + \
               (((str(datetime.now())).split(' ')[1]).split('.')[0]).split(':')[1] + ':' + \
               (((str(datetime.now())).split(' ')[1]).split('.')[0]).split(':')[0]
    elif timedateformat == 'complete':
        return str(datetime.now())
    elif timedateformat == 'datetime':
        return (str(datetime.now())).split('.')[0]
    elif timedateformat == 'timedate':
        return ((str(datetime.now())).split('.')[0]).split(' ')[1] + ' ' + \
               ((str(datetime.now())).split('.')[0]).split(' ')[0]

# x = -0.027984769861725347 # np.array([10, 20, 30, 40, 50])
# norm = normalize(x, -3.4028235e+38, 3.4028235e+38, -10, 10)
# print("norm =", norm, "\ndenorm =", denormalize(norm, 0, 100, 0, 5))
