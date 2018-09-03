import random
import time

import deap.tools as tools
import numpy as np

from fuzzrl.core.algorithm.alg import Algorithm
from fuzzrl.core.conf import setconstants
from fuzzrl.core.conf.parser import *
from fuzzrl.core.ga.genalg import GeneticAlgorithm
from fuzzrl.core.ga.op import Operator

POP_SIZE = 4
LIN_VARS_FILE = "../res/linvarsGFT7.xml"
GFT_FILE = "../res/gft9.xml"


def startsim():
    # sets up the registry
    reg = xmlToGFT(open(GFT_FILE).read(), registry=xmlToLinvars(open(LIN_VARS_FILE).read()))

    # create the GA object for accessing GA operations
    ga = GeneticAlgorithm(registry=reg)

    # get the algorithm for execution
    alg = Algorithm(registry=reg)

    # get the initial population
    population = ga.generate_initial_population(POP_SIZE)

    # print initial population
    for child in population:
        print(child)

    # get the one GFS for debugging
    gfs = reg.gft_dict[list(reg.gft_dict.keys())[2]]

    # # the total number of GFSs in the GFT
    # num_gfs = len(reg.gft_dict)

    # # extracts the RB and MF segments of a chromosome/individual
    # rb_chrom = population[0, gfs.descriptor.position]
    # mf_chrom = population[0, gfs.descriptor.position + num_gfs]
    #
    # # construct the control system of the selected GFS
    # gfs.contructControlSystemSim(rb_chrom, mf_chrom)

    # print(str(population[0].fitness.values))

    # configure the KB
    alg.configuregft(np.array(population[0]))

    # execute gfs
    code, action, input_vec_dict, probs_dict = alg.executegft(TestObserve(), 0)
    print("code = {0}, action = {1}\nprobs = {2}".format(code, action, str(probs_dict)))

    # print generated rules
    rules = gfs.rules
    for i in range(len(rules)):
        print("[{0}] {1}".format(i + 1, str(rules[i])))

    # RB and MF redefinition test
    tic = time.time()
    alg.configuregft(np.array(population[1]))
    code, action, input_vec_dict, probs_dict = alg.executegft(TestObserve(), 0)
    print("\ncode = {0}, action = {1}\nprobs = {2}".format(code, action, str(probs_dict)))
    print("time for redefintion =", (time.time() - tic))
    rules = gfs.rules
    for i in range(len(rules)):
        print("[{0}] {1}".format(i + 1, str(rules[i])))

    # dummy fitness values
    for i in range(len(population)):
        population[i].fitness.values = (random.randint(0, 10), 0)

    # create selection operator
    selargs = {"k": len(population),
               "tournsize": 3}
    selop = Operator(tools.selTournament, **selargs)

    # create crossover operator
    crossargs = {"indpb": 0.2}
    crossop = Operator(tools.cxUniform, **crossargs)

    # create mutation operator
    mutargs = {"mu": 0,
               "sigma": 1,
               "indpb": 0.2}
    mutop = Operator(tools.mutGaussian, **mutargs)

    # Perform one step of evolution
    offspring = ga.evolve(population, selop=selop, crossop=crossop,
                          mutop=mutop, mut_prob=0.2, cross_prob=0.7)

    assert offspring is not None

    # print out the offspring of the evolution step
    print("Num of offspring =", len(offspring))
    for child in offspring:
        print(child)


class TestObserve(object):
    def getNumberOfUnconqueredIslands(self, agent):
        return random.randint(0, 5)

    def pgf_attacked(self, agent):
        return random.random()

    def pgf_moved(self, agent):
        return random.random()

    def pgf_conquered(self, agent):
        return random.random()

    def pgf_retreated(self, agent):
        return random.random()

    def getNumberOfDetectedEnemies(self, agent):
        return random.randint(0, 5)

    def getStayingPower(self, agent):
        return random.randint(0, 5)

    def getNumTeammatesUnderFire(self, agent):
        return random.randint(0, 5)

    def getPrincipalEigenValue(self, agent):
        return random.randint(0, 4)


if __name__ == "__main__":
    setconstants()
    startsim()
