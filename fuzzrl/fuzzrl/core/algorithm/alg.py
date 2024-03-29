# project: fuzzrl
# Copyright (C) 6/6/18 - 9:03 AM
# Author: bbrighttaer
from collections import OrderedDict

import numpy as np
from fuzzrl.core.conf import Constants as const
from fuzzrl.core.util.ops import softmax
from skfuzzy import interp_membership


class Algorithm(object):
    """
    Implements the algorithms for executing a GFT or an NN tree.
    The configure algorithm is used in the case of fuzzy control where a chromosome has to be decomposed
    """

    def __init__(self, registry, random_process=None):
        """
        :param registry: The GFT registry
        """
        self.__random_process = random_process
        self.__reg = registry
        # get the name of the root GFS of the GFT
        self.__root = self.__reg.gft_config.rootInfSystem
        print("root =", self.__root)

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
            out_mf_seg = None

            seg_skip = 1
            # check for rule operator learning
            if const.LEARN_RULE_OP:
                seg_skip += 1
                rb_op_segment = chromosome[gfs.descriptor.position + (seg_skip * num_gfs)]

            # check for output variable membership functions tuning (thus, continuous action space activated)
            if const.ACTION_SPACE == const.CONTINUOUS:
                seg_skip += 1
                out_mf_seg = chromosome[gfs.descriptor.position + (seg_skip * num_gfs)]

            gfs.buildControlSystemSim(rb_chrom=rb_segment, mf_chrom=mf_segment,
                                      rb_op_chrom=rb_op_segment, out_mf_chrom=out_mf_seg)

    def executegft(self, obclassobj, agent_id, gfs_name=None, formatting_func=round):
        return self._executegft(obclassobj, agent_id, gfs_name, formatting_func, OrderedDict(), OrderedDict())

    def _executegft(self, obclassobj, agent_id, gfs_name, formatting_func, input_vec_dict, probs_dict):
        """
        Executes the GFT algorithm to get the action for an agent
        -------
        :param input_vec_dict: keeps track of all input vectors to the GFSs executed in the tree
        :param formatting_func: A user-defined function for receiving the crisp value of the inference process and
        returning the code for determining the final output term. The function must have only one required parameter.

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
            gfs_name = self.__root

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
                if self.__random_process is not None:
                    input_value += self.__random_process.sample()[0]
                input_vector.append(input_value)

            # record the current input vector in the dictionary
            input_vec_dict[gfs_name] = input_vector

            # execute the control system
            gfs.controlSystemSimulation.compute()

            # get the crisp value from the control system
            out = gfs.controlSystemSimulation.output[gfs.consequent.label]
            if formatting_func is not None:
                out = formatting_func(out)

            # adds the action probabilities to the dictionary
            probs = self.__get_action_probs(gfs.consequent, gfs.controlSystemSimulation)
            probs_dict[gfs_name] = probs

            # search for the corresponding output term
            selected_term = None
            for term in gfs.descriptor.outputVariable.term:
                if term.code == out:
                    selected_term = term
                    break

            if selected_term is not None:
                # if the target is another FIS or GFS to be executed start a recursive call
                if selected_term.target.targetType == "fis":
                    return self._executegft(obclassobj, agent_id, selected_term.target.name, formatting_func,
                                            input_vec_dict,
                                            probs_dict)
                # if the target is an action report it
                else:
                    return out, selected_term.target.name, input_vec_dict, probs_dict
            else:
                print("Term with code {} could not be found in GFS: {}", out, gfs_name)
        else:
            print("{} could not be found".format(gfs_name))

    def executenntree(self, obclassobj, agent_id, action_selection_func, func_args=None, nn_name=None,
                      input_vec_dict=OrderedDict(),
                      probs_dict=OrderedDict()):
        """
        Executes the NN tree algorithm to get the action for an agent

        Parameters:
        -----------

        :param func_args: Function arguments that are passed to the action selection function with the action probabilities
        :param obclassobj: The instance of the observation class which implements procedures for getting input values

        :param agent_id: The ID of the agent whose action is being computed

        :param action_selection_func: A callback function that implements an exploration-exploitation strategy.
        The predictions of the NN model are passed as a numpy array argument to the function. This action selection
        function shall return the code (integer) of the action to be taken.

        :param nn_name: The name of the NN model to be executed. Default is None to indicate execution starts from root

        :param input_vec_dict: A dictionary containing the inputs to each NN model in a single pass through the tree

        :param probs_dict: A dictionary containing the predicted probabilities of each node in a single pass through
        the tree

        :return:  output code, action name, input_vec_dict, probs_dict
        """
        # select the nn_model for execution
        if nn_name is None:
            nn_name = self.__root

        # stores the input values of the currently executing GFS
        input_vector = []

        nn_model = self.__reg.nn_models_dict[nn_name]
        gfs = self.__reg.gft_dict[nn_name]
        if gfs is not None:
            # try:
            num_inputs = 0
            for var in gfs.descriptor.inputVariables.inputVar:
                # get config details from registry
                var_config = self.__reg.linvar_dict[var.identity.type]
                # select procedure for input value
                func = getattr(obclassobj, var_config.procedure)
                # set input value of variable
                input_value = func(agent_id)
                input_vector.append(input_value)
                num_inputs += 1

            # record the current input vector in the dictionary
            input_vec_dict[nn_name] = input_vector

            # predict the action to be taken using the NN model
            if hasattr(nn_model, "predict"):
                input_vector = np.array(input_vector).reshape((1, num_inputs))
                predictions = nn_model.predict(input_vector)

                # Use an action selection strategy to select the output code of the action to be taken
                if func_args is not None and hasattr(func_args, "__iter__"):
                    out = action_selection_func(predictions, *func_args)
                else:
                    out = action_selection_func(predictions)

                # adds the predictions to the dictionary
                probs_dict[nn_name] = predictions

                selected_term = None
                for term in gfs.descriptor.outputVariable.term:
                    if term.code == out:
                        selected_term = term
                        break

                if selected_term is not None:
                    # if the target is another NN model to be executed start a recursive call
                    if selected_term.target.targetType == "fis":
                        return self._executegft(obclassobj, agent_id, action_selection_func,
                                                selected_term.target.name,
                                                input_vec_dict,
                                                probs_dict)
                    # if the target is an action report it
                    else:
                        return out, selected_term.target.name, input_vec_dict, probs_dict
                else:
                    print("Term with code {} could not be found in NN: {}", out, nn_name)
        else:
            print("{} could not be found".format(nn_name))

    @staticmethod
    def __get_action_probs(out_var, sim):
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

    def executebfc(self, obclassobj, agent_id, add_noise=True):
        """
        Executes a Bidirectional Fuzzy Chain (BFC) for continuous action(s)
        :param add_noise:
        :param obclassobj:
        :param agent_id:
        :param gfs_name:
        :param input_vec_dict:
        :param actions_dict:
        :return:
        """
        # stores the inputs of each node
        input_vec_dict = OrderedDict()

        # stores the selected actions using the names of the respective GFSs as keys
        actions_dict = OrderedDict()

        # stores the input values of the currently executing GFS
        input_vector = []

        # sort GFSs according to position
        gfs_list = sorted(self.__reg.gft_dict.values(), key=lambda x: x.descriptor.position)

        # dict for storing forward and backward pass outputs
        interm_actions_dict = {k.name: () for k in gfs_list}

        # Forward pass
        next_cell_value = 0

        inner_state_required = True if len(gfs_list) > 1 else False

        for gfs in gfs_list:
            # clear previous data
            gfs.reset()

            # set input values
            for var in gfs.descriptor.inputVariables.inputVar:
                if var.identity.type == const.INNER_STATE_VAR:
                    continue
                # get config details from registry
                var_config = self.__reg.linvar_dict[var.identity.type]
                # select procedure for input value
                func = getattr(obclassobj, var_config.procedure)
                # set input value of variable
                input_value = func(agent_id)
                gfs.controlSystemSimulation.input[var.identity.name] = input_value
                # if self.__random_process is not None:
                #     input_value += self.__random_process.sample()[0]
                input_vector.append(input_value)

            if inner_state_required:
                # set internal state variable
                gfs.controlSystemSimulation.input[const.INNER_STATE_VAR] = next_cell_value
                input_vector.append(next_cell_value)

            # record the current input vector in the dictionary
            input_vec_dict[gfs.name] = input_vector

            # execute the control system
            gfs.controlSystemSimulation.compute()

            # get the crisp value from the control system
            out = gfs.controlSystemSimulation.output[gfs.consequent.label]

            # store forward pass output as an intermediate value
            interm_actions_dict[gfs.name] = interm_actions_dict[gfs.name] + (out,)

            # update next cell's value
            next_cell_value = out

        # Backward pass
        next_cell_value = 0
        for gfs in reversed(gfs_list):
            if inner_state_required:
                # set internal variable
                gfs.controlSystemSimulation.input[const.INNER_STATE_VAR] = next_cell_value

                # append current internal variable value to the input values list of the GFS
                input_vec_dict[gfs.name] = input_vec_dict[gfs.name] + [next_cell_value]

            # execute the control system
            gfs.controlSystemSimulation.compute()

            # get the crisp value from the control system
            out = gfs.controlSystemSimulation.output[gfs.consequent.label]

            # store forward pass output as an intermediate value
            interm_actions_dict[gfs.name] = interm_actions_dict[gfs.name] + (out,)

            # update next cell's value
            next_cell_value = out

        # Action selection
        for k, v in interm_actions_dict.items():
            # v contains (o_forward, o_backward)
            a = np.mean(v)
            if self.__random_process is not None and add_noise:
                a += self.__random_process.sample()[0]
            actions_dict[k] = a

        return actions_dict, input_vec_dict
