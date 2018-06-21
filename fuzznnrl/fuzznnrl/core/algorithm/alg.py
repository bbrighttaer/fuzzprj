# project: fuzznnrl
# Copyright (C) 6/6/18 - 9:03 AM
# Author: bbrighttaer
from collections import OrderedDict
from math import floor

import numpy as np
from fuzznnrl.core.conf import Constants
from fuzznnrl.core.util.ops import softmax, boltzmanexp
from skfuzzy import interp_membership


class Algorithm(object):
    """
    Implements the algorithms for executing a GFT or an NN tree.
    The configure algorithm is used in the case of fuzzy control where a chromosome has to be decomposed
    """

    def __init__(self, registry):
        """
        :param registry: The GFT registry
        """
        self.__reg = registry
        # get the name of the root GFS of the GFT
        self.__root_gfs = self.__reg.gft_config.rootInfSystem
        print("root =", self.__root_gfs)

    def configuregft(self, chromosome):
        """
        Builds the KB of the GFT in the registry using the given chromosome

        :param chromosome: The multi-part chromosome for KB construction.
        """
        num_gfs = len(self.__reg.gft_dict.items())
        for _, gfs in self.__reg.gft_dict.items():
            rb_segment = chromosome[gfs.descriptor.position]
            mf_segment = chromosome[gfs.descriptor.position + num_gfs]
            rb_op_segment = None
            if Constants.LEARN_RULE_OP:
                rb_op_segment = chromosome[gfs.descriptor.position + (2 * num_gfs)]
            gfs.buildControlSystemSim(rb_chrom=rb_segment, mf_chrom=mf_segment, rb_op_chrom=rb_op_segment)

    def executegft(self, obclassobj, agent_id, gfs_name=None, func_format_val=floor, input_vec_dict=OrderedDict(),
                   probs_dict=OrderedDict(), boltzmann=False, tau=1):
        """
        Executes the GFT algorithm to get the action for an agent
        -------
        :param input_vec_dict: keeps track of all input vectors to the GFSs executed in the tree
        :param func_format_val: A user-defined function for receiving the crisp value of the inference process and
        returning the code for determining the final output term. The must have only one argument. math.floor is the
        default function.

        :param gfs_name: The name of GFS to be executed

        :param obclassobj: The instance of the observation class which implements procedures for getting input values

        :param agent_id: The ID of the agent triggering the execution

        :param probs_dict: The output probabilities dictionary

        :return: The values returned are:
                - the code of the action to be taken
                - the action to be taken as found in the GFT configuration details
                - the output probabilities of all executed GFS in the GFT in a dictionary where the key is the name
                of the GFS and the value is a list containing the probabilities.
        """
        # select the gfs for execution
        if gfs_name is None:
            gfs_name = self.__root_gfs

        # stores the input values of the currently executing GFS
        input_vector = []

        gfs = self.__reg.gft_dict[gfs_name]
        if gfs is not None:
            # Clear previous data in memory
            gfs.reset()

            # try:
            for var in gfs.descriptor.inputVariables.inputVar:
                # get config details from registry
                var_config = self.__reg.linvar_dict[var.identity.type]
                # select procedure for input value
                func = getattr(obclassobj, var_config.procedure)
                # set input value of variable
                input_value = func(agent_id)
                gfs.controlSystemSimulation.input[var.identity.name] = input_value
                input_vector.append(input_value)

            # record the current input vector in the dictionary
            input_vec_dict[gfs_name] = input_vector

            # execute the control system
            gfs.controlSystemSimulation.compute()

            # get the crisp value from the control system
            out = gfs.controlSystemSimulation.output[gfs.consequent.label]
            out = func_format_val(out)

            # adds the action probabilities to the dictionary
            probs = self.__getActionProbs(gfs.consequent, gfs.controlSystemSimulation)
            probs_dict[gfs_name] = probs

            # check for boltzmann exploration
            if boltzmann:
                out = np.where(probs == np.random.choice(probs, p=boltzmanexp(probs, tau=tau)))[0][0]

            # search for the corresponding output term
            selected_term = None
            for term in gfs.descriptor.outputVariable.term:
                if term.code == out:
                    selected_term = term
                    break

            if selected_term is not None:
                # if the target is another FIS or GFS to be executed start a recursive call
                if selected_term.target.targetType == "fis":
                    return self.executegft(obclassobj, agent_id, selected_term.target.name, func_format_val,
                                           input_vec_dict,
                                           probs_dict)
                # if the target is an action report it
                else:
                    return out, selected_term.target.name, input_vec_dict, probs_dict
            else:
                print("Term with code {} could not be found in GFS: {}", out, gfs_name)
            # except:
            #     print("Error executing GFT. Stage:", gfs_name)
        else:
            print("{} could not be found".format(gfs_name))

    def executenntree(self, obclassobj, agent_id):
        """
        Executes the NN tree algorithm to get the action for an agent

        :param obclassobj: The instance of the observation class which implements procedures for getting input values

        :param agent_id: The ID of the agent triggering the execution

        :return: an action for the agent to take in the environment
        """
        pass

    def __getActionProbs(self, out_var, sim):
        """
        Gets the fuzzy values for all possible actions and transform them into probabilities
        as a softmax layer of an NN would

        :param out_var: The fuzzy output variable with computed value

        :return: action probabilities

        :rtype: ndarray
        """
        out = []
        for _, term in out_var.terms.items():
            val = interp_membership(out_var.universe, term.mf, sim.output[out_var.label])
            out.append(val)
        return softmax(x=out)