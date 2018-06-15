import sys

import numpy as np
import skfuzzy as fuzz
import skfuzzy.control as ctrl

import fuzznnrl.core.conf.exceptions as ex
from fuzznnrl.core.fuzzy import GAUSSIAN_MF, SIGMOID_MF, TRAPEZOID_MF
from fuzznnrl.core.fuzzy.tunemf import tunemf, gettuningparamsize


class GeneticFuzzySystem(object):
    """
    The structure of Genetic Fuzzy Systems in a GFT
    """

    def __init__(self, descriptor, vars_config_dict={}, defuzz_method="lom"):
        """
        Creates an GFS
        ---------------

        :param defuzz_method: The defuzzification method to be used in the control system. The default is the
        max-of-maximum method.

        :param descriptor: The configuration details of this GFS

        :param vars_config_dict: The configuration details of all linguistic variables of the GFS
        """
        self.__name = descriptor.name
        self.__descriptor = descriptor
        self.__vars_config_dict = vars_config_dict
        self.__defuzz_method = defuzz_method
        self.__rules = []
        self.__controlSystem = None
        self.__controlSystemSimulation = None
        self.__antecedents = []
        self.__consequent = None
        self.__controlSystem_created = False

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
    def consequent(self):
        return self.__consequent

    @property
    def rules(self):
        return self.__rules

    @property
    def controlSystem(self):
        return self.__controlSystem

    @property
    def controlSystemSimulation(self):
        return self.__controlSystemSimulation

    def buildControlSystem(self):
        pass

    def buildControlSystemSim(self, rb_chrom, mf_chrom):
        """
        Creates the control system for simulation if no control system has been created or
        reuse created properties by re-configuring them with the submitted rb_chrom and mf_chrom
        :param rb_chrom: The RCGA string for constructing the GFS-RB
        :param mf_chrom: The RCGA string for tuning tunable MFs
        """
        if self.__controlSystem_created:
            self.__redefineAntecedentMFs(mf_chrom)
            self.__redefineConsequentTerms(rb_chrom)
        else:
            # step 1. create rule antecedents and consequent
            self.__createAntecedents(mf_chrom=mf_chrom)
            self.__createConsequent()

            # step 2. create rules
            self.__createFuzzyRules(rb_chrom=rb_chrom, depth=len(self.__antecedents))

            # step 3. create control system simulation
            self.__controlSystem = ctrl.ControlSystem(self.__rules)

            self.__controlSystemSimulation = ctrl.ControlSystemSimulation(control_system=self.__controlSystem,
                                                                          clip_to_bounds=False)
            self.__controlSystem_created = True

    def __createAntecedents(self, mf_chrom):
        pointer = 0
        try:
            for var in self.__descriptor.inputVariables.inputVar:
                var_config = self.__vars_config_dict[var.identity.type]
                universe = np.linspace(var_config.rangeMin, var_config.rangeMax)
                if var.identity.name is not None:
                    label = var.identity.name
                else:
                    label = var.identity.type
                antecedent = ctrl.Antecedent(universe, label)
                self.__antecedents.append(antecedent)
                for term in var_config.terms.term:
                    psize = gettuningparamsize(term.mf)
                    if var.tune:
                        t_params = mf_chrom[pointer: pointer + psize]
                        args = term.params + t_params
                        params = tunemf(term.mf, *args)
                        # print("original = {}, tuned = {}, t_params = {}".format(str(term.params), str(params),
                        #                                                         str(t_params)))
                        pointer += psize
                    else:
                        params = term.params
                    antecedent[term.name] = self.__createMF(term.mf, params=params, universe=antecedent.universe)
                    # antecedent.view()
        except IndexError:
            print("Error creating antecedents for {}".format(self.name))
            sys.exit(-1)
        else:
            print("All antecedents for {} GFS created successfully".format(self.name))

    def __createConsequent(self):
        var = self.__descriptor.outputVariable
        var_config = self.__vars_config_dict[var.type]
        self.__consequent = ctrl.Consequent(np.linspace(var_config.rangeMin, var_config.rangeMax),
                                            var_config.name)
        self.__consequent.defuzzify_method = self.__defuzz_method

        for term in var_config.terms.term:
            self.__consequent[term.name] = self.__createMF(term.mf, term.params, self.__consequent.universe)

    def __createMF(self, mf_type, params, universe):
        """
        Creates a membership function based on the given type.
        The triangular MF is considered as the default case

        Parameters
        --------------
        :param mf_type:
        :param params:
        :param universe:
        :return: a membership function
        """
        return {TRAPEZOID_MF: lambda *args: fuzz.trapmf(*args),
                GAUSSIAN_MF: lambda *args: fuzz.gaussmf(*args),
                SIGMOID_MF: lambda *args: fuzz.sigmf(*args)
                }.get(mf_type.lower(), lambda *args: fuzz.trimf(*args))(universe, params)

    def __createFuzzyRules(self, rb_chrom, depth, rule_terms_list=[]):
        """
        Uses recursion to form rules

        Parameters:
        -----------
        :param rb_chrom: The rule base string
        :param rule_terms_list: the terms to be used for rule formulation in a single pass in the network
        :param depth: The number of input variables yet to be visited
        """
        depth -= 1
        antecedent = self.__antecedents[::-1][depth]

        # base case check
        if depth == 0:
            for _, term in antecedent.terms.items():
                arg = term

                # for the antecedent parts of the rule
                for t in rule_terms_list:
                    arg = arg & t

                # form the rule with the joined antecedents
                rule = ctrl.Rule(arg, self.__consequent[self.__getOutputTerm(rb_chrom[len(self.__rules)])])
                # add the created rule to the list of rules
                self.__rules.append(rule)
        else:
            for _, term in antecedent.terms.items():
                rule_terms_list.append(term)
                self.__createFuzzyRules(rb_chrom=rb_chrom, rule_terms_list=rule_terms_list, depth=depth)
                rule_terms_list.pop()

    def __getOutputTerm(self, code):
        try:
            for term in self.__descriptor.outputVariable.term:
                if term.code == code:
                    return term.successOpTitle
            raise ex.OutputCodeError(
                "corresponding term for code {0} in {1} could not be mapped to an output variable term"
                    .format(code, self.name))
        except TypeError:
            raise ex.OutputCodeError("code {0} in {1} could not be mapped to an output variable term"
                                     .format(code, self.name))

    def __redefineConsequentTerms(self, rb_chrom):
        """
        This method steps through all created rules and set their consequent terms
        using the given rb_chrom.

        Parameters:
        -------------
        :param rb_chrom: RB string for the redefinition process
        """
        assert len(rb_chrom) == len(self.__rules)
        for i, rule in zip(rb_chrom, self.__rules):
            rule.consequent = self.__consequent[self.__getOutputTerm(code=i)]

    def __redefineAntecedentMFs(self, mf_chrom):
        """
        Uses the given MF tuning string to adjust the MF parameters of all
        created and tunable antecedent MFs.

        Parameters:
        -------------
        :param mf_chrom: MF tuning string
        """

        pointer = 0
        try:
            for antecedent, var in zip(self.__antecedents, self.__descriptor.inputVariables.inputVar):
                var_config = self.__vars_config_dict[var.identity.type]
                for term, term_config in zip(antecedent.terms, var_config.terms.term):
                    psize = gettuningparamsize(term_config.mf)
                    if var.tune:
                        t_params = mf_chrom[pointer: pointer + psize]
                        args = term_config.params + t_params
                        params = tunemf(term_config.mf, *args)
                        pointer += psize
                        term.mf = np.asarray(self.__createMF(term_config.mf, params=params,
                                                             universe=antecedent.universe))
        except IndexError:
            print("Error tuning antecedents for {}".format(self.name))
            sys.exit(-1)
        # else:
        #     print("All antecedents for {} GFS tuned successfully".format(self.name))

    def __str__(self):
        return "{0}\n\t{1}\n\t{2}".format(self.name, str(self.__antecedents), str(self.__consequent))