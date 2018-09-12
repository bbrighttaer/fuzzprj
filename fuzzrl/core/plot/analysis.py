# project: fuzzrl
# Copyright (C) 6/12/18 - 11:34 AM
# Author: bbrighttaer

import random


class _SeriesData(object):
    """
    Data container for a chart series
    """

    def __init__(self):
        self.__data = {'x': [], 'y': []}

    @property
    def data(self):
        return self.__data

    def record(self, t, v):
        """
        Add a record the series data

        Parameters
        ----------
        :param t: The x-axis value
        :param v: The y-axis value
        """
        if t is not None and v is not None:
            self.__data['x'].append(t)
            self.__data['y'].append(v)

    def clear(self):
        self.__data['x'].clear()
        self.__data['y'].clear()


class Series(object):
    """
    Models a series of a chart
    """

    def __init__(self, name, color="#%06x" % random.randint(0, 0xFFFFFF), marker='', linestyle='-', linewidth=1.0):
        self.__name = name
        self.__color = color
        self.__marker = marker
        self.__linestyle = linestyle
        self.__seriesData = _SeriesData()
        self.__linewidth = linewidth

    @property
    def name(self):
        return self.__name

    @property
    def color(self):
        return self.__color

    @property
    def marker(self):
        return self.__marker

    @property
    def linestyle(self):
        return self.__linestyle

    @property
    def linewidth(self):
        return self.__linewidth

    def data(self):
        """
        Returns the data of this series in a dictionary of two keys: {'x':[...],'y':[...]}
        """
        return self.__seriesData.data

    def addrecord(self, t, v):
        """
        Add a record the series data

        Parameters
        ----------
        :param t: The x-axis value
        :param v: The y-axis value
        """
        self.__seriesData.record(t, v)


class WeightedAvg(object):
    """
    Keeps an exponentially weighted average of the record given to it
    """

    def __init__(self, beta, correct_bias=True):
        self.__beta = beta
        self.__value = 0
        self.__t = 0
        self.__correct_bias = correct_bias

    @property
    def beta(self):
        return self.__beta

    @property
    def value(self):
        return self.__value

    def update(self, theta):
        self.__value = (self.__beta * self.__value) + ((1 - self.__beta) * theta)
        if self.__correct_bias:
            return self.__correction()
        else:
            return self.__value

    def __correction(self):
        self.__t = self.__t + 1
        return self.__value / (1 - (self.__beta ** self.__t))
