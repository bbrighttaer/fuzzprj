# project: fuzzrl
# Copyright (C) 6/12/18 - 9:03 PM
# Author: bbrighttaer


import random
from collections import OrderedDict

import numpy as np
from fuzzrl.core.io.simdata import *


class Experience:
    def __init__(self, agent_id, state, action_probs, action, reward, next_state=None):
        """
        Stores an experience of an agent in a single time step.
        In the case of the GFT execution, the next state may be None since it is not of any use.
        However, when an NN experience is being created the next state shall be specified.

        Parameters
        -----------
        :param agent_id: The ID of the agent
        :param state: The state or observation leading to this experience
        :param action_probs: The action probabilities computed by the reasoner or model
        :param action: The eventually selected action.
        :param reward: The reward received for performing the selected action
        :param next_state: The next state or observation received after performing the selected action
        """
        self.__agent_id = agent_id
        self.__state = state
        self.__action_outputs = action_probs
        self.__action = action
        self.__reward = reward
        self.__next_state = next_state
        self.__state_value = None

    @property
    def agent_id(self):
        return self.__agent_id

    @agent_id.setter
    def agent_id(self, agent_id):
        self.__agent_id = agent_id

    @property
    def state(self):
        return self.__state

    @state.setter
    def state(self, s):
        self.__state = s

    @property
    def action_outputs(self):
        return self.__action_outputs

    @action_outputs.setter
    def action_outputs(self, probs):
        self.__action_outputs = probs

    @property
    def action(self):
        return self.__action

    @action.setter
    def action(self, a):
        self.__action = a

    @property
    def reward(self):
        return self.__reward

    @reward.setter
    def reward(self, r):
        self.__reward = r

    @property
    def next_state(self):
        return self.__next_state

    @next_state.setter
    def next_state(self, s_prime):
        self.__next_state = s_prime

    @property
    def state_value(self):
        return self.__state_value

    @state_value.setter
    def state_value(self, value):
        self.__state_value = value


class Cache:
    """
    provides helper methods for performing operations on temporal data.
    """

    def __init__(self, node_names):
        """
        :param node_names:  The list of nodes in the tree which the cache focuses on.
        """
        self.__cache_init(node_names)
        self.__node_names = node_names
        self.__file_suffix = self.__get_date_suffix()

    def __cache_init(self, node_names):
        # Node/GFS execution count table.
        self.__count_dict = OrderedDict()
        # Node - TimestepTuple table. Stores the experiences due to a node in a time step
        # node
        # time step
        # 1
        # experiences
        self.__node_time_steps_dict = OrderedDict()
        # create all possible keys of both dictionaries or tables
        for name in node_names:
            self.__count_dict[name] = 0
            self.__node_time_steps_dict[name] = OrderedDict()

    def mark(self, output_dict_keys):
        """
        Marks that there has been a single execution of each node in the given list.
        This list is retrieved from the probs_dict that is returned after the execution of the GFT algorithm to
        indicate the probabilities of each executed GFS - hence the name probs_dict_keys.
        The tally of execution are used in the reward decomposition process.

        Parameters
        ------------
        :param output_dict_keys: The list containing tree nodes or names of GFSs whose execution counts are to be
        incremented
        """
        for name in output_dict_keys:
            self.__count_dict[name] += 1

    # def resetCount(self):
    #     """
    #     Sets all value of the count_dict to 0 value
    #     """
    #     for k, _ in self.__count_dict.items():
    #         self.__count_dict[k] = 0

    def createExperiences(self, agent_id, action, dec_reward_dict, input_vec_dict, output_dict,
                          next_state_dict=None):
        """
        Creates experiences for the given agent from GFT algorithm execution outputs.

        Parameters
        ------------
        :param next_state_dict: A dictionary containing the corresponding next states of each node in the tree

        :param agent_id: The ID of the agent

        :param action: The selected action (code) from the

        :param dec_reward_dict: A dictionary of decomposed rewards indicating the reward of each node in the tree
        with respect to the time step under consideration.

        :param input_vec_dict: A dictionary containing the corresponding input vectors of each node in the tree

        :param output_dict: A dictionary containing the output probabilities of each node in the tree

        :return: A dictionary of experiences corresponding to nodes in the tree for the given agent
        """
        exp_dict = OrderedDict()
        for key, input_vec, output_vec in zip(input_vec_dict.keys(), input_vec_dict.values(), output_dict.values()):
            exp = Experience(agent_id=agent_id, state=input_vec, action_probs=output_vec,
                             action=action, reward=dec_reward_dict.get(key, 0))
            if next_state_dict is not None:
                exp.next_state = next_state_dict.get(key, None)
            exp_dict[key] = exp
        return exp_dict

    def decomposeReward(self, reward):
        """
        Decomposes the given received reward based on the performance of each node in the tree as recorded by the
        execution counting dictionary.

        Parameters
        ------------
        :param reward: The received reward from the environment.
        :return: A dictionary indicating the corresponding rewards for all nodes in the tree for the time step under
        consideration.
        """
        # compute the total number of executions
        total_count = 0
        for _, v in self.__count_dict.items():
            total_count += v

        # decompose the reward for the nodes
        reward_dict = OrderedDict()
        for k, v in self.__count_dict.items():
            reward_dict[k] = (v / total_count) * reward
        return reward_dict

    def addExperiences(self, time_step, exp_dict):
        """
        Stores the experiences of an agent, corresponding to each GFS or node, in a time step

        Parameters
        -----------
        :param time_step: The time step that the experiences to be added belong to
        :param exp_dict: The experiences dictionary where the keys are the names of the nodes in the tree.
        """
        for key, exp in exp_dict.items():
            # get the corresponding node in the time steps records
            time_step_dict = self.__node_time_steps_dict[key]

            # try finding an existing list of experiences for the given time step so the new ones can be appended to it
            if time_step in time_step_dict:
                records = time_step_dict[time_step]
            else:
                # create a new experiences record for the given time step if no existing record was found
                records = []
                time_step_dict[time_step] = records
            records.append(exp)

    def compute_states_value(self, gamma=1.0):
        """
        Computes the state values of all experiences in the cache
        """
        for k, ts_dict in self.__node_time_steps_dict.items():
            agent_avg_dict = {}
            # reverse the time step keys to facilitate computation
            ts_keys_list = list(ts_dict.keys())
            for t in reversed(ts_keys_list):
                # Get the experiences of the current time step
                ts_exp_list = ts_dict.get(t)
                # for each experience calculate its state-value
                for exp in ts_exp_list:
                    # find the rewards tracking list of the agent with this experience
                    if exp.agent_id in agent_avg_dict:
                        avg_reward = agent_avg_dict.get(exp.agent_id)
                    else:
                        avg_reward = []
                        agent_avg_dict[exp.agent_id] = avg_reward

                    # Get the corresponding experience in the time step ahead if not terminal ts
                    next_ts_exp_list = ts_dict.get(t + 1, None)
                    if next_ts_exp_list is not None:
                        for next_exp in next_ts_exp_list:
                            if next_exp.agent_id == exp.agent_id:
                                avg_reward.append(next_exp.reward)
                                break
                        temp = avg_reward + [exp.reward]
                        temp = temp[::-1]
                        temp = [gamma ** k * r for k, r in enumerate(temp)]
                        exp.state_value = np.mean(temp)
                    else:  # terminal time step
                        exp.state_value = exp.reward

    def clear(self):
        self.__cache_init(self.__node_names)

    def save_csv(self, path='', clear_after_save=True):
        """
        Saves the contents of the cache into files at the given path (if permission to the path is allowed).

        Parameters
        ------------
        :param path: The location/directory of the files
        :param clear_after_save: If true the cache is re-initialized if the save operation succeeds
        """
        for node, time_step_dict in self.__node_time_steps_dict.items():
            # container for experiences for this node
            exp_lines = []

            # go through all time step data
            for _, data in time_step_dict.items():

                # create a CSV line for each experience in this time step
                for exp in data:

                    # creates a line from the I/O module and set a CSV delimiter
                    line = Line(delimiter=',')

                    # combine the data into a single list
                    if hasattr(exp.action_outputs, '__iter__'):
                        if type(exp.action_outputs == np.ndarray):
                            merged_list = exp.state + exp.action_outputs.tolist()
                        else:
                            merged_list = exp.state + exp.action_outputs
                    else:
                        merged_list = exp.state + [exp.action_outputs]
                    merged_list.append(exp.reward)
                    if exp.state_value is not None:
                        merged_list.append(exp.state_value)

                    # add the entries in the list to the line
                    for text in merged_list:
                        line.add(text)

                    # add the line to the lines list
                    exp_lines.append(line)

            # create a document with the lines
            file_name = node + '-' + self.__file_suffix + ".csv"
            document = Document(name=file_name, path=path, lines=exp_lines)

            # save the document in append mode
            document.save(append=True)

        # re-initialize the cache if specified
        if clear_after_save:
            # self.__cache_init(self.__node_names)
            self.clear()

    def __get_date_suffix(self):
        from fuzzrl.core.util.ops import getdatetime
        return getdatetime("yearmonthday")  # + '-' + getdatetime("hour") + '-' + getdatetime("minute")


class ReplayBuffer:
    """
    Implements an experience replay buffer
    """

    def __init__(self, max_size=300, label=''):
        self.__max_size = max_size
        self.__replay_buffer = []  # initializes buffer
        self.__label = label

    @property
    def label(self):
        return self.__label

    @label.setter
    def label(self, l):
        self.__label = l

    def add(self, exp):
        """
        Adds an experience to the replay buffer
        :param exp: the experience object of dtype: @link{Experience}
        :return:
        """
        if exp is not None:
            # if the buffer is full remove the oldest experience
            if len(self.__replay_buffer) > self.__max_size:
                self.__replay_buffer.pop(0)
            self.__replay_buffer.append(exp)

    def get_mini_batch(self, batch_size=128):
        """
        Gets a mini batch for training
        :param batch_size: The batch size
        :return:
        """
        return random.sample(self.__replay_buffer, batch_size)

    def clear_buffer(self):
        self.__replay_buffer.clear()

    def size(self):
        return len(self.__replay_buffer)
