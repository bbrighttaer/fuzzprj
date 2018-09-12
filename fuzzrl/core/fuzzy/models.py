import sys

import numpy as np
import skfuzzy as fuzz
import skfuzzy.control as ctrl


class GeneticFuzzySystem(object):
    """
    The structure of Genetic Fuzzy Systems in a GFT
    """

    def __init__(self, name, descriptor, vars_config_dict={}):
        """
        Creates an GFS
        :param name: The name of the GFS
        :param descriptor: The configuration details of this GFS
        :param vars_config_dict: The configuration details of all linguistic variables of the GFS
        """
        self.__name = name
        self.__descriptor = descriptor
        self.__vars_config_dict = vars_config_dict
        self.__rules = []
        self.controlSystemSimulation = None
        self.__antecedents = []
        self.__consequent = None

    @property
    def name(self):
        return self.__name

    @name.setter
    def name(self, name):
        self.__name = name

    @property
    def descriptor(self):
        return self.__descriptor

    @descriptor.setter
    def descriptor(self, desc):
        self.__descriptor = desc

    @property
    def vars_config_dict(self):
        return self.__vars_config_dict

    @vars_config_dict.setter
    def vars_config_dict(self, dict):
        self.__vars_config_dict = dict

    @property
    def rules(self):
        return self.__rules

    @property
    def controlSystemSimulation(self):
        return self.__controlSystemSimulation

    def contructControlSystemSim(self, rb_chrom=[], mf_chrom=[]):
        """
        Creates the control system for simulation
        :param rb_chrom: The RCGA string for constructing the GFS-RB
        :param mf_chrom: The RCGA string for tuning tunable MFs
        """
        pass

    def __createAntecedents(self, mf_chrom):
        chrom_index = 0
        try:
            for var in self.__descriptor.inputVariables:
                var_config = self.__vars_config_dict[var.identity.type]
                universe = np.arange(var_config.rangeMin, var_config.rangeMax, 1, dtype=float)
                antecedent = ctrl.Antecedent(universe, var_config.name)
                self.__antecedents.append(antecedent)
                for term in var_config.terms:
                    pSize = len(term.params)
                    if var.tune:
                        params = np.array(term.params) + mf_chrom[chrom_index:(chrom_index + pSize)]
                        chrom_index += pSize
                    else:
                        params = np.array(term.params)
                    antecedent[term.name] = self.__createMF(term.mf, params=params, universe=universe)
        except IndexError:
            print("Error creating antecedents for {}".format(self.name))
            sys.exit(-1)
        else:
            print("All antecedents for {} created successfully", self.name)

    def __createConsequent(self):
        var = self.__descriptor.outputVariable
        var_config = self.__vars_config_dict[var.type]
        self.__consequent = ctrl.Consequent(np.arange(var_config.rangeMin, var_config.rangeMax, 1, dtype=float),
                                            var_config.name)
        for term in var_config.terms:
            self.__consequent[term.name] = self.__createMF(term.mf, term.params, self.__consequent.universe)

    def __createMF(self, mf_type, params, universe):
        return {"trapezoid": lambda *args: fuzz.trapmf(*args),
                "gaussian": lambda *args: fuzz.gaussmf(*args),
                "sigmoid": lambda *args: fuzz.sigmf(*args)
                }.get(mf_type.lower(), lambda *args: fuzz.trimf(*args))(universe, params)

    def __createRuleBase(self, rb_chrom):
        pass

    def __genrule(self):
        pass
