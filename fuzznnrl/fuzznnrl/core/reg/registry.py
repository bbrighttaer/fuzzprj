class Registry(object):
    """
     ## Serves as the main registry for:
     --------------------------------
     - parsed configuration details
     - created linguistic variables
     - created nodes in the tree. In the case of a fuzzy control system these nodes are the GFSs whereas the nodes are
        NNs in the case of NN/DRL control
    """

    def __init__(self, label=None):
        # a label for the registry
        self.__label = label

        # a dictionary of all linguistic variables from the linguistic variables configuration file
        self.__linvar_dict = {}

        # a dictionary of all fuzzy inference systems in the GFT configuration file
        self.__gft_dict = {}

        # an object representing the parsed details of the linguistic variables configuration file.
        self.__linvar_config = None

        # an object representing the parsed details of the GFT configuration file
        self.__gft_config = None

    @property
    def label(self):
        return self.__label

    @label.setter
    def label(self, label):
        self.__label = label

    @property
    def linvar_dict(self):
        return self.__linvar_dict

    @linvar_dict.setter
    def linvar_dict(self, dict={}):
        self.__linvar_dict = dict

    @property
    def gft_dict(self):
        return self.__gft_dict

    @gft_dict.setter
    def gft_dict(self, dict):
        return self.__gft_dict

    @property
    def linvar_config(self):
        return self.__linvar_config

    @linvar_config.setter
    def linvar_config(self, config):
        self.__linvar_config = config

    @property
    def gft_config(self):
        return self.__gft_config

    @gft_config.setter
    def gft_config(self, config):
        self.__gft_config = config
