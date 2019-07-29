# project: fuzzprj
# Copyright (C) 9/6/18 - 5:19 PM
# Author: bbrighttaer


import deap.tools as tools
import fuzzrl.core.ga.schedule as sch
import fuzzrl.core.plot.analysis as ana
import gym
import matplotlib.pyplot as plt
import seaborn as sb
# import rlmarsenvs
from fuzzrl.core.conf import Defuzz as dfz
from fuzzrl.core.fuzzy.runner import *
from fuzzrl.core.io.randomprocess import OrnsteinUhlenbeckProcess
from fuzzrl.core.io.simdata import Document, Text, Line

from fuzzrl_projects.generic import *

sb.set()

SAVE_BEST = False
ep_calbk = True

# chart series
weighted_avg = ana.WeightedAvg(beta=0.9)
all_ind_series = ana.Series(name="Individuals Performance")
avg_series = ana.Series(name="Average (window = {})".format(round((1 / (1 - weighted_avg.beta)))))
gen_series = ana.Series(name="Generation Performance")
mut_prob_series = ana.Series(name="Mutation probability")


# callback functions
def create_episode_finished_callback(score_threshold, qlfd_ind_file):
    def episode_finished(ind, ind_i, total_eps, total_r):
        print("Episode: {}/{} | score: {}".format(ind_i, total_eps, total_r))

        # save qualified individual
        if SAVE_BEST and score_threshold is not None and qlfd_ind_file is not None and total_r > score_threshold:
            document = Document(name=qlfd_ind_file)
            document.addline(line=Line().add(text=Text(str(ind))))
            document.save(append=True)

        # store the performance of this individual in the corresponding series
        all_ind_series.addrecord(ind_i, total_r)
        weighted_avg.update(total_r)
        avg_series.addrecord(ind_i, weighted_avg.value)

    return episode_finished


def epoch_finished(epoch, pop, record):
    print("Epoch {} completed".format(epoch))
    print("Statistics for epoch {} = {}".format(epoch, record))


def sim_finished(ga, pop):
    # print logbook
    ga.logbook.header = "epoch", "avg", "std", "min", "max"
    print(ga.logbook)
    plot_charts()


# helper class
class Simulation(object):

    def __init__(self, env_id, lin_vars_file, gft_file, action_space_type, defuzz_method, obs_class,
                 qlfd_ind_file, score_threshold, rand_proc, tuning, reward_shaping_callback=None):
        self.env_id = env_id
        self.lin_vars_file = lin_vars_file
        self.gft_file = gft_file
        self.action_space_type = action_space_type
        self.defuzz_method = defuzz_method
        self.qlfd_ind_file = qlfd_ind_file
        self.score_threshold = score_threshold
        self.tuning = tuning
        self.rand_proc = rand_proc
        self.reward_shaping = reward_shaping_callback
        assert type(obs_class) == type
        self.obs_class = obs_class


def main(sim):
    # create a mutation probability schedule
    mut_sch = sch.ExponentialDecaySchedule(initial_prob=.1, decay_factor=1e-2)

    # cross over probability schedule
    cross_sch = sch.ConstantSchedule(0.8)

    pop_size = 50

    # Evolution operators information
    ev_conf = EvolutionConfig(sel_args={"k": pop_size, "tournsize": 5},
                              sel_func=tools.selTournament,
                              cross_args={"indpb": 0.4},
                              cross_func=tools.cxUniform,
                              mut_args={"mu": 0, "sigma": 0.1, "indpb": 0.1},
                              mut_func=tools.mutGaussian)

    # GA configuration
    ga_conf = GeneticAlgConfiguration(evol_config=ev_conf,
                                      pop_size=pop_size,
                                      num_gens=1000,
                                      mf_tuning_range=sim.tuning,
                                      lin_vars_file=sim.lin_vars_file,
                                      gft_file=sim.gft_file,
                                      load_init_pop_file=sim.qlfd_ind_file,
                                      apply_evolution=True,
                                      defuzz_method=sim.defuzz_method,
                                      mutation_prob_schdl=mut_sch,
                                      cross_prob_schdl=cross_sch,
                                      learn_rb_ops=False)

    print(sim.env_id)
    # Sim execution configuration
    sim_conf = SimExecutionConfiguration(env=gym.make(sim.env_id),
                                         agents=[Agent(0, sim.obs_class)],
                                         max_time_steps=500,
                                         episodes_per_ind=1,
                                         noise_process=sim.rand_proc,
                                         action_space=sim.action_space_type,
                                         persist_cache_per_ind=False,
                                         visualize_env=True)
    runner = Runner(ga_config=ga_conf,
                    sim_config=sim_conf,
                    seed=5,
                    episode_finished_callback=
                    create_episode_finished_callback(score_threshold=sim.score_threshold,
                                                     qlfd_ind_file=sim.qlfd_ind_file) if ep_calbk else None,
                    epoch_finished_callback=epoch_finished,
                    sim_finished_callback=sim_finished,
                    evolution_finished_callback=
                    lambda pop, m_prob, c_prob, epoch: mut_prob_series.addrecord(epoch, mut_sch.prob),
                    r_shaping_callback=sim.reward_shaping)

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


def mountain_car_reshape(state, reward, done):
    reward = state[0] + .5
    if state[0] >= 0.5:
        reward += 1

    if -0.6 < state[0] < -0.4:
        reward -= 1

    return reward


if __name__ == "__main__":
    sims = {
        # cart pole
        0: Simulation(env_id="CartPole-v1",
                      lin_vars_file="res/cartpole_linvars.xml",
                      gft_file="res/cartpole_gft.xml",
                      action_space_type=Const.DISCRETE,
                      defuzz_method=dfz.max_of_maximum,
                      obs_class=CartPoleObs,
                      qlfd_ind_file="data/cart_pole_qlfd.txt",
                      score_threshold=400,
                      rand_proc=None,
                      tuning=[-0.1, 0.1]),

        # carmunk
        # 1: Simulation(env_id=rlmarsenvs.carmunk_id,
        #               lin_vars_file="res/carmunk_linvars.xml",
        #               gft_file="res/carmunk_gft.xml",
        #               action_space_type=Const.DISCRETE,
        #               defuzz_method=dfz.max_of_maximum,
        #               obs_class=CarmunkObs,
        #               qlfd_ind_file="data/carmunk_qlfd.txt",
        #               score_threshold=5000,
        #               rand_proc= None,
        #               tuning=[-1.0, 1.0],
        #               reward_shaping_callback=None),
        # # pendulum
        2: Simulation(env_id="Pendulum-v0",
                      lin_vars_file="res/pendulum_linvars.xml",
                      gft_file="res/pendulum.xml",
                      action_space_type=Const.CONTINUOUS,
                      defuzz_method=dfz.centroid,
                      obs_class=PendulumObs,
                      qlfd_ind_file="data/pendulum_qlfd.txt",
                      score_threshold=-200,
                      rand_proc=OrnsteinUhlenbeckProcess(theta=0.1),
                      tuning=[-0.01, 0.01]),

        # mountain car continuous
        3: Simulation(env_id="MountainCarContinuous-v0",
                      lin_vars_file="res/mountain_car_linvars.xml",
                      gft_file="res/mountain_car.xml",
                      action_space_type=Const.CONTINUOUS,
                      defuzz_method=dfz.centroid,
                      obs_class=MountainCarObs,
                      qlfd_ind_file="data/mountain_car_cont_qlfd.txt",
                      score_threshold=90,
                      rand_proc=OrnsteinUhlenbeckProcess(theta=0.1),
                      tuning=[-0.01, 0.01],
                      reward_shaping_callback=None),

        # bipedal walker v2
        4: Simulation(env_id="BipedalWalker-v2",
                      lin_vars_file="res/bipedalwalker_linvars.xml",
                      gft_file="res/bipedalwalker.xml",
                      action_space_type=Const.CONTINUOUS,
                      defuzz_method=dfz.centroid,
                      obs_class=BipedalWalkerObs,
                      qlfd_ind_file="data/bipedalwalker_qlfd.txt",
                      score_threshold=300,
                      rand_proc=OrnsteinUhlenbeckProcess(theta=0.1),
                      tuning=[-0.01, 0.01],
                      reward_shaping_callback=None)}

    main(sims[3])
