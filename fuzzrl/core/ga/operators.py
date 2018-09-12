# project: fuzzrl
# Copyright (C) 6/8/18 - 5:57 PM
# Author: bbrighttaer

# import random
# from deap import base
# from deap import creator
# from deap import tools


def selection(population, selago, selprob):
    """
    Performs selection on a GFT chromosome.

    Parameters:
    -------------
    :param population: The population for the selection process. Must be sk-fuzzy
    individuals with fitness value
    :param selago: The selection algorithm to use
    :param selprob: The selection probability
    :return: Selected individuals
    """
    pass


def crossover(population, crossalgo, crossprob, epoch):
    """
    Applies crossover on the given population

    Parameters:
    ------------
    :param population: The GFT individuals for the crossover process
    :param crossalgo: The crossover algorithm to use
    :param crossprob: The crossover probability
    :param epoch: The current generation number
    """
    pass


def mutation(population, mutalgo, mutprob, epoch):
    """
    Applies mutation on the members of the given population

    Parameters:
    -------------
    :param population: The population for the mutation operation
    :param mutalgo: The mutation algorithm to be used
    :param mutprob: The mutation probability
    :param epoch: The current generation number
    :return:
    """
    pass
