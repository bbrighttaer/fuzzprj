from fuzzrl.core.test import *
import numpy as np

LIN_VARS_FILE = "../res/linvarsGFT7.xml"
GFT_FILE = "../res/gft9.xml"


class TestGenAlg(unittest.TestCase):
    def test_initPopulation(self):
        pop_size = 1
        reg = Registry("test_reg")
        xmlToLinvars(open(LIN_VARS_FILE).read(), registry=reg)
        xmlToGFT(open(GFT_FILE).read(), registry=reg)
        ga = GeneticAlgorithm(registry=reg)
        population = ga.generate_initial_population(pop_size)
        self.assertEqual(np.array(population).shape[0], pop_size)
        log.debug("Population size = {}".format(np.array(population).shape))
        print(str(population))
