class Constants:
    """
    Maintains all operating constants of core modules
    """
    INNER_STATE_VAR = "internalStateInputVariable"
    MF_TUNING_RANGE = [-0.2, 0.2]
    LEARN_RULE_OP = False
    ZEROS_MF_SEGMENT = 0.01
    DISCRETE = "discrete_action_space"
    CONTINUOUS = "continuous_action_space"
    ACTION_SPACE = DISCRETE


def setconstants(**kwargs):
    """
    Helper function to enable setting initial values
    :param kwargs:
    :return:
    """
    for k, v in kwargs.items():
        setattr(Constants, k, v)
