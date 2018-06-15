# project: fuzznnrl
# Copyright (C) 6/8/18 - 5:57 PM
# Author: bbrighttaer


class Operator(object):
    """
    Container for a GA operator and its arguments to be passed to
    the operator when it is called.
    """
    def __init__(self, func, **kwargs):
        """
        Creates a GA operator.

        Parameters
        ------------
        :param func: The function serving as a GA operator
        :param kwargs: The arguments to be passed to the function
        """
        self.__func = func
        self.__kwargs = kwargs

    @property
    def func(self):
        return self.__func

    @property
    def kwargs(self):
        return self.__kwargs
