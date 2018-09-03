import logging as log
import unittest

from fuzzrl.core.conf.parser import *

LOG_FORMAT = "%(asctime)s - %(levelname)s - %(message)s"
log.basicConfig(level=log.DEBUG, format=LOG_FORMAT)

LIN_VARS_FILE = "../../res/linvarsGFT8.xml"
GFT_FILE = "../../res/gft9.xml"


class TestParsers(unittest.TestCase):
    def test_xmlToLinvars(self):
        reg = Registry("test_reg")
        xml = open(LIN_VARS_FILE).read()
        xmlToLinvars(xml, reg)
        self.assertGreater(len(reg.linvar_dict), 0)
        log.debug("loaded linguistic variables = {}".format(len(reg.linvar_dict)))

    def test_xmlToGFT(self):
        reg = Registry("test_reg")

        # 1. set the linguistic variables
        xmlToLinvars(open(LIN_VARS_FILE).read(), registry=reg)

        # 2. now create GFT in the registry
        xml = open(GFT_FILE).read()
