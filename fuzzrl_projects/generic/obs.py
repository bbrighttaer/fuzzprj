# project: fuzzprj
# Copyright (C) 9/6/18 - 5:19 PM
# Author: bbrighttaer


from fuzzrl.core.util.ops import normalize, sigmoid


class CartPoleObs(object):
    def __init__(self):
        self.current_observation = None

    def getCartPosition(self, agentId):
        assert self.current_observation is not None
        return self.current_observation[0]

    def getCartVelocity(self, agentId):
        assert self.current_observation is not None
        return sigmoid(self.current_observation[1])

    def getPoleAngle(self, agentId):
        assert self.current_observation is not None
        return self.current_observation[2]

    def getPoleVelocity(self, agentId):
        assert self.current_observation is not None
        return sigmoid(self.current_observation[3])


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


class MountainCarObs(object):
    def __init__(self):
        self.current_observation = None

    def getCarPosition(self, agentId):
        assert self.current_observation is not None
        return self.current_observation[0]

    def getCarVelocity(self, agentId):
        assert self.current_observation is not None
        return self.current_observation[1]
