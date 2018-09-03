
import random
import numpy as np
from deap import base
from deap import creator
from deap import tools
from fuzzrl.core.conf import Constants as const, Constants


class GeneticAlgorithm(object):
    """
    Provides all GA operations
    """

    def __init__(self, registry, weights=(1.0,), seed=None):
        """
        Creates a GA instance
        :type weights: Indicator whether the GA operation is for maximization or minimization problem.
        The default indicates a maximization task for a single fitness function.
        :param registry: The GFT registry with already created linguistic variables and GFSs of the GFT
        """
        if seed is not None:
            random.seed(seed)
        creator.create("FitnessMax", base.Fitness, weights=weights)
        creator.create("Partial_Individual", list)
        creator.create("Individual", list, fitness=creator.FitnessMax)
        self.__registry = registry
        self.__toolbox = base.Toolbox()
        self.__toolbox.register("partial_ind", tools.initRepeat, creator.Partial_Individual)

        # statistics
        self.__stats = tools.Statistics(key=lambda ind: ind.fitness.values)
        self.__stats.register("avg", np.mean)
        self.__stats.register("std", np.std)
        self.__stats.register("min", np.min)
        self.__stats.register("max", np.max)

        # logging
        self.__logbook = tools.Logbook()

    @property
    def stats(self):
        return self.__stats

    @property
    def logbook(self):
        return self.__logbook

    def __create_rb_partial_chrom(self, rbsize, generange):
        return self.__toolbox.partial_ind(self.__rand_rb(generange[0], generange[1]), rbsize)

    def __create_mf_partial_chrom(self, mfsize):
        if random.random() < const.ZEROS_MF_SEGMENT:
            return self.__toolbox.partial_ind(self.__rand_mf(0, 0), mfsize)
        else:
            return self.__toolbox.partial_ind(self.__rand_mf(const.MF_TUNING_RANGE[0], const.MF_TUNING_RANGE[1]),
                                              mfsize)

    def __create_rb_operators_chrom(self, size):
        return self.__toolbox.partial_ind(self.__rand_rb(0, 1), size)

    def __rand_mf(self, min, max):
        return lambda a=min, b=max: random.uniform(a, b)

    def __rand_rb(self, min, max):
        return lambda a=min, b=max: random.randint(a, b)

    def generate_initial_population(self, pop_size):
        """
        Randomly generates initial population using the GFT information in the registry
        :rtype: np.ndarray
        :param pop_size: The population size
        :return: A list of individuals
        """
        population = []
        for _ in range(pop_size):
            # construct the individual
            rb_segment, mf_segment, rb_operator_seg = [], [], []
            for _, fis in self.__registry.gft_dict.items():
                descriptor = fis.descriptor
                rb_segment.append(self.__create_rb_partial_chrom(descriptor.rbSize, descriptor.outputGeneRange))
                mf_segment.append(self.__create_mf_partial_chrom(descriptor.mfSize))
                if const.LEARN_RULE_OP:
                    rbopsnum = getrbopsnum(descriptor)
                    rb_operator_seg.append(self.__create_rb_operators_chrom(rbopsnum))

            individual = rb_segment + mf_segment + rb_operator_seg

            # convert the individual to DEAP individual and add it to the population (wrapping)
            individual = creator.Individual(individual)
            population.append(individual)
        return population

    @staticmethod
    def load_initial_population(file, size):
        """
        Loads an already saved list of individuals
        :param file: The full filename containing the individuals
        :param size: The number of individuals to be created from the file
        :return: A list of individuals
        """
        population = []
        if file is not None and size > 0:
            with open(file) as f:
                data = f.read().split('\n')
                if data is not None and len(data) > 0:
                    # clean the last empty line
                    data = data[:len(data) - 2]
                    # stores the evaluated data
                    eval_data = []
                    # convert the file contents to python object
                    for d in data:
                        eval_data.append(eval(d))
                    data = eval_data
                    i = 0
                    while len(data) > 0 and len(population) < size:
                        ind = data[i % len(data)]
                        if len(ind) > 0:
                            population.append(creator.Individual(ind))
                        i += 1
        return population

    def selection(self, individuals, func, **kwargs):
        """
        Performs selection on the GFT individuals using the given function/algorithm and arguments

        Parameters
        -------------
        :param individuals: The GFT chromosomes
        :param func: The selection operator
        :param kwargs: The arguments to the selection operator
        :return: A list of selected individuals.
        """
        if callable(func):
            return func(individuals, **kwargs)

    def crossover(self, cross_prob, offspring, func, **kwargs):
        """
        Applies crossover to the different segments of the GFT chromosomes in place.

        Parameters
        ------------
        :param cross_prob: Crossover probability
        :param offspring: The GFT chromosomes
        :param func: The mating function
        :param kwargs: The arguments to the function
        :return: The offspring
        """
        # Clone the selected individuals
        offspring = [self.__toolbox.clone(ind) for ind in offspring]

        # for keeping best performing parents
        offspring.sort(key=lambda ind: ind.fitness.values, reverse=True)
        next_gen = []

        # Apply crossover on the offspring
        for child1, child2 in zip(offspring[::2], offspring[1::2]):
            if random.random() < cross_prob:
                for p1, p2 in zip(child1, child2):
                    func(p1, p2, **kwargs)
                next_gen.append(self.__toolbox.clone(child1))
                next_gen.append(self.__toolbox.clone(child2))

        # apply elitism
        keep_num = len(offspring) - len(next_gen)
        for i in range(keep_num):
            next_gen.append(offspring[i])

        # clear existing fitness values
        for child in next_gen:
            del child.fitness.values
        return next_gen

    def mutation(self, mut_prob, offspring, func, **kwargs):
        """
        Applies mutation to the different segments of the GFT chromosomes in place.

        Parameters
        -----------
        :param mut_prob: Mutation probability
        :param offspring: The GFT chromosomes
        :param func: The mutation operator
        :param kwargs: The arguments to the mutation operator
        """
        # Apply mutation on the offspring
        for mutant in offspring:
            if random.random() < mut_prob:
                for part in mutant:
                    func(part, **kwargs)
                del mutant.fitness.values

        # check bounds of mutation of RB & MF parts
        num_gfts = len(self.__registry.gft_dict)
        for _, fis in self.__registry.gft_dict.items():
            for mutant in offspring:
                # RB segment
                self.__checkbounds(mutant[fis.descriptor.position],
                                   fis.descriptor.outputGeneRange[0],
                                   fis.descriptor.outputGeneRange[1])
                # MF segment
                self.__checkbounds(mutant[fis.descriptor.position + num_gfts],
                                   const.MF_TUNING_RANGE[0],
                                   const.MF_TUNING_RANGE[1], apply_round=False)

                # RB operator segment
                if Constants.LEARN_RULE_OP:
                    self.__checkbounds(mutant[fis.descriptor.position + (2 * num_gfts)], 0, 1)

    def __checkbounds(self, child, min, max, apply_round=True):
        """
        Ensures that all genes are within defined ranges.

        Parameters
        ------------
        :param child: The child or chromosome under inspection
        :param min: The minimum value of the range
        :param max: The maximum value of the range
        :param apply_round: Whether gene values should be rounded to the nearest integer
        :return: An inspected child or chromosome
        """
        for i in range(len(child)):
            if child[i] > max:
                child[i] = max
            elif child[i] < min:
                child[i] = min
            if apply_round:
                child[i] = round(child[i])
        return child

    def evolve(self, individuals, selop, crossop, mutop, cross_prob, mut_prob):
        """
        Performs a single GA evolution operation on the given individuals.

        Parameters
        ------------
        :param cross_prob: Crossover probability (NB: when less than 1 then elitism is enabled).
        :param mut_prob: Mutation probability
        :param individuals: The individuals for the GA process
        :param selop: The selection operator
        :param crossop: The crossover operator
        :param mutop: The mutation operator
        :return: Offspring from the GA process
        """
        # Select the next generation individuals
        offspring = self.selection(individuals, selop.func, **selop.kwargs)

        # Apply crossover on the offspring
        offspring = self.crossover(cross_prob, offspring, crossop.func, **crossop.kwargs)

        # Apply mutation on the offspring
        self.mutation(mut_prob, offspring, mutop.func, **mutop.kwargs)

        return offspring


def getrbopsnum(descriptor):
    """
    Returns the total number of AND or OR operators that are needed to construct the rules of a GFS
    :param descriptor: Provides the details of a GFS as specified in the configuration file
    :return:
    """
    return descriptor.rbSize * (len(descriptor.inputVariables.inputVar) - 1)
