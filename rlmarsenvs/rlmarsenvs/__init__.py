#
# Project: rlmarsenvs
# Created by bbrighttaer on 6/14/18
#

# Environments registration

from gym.envs.registration import register

from .envs.carmunk import ENV_NAME, VERSION

# from https://github.com/harvitronix/reinforcement-learning-car
register(id="{}-{}".format(ENV_NAME, VERSION),
         entry_point="rlmarsenvs.envs:Carmunk", )
