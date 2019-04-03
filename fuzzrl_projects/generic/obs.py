# project: fuzzprj
# Copyright (C) 9/6/18 - 5:19 PM
# Author: bbrighttaer


from fuzzrl.core.util.ops import normalize, sigmoid
from numpy import tanh, mean

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


class BipedalWalkerObs(object):
    def __init__(self):
        self.current_observation = None

    def get_hull_angle(self, agentId):
        return self.current_observation[0]

    def get_hull_angularVelocity(self, agentId):
        return tanh(self.current_observation[1])

    def get_vel_x(self, agentId):
        return tanh(self.current_observation[2])

    def get_vel_y(self, agentId):
        return tanh(self.current_observation[3])

    def get_hip_joint_1_angle(self, agentId):
        return tanh(self.current_observation[4])

    def get_hip_joint_1_speed(self, agentId):
        return tanh(self.current_observation[5])

    def get_knee_joint_1_angle(self, agentId):
        return tanh(self.current_observation[6])

    def get_knee_joint_1_speed(self, agentId):
        return tanh(self.current_observation[7])

    def leg_1_ground_contact_flag(self, agentId):
        return sigmoid(self.current_observation[8])

    def get_hip_joint_2_angle(self, agentId):
        return tanh(self.current_observation[9])

    def get_hip_joint_2_speed(self, agentId):
        return tanh(self.current_observation[10])

    def get_knee_joint_2_angle(self, agentId):
        return tanh(self.current_observation[11])

    def get_knee_joint_2_speed(self, agentId):
        return tanh(self.current_observation[12])

    def get_leg_2_ground_contact_flag(self, agentId):
        return sigmoid(self.current_observation[13])

    def get_lidar_readings(self, agentId):
        lidar = self.current_observation[14:len(self.current_observation)]
        return tanh(mean(lidar))
