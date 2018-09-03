class Constants:
    """
    Maintains all operating constants of core modules
    """
    # RAND_SEED = 1
    MF_TUNING_RANGE = [-0.2, 0.2]
    LEARN_RULE_OP = True
    ZEROS_MF_SEGMENT = 0.01


def setconstants(**kwargs):
    """
    Helper function to enable setting initial values
    :param kwargs:
    :return:
    """
    for k, v in kwargs.items():
        setattr(Constants, k, v)
