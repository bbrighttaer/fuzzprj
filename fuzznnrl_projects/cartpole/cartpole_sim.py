# project: fuzz_nn_rl
# Copyright (C) 6/11/18 - 1:48 PM
# Author: bbrighttaer

import deap.tools as tools
import fuzznnrl.core.ga.schedule as sch
import fuzznnrl.core.plot.analysis as ana
import gym
import matplotlib.pyplot as plt
import numpy as np
from fuzznnrl.core.io.randomprocess import OrnsteinUhlenbeckProcess
from fuzznnrl.core.algorithm.alg import Algorithm
from fuzznnrl.core.conf import Constants
from fuzznnrl.core.conf.parser import *
from fuzznnrl.core.ga.genalg import GeneticAlgorithm
from fuzznnrl.core.ga.op import Operator
from fuzznnrl.core.io.memory import Cache
from fuzznnrl.core.io.simdata import Document, Text, Line
from matplotlib import style

style.use("seaborn-paper")

Constants.MF_TUNING_RANGE = [-0.1, 0.1]
Constants.LEARN_RULE_OP = False

NUM_OF_GENS = 20
NUM_EPISODES_PER_IND = 1
MAX_TIME_STEPS = 700
POP_SIZE = 100
LIN_VARS_FILE = "cartpole_linvars.xml"
GFT_FILE = "cartpole_gft.xml"
LOAD_INIT_POP = False
APPLY_EVO = True
QLFD_IND_FILE = "qualified.txt"
SAVE_BEST = True
SCORE_THRESHOLD = 300


def main():
    # creates an environment
    env = gym.make("CartPole-v1")

    # print observation space ranges
    print("observation space ranges\nhigh = {}\nlow = {}\n".format(str(env.observation_space.high),
                                                                   str(env.observation_space.low)))
    # chart series
    weighted_avg = ana.WeightedAvg(beta=0.9)
    all_ind_series = ana.Series(name="Individuals Performance")
    avg_series = ana.Series(name="Average (window = {})".format(round((1 / (1 - weighted_avg.beta)))))
    gen_series = ana.Series(name="Generation Performance")
    mut_prob_series = ana.Series(name="Mutation probability")

    # create linguistic variables in a registry
    reg = xmlToLinvars(open(LIN_VARS_FILE).read())

    # create GFT with linguistic variables in the registry
    reg = xmlToGFT(open(GFT_FILE).read(), registry=reg)

    # create GA instance with the registry object
    ga = GeneticAlgorithm(registry=reg, seed=2)

    # create a mutation probability schedule
    mut_sch = sch.ExponentialDecaySchedule(initial_prob=.2, decay_factor=1e-2)

    tau_sch = sch.ExponentialDecaySchedule(initial_prob=.5, decay_factor=1e-1)

    # create GFT algorithm object with the registry
    rand_proc = OrnsteinUhlenbeckProcess(theta=0.01)
    alg = Algorithm(registry=reg, random_process=rand_proc)

    # create a cache for managing simulation data
    cache = Cache(reg.gft_dict.keys())

    # get initial population
    if LOAD_INIT_POP:
        pop = ga.load_initial_population(QLFD_IND_FILE, POP_SIZE)
        pop = pop[::-1]
    else:
        pop = ga.generate_initial_population(POP_SIZE)

    # initialize epoch or generation counter
    epoch = 0

    # initialize individual counter
    ind_count = 0

    # create an object for retrieving input values
    obs_cartpole = CartPoleObs()

    # create agents list
    agents = [("agentLabel", 0)]

    # perform the simulation for a specified number of generations
    while epoch < NUM_OF_GENS:

        # Run the simulation with the current population
        for ind in pop:
            ind_count += 1

            # initialize reward accumulator for the individual
            total_reward = 0

            # configure the GFT with the current individual
            alg.configuregft(chromosome=ind)

            # control the environment with the configured GFT
            # for i_episode in range(NUM_EPISODES_PER_IND):

            # reset the environment
            observation = env.reset()

            # set the received observation as the current array for retrieving input values
            obs_cartpole.current_observation = observation

            # run through the time steps of the simulation
            for t in range(MAX_TIME_STEPS):

                # show the environment
                env.render()

                # since only one agent applies to this case study set a dummy agent ID
                agent_id = 0

                # get an action
                code, action, input_vec_dict, probs_dict = alg.executegft(obs_cartpole, agent_id)

                # mark the GFSs that executed for the agent in this time step
                cache.mark(probs_dict_keys=probs_dict.keys())

                # apply the selected action to the environment and observe feedback
                next_state, reward, done, _ = env.step(int(code))  # cartpole's step func expects an integer type code

                # decompose the received reward
                reward_dict = cache.decomposeReward(reward)

                # create experiences for the agent with respect to each GFSs that executed for the agent
                exp_dict = cache.createExperiences(agent_id=agent_id, action_code=code, dec_reward_dict=reward_dict,
                                                   input_vec_dict=input_vec_dict, probs_dict=probs_dict,
                                                   next_state_dict=None)

                # add the experiences of the agent to the cache
                cache.addExperiences(time_step=t, exp_dict=exp_dict)

                # set the received observation as the current array for retrieving input values
                obs_cartpole.current_observation = next_state

                # accumulate the rewards of all time steps
                total_reward += reward

                # if the episode is over end the current episode
                if done:
                    break

            # save contents of the cache and clear it for the next episode
            cache.compute_states_value(gamma=.9)
            cache.save_csv()

            # if total_reward < 50:
            #     total_reward = - 50
            # print("Episode finished after {} time steps".format(t + 1))
            print("Episode: {}/{} | score: {}".format(ind_count, (NUM_OF_GENS * POP_SIZE), total_reward))

            # set the return from the environment as the fitness value of the current individual
            ind.fitness.values = (total_reward,)

            # save qualified individual
            if SAVE_BEST and total_reward > SCORE_THRESHOLD:
                document = Document(name=QLFD_IND_FILE)
                document.addline(line=Line().add(text=Text(str(ind))))
                document.save(append=True)

            # store the performance of this individual in the corresponding series
            all_ind_series.addrecord(ind_count, total_reward)
            weighted_avg.update(total_reward)
            avg_series.addrecord(ind_count, weighted_avg.value)

        # Logging and other I/O operations
        print("Epoch {} completed".format(epoch))
        record = ga.stats.compile(pop)
        print("Statistics for epoch {} = {}".format(epoch, record))
        ga.logbook.record(epoch=epoch, **record)

        # store max return
        gen_series.addrecord(epoch, record["max"])
        if APPLY_EVO:
            # perform evolution
            offspring = applyEvolution(population=pop, ga_alg=ga, mut_sch=mut_sch, epoch=epoch)

            # set offspring as current population
            pop = offspring

        # update mutation probability series
        mut_prob_series.addrecord(epoch, mut_sch.prob)
        # increment epoch
        epoch += 1

    # print logbook
    ga.logbook.header = "epoch", "avg", "std", "min", "max"
    print(ga.logbook)

    # plotting
    plot_charts(avg_series, mut_prob_series)

    # terminates environment
    env.close()


def plot_charts(avg_series, mut_prob_series):
    fig, (ax1, ax2) = plt.subplots(nrows=1, ncols=2, dpi=300)
    # epochs = ga.logbook.select("epoch")
    # fit_avg = ga.logbook.select("avg")
    # fig0 = plt.figure(0)
    # plt.plot(epochs, fit_avg)
    # plt.xlabel("epoch")
    # plt.ylabel("avg")
    # plt.grid(True)
    # fig1 = plt.figure(1)
    ax1.set_title(avg_series.name)
    ax1.set_xlabel("individual")
    ax1.set_ylabel("score")
    ax1.plot(avg_series.data()['x'], avg_series.data()['y'], linewidth=avg_series.linewidth, label=avg_series.name,
             color=avg_series.color,
             marker=avg_series.marker,
             linestyle=avg_series.linestyle)
    # ax1.legend(fancybox=True, shadow=True, fontsize='small')  # loc="upper right"
    # plt.grid(True)
    # fig2 = plt.figure(2)
    ax2.set_title(mut_prob_series.name)
    ax2.set_xlabel("epoch")
    ax2.set_ylabel("probability")
    ax2.plot(mut_prob_series.data()['x'], mut_prob_series.data()['y'], linewidth=mut_prob_series.linewidth,
             label=mut_prob_series.name,
             color=mut_prob_series.color,
             marker=mut_prob_series.marker,
             linestyle=mut_prob_series.linestyle)
    # ax2.legend(fancybox=True, shadow=True, fontsize='small')  # loc="upper right"
    plt.grid(True)
    fig.suptitle("cartpole simulation")
    plt.subplots_adjust(left=0.2, wspace=0.8, top=0.8)
    plt.show()


def applyEvolution(population, ga_alg, mut_sch, epoch):
    """
    Helper function to apply one step of evolution to the submitted population

    Parameters
    ------------
    :param epoch: current epoch
    :param mut_sch: The mutation probability schedule in use
    :param population: The population for the current evolution task
    :param ga_alg: An instance of the GeneticAlgorithm class
    :return: Offspring of the evolution exercise
    """
    # create selection operator
    selargs = {"k": len(population),
               "tournsize": 3}
    selop = Operator(tools.selTournament, **selargs)

    # create crossover operator
    crossargs = {"indpb": 0.2}
    crossop = Operator(tools.cxUniform, **crossargs)

    # create mutation operator
    mutargs = {"mu": 0,
               "sigma": 0.1,
               "indpb": 0.1}
    mutop = Operator(tools.mutGaussian, **mutargs)

    # Perform one step of evolution
    prob = mut_sch.get_prob(epoch)
    # print("{} - {}".format(epoch, prob))
    offspring = ga_alg.evolve(population, selop=selop, crossop=crossop,
                              mutop=mutop, mut_prob=prob, cross_prob=0.7)
    return offspring


class CartPoleObs(object):
    def __init__(self):
        self.current_observation = None

    def getCartPosition(self, agentId):
        assert self.current_observation is not None
        return self.current_observation[0]

    def getCartVelocity(self, agentId):
        assert self.current_observation is not None
        # return  normalize(self.current_observation[1], -3.4028235e+38, 3.4028235e+38, -10, 10)
        return sigmoid(self.current_observation[1])

    def getPoleAngle(self, agentId):
        assert self.current_observation is not None
        return self.current_observation[2]

    def getPoleVelocity(self, agentId):
        assert self.current_observation is not None
        # return normalize(self.current_observation[3], 3.4028235e+38, 3.4028235e+38, -10, 10)
        return sigmoid(self.current_observation[3])


def sigmoid(x):
    return 1 / (1 + np.exp(-x))


if __name__ == "__main__":
    main()
