from fuzznnrl.core.test import *

LIN_VARS_FILE = "../../res/linvarsGFT7.xml"
GFT_FILE = "../../res/gft9.xml"


class TestParsers(unittest.TestCase):
    def test_xmlToLinvars(self):
        reg = Registry("test_reg")
        xml = open(LIN_VARS_FILE).read()
        xmlToLinvars(xml, reg)
        self.assertGreater(len(reg.linvar_dict), 0)
        log.debug("Number of loaded linguistic variables = {}".format(len(reg.linvar_dict)))

    def test_xmlToGFT(self):
        reg = Registry("test_reg")

        # 1. set the linguistic variables
        xmlToLinvars(open(LIN_VARS_FILE).read(), registry=reg)

        # 2. now create GFT in the registry
        xml = open(GFT_FILE).read()
        xmlToGFT(xml, reg)
        self.assertGreater(len(reg.gft_dict), 0)
        log.debug("Number of created GFS = {}".format(len(reg.gft_dict)))

    def test_displayGFSs(self):
        reg = Registry("test_reg")
        xmlToLinvars(open(LIN_VARS_FILE).read(), registry=reg)
        xmlToGFT(open(GFT_FILE).read(), registry=reg)
        for (_, gfs) in reg.gft_dict.items():
            print(str(gfs))
