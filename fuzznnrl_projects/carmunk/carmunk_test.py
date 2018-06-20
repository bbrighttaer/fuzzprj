#
# Project: fuzzprj
# Created by bbrighttaer on 6/20/18
#


import logging as log

import gym

# registers the environment to use the gym interface
import rlmarsenvs

LOG_FORMAT = "%(asctime)s - %(levelname)s - %(message)s"
log.basicConfig(level=log.DEBUG, format=LOG_FORMAT)


def main():
    env = gym.make("carmunk-v2")
    log.info("action_space = {}".format(env.action_space))
    log.info("observation_space = {}, low = {}, high = {}".format(env.observation_space, env.observation_space.low,
                                                                  env.observation_space.high))
    for i_episode in range(5):
        env.reset()
        while True:
            env.render()
            ob, reward, done, info = env.step(env.action_space.sample())
            log.info("ob={}, reward={}, done={}, info={}".format(str(ob), reward, str(done), str(info)))
            if done:
                break


if __name__ == '__main__':
    main()
