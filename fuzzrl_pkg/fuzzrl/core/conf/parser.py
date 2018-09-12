import copy

from fuzzrl.core.conf.fuzzynetxsd import CreateFromDocument as createFuzzyNet
from fuzzrl.core.conf.linvars import CreateFromDocument as createLinvars
from fuzzrl.core.fuzzy.gfs import GeneticFuzzySystem
from fuzzrl.core.reg.registry import Registry
import pyxb.namespace.builtin as pyxb


def xmlToLinvars(xmlText, registry=Registry("default_reg")):
    """
    Parse the submitted linguistic variables configuration into an accessible object and
    create the corresponding variables in the registry

    :param xmlText: The read xml text
    :param registry: The registry object for storage
    :return The updated registry
    """
    vars_config = createLinvars(xmlText)
    registry.linvar_config = vars_config

    for var in vars_config.variable:
        registry.linvar_dict[var.name] = var
    return registry


def _create_layer_nodes(config, linvars, registry, layer):
    # create each GFT
    for fis in config.fis:
        var_dict = {}
        for v in fis.inputVariables.inputVar:
            # tic = time.time()
            var_dict[v.identity.type] = copy.deepcopy(linvars[v.identity.type])
            # print((time.time() - tic)*1000)
        var_dict[fis.outputVariable.type] = linvars[fis.outputVariable.type]
        gfs = GeneticFuzzySystem(fis, vars_config_dict=var_dict, defuzz_method=fis.defuzz)
        registry.gft_dict[gfs.name] = gfs
    return registry


def xmlToFuzzyNet(xmlText, registry):
    """
    Reads the fuzzy net configuration file and create the net from the details
    -----------------------

    :param xmlText: The configuration file content
    :param registry: The registry object which already has a configured set of linguistic variables
    :param defuzz_methods: a tuple of defuzzification methods to be used by each layer.
    If the tuple contents shall be applied across the layers in a toroidal fashion. Hence, if the same defuzzification
    method is to be used across all layers, then that method shall be the only element in the tuple.
    :return: Updated registry containing the created network
    """
    pyxb.XMLSchema_instance
    # create the fuzzy net object from configuration file content
    fn_config = createFuzzyNet(xmlText)

    # get the parsed linguistic variables
    linvars = registry.linvar_dict

    # store the parsed net configuration object
    registry.fuzzynet_config = fn_config

    # combine all layers for GFS creation
    all_layers = {"input": [fn_config.input], "hidden": [h_layer for h_layer in fn_config.hidden],
                  "output": [fn_config.output]}

    # create all nodes of the net
    for k, layer_segment in all_layers.items():
        for layer in layer_segment:
            _create_layer_nodes(layer, linvars, registry, layer=k)
