# project: fuzznnrl
# Copyright (C) 6/14/18 - 10:28 AM
# Author: bbrighttaer
from abc import abstractmethod, ABCMeta
from math import exp, floor, pow


class ProbabilitySchedule(metaclass=ABCMeta):
    """
    Parent class for adjusting probabilities during the simulation.
    """

    def __init__(self, initial_prob, decay_factor):
        """
        :param initial_prob: The initial probability
        :param decay_factor: The probability decay factor in each epoch
        """
        self.__prob = initial_prob
        self.__decay_factor = decay_factor

    @property
    def prob(self):
        return self.__prob

    @prob.setter
    def prob(self, val):
        self.__prob = val

    @property
    def decay_factor(self):
        return self.__decay_factor

    @decay_factor.setter
    def decay_factor(self, val):
        self.__decay_factor = val

    @abstractmethod
    def get_prob(self, epoch):
        """
        Retrieves the probability to be used for the given epoch as defined by the schedule
        :param epoch: The current epoch whose probability is of interest
        :return: the probability to be applied
        :rtype: float
        """


class LinearDecaySchedule(ProbabilitySchedule):
    """
    Decays the probability by a constant factor
    """

    def __init__(self, initial_prob, decay):
        super().__init__(initial_prob, decay)

    def get_prob(self, epoch):
        v = self.prob
        self.prob -= self.decay_factor
        return v


class ExponentialDecaySchedule(ProbabilitySchedule):
    """
    Decays the probability exponentially over the course of the simulation
    """

    def __init__(self, initial_prob, decay_factor):
        super().__init__(initial_prob, decay_factor)
        self.__init_prob = initial_prob

    def get_prob(self, epoch):
        self.prob = self.__init_prob * exp(-self.decay_factor * epoch)
        return self.prob


class StepDecaySchedule(ProbabilitySchedule):
    """
    Applies a step-wise decay to the probability over the course of the simulation
    """

    def __init__(self, initial_prob, decay_factor, epochs_drop):
        super().__init__(initial_prob, decay_factor)
        self.__epochs_drop = epochs_drop
        self.__init_prob = initial_prob

    def get_prob(self, epoch):
        self.prob = self.__init_prob * pow(self.decay_factor, floor((1 + epoch) / self.__epochs_drop))
        return self.prob


class TimeBasedSchedule(ProbabilitySchedule):
    """
    Decays the probability over time
    """

    def __init__(self, decay_factor):
        super().__init__(initial_prob=0, decay_factor=decay_factor)

    def get_prob(self, epoch):
        self.prob = 1. / (1. + self.decay_factor * epoch)
        return self.prob
