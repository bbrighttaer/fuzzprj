import logging as log
import unittest

from fuzzrl.core.conf.parser import *
from fuzzrl.core.ga.genalg import *

LOG_FORMAT = "%(asctime)s - %(levelname)s - %(message)s"
log.basicConfig(level=log.DEBUG, format=LOG_FORMAT)
