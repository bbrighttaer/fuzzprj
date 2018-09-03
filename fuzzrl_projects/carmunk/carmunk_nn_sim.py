# project: fuzzprj
# Copyright (C) 6/25/18 - 6:54 PM
# Author: bbrighttaer

import numpy as np
import tensorflow as tf
import gym
import matplotlib.pyplot as plt
import keras.backend as K
import fuzzrl.core.ga.schedule as sch
import fuzzrl.core.plot.analysis as ana
import random

# registers the environment to use the gym interface
import rlmarsenvs

from fuzzrl.core.algorithm.alg import Algorithm
from fuzzrl.core.conf import Constants
from fuzzrl.core.conf.parser import *
from fuzzrl.core.io.memory import Cache, ReplayBuffer
from fuzzrl.core.io.simdata import Document, Text, Line
from matplotlib import style
from fuzzrl_projects.carmunk.carmunk_nn import neural_net, LossHistory
from fuzzrl.core.util.ops import boltzmanexp
from fuzzrl.core.util.ops import normalize

style.use("seaborn-paper")

# for reproducibility
np.random.seed(1)
random.seed(1)
tf.set_random_seed(1)

LIN_VARS_FILE = "carmunk_linvars.xml"
GFT_FILE = "carmunk_gft.xml"
model_path = "carmunk_model.h5"

MAX_NUM_EPISODES = 100
TIME_STEPS_BEFORE_TRAIN = 1000
epsilon = 1e-4

tau_sch = sch.ExponentialDecaySchedule(initial_prob=0.1, decay_factor=1e-1)


def main():
    # creates an environment
    env = gym.make("carmunk-v2")

    # print observation space ranges
    print("observation space ranges\nhigh = {}\nlow = {}\n".format(str(env.observation_space.high),
                                                                   str(env.observation_space.low)))
    # chart series
    weighted_avg = ana.WeightedAvg(beta=0.9)
    all_ind_series = ana.Series(name="Episode Performance")
    avg_series = ana.Series(name="Average (window = {})".format(round((1 / (1 - weighted_avg.beta)))))

    # create linguistic variables in a registry
    reg = xmlToLinvars(open(LIN_VARS_FILE).read())

    # create GFT with linguistic variables in the registry
    reg = xmlToGFT(open(GFT_FILE).read(), registry=reg)

    # Load pretrained NN model weights
    params = [32, 512, 512, 254, 64, 3]
    model = neural_net(num_inputs=3, params=params, lr=0.1, load=model_path, loss=neg_log_likelihood,
                       use_dropout=False)
    reg.nn_models_dict["CarMovement"] = model

    # create GFT algorithm object with the registry
    alg = Algorithm(registry=reg)

    # create a cache for managing simulation data
    cache = Cache(reg.nn_models_dict.keys())

    # create an object for retrieving input values
    obs_carmunk = CarmunkObs()

    # replay buffer
    replay_buffer = ReplayBuffer(max_size=1000)

    ts_elapsed = 0

    for i_episode in range(MAX_NUM_EPISODES):
        # get initial state
        state = env.reset()

        # initialize reward accumulator for the individual
        total_reward = 0

        # set the current state for retrieving specific inputs
        obs_carmunk.current_observation = state

        while True:
            # show the environment
            env.render()

            # since only one agent applies to this case study set a dummy agent ID
            agent_id = 0

            # get an action
            code, action, input_vec_dict, probs_dict = alg.executenntree(obs_carmunk, agent_id,
                                                                         action_selection_func=greedy_strategy,
                                                                         func_args=None)

            # apply the selected action to the environment and observe feedback
            next_state, reward, done, _ = env.step(code)

            # set the received observation as the current array for retrieving input values
            obs_carmunk.current_observation = next_state

            # mark the models that executed for the agent in this time step
            cache.mark(probs_dict_keys=probs_dict.keys())

            # decompose the received reward
            reward_dict = cache.decomposeReward(reward)

            # create experiences for the agent with respect to each GFSs that executed for the agent
            state_dict = {"CarMovement": np.array([obs_carmunk.getleftsensors(agent_id),
                                                   obs_carmunk.getmidsensors(agent_id),
                                                   obs_carmunk.getrightsensors(agent_id)])}
            exp_dict = cache.createExperiences(agent_id=agent_id, action_code=code, dec_reward_dict=reward_dict,
                                               input_vec_dict=input_vec_dict, probs_dict=probs_dict,
                                               next_state_dict=state_dict)

            # accumulate the rewards of all time steps
            total_reward += reward

            # add the experiences of an agent to their corresponding replay buffers
            for key, exp in exp_dict.items():
                if key == "CarMovement":
                    replay_buffer.add(exp)

            # increment time steps played
            ts_elapsed += 1

            if ts_elapsed >= TIME_STEPS_BEFORE_TRAIN:
                # print("train the model")
                pass

            # if the episode is over end the current episode
            if done:
                break

        print("Episode: {}/{} | score: {}".format(i_episode + 1, MAX_NUM_EPISODES, total_reward))

        avg_series.addrecord(i_episode, weighted_avg.update(total_reward))

    plt.figure(0)
    plt.title("Carmunk with NN")
    plt.plot(avg_series.data()['x'], avg_series.data()['y'])
    plt.xlabel("episode")
    plt.ylabel("score")
    plt.show()


class CarmunkObs(object):
    def __init__(self):
        self.current_observation = None

    def getleftsensors(self, agentId):
        assert self.current_observation is not None
        return normalize(self.current_observation[0], 0, 39, 0, 5)

    def getmidsensors(self, agentId):
        assert self.current_observation is not None
        return normalize(self.current_observation[1], 0, 39, 0, 5)

    def getrightsensors(self, agentId):
        assert self.current_observation is not None
        return normalize(self.current_observation[2], 0, 39, 0, 5)


def sigmoid(x):
    return 1 / (1 + np.exp(-x))


def neg_log_likelihood(y_true, y_pred):
    return -K.mean(y_true * K.log(y_pred), axis=-1)


def boltzmann_strategy(probs, episode):
    p = boltzmanexp(np.squeeze(probs), tau=tau_sch.get_prob(episode))
    choice = np.random.choice(np.squeeze(probs), p=p)
    out = np.where(probs == choice)[0][0]
    return out


def greedy_strategy(probs):
    return np.argmax(np.squeeze(probs))


def epsilon_greedy(probs):
    if random.random() < epsilon:
        return np.random.choice(np.squeeze(probs), p=probs)
    else:
        return np.argmax(np.squeeze(probs))


if __name__ == '__main__':
    main()
