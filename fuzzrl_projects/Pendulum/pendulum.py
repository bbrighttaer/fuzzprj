#
# Project: fuzzrl
# Created by bbrighttaer on 9/3/18
#


import random

import gym

env = gym.make("Pendulum-v0")

env.reset()

print("action: low = {l}, high = {h}".format(l=env.action_space.low, h=env.action_space.high))

for i_episode in range(1000):
    env.render()
    a = random.uniform(env.action_space.low, env.action_space.high)
    print("action =", str(a))
    s, r, done, _ = env.step([a])
    # if done:
    #     print("episode ended after {t} time steps".format(t=i_episode + 1))

env.close()
