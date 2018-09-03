# project: fuzzrl
# Copyright (C) 6/8/18 - 2:54 PM
# Author: bbrighttaer


"""
slight modification of scikit-fuzzy skfuzzext.py : RuleOrderGenerator
"""

from skfuzzy.control.controlsystem import RuleOrderGenerator
from skfuzzy.control.rule import Rule


class RuleGenerator(RuleOrderGenerator):
    """
    Generator to yield rules in the correct order for calculation.

    Parameters
    ----------
    control_system : ControlSystem
        Fuzzy control system object, instance of `skfuzzy.ControlSystem`.

    Returns
    -------
    out : Rule
        Fuzzy rules in computation order.
    """

    def __init__(self, control_system):
        super(RuleGenerator, self).__init__(control_system)

    def __iter__(self):
        """
        Method to yield the fuzzy rules in order for computation.
        """
        # Determine if we can return the cached version or must calc new
        if self._cached_graph is not self.control_system.graph:
            # The controller is still using a different version of the graph
            #  than we created the rule order for.  Thus, make new cache
            self._init_state()
            # original:
            # self._cache = list(self._process_rules(self.all_rules[:]))
            # modified :
            self._cache = list(self.all_rules[:])
            self._cached_graph = self.control_system.graph

        for n, r in enumerate(self._cache):
            yield r
        else:
            n = 0

        if n == 0:
            pass
        else:
            assert n == len(self.all_rules) - 1, "Not all rules exposed"
