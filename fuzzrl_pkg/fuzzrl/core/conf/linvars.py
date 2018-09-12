# ./linvars/py.py
# -*- coding: utf-8 -*-
# PyXB bindings for NM:e92452c8d3e28a9e27abfc9994d2007779e7f4c9
# Generated 2018-06-11 17:42:21.007756 by PyXB version 1.2.6 using Python 3.6.4.final.0
# Namespace AbsentNamespace0

from __future__ import unicode_literals

import io

import pyxb
import pyxb.binding
import pyxb.binding.saxer
import pyxb.utils.domutils
import pyxb.utils.six as _six
import pyxb.utils.utility

# Unique identifier for bindings created at the same time
_GenerationUID = pyxb.utils.utility.UniqueIdentifier('urn:uuid:bcaf0c7a-6d5b-11e8-a7c0-4439c4558c33')

# Version of PyXB used to generate the bindings
_PyXBVersion = '1.2.6'
# Generated bindings are not compatible across PyXB versions
if pyxb.__version__ != _PyXBVersion:
    raise pyxb.PyXBVersionError(_PyXBVersion)

# A holder for module-level binding classes so we can access them from
# inside class definitions where property names may conflict.
_module_typeBindings = pyxb.utils.utility.Object()

# Import bindings for namespaces imported into schema
import pyxb.binding.datatypes

# NOTE: All namespace declarations are reserved within the binding
Namespace = pyxb.namespace.CreateAbsentNamespace()
Namespace.configureCategories(['typeBinding', 'elementBinding'])


def CreateFromDocument(xml_text, default_namespace=None, location_base=None):
    """Parse the given XML and use the document element to create a
    Python instance.

    @param xml_text An XML document.  This should be data (Python 2
    str or Python 3 bytes), or a text (Python 2 unicode or Python 3
    str) in the L{pyxb._InputEncoding} encoding.

    @keyword default_namespace The L{pyxb.Namespace} instance to use as the
    default namespace where there is no default namespace in scope.
    If unspecified or C{None}, the namespace of the module containing
    this function will be used.

    @keyword location_base: An object to be recorded as the base of all
    L{pyxb.utils.utility.Location} instances associated with events and
    objects handled by the parser.  You might pass the URI from which
    the document was obtained.
    """

    if pyxb.XMLStyle_saxer != pyxb._XMLStyle:
        dom = pyxb.utils.domutils.StringToDOM(xml_text)
        return CreateFromDOM(dom.documentElement, default_namespace=default_namespace)
    if default_namespace is None:
        default_namespace = Namespace.fallbackNamespace()
    saxer = pyxb.binding.saxer.make_parser(fallback_namespace=default_namespace, location_base=location_base)
    handler = saxer.getContentHandler()
    xmld = xml_text
    if isinstance(xmld, _six.text_type):
        xmld = xmld.encode(pyxb._InputEncoding)
    saxer.parse(io.BytesIO(xmld))
    instance = handler.rootObject()
    return instance


def CreateFromDOM(node, default_namespace=None):
    """Create a Python instance from the given DOM node.
    The node tag must correspond to an element declaration in this module.

    @deprecated: Forcing use of DOM interface is unnecessary; use L{CreateFromDocument}."""
    if default_namespace is None:
        default_namespace = Namespace.fallbackNamespace()
    return pyxb.binding.basis.element.AnyCreateFromDOM(node, default_namespace)


# Atomic simple type: [anonymous]
class STD_ANON(pyxb.binding.datatypes.string, pyxb.binding.basis.enumeration_mixin):
    """An atomic simple type."""

    _ExpandedName = None
    _XSDLocation = pyxb.utils.utility.Location(
        '../res/linguisticVariables.xsd', 19, 56)
    _Documentation = None


STD_ANON._CF_enumeration = pyxb.binding.facets.CF_enumeration(value_datatype=STD_ANON, enum_prefix=None)
STD_ANON.LTunableTerminalTriangle = STD_ANON._CF_enumeration.addEnumeration(unicode_value='LTunableTerminalTriangle',
                                                                            tag='LTunableTerminalTriangle')
STD_ANON.TunableTriangle = STD_ANON._CF_enumeration.addEnumeration(unicode_value='TunableTriangle',
                                                                   tag='TunableTriangle')
STD_ANON.RTunableTerminalTriangle = STD_ANON._CF_enumeration.addEnumeration(unicode_value='RTunableTerminalTriangle',
                                                                            tag='RTunableTerminalTriangle')
STD_ANON.Triangle = STD_ANON._CF_enumeration.addEnumeration(unicode_value='Triangle', tag='Triangle')
STD_ANON.Gaussian = STD_ANON._CF_enumeration.addEnumeration(unicode_value='Gaussian', tag='Gaussian')
STD_ANON.Sigmoid = STD_ANON._CF_enumeration.addEnumeration(unicode_value='Sigmoid', tag='Sigmoid')
STD_ANON._InitializeFacetMap(STD_ANON._CF_enumeration)
_module_typeBindings.STD_ANON = STD_ANON


# List simple type: [anonymous]
# superclasses pyxb.binding.datatypes.anySimpleType
class STD_ANON_(pyxb.binding.basis.STD_list):
    """Simple type that is a list of pyxb.binding.datatypes.double."""

    _ExpandedName = None
    _XSDLocation = pyxb.utils.utility.Location(
        '../res/linguisticVariables.xsd', 31, 56)
    _Documentation = None

    _ItemType = pyxb.binding.datatypes.double


STD_ANON_._InitializeFacetMap()
_module_typeBindings.STD_ANON_ = STD_ANON_


# Atomic simple type: varType
class varType(pyxb.binding.datatypes.string, pyxb.binding.basis.enumeration_mixin):
    """An atomic simple type."""

    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'varType')
    _XSDLocation = pyxb.utils.utility.Location(
        '../res/linguisticVariables.xsd', 53, 4)
    _Documentation = None


varType._CF_enumeration = pyxb.binding.facets.CF_enumeration(value_datatype=varType, enum_prefix=None)
varType.input = varType._CF_enumeration.addEnumeration(unicode_value='input', tag='input')
varType.output = varType._CF_enumeration.addEnumeration(unicode_value='output', tag='output')
varType._InitializeFacetMap(varType._CF_enumeration)
Namespace.addCategoryObject('typeBinding', 'varType', varType)
_module_typeBindings.varType = varType


# Complex type [anonymous] with content type ELEMENT_ONLY
class CTD_ANON(pyxb.binding.basis.complexTypeDefinition):
    """Complex type [anonymous] with content type ELEMENT_ONLY"""
    _TypeDefinition = None
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_ELEMENT_ONLY
    _Abstract = False
    _ExpandedName = None
    _XSDLocation = pyxb.utils.utility.Location(
        '../res/linguisticVariables.xsd', 7, 8)
    _ElementMap = {}
    _AttributeMap = {}
    # Base type is pyxb.binding.datatypes.anyType

    # Element variable uses Python identifier variable
    __variable = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(None, 'variable'), 'variable',
                                                         '__AbsentNamespace0_CTD_ANON_variable', True,
                                                         pyxb.utils.utility.Location(
                                                             '../res/linguisticVariables.xsd',
                                                             9, 16), )

    variable = property(__variable.value, __variable.set, None, None)

    _ElementMap.update({
        __variable.name(): __variable
    })
    _AttributeMap.update({

    })


_module_typeBindings.CTD_ANON = CTD_ANON


# Complex type [anonymous] with content type ELEMENT_ONLY
class CTD_ANON_(pyxb.binding.basis.complexTypeDefinition):
    """Complex type [anonymous] with content type ELEMENT_ONLY"""
    _TypeDefinition = None
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_ELEMENT_ONLY
    _Abstract = False
    _ExpandedName = None
    _XSDLocation = pyxb.utils.utility.Location(
        '../res/linguisticVariables.xsd', 13, 32)
    _ElementMap = {}
    _AttributeMap = {}
    # Base type is pyxb.binding.datatypes.anyType

    # Element term uses Python identifier term
    __term = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(None, 'term'), 'term',
                                                     '__AbsentNamespace0_CTD_ANON__term', True,
                                                     pyxb.utils.utility.Location(
                                                         '../res/linguisticVariables.xsd',
                                                         15, 40), )

    term = property(__term.value, __term.set, None, None)

    _ElementMap.update({
        __term.name(): __term
    })
    _AttributeMap.update({

    })


_module_typeBindings.CTD_ANON_ = CTD_ANON_


# Complex type [anonymous] with content type ELEMENT_ONLY
class CTD_ANON_2(pyxb.binding.basis.complexTypeDefinition):
    """Complex type [anonymous] with content type ELEMENT_ONLY"""
    _TypeDefinition = None
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_ELEMENT_ONLY
    _Abstract = False
    _ExpandedName = None
    _XSDLocation = pyxb.utils.utility.Location(
        '../res/linguisticVariables.xsd', 16, 44)
    _ElementMap = {}
    _AttributeMap = {}
    # Base type is pyxb.binding.datatypes.anyType

    # Element mf uses Python identifier mf
    __mf = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(None, 'mf'), 'mf',
                                                   '__AbsentNamespace0_CTD_ANON_2_mf', False,
                                                   pyxb.utils.utility.Location(
                                                       '../res/linguisticVariables.xsd',
                                                       18, 52), )

    mf = property(__mf.value, __mf.set, None, None)

    # Element params uses Python identifier params
    __params = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(None, 'params'), 'params',
                                                       '__AbsentNamespace0_CTD_ANON_2_params', False,
                                                       pyxb.utils.utility.Location(
                                                           '../res/linguisticVariables.xsd',
                                                           30, 52), )

    params = property(__params.value, __params.set, None, None)

    # Attribute name uses Python identifier name
    __name = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'name'), 'name',
                                               '__AbsentNamespace0_CTD_ANON_2_name', pyxb.binding.datatypes.string,
                                               required=True)
    __name._DeclarationLocation = pyxb.utils.utility.Location(
        '../res/linguisticVariables.xsd', 36, 48)
    __name._UseLocation = pyxb.utils.utility.Location(
        '../res/linguisticVariables.xsd', 36, 48)

    name = property(__name.value, __name.set, None, None)

    _ElementMap.update({
        __mf.name(): __mf,
        __params.name(): __params
    })
    _AttributeMap.update({
        __name.name(): __name
    })


_module_typeBindings.CTD_ANON_2 = CTD_ANON_2


# Complex type [anonymous] with content type ELEMENT_ONLY
class CTD_ANON_3(pyxb.binding.basis.complexTypeDefinition):
    """Complex type [anonymous] with content type ELEMENT_ONLY"""
    _TypeDefinition = None
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_ELEMENT_ONLY
    _Abstract = False
    _ExpandedName = None
    _XSDLocation = pyxb.utils.utility.Location(
        '../res/linguisticVariables.xsd', 10, 20)
    _ElementMap = {}
    _AttributeMap = {}
    # Base type is pyxb.binding.datatypes.anyType

    # Element terms uses Python identifier terms
    __terms = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(None, 'terms'), 'terms',
                                                      '__AbsentNamespace0_CTD_ANON_3_terms', False,
                                                      pyxb.utils.utility.Location(
                                                          '../res/linguisticVariables.xsd',
                                                          12, 28), )

    terms = property(__terms.value, __terms.set, None, None)

    # Attribute name uses Python identifier name
    __name = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'name'), 'name',
                                               '__AbsentNamespace0_CTD_ANON_3_name', pyxb.binding.datatypes.string,
                                               required=True)
    __name._DeclarationLocation = pyxb.utils.utility.Location(
        '../res/linguisticVariables.xsd', 43, 24)
    __name._UseLocation = pyxb.utils.utility.Location(
        '../res/linguisticVariables.xsd', 43, 24)

    name = property(__name.value, __name.set, None, None)

    # Attribute rangeMin uses Python identifier rangeMin
    __rangeMin = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'rangeMin'), 'rangeMin',
                                                   '__AbsentNamespace0_CTD_ANON_3_rangeMin',
                                                   pyxb.binding.datatypes.double, required=True)
    __rangeMin._DeclarationLocation = pyxb.utils.utility.Location(
        '../res/linguisticVariables.xsd', 44, 24)
    __rangeMin._UseLocation = pyxb.utils.utility.Location(
        '../res/linguisticVariables.xsd', 44, 24)

    rangeMin = property(__rangeMin.value, __rangeMin.set, None, None)

    # Attribute rangeMax uses Python identifier rangeMax
    __rangeMax = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'rangeMax'), 'rangeMax',
                                                   '__AbsentNamespace0_CTD_ANON_3_rangeMax',
                                                   pyxb.binding.datatypes.double, required=True)
    __rangeMax._DeclarationLocation = pyxb.utils.utility.Location(
        '../res/linguisticVariables.xsd', 45, 24)
    __rangeMax._UseLocation = pyxb.utils.utility.Location(
        '../res/linguisticVariables.xsd', 45, 24)

    rangeMax = property(__rangeMax.value, __rangeMax.set, None, None)

    # Attribute type uses Python identifier type
    __type = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'type'), 'type',
                                               '__AbsentNamespace0_CTD_ANON_3_type', _module_typeBindings.varType,
                                               required=True)
    __type._DeclarationLocation = pyxb.utils.utility.Location(
        '../res/linguisticVariables.xsd', 46, 24)
    __type._UseLocation = pyxb.utils.utility.Location(
        '../res/linguisticVariables.xsd', 46, 24)

    type = property(__type.value, __type.set, None, None)

    # Attribute procedure uses Python identifier procedure
    __procedure = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'procedure'), 'procedure',
                                                    '__AbsentNamespace0_CTD_ANON_3_procedure',
                                                    pyxb.binding.datatypes.string)
    __procedure._DeclarationLocation = pyxb.utils.utility.Location(
        '../res/linguisticVariables.xsd', 47, 24)
    __procedure._UseLocation = pyxb.utils.utility.Location(
        '../res/linguisticVariables.xsd', 47, 24)

    procedure = property(__procedure.value, __procedure.set, None, None)

    _ElementMap.update({
        __terms.name(): __terms
    })
    _AttributeMap.update({
        __name.name(): __name,
        __rangeMin.name(): __rangeMin,
        __rangeMax.name(): __rangeMax,
        __type.name(): __type,
        __procedure.name(): __procedure
    })


_module_typeBindings.CTD_ANON_3 = CTD_ANON_3

linguisticVariables = pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'linguisticVariables'),
                                                 CTD_ANON, location=pyxb.utils.utility.Location(
        '../res/linguisticVariables.xsd', 6, 4))
Namespace.addCategoryObject('elementBinding', linguisticVariables.name().localName(), linguisticVariables)

CTD_ANON._AddElement(
    pyxb.binding.basis.element(pyxb.namespace.ExpandedName(None, 'variable'), CTD_ANON_3, scope=CTD_ANON,
                               location=pyxb.utils.utility.Location(
                                   '../res/linguisticVariables.xsd', 9, 16)))


def _BuildAutomaton():
    # Remove this helper function from the namespace after it is invoked
    global _BuildAutomaton
    del _BuildAutomaton
    import pyxb.utils.fac as fac

    counters = set()
    states = []
    final_update = set()
    symbol = pyxb.binding.content.ElementUse(CTD_ANON._UseForTag(pyxb.namespace.ExpandedName(None, 'variable')),
                                             pyxb.utils.utility.Location(
                                                 '../res/linguisticVariables.xsd',
                                                 9, 16))
    st_0 = fac.State(symbol, is_initial=True, final_update=final_update, is_unordered_catenation=False)
    states.append(st_0)
    transitions = []
    transitions.append(fac.Transition(st_0, [
    ]))
    st_0._set_transitionSet(transitions)
    return fac.Automaton(states, counters, False, containing_state=None)


CTD_ANON._Automaton = _BuildAutomaton()

CTD_ANON_._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(None, 'term'), CTD_ANON_2, scope=CTD_ANON_,
                                                 location=pyxb.utils.utility.Location(
                                                     '../res/linguisticVariables.xsd',
                                                     15, 40)))


def _BuildAutomaton_():
    # Remove this helper function from the namespace after it is invoked
    global _BuildAutomaton_
    del _BuildAutomaton_
    import pyxb.utils.fac as fac

    counters = set()
    states = []
    final_update = set()
    symbol = pyxb.binding.content.ElementUse(CTD_ANON_._UseForTag(pyxb.namespace.ExpandedName(None, 'term')),
                                             pyxb.utils.utility.Location(
                                                 '../res/linguisticVariables.xsd',
                                                 15, 40))
    st_0 = fac.State(symbol, is_initial=True, final_update=final_update, is_unordered_catenation=False)
    states.append(st_0)
    transitions = []
    transitions.append(fac.Transition(st_0, [
    ]))
    st_0._set_transitionSet(transitions)
    return fac.Automaton(states, counters, False, containing_state=None)


CTD_ANON_._Automaton = _BuildAutomaton_()

CTD_ANON_2._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(None, 'mf'), STD_ANON, scope=CTD_ANON_2,
                                                  location=pyxb.utils.utility.Location(
                                                      '../res/linguisticVariables.xsd',
                                                      18, 52)))

CTD_ANON_2._AddElement(
    pyxb.binding.basis.element(pyxb.namespace.ExpandedName(None, 'params'), STD_ANON_, scope=CTD_ANON_2,
                               location=pyxb.utils.utility.Location(
                                   '../res/linguisticVariables.xsd', 30, 52)))


def _BuildAutomaton_2():
    # Remove this helper function from the namespace after it is invoked
    global _BuildAutomaton_2
    del _BuildAutomaton_2
    import pyxb.utils.fac as fac

    counters = set()
    states = []
    final_update = None
    symbol = pyxb.binding.content.ElementUse(CTD_ANON_2._UseForTag(pyxb.namespace.ExpandedName(None, 'mf')),
                                             pyxb.utils.utility.Location(
                                                 '../res/linguisticVariables.xsd',
                                                 18, 52))
    st_0 = fac.State(symbol, is_initial=True, final_update=final_update, is_unordered_catenation=False)
    states.append(st_0)
    final_update = set()
    symbol = pyxb.binding.content.ElementUse(CTD_ANON_2._UseForTag(pyxb.namespace.ExpandedName(None, 'params')),
                                             pyxb.utils.utility.Location(
                                                 '../res/linguisticVariables.xsd',
                                                 30, 52))
    st_1 = fac.State(symbol, is_initial=False, final_update=final_update, is_unordered_catenation=False)
    states.append(st_1)
    transitions = []
    transitions.append(fac.Transition(st_1, [
    ]))
    st_0._set_transitionSet(transitions)
    transitions = []
    st_1._set_transitionSet(transitions)
    return fac.Automaton(states, counters, False, containing_state=None)


CTD_ANON_2._Automaton = _BuildAutomaton_2()

CTD_ANON_3._AddElement(
    pyxb.binding.basis.element(pyxb.namespace.ExpandedName(None, 'terms'), CTD_ANON_, scope=CTD_ANON_3,
                               location=pyxb.utils.utility.Location(
                                   '../res/linguisticVariables.xsd', 12, 28)))


def _BuildAutomaton_3():
    # Remove this helper function from the namespace after it is invoked
    global _BuildAutomaton_3
    del _BuildAutomaton_3
    import pyxb.utils.fac as fac

    counters = set()
    states = []
    final_update = set()
    symbol = pyxb.binding.content.ElementUse(CTD_ANON_3._UseForTag(pyxb.namespace.ExpandedName(None, 'terms')),
                                             pyxb.utils.utility.Location(
                                                 '../res/linguisticVariables.xsd',
                                                 12, 28))
    st_0 = fac.State(symbol, is_initial=True, final_update=final_update, is_unordered_catenation=False)
    states.append(st_0)
    transitions = []
    st_0._set_transitionSet(transitions)
    return fac.Automaton(states, counters, False, containing_state=None)


CTD_ANON_3._Automaton = _BuildAutomaton_3()
