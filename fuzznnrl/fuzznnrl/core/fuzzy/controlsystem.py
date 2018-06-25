# project: fuzznnrl
# Copyright (C) 6/8/18 - 2:54 PM
# Author: bbrighttaer

import skfuzzy.control as ctrl


class ControlSystem(ctrl.ControlSystem):
    def __init__(self, rules=None):
        super(ControlSystem, self).__init__(rules=rules)

    def addrule(self, rule):
        """
        Add a new rule to the system.
        """
        if not isinstance(rule, ctrl.Rule):
            raise ValueError("Input rule must be a Rule object!")

        # Ensure no label duplication
        labels = []
        for r in self.rules:
            if r.label in labels:
                raise ValueError("Input rule cannot have same label, '{0}', "
                                 "as any other rule.".format(r.label))
            labels.append(r.label)

        # Combine the two graphs, which may not be disjoint
        # self.graph = nx.compose(self.graph, rule.graph)
