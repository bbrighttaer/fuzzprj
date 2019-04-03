# project: fuzzrl_pkg
# Copyright (C) 9/19/18 - 3:33 PM
# Author: bbrighttaer


import argparse
import pprint as pp

import logging as log
import gym
import numpy as np
import tensorflow as tf
import tflearn
import deap.tools as tools
from fuzzrl.core.algorithm.alg import Algorithm
from fuzzrl.core.conf import Constants as Const
from fuzzrl_projects.generic import *
from fuzzrl.core.io.randomprocess import OrnsteinUhlenbeckProcess
import fuzzrl.core.ga.schedule as sch
from gym import wrappers
from fuzzrl.core.fuzzy.runner import EvolutionConfig, GeneticAlgConfiguration, Agent
from fuzzrl_projects.generic.replay_buffer import ReplayBuffer

LOG_FORMAT = "%(asctime)s - %(levelname)s - %(message)s"
log.basicConfig(level=log.DEBUG, format=LOG_FORMAT)


class ActorNetwork(object):
    def __init__(self, sess, state_dim, action_dim, action_bound, learning_rate, tau, batch_size):
        self.sess = sess
        self.s_dim = state_dim
        self.a_dim = action_dim
        self.action_bound = action_bound
        self.learning_rate = learning_rate
        self.tau = tau
        self.batch_size = batch_size
        self.actor_net_label = "ddpg/actor_net"
        self.target_net_label = "ddpg/actor_target_net"

        # actor net
        self.inputs, self.out, self.scaled_out = self.create_actor_network(self.actor_net_label)
        self.actor_net_params = tf.get_collection(tf.GraphKeys.TRAINABLE_VARIABLES, scope=self.actor_net_label)

        # target net
        self.target_inputs, self.target_out, self.target_scaled_out = self.create_actor_network(self.target_net_label)
        self.target_net_params = tf.get_collection(tf.GraphKeys.TRAINABLE_VARIABLES, scope=self.target_net_label)

        # Operations for periodic update of target network parameters using actor net weights
        self.update_target_network_params = [self.target_net_params[i].assign(
            tf.multiply(self.actor_net_params[i], tau) + tf.multiply(self.target_net_params[i], 1.0 - self.tau)) for i
            in range(len(self.target_net_params))]

        # placeholder for action gradients from the critic net
        self.action_gradient = tf.placeholder(tf.float32, shape=[None, self.a_dim])

        # combine and normalize gradients
        self.unnormalized_actor_gradients = tf.gradients(self.scaled_out, self.actor_net_params, -self.action_gradient)
        self.actor_grads = list(map(lambda x: tf.div(x, self.batch_size), self.unnormalized_actor_gradients))

        # optimization operation
        self.optimize = tf.train.AdamOptimizer(self.learning_rate) \
            .apply_gradients(zip(self.actor_grads, self.actor_net_params))

        self.num_trainable_vars = len(self.actor_net_params) + len(self.target_net_params)

    def create_actor_network(self, label):
        with tf.variable_scope(label, reuse=False):
            inputs = tflearn.input_data(shape=[None, self.s_dim])
            # input layer
            net = tflearn.fully_connected(inputs, 400)
            net = tflearn.layers.normalization.batch_normalization(net)
            net = tflearn.activations.relu(net)

            # hidden layer
            net = tflearn.fully_connected(net, 300)
            net = tflearn.layers.normalization.batch_normalization(net)
            net = tflearn.activations.relu(net)

            # output layer
            w_init = tflearn.initializations.uniform(minval=-0.003, maxval=0.003)
            out = tflearn.fully_connected(net, self.a_dim, weights_init=w_init)
            out = tflearn.activations.tanh(out)

            # scale output to -action_bound to action_bound
            scaled_out = tf.multiply(out, self.action_bound)
        return inputs, out, scaled_out

    def train(self, inputs, a_gradient):
        self.sess.run(self.optimize, feed_dict={self.inputs: inputs, self.action_gradient: a_gradient})

    def predict(self, inputs):
        return self.sess.run(self.scaled_out, feed_dict={self.inputs: inputs})

    def predict_target(self, inputs):
        return self.sess.run(self.target_scaled_out, feed_dict={self.target_inputs: inputs})

    def update_target_network(self):
        self.sess.run(self.update_target_network_params)

    def get_num_trainable_vars(self):
        return self.num_trainable_vars


class CriticNetwork(object):
    def __init__(self, sess, state_dim, action_dim, learning_rate, tau, gamma):
        self.sess = sess
        self.s_dim = state_dim
        self.a_dim = action_dim
        self.tau = tau
        self.gamma = gamma
        self.learning_rate = learning_rate
        self.critic_net_label = "ddpg/critic_net"
        self.target_net_label = "ddpg/critic_target_net"

        # critic network
        self.observation, self.action, self.out = self.create_critic_network(self.critic_net_label)
        self.critic_net_params = tf.get_collection(tf.GraphKeys.TRAINABLE_VARIABLES, scope=self.critic_net_label)

        # target network
        self.target_observation, self.target_action, self.target_out = self.create_critic_network(self.target_net_label)
        self.target_net_params = tf.get_collection(tf.GraphKeys.TRAINABLE_VARIABLES, scope=self.target_net_label)

        # target network update operations
        self.update_target_net_params = [self.target_net_params[i].assign(
            tf.multiply(self.critic_net_params[i], self.tau) + tf.multiply(self.target_net_params[i], 1.0 - self.tau))
            for i in range(len(self.target_net_params))]

        # network target
        self.predicted_q_value = tf.placeholder(tf.float32, shape=[None, 1])

        # optimization op
        self.loss = tflearn.mean_square(self.predicted_q_value, self.out)
        self.optimize = tf.train.AdamOptimizer(self.learning_rate).minimize(self.loss)

        # get the gradients w.r.t the action
        self.action_grads = tf.gradients(self.out, self.action)

    def create_critic_network(self, label):
        with tf.variable_scope(label, reuse=False):
            observation = tflearn.input_data(shape=[None, self.s_dim])
            action = tflearn.input_data(shape=[None, self.a_dim])

            # input layer
            net = tflearn.fully_connected(observation, 400)
            net = tflearn.layers.normalization.batch_normalization(net)
            net = tflearn.activations.relu(net)

            # hidden layer: add the action input to the graph in this layer using temporal layers
            t1 = tflearn.fully_connected(net, 300)
            t2 = tflearn.fully_connected(action, 300)
            temp = tf.matmul(net, t1.W) + tf.matmul(action, t2.W) + t2.b
            net = tflearn.activations.relu(temp)

            # output layer (layer 2)
            # linear layer connected to 1 output representing Q(s,a)
            # weights are initialized to uniform [-3e-3, 3e-3]
            w_init = tflearn.initializations.uniform(minval=-0.003, maxval=0.003)
            out = tflearn.fully_connected(net, 1, weights_init=w_init)
        return observation, action, out

    def train(self, observation, action, predicted_q_value):
        return self.sess.run([self.out, self.loss, self.optimize],
                             feed_dict={self.observation: observation,
                                        self.action: action,
                                        self.predicted_q_value: predicted_q_value})

    def predict(self, observation, action):
        return self.sess.run(self.out, feed_dict={self.observation: observation,
                                                  self.action: action})

    def predict_target(self, observation, action):
        return self.sess.run(self.target_out, feed_dict={self.target_observation: observation,
                                                         self.target_action: action})

    def action_gradients(self, observation, action):
        return self.sess.run(self.action_grads, feed_dict={self.observation: observation,
                                                           self.action: action})

    def update_target_network(self):
        self.sess.run(self.update_target_net_params)


class FuzzyNet(object):
    def __init__(self, ga_config, seed=0, noise_process=None, evolution_finished_callback=None):
        self.noise = noise_process
        self.ga_config = ga_config
        self.evolution_finished_callback = evolution_finished_callback

        # GA ops initialization
        ga_config.init_ops(seed)
        self.reg = ga_config.registry
        self.ga = ga_config.ga
        self.epoch = 0
        self.record = None

        # create algorithm instance
        self.alg = Algorithm(registry=self.reg, random_process=self.noise)

        # get initial population
        if self.ga_config.load_init_pop_file is not None:
            self.pop = self.ga.load_initial_population(self.ga_config.load_init_pop_file, self.ga_config.pop_size)
            print("Num. of loaded individuals =", len(self.pop))
        else:
            self.pop = self.ga.generate_initial_population(self.ga_config.pop_size)

        # current individual index
        self.current_ind_idx = -1
        self.current_ind = None

    def predict(self, agent):
        # get an action
        out_vec, _, _, _ = self.alg.execute_fuzzy_net(agent.obs_accessor, agent_id=agent.id)
        return out_vec

    def evaluate(self, fit_vals):
        for ind, (val1, val2) in zip(self.pop, fit_vals):
            ind.fitness.values = (val1, val2)
        record = self.ga.stats.compile(self.pop)
        self.ga.logbook.record(epoch=self.epoch, **record)
        return record, self.epoch

    def next(self):
        self.current_ind_idx += 1
        self.current_ind = self.pop[self.current_ind_idx]
        if self.current_ind is not None:
            self.alg.configuregft(self.current_ind)

    def evolve(self):
        # GA stats by DEAP
        record = self.ga.stats.compile(self.pop)
        self.ga.logbook.record(epoch=self.epoch, **record)

        # perform evolution
        if self.ga_config.apply_evolution:
            m_prob = self.ga_config.mutation_prob_schdl.get_prob(self.epoch)
            c_prob = self.ga_config.cross_prob_schdl.get_prob(self.epoch)
            ev = self.ga_config.evol_config
            self.pop = self.ga.evolve(self.pop, selop=ev.selection_op, crossop=ev.crossover_op, mutop=ev.mutation_op,
                                      mut_prob=m_prob, cross_prob=c_prob)
            if self.evolution_finished_callback is not None and callable(self.evolution_finished_callback):
                self.evolution_finished_callback(self.pop, m_prob, c_prob, self.epoch)
            self.epoch += 1
            self.current_ind_idx = -1

    def train(self):
        pass


# Taken from https://github.com/openai/baselines/blob/master/baselines/ddpg/noise.py, which is
# based on http://math.stackexchange.com/questions/1287634/implementing-ornstein-uhlenbeck-in-matlab
class OrnsteinUhlenbeckActionNoise:
    def __init__(self, mu, sigma=0.3, theta=.15, dt=1e-2, x0=None):
        self.theta = theta
        self.mu = mu
        self.sigma = sigma
        self.dt = dt
        self.x0 = x0
        self.reset()

    def __call__(self):
        x = self.x_prev + self.theta * (self.mu - self.x_prev) * self.dt + \
            self.sigma * np.sqrt(self.dt) * np.random.normal(size=self.mu.shape)
        self.x_prev = x
        return x

    def reset(self):
        self.x_prev = self.x0 if self.x0 is not None else np.zeros_like(self.mu)

    def __repr__(self):
        return 'OrnsteinUhlenbeckActionNoise(mu={}, sigma={})'.format(self.mu, self.sigma)


# helper class
class Simulation(object):

    def __init__(self, env_id, lin_vars_file, gft_file, action_space_type, obs_class,
                 qlfd_ind_file, score_threshold, rand_proc, tuning, pop_size, reward_shaping_callback=None):
        self.env_id = env_id
        self.lin_vars_file = lin_vars_file
        self.gft_file = gft_file
        self.action_space_type = action_space_type
        self.qlfd_ind_file = qlfd_ind_file
        self.score_threshold = score_threshold
        self.tuning = tuning
        self.rand_proc = rand_proc
        self.reward_shaping = reward_shaping_callback
        self.pop_size = pop_size
        assert type(obs_class) == type
        self.obs_class = obs_class


def print_stats(record, epoch):
    print("Epoch {} completed".format(epoch))
    print("Statistics for epoch {} = {}".format(epoch, record))


def get_ga_config(sim):
    # create a mutation probability schedule
    mut_sch = sch.ExponentialDecaySchedule(initial_prob=.2, decay_factor=1e-2)

    # cross over probability schedule
    cross_sch = sch.ConstantSchedule(0.8)

    # Evolution operators information
    ev_conf = EvolutionConfig(sel_args={"k": sim.pop_size, "tournsize": 3},
                              sel_func=tools.selTournament,
                              cross_args={"indpb": 0.1},
                              cross_func=tools.cxUniform,
                              mut_args={"mu": 0, "sigma": 0.1, "indpb": 0.1},
                              mut_func=tools.mutGaussian)

    # GA configuration
    ga_conf = GeneticAlgConfiguration(evol_config=ev_conf,
                                      pop_size=sim.pop_size,
                                      num_gens=10,
                                      mf_tuning_range=sim.tuning,
                                      lin_vars_file=sim.lin_vars_file,
                                      gft_file=sim.gft_file,
                                      load_init_pop_file=None,  # sim.qlfd_ind_file,
                                      apply_evolution=True,
                                      mutation_prob_schdl=mut_sch,
                                      cross_prob_schdl=cross_sch,
                                      learn_rb_ops=False)
    return ga_conf


# ===========================
#   Tensorflow Summary Ops
# ===========================

def build_summaries():
    episode_reward = tf.Variable(0.)
    tf.summary.scalar("Reward", episode_reward)
    episode_ave_max_q = tf.Variable(0.)
    tf.summary.scalar("Qmax_Value", episode_ave_max_q)

    summary_vars = [episode_reward, episode_ave_max_q]
    summary_ops = tf.summary.merge_all()

    return summary_ops, summary_vars


# ===========================
#   Agent Training
# ===========================

def objective(sess, env, args, actor, critic, actor_noise, sim, fuzzynet, replay_buffer, summary_ops, summary_vars):
    activate_fuzzynet = True
    agent = Agent(0, sim.obs_class)

    sess.run(tf.global_variables_initializer())
    # writer = tf.summary.FileWriter(args['summary_dir'], sess.graph)

    # Initialize target network weights
    actor.update_target_network()
    critic.update_target_network()

    # Needed to enable BatchNorm.
    # This hurts the performance on Pendulum but could be useful
    # in other environments.
    tflearn.is_training(True)

    scores, losses = [], []

    for i in range(int(args['max_episodes'])):

        s = env.reset()

        ep_reward = 0
        ep_ave_max_q = 0

        for j in range(int(args['max_episode_len'])):

            if args['render_env']:
                env.render()

            # Added exploration noise
            # a = actor.predict(np.reshape(s, (1, 3))) + (1. / (1. + i))
            agent.obs_accessor.current_observation = s
            if activate_fuzzynet:
                s = fuzzynet.predict(agent)
            a = actor.predict(np.reshape(s, (1, actor.s_dim))) + actor_noise()

            s2, r, terminal, info = env.step(a[0])

            agent.obs_accessor.current_observation = s2
            if activate_fuzzynet:
                s2 = fuzzynet.predict(agent)

            replay_buffer.add(np.reshape(s, (actor.s_dim,)), np.reshape(a, (actor.a_dim,)), r,
                              terminal, np.reshape(s2, (actor.s_dim,)))

            # Keep adding experience to the memory until
            # there are at least minibatch size samples
            if replay_buffer.size() > int(args['minibatch_size']):
                s_batch, a_batch, r_batch, t_batch, s2_batch = \
                    replay_buffer.sample_batch(int(args['minibatch_size']))

                # Calculate targets
                target_q = critic.predict_target(s2_batch, actor.predict_target(s2_batch))

                y_i = []
                for k in range(int(args['minibatch_size'])):
                    if t_batch[k]:
                        y_i.append(r_batch[k])
                    else:
                        y_i.append(r_batch[k] + critic.gamma * target_q[k])

                # actor score
                state_vals = critic.predict_target(s_batch, actor.predict_target(s_batch))
                score = np.mean(state_vals)
                scores.append(score)

                # Update the critic given the targets
                predicted_q_value, loss, _ = critic.train(s_batch, a_batch,
                                                          np.reshape(y_i, (int(args['minibatch_size']), 1)))
                losses.append(loss)

                ep_ave_max_q += np.amax(predicted_q_value)

                # Update the actor policy using the sampled gradient
                a_outs = actor.predict(s_batch)
                grads = critic.action_gradients(s_batch, a_outs)
                actor.train(s_batch, grads[0])

                # Update target networks
                actor.update_target_network()
                critic.update_target_network()

            s = s2
            ep_reward += r

            if terminal:
                summary_str = sess.run(summary_ops, feed_dict={
                    summary_vars[0]: ep_reward,
                    summary_vars[1]: ep_ave_max_q / float(j)
                })

                # writer.add_summary(summary_str, i)
                # writer.flush()

                print('| Reward: {:d} | Episode: {:d} | Qmax: {:.4f}'.format(int(ep_reward), i,
                                                                             (ep_ave_max_q / float(j))))
                break
    return np.mean(scores), np.mean(losses)


def main(args, sim):
    with tf.Session() as sess:

        env = gym.make(args['env'])
        np.random.seed(int(args['random_seed']))
        tf.set_random_seed(int(args['random_seed']))
        env.seed(int(args['random_seed']))

        state_dim = env.observation_space.shape[0]
        action_dim = env.action_space.shape[0]
        action_bound = env.action_space.high
        # Ensure action bound is symmetric
        assert (env.action_space.high == -env.action_space.low)

        ga_config = get_ga_config(sim)
        ga_config.fitness_weight = (1.0, -1.0)
        fuzzynet = FuzzyNet(ga_config, seed=args['random_seed'])

        actor = ActorNetwork(sess, state_dim, action_dim, action_bound,
                             float(args['actor_lr']), float(args['tau']),
                             int(args['minibatch_size']))

        critic = CriticNetwork(sess, state_dim, action_dim,
                               float(args['critic_lr']), float(args['tau']),
                               float(args['gamma']))

        actor_noise = OrnsteinUhlenbeckActionNoise(mu=np.zeros(action_dim))

        if args['use_gym_monitor']:
            if not args['render_env']:
                env = wrappers.Monitor(
                    env, args['monitor_dir'], video_callable=False, force=True)
            else:
                env = wrappers.Monitor(env, args['monitor_dir'], force=True)

        # Initialize replay memory
        replay_buffer = ReplayBuffer(int(args['buffer_size']), int(args['random_seed']))

        # Set up summary Ops
        summary_ops, summary_vars = build_summaries()

        for i in range(10):
            fitness = []
            for j in range(sim.pop_size):
                fuzzynet.next()
                score, loss = objective(sess, env, args, actor, critic, actor_noise, sim, fuzzynet,
                                        replay_buffer, summary_ops, summary_vars)
                fitness.append((abs(score), abs(loss)))
                print("individual {ind} - gen {g}; score = {s}, loss = {loss}".format(ind=j, g=i, s=score, loss=loss))
            record, epoch = fuzzynet.evaluate(fitness)
            print_stats(record, epoch)
            fuzzynet.evolve()

        if args['use_gym_monitor']:
            env.monitor.close()


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='provide arguments for DDPG agent')

    # agent parameters
    parser.add_argument('--actor-lr', help='actor network learning rate', default=0.0001)
    parser.add_argument('--critic-lr', help='critic network learning rate', default=0.001)
    parser.add_argument('--gamma', help='discount factor for critic updates', default=0.99)
    parser.add_argument('--tau', help='soft target update parameter', default=0.001)
    parser.add_argument('--buffer-size', help='max size of the replay buffer', default=1000000)
    parser.add_argument('--minibatch-size', help='size of minibatch for minibatch-SGD', default=64)

    # run parameters
    parser.add_argument('--env', help='choose the gym env- tested on {Pendulum-v0}', default='Pendulum-v0')
    parser.add_argument('--random-seed', help='random seed for repeatability', default=1234)
    parser.add_argument('--max-episodes', help='max num of episodes to do while training', default=20)
    parser.add_argument('--max-episode-len', help='max length of 1 episode', default=200)
    parser.add_argument('--render-env', help='render the gym env', action='store_true')
    parser.add_argument('--use-gym-monitor', help='record gym results', action='store_true')
    parser.add_argument('--monitor-dir', help='directory for storing gym results', default='./results/gym_ddpg')
    parser.add_argument('--summary-dir', help='directory for storing tensorboard info', default='./results/tf_ddpg')

    parser.set_defaults(render_env=False)
    parser.set_defaults(use_gym_monitor=False)

    args = vars(parser.parse_args())

    pp.pprint(args)

    sims = {
        # pendulum
        1: Simulation(env_id="Pendulum-v0",
                      lin_vars_file="res/pendulum_linvars.xml",
                      gft_file="res/fuzzynet_pendulum2.xml",
                      action_space_type=Const.CONTINUOUS,
                      obs_class=PendulumObs,
                      qlfd_ind_file="data/pendulum_qlfd.txt",
                      score_threshold=-200,
                      rand_proc=OrnsteinUhlenbeckProcess(theta=0.1),
                      pop_size=20,
                      tuning=[-0.1, 0.1]),

        # mountain car continuous
        2: Simulation(env_id="MountainCarContinuous-v0",
                      lin_vars_file="res/mountain_car_linvars.xml",
                      gft_file="res/mountain_car.xml",
                      action_space_type=Const.CONTINUOUS,
                      obs_class=MountainCarObs,
                      qlfd_ind_file="data/mountain_car_cont_qlfd.txt",
                      score_threshold=90,
                      rand_proc=OrnsteinUhlenbeckProcess(theta=0.1),
                      tuning=[-0.01, 0.01],
                      pop_size=20,
                      reward_shaping_callback=None),

        # bipedal walker v2
        3: Simulation(env_id="BipedalWalker-v2",
                      lin_vars_file="res/bipedalwalker_linvars.xml",
                      gft_file="res/bipedalwalker.xml",
                      action_space_type=Const.CONTINUOUS,
                      obs_class=BipedalWalkerObs,
                      qlfd_ind_file="data/bipedalwalker_qlfd.txt",
                      score_threshold=300,
                      rand_proc=OrnsteinUhlenbeckProcess(theta=0.1),
                      tuning=[-0.01, 0.01],
                      pop_size=20,
                      reward_shaping_callback=None)}

    main(args, sims[1])
