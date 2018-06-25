import fuzznnrl.core.ga.schedule as sch
import matplotlib.pyplot as plt
from fuzznnrl.core.test import *

init_prob = 0.9
decay_factor = 1e-1


class MyTestCase(unittest.TestCase):
    def test_ConstantDecaySchedule(self):
        s = sch.LinearDecaySchedule(initial_prob=init_prob, decay_factor=decay_factor)
        runschedule(s)

    def test_ExponentialDecaySchedule(self):
        s = sch.ExponentialDecaySchedule(init_prob, decay_factor)
        runschedule(s)

    def test_StepDecaySchedule(self):
        s = sch.StepDecaySchedule(init_prob, decay_factor=decay_factor, epochs_drop=20)
        runschedule(s, 100)

    def test_TimeBasedSchedule(self):
        s = sch.TimeBasedSchedule(decay_factor)
        runschedule(s, epochs=10)


def runschedule(s, epochs=1000):
    vals = []
    for i in range(epochs):
        vals.append(s.get_prob(i))
    plt.figure(0)
    plt.plot(vals)
    plt.show()


if __name__ == '__main__':
    unittest.main()
