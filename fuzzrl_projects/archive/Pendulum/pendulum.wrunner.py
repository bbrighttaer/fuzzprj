# project: fuzz_nn_rl
# Copyright (C) 6/11/18 - 1:48 PM
# Author: bbrighttaer

import deap.tools as tools
import fuzzrl.core.ga.schedule as sch
import fuzzrl.core.plot.analysis as ana
import gym
import matplotlib.pyplot as plt
import seaborn as sb
from fuzzrl.core.fuzzy.runner import *
from fuzzrl.core.io.randomprocess import OrnsteinUhlenbeckProcess
from fuzzrl.core.io.simdata import Document, Text, Line
from fuzzrl.core.conf import Defuzz as dfz

sb.set()

SAVE_BEST = True
SCORE_THRESHOLD = -200
QLFD_IND_FILE = "data/qualified.txt"

# chart series
weighted_avg = ana.WeightedAvg(beta=0.9)
all_ind_series = ana.Series(name="Individuals Performance")
avg_series = ana.Series(name="Average (window = {})".format(round((1 / (1 - weighted_avg.beta)))))
gen_series = ana.Series(name="Generation Performance")
mut_prob_series = ana.Series(name="Mutation probability")


def episode_finished(ind, ind_i, total_eps, total_r):
    print("Episode: {}/{} | score: {}".format(ind_i, total_eps, total_r))

    # save qualified individual
    if SAVE_BEST and total_r > SCORE_THRESHOLD:
        document = Document(name=QLFD_IND_FILE)
        document.addline(line=Line().add(text=Text(str(ind))))
        document.save(append=True)

    # store the performance of this individual in the corresponding series
    all_ind_series.addrecord(ind_i, total_r)
    weighted_avg.update(total_r)
    avg_series.addrecord(ind_i, weighted_avg.value)


def epoch_finished(epoch, pop, record):
    print("Epoch {} completed".format(epoch))
    print("Statistics for epoch {} = {}".format(epoch, record))


def sim_finished(ga, pop):
    # print logbook
    ga.logbook.header = "epoch", "avg", "std", "min", "max"
    print(ga.logbook)
    plot_charts()


def main():
    # creates an environment
    env = gym.make("Pendulum-v0")

    # create a mutation probability schedule
    mut_sch = sch.ExponentialDecaySchedule(initial_prob=.2, decay_factor=1e-2)

    # cross over probability schedule
    cross_sch = sch.ConstantSchedule(0.7)

    # random process for introducing noise
    rand_proc = OrnsteinUhlenbeckProcess(theta=0.01)

    # Evolution operators information
    ev_conf = EvolutionConfig(sel_args={"k": 30, "tournsize": 3},
                              sel_func=tools.selTournament,
                              cross_args={"indpb": 0.2},
                              cross_func=tools.cxUniform,
                              mut_args={"mu": 0, "sigma": 0.1, "indpb": 0.1},
                              mut_func=tools.mutGaussian)

    # GA configuration
    ga_conf = GeneticAlgConfiguration(evol_config=ev_conf,
                                      pop_size=30,
                                      num_gens=10,
                                      mf_tuning_range=[-0.1, 0.1],
                                      lin_vars_file="res/pendulum_linvars.xml",
                                      gft_file="res/pendulum.xml",
                                      load_init_pop_file=None,
                                      apply_evolution=True,
                                      defuzz_method=dfz.centroid,
                                      mutation_prob_schdl=mut_sch,
                                      cross_prob_schdl=cross_sch,
                                      learn_rb_ops=False)

    # Sim execution configuration
    sim_conf = SimExecutionConfiguration(env=env,
                                         agents=[Agent(0, PendulumObs)],
                                         max_time_steps=600,
                                         episodes_per_ind=1,
                                         noise_process=rand_proc,
                                         action_space=Const.CONTINUOUS,
                                         persist_cache_per_ind=False,
                                         visualize_env=True)
    runner = Runner(ga_config=ga_conf,
                    sim_config=sim_conf,
                    seed=5,
                    episode_finished_callback=episode_finished,
                    epoch_finished_callback=epoch_finished,
                    sim_finished_callback=sim_finished,
                    evolution_finished_callback=
                    lambda pop, m_prob, c_prob, epoch: mut_prob_series.addrecord(epoch, mut_sch.prob))

    runner.run()


def plot_charts():
    fig, (ax1, ax2) = plt.subplots(nrows=1, ncols=2, dpi=300)
    ax1.set_title(avg_series.name)
    ax1.set_xlabel("individual")
    ax1.set_ylabel("score")
    ax1.plot(avg_series.data()['x'], avg_series.data()['y'], linewidth=avg_series.linewidth, label=avg_series.name,
             color=avg_series.color,
             marker=avg_series.marker,
             linestyle=avg_series.linestyle)
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
    plt.tight_layout()
    plt.show()


class PendulumObs(object):
    def __init__(self):
        self.current_observation = None

    def getCosTheta(self, agentId):
        assert self.current_observation is not None
        return self.current_observation[0]

    def getSinTheta(self, agentId):
        assert self.current_observation is not None
        return self.current_observation[1]

    def getThetaDot(self, agentId):
        assert self.current_observation is not None
        return self.current_observation[2]


def sigmoid(x):
    return 1 / (1 + np.exp(-x))


if __name__ == "__main__":
    main()
