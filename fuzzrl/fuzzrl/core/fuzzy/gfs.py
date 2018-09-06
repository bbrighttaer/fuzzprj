import sys

import fuzzrl.core.conf.exceptions as ex
import numpy as np
import skfuzzy as fuzz
import skfuzzy.control as ctrl
from fuzzrl.core.conf import Constants as const
from fuzzrl.core.fuzzy import GAUSSIAN_MF, SIGMOID_MF, TRAPEZOID_MF
from fuzzrl.core.fuzzy.tunemf import tunemf, gettuningparamsize

# customized version of scikit-fuzzy skfuzzext.py
from .skfuzzext import RuleGenerator


class GeneticFuzzySystem(object):
    """
    The structure of Genetic Fuzzy Systems in a GFT
    """

    def __init__(self, descriptor, vars_config_dict, defuzz_method):
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
        self.__undefined_code = -1
        self._initialize()

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

    def buildControlSystemSim(self, rb_chrom, mf_chrom, rb_op_chrom=None, out_mf_chrom=None):
        """
        Creates the control system for simulation if no control system has been created or
        reuse created properties by re-configuring them with the submitted rb_chrom and mf_chrom
        :param rb_chrom: The RCGA string for constructing the GFS-RB
        :param mf_chrom: The RCGA string for tuning tunable MFs
        :param rb_op_chrom: The RCGA string for setting rule operators (AND and OR)
        """
        # if self.__controlSystem_created:
        #     self.__redefineAntecedentMFs(mf_chrom)
        #     self.__redefineConsequentTerms(rb_chrom)
        #     if const.LEARN_RULE_OP and rb_op_chrom is not None:
        #         self.__redefineRuleOperators(rb_op_chrom)
        # else:

        self._initialize()

        # step 1. create rule antecedents and consequent
        self.__createAntecedents(mf_chrom=mf_chrom)
        self.__createConsequent(mf_chrom=out_mf_chrom)

        # step 2. create rules
        self.__createFuzzyRules(rb_chrom=rb_chrom, rb_op_chrom=rb_op_chrom, depth=len(self.__antecedents))

        # step 3.1 create control system simulation
        self.__controlSystem = ctrl.ControlSystem()

        # step 3.2 overwrite the default scikit-fuzzy rule generator to avoid recursion
        self.__controlSystem._rule_generator = RuleGenerator(self.__controlSystem)

        # step 3.3 add all rules to the control system
        for rule in self.__rules:
            self.__controlSystem.addrule(rule)

        # step 4
        self.__controlSystemSimulation = ctrl.ControlSystemSimulation(control_system=self.__controlSystem,
                                                                      clip_to_bounds=False)
        self.__controlSystem_created = True

    def _initialize(self):
        self.__rules = []
        self.__controlSystem = None
        self.__controlSystemSimulation = None
        self.__antecedents = []
        self.__consequent = None
        self.__controlSystem_created = False
        self.__rules_count = 0

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
        # else:
        #     print("All antecedents for {} GFS created successfully".format(self.name))

    def __createConsequent(self, mf_chrom):
        var = self.__descriptor.outputVariable
        var_config = self.__vars_config_dict[var.type]
        self.__consequent = ctrl.Consequent(np.linspace(var_config.rangeMin, var_config.rangeMax),
                                            var_config.name)
        self.__consequent.defuzzify_method = self.__defuzz_method

        pointer = 0
        for term in var_config.terms.term:
            # if the problem domain is continuous control tune the output membership functions
            if mf_chrom is not None:
                p_size = gettuningparamsize(term.mf)
                t_params = mf_chrom[pointer: pointer + p_size]
                args = term.params + t_params
                params = tunemf(term.mf, *args)
                pointer += p_size
            else:
                params = term.params
            self.__consequent[term.name] = self.__createMF(term.mf, params, self.__consequent.universe)

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
                GAUSSIAN_MF: lambda *args: fuzz.gaussmf(args[0], *args[1]),
                SIGMOID_MF: lambda *args: fuzz.sigmf(*args)
                }.get(mf_type.lower(), lambda *args: fuzz.trimf(*args))(universe, params)

    def __createFuzzyRules(self, rb_chrom, rb_op_chrom, depth, rule_terms_list=[]):
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

                rb_code = rb_chrom[self.__rules_count]
                if rb_code == self.__undefined_code:
                    self.__rules_count += 1
                    continue

                # for the antecedent parts of the rule
                for t in rule_terms_list:
                    if const.LEARN_RULE_OP:
                        # 0 - & (AND), 1 - | (OR)
                        if rb_op_chrom[self.__rules_count] == 1:
                            arg = arg | t
                        else:
                            arg = arg & t
                    else:  # default case
                        arg = arg & t

                # form the rule with the joined antecedents
                rule = ctrl.Rule(arg, self.__consequent[self.__getOutputTerm(rb_code)])
                # add the created rule to the list of rules
                self.__rules.append(rule)
                self.__rules_count += 1
        else:
            for _, term in antecedent.terms.items():
                rule_terms_list.append(term)
                self.__createFuzzyRules(rb_chrom=rb_chrom, rb_op_chrom=rb_op_chrom, rule_terms_list=rule_terms_list,
                                        depth=depth)
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
        assert len(rb_chrom) == self.__rules_count
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

    def reset(self):
        self.__controlSystemSimulation.reset()

    def __str__(self):
        return "{0}\n\t{1}\n\t{2}".format(self.name, str(self.__antecedents), str(self.__consequent))

    def __redefineRuleOperators(self, rb_op_chrom):
        """
        Re-configures the conjunction operators of the rule antecedents (The AND and OR)
        :param rb_op_chrom: The RCGA string for the reconfiguration
        """
        if len(rb_op_chrom) > 0:
            step_size = len(self.__descriptor.inputVariables.inputVar) - 1
            i = 0
            for rule in self.__rules:
                antecedent = rule.antecedent
                self.__setantecedentoperator(antecedent, depth=step_size, op_codes=rb_op_chrom[i:(i + step_size)])
                i += step_size

    def __setantecedentoperator(self, antecedent, depth, op_codes):
        """
        recursively sets the operator of two terms
        :return:
        """
        depth -= 1
        # 0 - & (AND), 1 - | (OR)
        if op_codes[depth] == 1:
            antecedent.kind = "or"
        else:
            antecedent.kind = "and"
        if depth > 0:
            self.__setantecedentoperator(antecedent.term1, depth, op_codes)
