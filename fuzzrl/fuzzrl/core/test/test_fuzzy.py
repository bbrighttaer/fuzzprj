from fuzzrl.core.test import *

from fuzzrl.core.conf import Defuzz as dfz
LIN_VARS_FILE = "../../res/linvarsGFT7.xml"
GFT_FILE = "../../res/gft9.xml"


class TestFuzzyModule(unittest.TestCase):
    def test_createControlSystemSim(self):
        reg, pop = getpopulation(1)
        num_gfs = len(reg.gft_dict)
        gfs = reg.gft_dict[list(reg.gft_dict.keys())[0]]
        print("\nrb:", pop[0, gfs.descriptor.position], " /", len(pop[0, gfs.descriptor.position]),
              "\nmf:", pop[0, gfs.descriptor.position + num_gfs], " /", len(pop[0, gfs.descriptor.position + num_gfs]))


def getpopulation(pop_size):
    reg = Registry("test_reg")
    xmlToLinvars(open(LIN_VARS_FILE).read(), registry=reg)
    xmlToGFT(open(GFT_FILE).read(), registry=reg, defuzz_method=dfz.max_of_maximum)
    ga = GeneticAlgorithm(registry=reg)
    return reg, ga.generate_initial_population(pop_size)
