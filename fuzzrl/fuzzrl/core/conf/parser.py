import copy

from fuzzrl.core.conf.gft import CreateFromDocument as createGFT
from fuzzrl.core.conf.linvars import CreateFromDocument as createLinvars
from fuzzrl.core.fuzzy.gfs import GeneticFuzzySystem
from fuzzrl.core.reg.registry import Registry


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


def xmlToGFT(xmlText, registry, defuzz_method):
    """
    Reads the GFT configuration file and create the nodes of the tree
    :param defuzz_method: Defuzzification method
    :param xmlText: The GFT configuration file content
    :param registry: The registry object which already has a configured set of linguistic variables
    :return The updated registry
    """
    # creates the GFT object from configuration file content
    gft_config = createGFT(xmlText)

    # gets the parsed linguistic variables
    linvars = registry.linvar_dict

    # stores the parsed GFT configuration object
    registry.gft_config = gft_config

    # create each GFT
    for fis in gft_config.fuzzyInferenceSystem:
        var_dict = {}
        for v in fis.inputVariables.inputVar:
            # tic = time.time()
            var_dict[v.identity.type] = copy.deepcopy(linvars[v.identity.type])
            # print((time.time() - tic)*1000)
        var_dict[fis.outputVariable.type] = linvars[fis.outputVariable.type]
        gfs = GeneticFuzzySystem(fis, vars_config_dict=var_dict, defuzz_method=defuzz_method)
        registry.gft_dict[gfs.name] = gfs
    return registry
