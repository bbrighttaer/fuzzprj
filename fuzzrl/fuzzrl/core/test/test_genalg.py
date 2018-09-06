import numpy as np
from fuzzrl.core.conf import Defuzz as dfz
from fuzzrl.core.test import *

LIN_VARS_FILE = "../res/linvarsGFT7.xml"
GFT_FILE = "../res/gft9.xml"


class TestGenAlg(unittest.TestCase):
    def test_initPopulation(self):
        pop_size = 1
        reg = Registry("test_reg")
        xmlToLinvars(open(LIN_VARS_FILE).read(), registry=reg)
        xmlToGFT(open(GFT_FILE).read(), registry=reg, defuzz_method=dfz.max_of_maximum)
        ga = GeneticAlgorithm(registry=reg)
        population = ga.generate_initial_population(pop_size)
        self.assertEqual(np.array(population).shape[0], pop_size)
        log.debug("Population size = {}".format(np.array(population).shape))
        print(str(population))
