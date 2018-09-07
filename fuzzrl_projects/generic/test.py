#
# Project: fuzzrl
# Created by bbrighttaer on 9/7/18
#

import gym

env = gym.make("Pendulum-v0")

env.reset()

for i_episode in range(5000):
    for i in range(500):
        env.render()
        s, r, d, _ = env.step([env.action_space.sample()])
        if d:
            break
    print("episode {} completed".format(i_episode))
