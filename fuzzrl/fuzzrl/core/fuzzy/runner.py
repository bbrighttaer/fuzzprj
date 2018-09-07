#
# Project: fuzzrl
# Created by bbrighttaer on 9/5/18
#

import logging as log

import numpy as np
from fuzzrl.core.algorithm.alg import Algorithm
from fuzzrl.core.conf import Constants as Const
from fuzzrl.core.conf.parser import *
from fuzzrl.core.ga.genalg import GeneticAlgorithm
from fuzzrl.core.ga.op import Operator
from fuzzrl.core.io.memory import Cache

LOG_FORMAT = "%(asctime)s - %(levelname)s - %(message)s"
log.basicConfig(level=log.DEBUG, format=LOG_FORMAT)


class EvolutionConfig(object):
    """
    Maintains the information needed for the GA evolution process
    """

    def __init__(self, sel_args, sel_func, cross_args, cross_func, mut_args, mut_func):
        self._sel_args = sel_args
        self._sel_func = sel_func
        self._cross_args = cross_args
        self._cross_func = cross_func
        self._mut_args = mut_args
        self._mut_func = mut_func

    @property
    def selection_op(self):
        return Operator(self._sel_func, **self._sel_args)

    @property
    def crossover_op(self):
        return Operator(self._cross_func, **self._cross_args)

    @property
    def mutation_op(self):
        return Operator(self._mut_func, **self._mut_args)


class GeneticAlgConfiguration(object):
    """
    Contains details for running the GA algorithm of the simulation
    """

    def __init__(self, evol_config, pop_size, num_gens, mf_tuning_range, lin_vars_file, gft_file, load_init_pop_file,
                 apply_evolution, defuzz_method, mutation_prob_schdl, cross_prob_schdl, learn_rb_ops=False):
        self.pop_size = pop_size
        self.num_gens = num_gens
        self.mf_tuning_range = mf_tuning_range
        self.lin_vars_file = lin_vars_file
        self.gft_file = gft_file
        self.load_init_pop_file = load_init_pop_file
        self.apply_evolution = apply_evolution
        self.defuzz_method = defuzz_method
        self.mutation_prob_schdl = mutation_prob_schdl
        self.learn_rb_ops = learn_rb_ops
        self.evol_config = evol_config
        self.cross_prob_schdl = cross_prob_schdl

        self.__ga = None
        self.__reg = None

    @property
    def ga(self):
        return self.__ga

    @property
    def registry(self):
        return self.__reg

    def init_ops(self, seed):
        Const.MF_TUNING_RANGE = self.mf_tuning_range
        Const.LEARN_RULE_OP = self.learn_rb_ops

        # create linguistic variables in a registry
        reg = xmlToLinvars(open(self.lin_vars_file).read())

        # create GFT with linguistic variables in the registry
        reg = xmlToGFT(open(self.gft_file).read(), registry=reg, defuzz_method=self.defuzz_method)

        # set registry object
        self.__reg = reg

        # create GA instance with the registry object
        self.__ga = GeneticAlgorithm(registry=reg, seed=seed)

        try:
            assert hasattr(self.mutation_prob_schdl, "get_prob") and hasattr(self.cross_prob_schdl, "get_prob")
        except AssertionError as e:
            log.error("Mutation probability schedule class must implement get_prob.\n{e}".format(e=str(e)))


class SimExecutionConfiguration(object):
    """
    Contains details for controlling the execution loop and simulation behavior
    """

    def __init__(self, env, agents, max_time_steps, episodes_per_ind, noise_process=None,
                 action_space=Const.DISCRETE, persist_cache_per_ind=True, visualize_env=False):
        self.env = env
        self.agents = agents
        self.max_time_steps = max_time_steps
        self.episodes_per_ind = episodes_per_ind
        self.random_process = noise_process
        self.action_space_type = Const.ACTION_SPACE = action_space
        self.persist_cached_data = persist_cache_per_ind
        self.render = visualize_env

    def init_ops(self, reg):
        # check environment APIs
        try:
            assert (hasattr(self.env, "reset") and hasattr(self.env, "render") and hasattr(self.env,
                                                                                           "step") and hasattr(
                self.env, "close"))
        except AssertionError as e:
            log.error("Environment APIs are incomplete. It must implement reset, render, step, and close methods.\n"
                      "{e}".format(e=str(e)))

        # check random process API
        if self.random_process is not None:
            try:
                assert hasattr(self.random_process, "sample")
            except AssertionError as e:
                log.error("The random process class must implement 'sample' method.\n{e}".format(e=str(e)))

        # get all methods that are supposed to be in obs_accessor class
        for _, gfs in reg.gft_dict.items():
            for var in gfs.descriptor.inputVariables.inputVar:
                var_config = reg.linvar_dict[var.identity.type]
                if var_config.name == Const.INNER_STATE_VAR:
                    continue
                try:
                    assert hasattr(self.agents[0].obs_accessor, var_config.procedure)
                except Exception as e:
                    log.error("Observation method \"{m}\" is missing in {c}. {e}. var: {var}"
                              .format(m=var_config.procedure, c=type(self.agents[0].obs_accessor),
                                      e=str(e), var=var_config.name))


class Runner(object):
    """
    Executes the simulation process
    """

    def __init__(self, ga_config, sim_config, r_shaping_callback=None, time_step_finished_callback=None,
                 episode_finished_callback=None, epoch_finished_callback=None, sim_finished_callback=None,
                 evolution_finished_callback=None, seed=5):
        self.seed = seed
        self.r_shaping_callback = r_shaping_callback
        self.ga_config = ga_config
        self.sim_config = sim_config
        self.time_step_finished_callback = time_step_finished_callback
        self.episode_finished_callback = episode_finished_callback
        self.epoch_finished_callback = epoch_finished_callback
        self.sim_finished_callback = sim_finished_callback
        self.evolution_finished_callback = evolution_finished_callback

    def run(self):
        # initialize GA ops
        self.ga_config.init_ops(self.seed)
        reg = self.ga_config.registry
        ga = self.ga_config.ga

        # initialize sim exec. config
        self.sim_config.init_ops(reg)

        # create GFT algorithm object with the registry
        alg = Algorithm(registry=reg, random_process=self.sim_config.random_process)

        # create a cache for managing simulation data
        cache = Cache(reg.gft_dict.keys())

        # get initial population
        if self.ga_config.load_init_pop_file is not None:
            pop = ga.load_initial_population(self.ga_config.load_init_pop_file, self.ga_config.pop_size)
            # pop = pop[::-1]
            print("Num. of loaded individuals =", len(pop))
        else:
            pop = ga.generate_initial_population(self.ga_config.pop_size)

        # initialize epoch or generation counter
        epoch = 0

        # initialize individual counter
        ind_count = 0

        env = self.sim_config.env

        agents = self.sim_config.agents

        while epoch < self.ga_config.num_gens:

            # Run the simulation with the current population
            for ind in pop:
                ind_count += 1

                # initialize reward accumulator for the individual
                total_reward = 0

                # configure the GFT with the current individual
                alg.configuregft(chromosome=ind)

                # reset the environment
                obs = env.reset()

                # set the received observation as the current array for retrieving input values
                for i, agent in enumerate(agents):
                    agent.obs_accessor.current_observation = obs if len(agents) == 1 else obs[i]

                for i_ep in range(self.sim_config.episodes_per_ind):
                    # run through the time steps of the simulation
                    for t in range(self.sim_config.max_time_steps):

                        if self.sim_config.render:
                            # show the environment
                            env.render()

                        a = None
                        for agent in agents:
                            if self.sim_config.action_space_type == Const.DISCRETE:
                                # get an action
                                code, action, input_vec_dict, probs_dict = alg.executegft(agent.obs_accessor,
                                                                                          agent_id=agent.id)

                                # mark the GFSs that executed for the agent in this time step
                                cache.mark(output_dict_keys=probs_dict.keys())

                                # store intermediate values
                                agent.temp_values = (code, action, input_vec_dict, probs_dict)
                            else:
                                # get an action
                                actions_dict, input_vec_dict = alg.executebfc(agent.obs_accessor, agent_id=agent.id,
                                                                              add_noise=True)
                                agent.temp_values = (actions_dict, input_vec_dict)
                                cache.mark(output_dict_keys=actions_dict.keys())

                        # apply the selected action to the environment and observe feedback
                        a = agents[0].temp_values[0] if len(agents) == 1 else [a.temp_values[0] for a in agents]
                        if self.sim_config.action_space_type == Const.DISCRETE:
                            a = np.array(a).astype('int').tolist() if hasattr(a, "__iter__") else int(a)
                        else:
                            a = list(a.values())
                        next_state, reward, done, _ = env.step(a)

                        if self.r_shaping_callback is not None and callable(self.r_shaping_callback):
                            reward = self.r_shaping_callback(next_state, reward, done)

                        if self.time_step_finished_callback is not None and callable(self.time_step_finished_callback):
                            self.time_step_finished_callback(next_state, reward)

                        if hasattr(reward, "__iter__"):
                            acc_reward = 0
                            for r in reward:
                                acc_reward += r
                            reward = acc_reward

                        # decompose the received reward
                        reward_dict = cache.decomposeReward(reward)

                        for i, agent in enumerate(agents):
                            if self.sim_config.action_space_type == Const.DISCRETE:
                                code, action, input_vec_dict, probs_dict = agent.temp_values
                                # create experiences for the agent with respect to each GFSs that executed for the agent
                                exp_dict = cache.createExperiences(agent_id=agent.id, action=code,
                                                                   dec_reward_dict=reward_dict,
                                                                   input_vec_dict=input_vec_dict,
                                                                   output_dict=probs_dict,
                                                                   next_state_dict=None)
                            else:
                                actions_dict, input_vec_dict = agent.temp_values
                                exp_dict = cache.createExperiences(agent_id=agent.id,
                                                                   action=list(actions_dict.values()),
                                                                   dec_reward_dict=reward_dict,
                                                                   input_vec_dict=input_vec_dict,
                                                                   output_dict=actions_dict,
                                                                   next_state_dict=None)

                            # add the experiences of the agent to the cache
                            cache.addExperiences(time_step=t, exp_dict=exp_dict)

                            # set the received observation as the current array for retrieving input values
                            agent.obs_accessor.current_observation = next_state if len(agents) == 1 else next_state[i]

                        # accumulate the rewards of all time steps
                        total_reward += reward

                        # if the episode is over end the current episode
                        if done:
                            break

                # set the return from the environment as the fitness value of the current individual
                total_reward /= float(self.sim_config.episodes_per_ind)
                ind.fitness.values = (total_reward,)

                # save contents of the cache and clear it for the next episode
                # cache.compute_states_value(gamma=.9)
                if self.sim_config.persist_cached_data:
                    cache.save_csv(path="data/")
                if self.episode_finished_callback is not None and callable(self.episode_finished_callback):
                    self.episode_finished_callback(ind, ind_count, self.ga_config.num_gens * self.ga_config.pop_size,
                                                   total_reward)
            # GA stats by DEAP
            record = ga.stats.compile(pop)
            ga.logbook.record(epoch=epoch, **record)

            if self.epoch_finished_callback is not None and callable(self.epoch_finished_callback):
                self.epoch_finished_callback(epoch, pop, record)
            # perform evolution
            if self.ga_config.apply_evolution:
                m_prob = self.ga_config.mutation_prob_schdl.get_prob(epoch)
                c_prob = self.ga_config.cross_prob_schdl.get_prob(epoch)
                ev = self.ga_config.evol_config
                pop = ga.evolve(pop, selop=ev.selection_op, crossop=ev.crossover_op, mutop=ev.mutation_op,
                                mut_prob=m_prob, cross_prob=c_prob)
                if self.evolution_finished_callback is not None and callable(self.evolution_finished_callback):
                    self.evolution_finished_callback(pop, m_prob, c_prob, epoch)

            epoch += 1

        if self.sim_finished_callback is not None and callable(self.sim_finished_callback):
            self.sim_finished_callback(ga, pop)

        env.close()


class Agent(object):

    def __init__(self, agent_id, obs_class):
        self.__id = agent_id
        try:
            assert isinstance(obs_class, type)
        except AssertionError as e:
            log.error("Class for retrieving agent observation must be passed.\n{e}".format(e=str(e)))
        self.__obs_accessor = obs_class()
        self.__short_mem = None

    @property
    def id(self):
        return self.__id

    @property
    def obs_accessor(self):
        return self.__obs_accessor

    @property
    def temp_values(self):
        return self.__short_mem

    @temp_values.setter
    def temp_values(self, temp):
        self.__short_mem = temp
