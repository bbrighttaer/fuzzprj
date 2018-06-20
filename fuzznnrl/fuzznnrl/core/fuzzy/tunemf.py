# project: fuzznnrl
# Copyright (C) 6/5/18 - 9:33 AM
# Author: bbrighttaer


from fuzznnrl.core.fuzzy import GAUSSIAN_MF, TRAPEZOID_MF, SIGMOID_MF


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


def tunegaussmf():
    pass


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
    return {GAUSSIAN_MF: lambda *x: tunegaussmf(),
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
