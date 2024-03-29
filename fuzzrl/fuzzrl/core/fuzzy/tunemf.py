# project: fuzzrl
# Copyright (C) 6/5/18 - 9:33 AM
# Author: bbrighttaer


from fuzzrl.core.fuzzy import GAUSSIAN_MF, TRAPEZOID_MF, SIGMOID_MF


def tunetrimf(a, b, c, delta, eta):
    """
    Tunes the parameters of a triangular membership function T(a, b, c) with the parameters delta and eta
    Condition: a <= b <= c

    Parameters
    -----------
    :param a: The first parameter of the triangle
    :param b: The second parameter of the triangle
    :param c: The third parameter of the triangle
    :param delta: tuning parameter
    :param eta: tuning parameter
    :return: a tuple (a', b', c')
    """
    assert a <= b <= c
    # left or right shift of MF on the x axis
    a = (a + delta) - eta
    b = b + delta
    c = (c + delta) - eta
    assert a <= b <= c
    return a, b, c


def tunegaussmf(mean, sigma, param1, param2):
    """
    Tunes the mean and standard deviation of a Gaussian MF
    ----------------------

    :param mean: The mean of the MF
    :param sigma: The S.D. of the MF
    :param param1: parameter 1 for tuning mean
    :param param2: parameter 2 for tuning sigma
    :return: a tuple: (mean_prime, sigma_prime)
    """
    mean += param1
    sigma += param2
    return mean, abs(sigma)


def tunetrapmf():
    pass


def tunemf(mftype, *args):
    """
    Convenience method for tuning membership functions.
    The triangular MF is treated as the default case

    Parameters
    -----------
    :param mftype: The type of membership function (e.g. Triangular, Gaussian, etc.)
    :param args: terms of the tuning function
    :return: tuned membership function parameters
    """
    return {GAUSSIAN_MF: lambda *x: tunegaussmf(*x),
            TRAPEZOID_MF: lambda *x: tunetrapmf()}.get(mftype.lower(),
                                                       lambda *x: tunetrimf(*x))(*args)


def gettuningparamsize(mftype):
    """
    Determines the number of tuning parameters of a given membership function.
    The triangular MF is treated as the default case.

    Parameters
    ------------
    :param mftype: The type of membership function
    :return: the number of tuning parameters
    :rtype: int
    """
    return {
        GAUSSIAN_MF: 2,
        TRAPEZOID_MF: 2,
        SIGMOID_MF: 3
    }.get(mftype.lower(), 2)
