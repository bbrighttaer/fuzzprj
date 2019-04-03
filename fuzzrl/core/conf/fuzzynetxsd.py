# ./fuzzynetxsd.py
# -*- coding: utf-8 -*-
# PyXB bindings for NM:e92452c8d3e28a9e27abfc9994d2007779e7f4c9
# Generated 2018-09-13 18:03:36.276535 by PyXB version 1.2.6 using Python 3.6.4.final.0
# Namespace AbsentNamespace0

from __future__ import unicode_literals
import pyxb
import pyxb.binding
import pyxb.binding.saxer
import io
import pyxb.utils.utility
import pyxb.utils.domutils
import sys
import pyxb.utils.six as _six

# Unique identifier for bindings created at the same time
_GenerationUID = pyxb.utils.utility.UniqueIdentifier('urn:uuid:47a180b8-b73c-11e8-be4b-4439c4558c33')

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


# List simple type: [anonymous]
# superclasses pyxb.binding.datatypes.anySimpleType
class STD_ANON(pyxb.binding.basis.STD_list):
    """Simple type that is a list of pyxb.binding.datatypes.int."""

    _ExpandedName = None
    _XSDLocation = pyxb.utils.utility.Location(
        '/home/bbrighttaer/PycharmProjects/fuzzrl_pkg/fuzzrl/core/res/gftlv1.0.0.xsd', 21, 7)
    _Documentation = None

    _ItemType = pyxb.binding.datatypes.int


STD_ANON._InitializeFacetMap()
_module_typeBindings.STD_ANON = STD_ANON


# List simple type: PartialChromOffsets
# superclasses pyxb.binding.datatypes.anySimpleType
class PartialChromOffsets(pyxb.binding.basis.STD_list):
    """Simple type that is a list of pyxb.binding.datatypes.int."""

    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'PartialChromOffsets')
    _XSDLocation = pyxb.utils.utility.Location(
        '/home/bbrighttaer/PycharmProjects/fuzzrl_pkg/fuzzrl/core/res/gftlv1.0.0.xsd', 52, 1)
    _Documentation = None

    _ItemType = pyxb.binding.datatypes.int


PartialChromOffsets._InitializeFacetMap()
Namespace.addCategoryObject('typeBinding', 'PartialChromOffsets', PartialChromOffsets)
_module_typeBindings.PartialChromOffsets = PartialChromOffsets


# Atomic simple type: layerType
class layerType(pyxb.binding.datatypes.string, pyxb.binding.basis.enumeration_mixin):
    """An atomic simple type."""

    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'layerType')
    _XSDLocation = pyxb.utils.utility.Location(
        '/home/bbrighttaer/PycharmProjects/fuzzrl_pkg/fuzzrl/core/res/gftlv1.0.0.xsd', 66, 1)
    _Documentation = None


layerType._CF_enumeration = pyxb.binding.facets.CF_enumeration(value_datatype=layerType, enum_prefix=None)
layerType.input_layer = layerType._CF_enumeration.addEnumeration(unicode_value='input_layer', tag='input_layer')
layerType.hidden_layer = layerType._CF_enumeration.addEnumeration(unicode_value='hidden_layer', tag='hidden_layer')
layerType._InitializeFacetMap(layerType._CF_enumeration)
Namespace.addCategoryObject('typeBinding', 'layerType', layerType)
_module_typeBindings.layerType = layerType


# Atomic simple type: defuzz_method
class defuzz_method(pyxb.binding.datatypes.string, pyxb.binding.basis.enumeration_mixin):
    """An atomic simple type."""

    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'defuzz_method')
    _XSDLocation = pyxb.utils.utility.Location(
        '/home/bbrighttaer/PycharmProjects/fuzzrl_pkg/fuzzrl/core/res/gftlv1.0.0.xsd', 72, 1)
    _Documentation = None


defuzz_method._CF_enumeration = pyxb.binding.facets.CF_enumeration(value_datatype=defuzz_method, enum_prefix=None)
defuzz_method.lom = defuzz_method._CF_enumeration.addEnumeration(unicode_value='lom', tag='lom')
defuzz_method.centroid = defuzz_method._CF_enumeration.addEnumeration(unicode_value='centroid', tag='centroid')
defuzz_method.mom = defuzz_method._CF_enumeration.addEnumeration(unicode_value='mom', tag='mom')
defuzz_method.som = defuzz_method._CF_enumeration.addEnumeration(unicode_value='som', tag='som')
defuzz_method._InitializeFacetMap(defuzz_method._CF_enumeration)
Namespace.addCategoryObject('typeBinding', 'defuzz_method', defuzz_method)
_module_typeBindings.defuzz_method = defuzz_method


# Complex type [anonymous] with content type ELEMENT_ONLY
class CTD_ANON(pyxb.binding.basis.complexTypeDefinition):
    """Complex type [anonymous] with content type ELEMENT_ONLY"""
    _TypeDefinition = None
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_ELEMENT_ONLY
    _Abstract = False
    _ExpandedName = None
    _XSDLocation = pyxb.utils.utility.Location(
        '/home/bbrighttaer/PycharmProjects/fuzzrl_pkg/fuzzrl/core/res/gftlv1.0.0.xsd', 7, 2)
    _ElementMap = {}
    _AttributeMap = {}
    # Base type is pyxb.binding.datatypes.anyType

    # Element input uses Python identifier input
    __input = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(None, 'input'), 'input',
                                                      '__AbsentNamespace0_CTD_ANON_input', False,
                                                      pyxb.utils.utility.Location(
                                                          '/home/bbrighttaer/PycharmProjects/fuzzrl_pkg/fuzzrl/core/res/gftlv1.0.0.xsd',
                                                          9, 4), )

    input = property(__input.value, __input.set, None, None)

    # Element hidden uses Python identifier hidden
    __hidden = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(None, 'hidden'), 'hidden',
                                                       '__AbsentNamespace0_CTD_ANON_hidden', True,
                                                       pyxb.utils.utility.Location(
                                                           '/home/bbrighttaer/PycharmProjects/fuzzrl_pkg/fuzzrl/core/res/gftlv1.0.0.xsd',
                                                           10, 4), )

    hidden = property(__hidden.value, __hidden.set, None, None)

    # Element output uses Python identifier output
    __output = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(None, 'output'), 'output',
                                                       '__AbsentNamespace0_CTD_ANON_output', False,
                                                       pyxb.utils.utility.Location(
                                                           '/home/bbrighttaer/PycharmProjects/fuzzrl_pkg/fuzzrl/core/res/gftlv1.0.0.xsd',
                                                           11, 4), )

    output = property(__output.value, __output.set, None, None)

    _ElementMap.update({
        __input.name(): __input,
        __hidden.name(): __hidden,
        __output.name(): __output
    })
    _AttributeMap.update({

    })


_module_typeBindings.CTD_ANON = CTD_ANON


# Complex type layer with content type ELEMENT_ONLY
class layer(pyxb.binding.basis.complexTypeDefinition):
    """Complex type layer with content type ELEMENT_ONLY"""
    _TypeDefinition = None
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_ELEMENT_ONLY
    _Abstract = False
    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'layer')
    _XSDLocation = pyxb.utils.utility.Location(
        '/home/bbrighttaer/PycharmProjects/fuzzrl_pkg/fuzzrl/core/res/gftlv1.0.0.xsd', 15, 1)
    _ElementMap = {}
    _AttributeMap = {}
    # Base type is pyxb.binding.datatypes.anyType

    # Element fis uses Python identifier fis
    __fis = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(None, 'fis'), 'fis',
                                                    '__AbsentNamespace0_layer_fis', True, pyxb.utils.utility.Location(
            '/home/bbrighttaer/PycharmProjects/fuzzrl_pkg/fuzzrl/core/res/gftlv1.0.0.xsd', 17, 3), )

    fis = property(__fis.value, __fis.set, None, None)

    _ElementMap.update({
        __fis.name(): __fis
    })
    _AttributeMap.update({

    })


_module_typeBindings.layer = layer
Namespace.addCategoryObject('typeBinding', 'layer', layer)


# Complex type [anonymous] with content type ELEMENT_ONLY
class CTD_ANON_(pyxb.binding.basis.complexTypeDefinition):
    """Complex type [anonymous] with content type ELEMENT_ONLY"""
    _TypeDefinition = None
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_ELEMENT_ONLY
    _Abstract = False
    _ExpandedName = None
    _XSDLocation = pyxb.utils.utility.Location(
        '/home/bbrighttaer/PycharmProjects/fuzzrl_pkg/fuzzrl/core/res/gftlv1.0.0.xsd', 30, 7)
    _ElementMap = {}
    _AttributeMap = {}
    # Base type is pyxb.binding.datatypes.anyType

    # Element inputVar uses Python identifier inputVar
    __inputVar = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(None, 'inputVar'), 'inputVar',
                                                         '__AbsentNamespace0_CTD_ANON__inputVar', True,
                                                         pyxb.utils.utility.Location(
                                                             '/home/bbrighttaer/PycharmProjects/fuzzrl_pkg/fuzzrl/core/res/gftlv1.0.0.xsd',
                                                             32, 9), )

    inputVar = property(__inputVar.value, __inputVar.set, None, None)

    _ElementMap.update({
        __inputVar.name(): __inputVar
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
        '/home/bbrighttaer/PycharmProjects/fuzzrl_pkg/fuzzrl/core/res/gftlv1.0.0.xsd', 33, 10)
    _ElementMap = {}
    _AttributeMap = {}
    # Base type is pyxb.binding.datatypes.anyType

    # Element tune uses Python identifier tune
    __tune = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(None, 'tune'), 'tune',
                                                     '__AbsentNamespace0_CTD_ANON_2_tune', False,
                                                     pyxb.utils.utility.Location(
                                                         '/home/bbrighttaer/PycharmProjects/fuzzrl_pkg/fuzzrl/core/res/gftlv1.0.0.xsd',
                                                         35, 12), )

    tune = property(__tune.value, __tune.set, None, None)

    # Element identity uses Python identifier identity
    __identity = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(None, 'identity'), 'identity',
                                                         '__AbsentNamespace0_CTD_ANON_2_identity', False,
                                                         pyxb.utils.utility.Location(
                                                             '/home/bbrighttaer/PycharmProjects/fuzzrl_pkg/fuzzrl/core/res/gftlv1.0.0.xsd',
                                                             36, 12), )

    identity = property(__identity.value, __identity.set, None, None)

    # Element input_fis uses Python identifier input_fis
    __input_fis = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(None, 'input_fis'), 'input_fis',
                                                          '__AbsentNamespace0_CTD_ANON_2_input_fis', False,
                                                          pyxb.utils.utility.Location(
                                                              '/home/bbrighttaer/PycharmProjects/fuzzrl_pkg/fuzzrl/core/res/gftlv1.0.0.xsd',
                                                              37, 12), )

    input_fis = property(__input_fis.value, __input_fis.set, None, None)

    _ElementMap.update({
        __tune.name(): __tune,
        __identity.name(): __identity,
        __input_fis.name(): __input_fis
    })
    _AttributeMap.update({

    })


_module_typeBindings.CTD_ANON_2 = CTD_ANON_2


# Complex type OutputVariableTerm with content type ELEMENT_ONLY
class OutputVariableTerm(pyxb.binding.basis.complexTypeDefinition):
    """Complex type OutputVariableTerm with content type ELEMENT_ONLY"""
    _TypeDefinition = None
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_ELEMENT_ONLY
    _Abstract = False
    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'OutputVariableTerm')
    _XSDLocation = pyxb.utils.utility.Location(
        '/home/bbrighttaer/PycharmProjects/fuzzrl_pkg/fuzzrl/core/res/gftlv1.0.0.xsd', 55, 1)
    _ElementMap = {}
    _AttributeMap = {}
    # Base type is pyxb.binding.datatypes.anyType

    # Element term uses Python identifier term
    __term = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(None, 'term'), 'term',
                                                     '__AbsentNamespace0_OutputVariableTerm_term', True,
                                                     pyxb.utils.utility.Location(
                                                         '/home/bbrighttaer/PycharmProjects/fuzzrl_pkg/fuzzrl/core/res/gftlv1.0.0.xsd',
                                                         57, 3), )

    term = property(__term.value, __term.set, None, None)

    # Attribute type uses Python identifier type
    __type = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'type'), 'type',
                                               '__AbsentNamespace0_OutputVariableTerm_type',
                                               pyxb.binding.datatypes.string, required=True)
    __type._DeclarationLocation = pyxb.utils.utility.Location(
        '/home/bbrighttaer/PycharmProjects/fuzzrl_pkg/fuzzrl/core/res/gftlv1.0.0.xsd', 64, 2)
    __type._UseLocation = pyxb.utils.utility.Location(
        '/home/bbrighttaer/PycharmProjects/fuzzrl_pkg/fuzzrl/core/res/gftlv1.0.0.xsd', 64, 2)

    type = property(__type.value, __type.set, None, None)

    _ElementMap.update({
        __term.name(): __term
    })
    _AttributeMap.update({
        __type.name(): __type
    })


_module_typeBindings.OutputVariableTerm = OutputVariableTerm
Namespace.addCategoryObject('typeBinding', 'OutputVariableTerm', OutputVariableTerm)


# Complex type [anonymous] with content type EMPTY
class CTD_ANON_3(pyxb.binding.basis.complexTypeDefinition):
    """Complex type [anonymous] with content type EMPTY"""
    _TypeDefinition = None
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_EMPTY
    _Abstract = False
    _ExpandedName = None
    _XSDLocation = pyxb.utils.utility.Location(
        '/home/bbrighttaer/PycharmProjects/fuzzrl_pkg/fuzzrl/core/res/gftlv1.0.0.xsd', 58, 4)
    _ElementMap = {}
    _AttributeMap = {}
    # Base type is pyxb.binding.datatypes.anyType

    # Attribute label uses Python identifier label
    __label = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'label'), 'label',
                                                '__AbsentNamespace0_CTD_ANON_3_label', pyxb.binding.datatypes.string,
                                                required=True)
    __label._DeclarationLocation = pyxb.utils.utility.Location(
        '/home/bbrighttaer/PycharmProjects/fuzzrl_pkg/fuzzrl/core/res/gftlv1.0.0.xsd', 59, 5)
    __label._UseLocation = pyxb.utils.utility.Location(
        '/home/bbrighttaer/PycharmProjects/fuzzrl_pkg/fuzzrl/core/res/gftlv1.0.0.xsd', 59, 5)

    label = property(__label.value, __label.set, None, None)

    # Attribute code uses Python identifier code
    __code = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'code'), 'code',
                                               '__AbsentNamespace0_CTD_ANON_3_code', pyxb.binding.datatypes.int,
                                               required=True)
    __code._DeclarationLocation = pyxb.utils.utility.Location(
        '/home/bbrighttaer/PycharmProjects/fuzzrl_pkg/fuzzrl/core/res/gftlv1.0.0.xsd', 60, 5)
    __code._UseLocation = pyxb.utils.utility.Location(
        '/home/bbrighttaer/PycharmProjects/fuzzrl_pkg/fuzzrl/core/res/gftlv1.0.0.xsd', 60, 5)

    code = property(__code.value, __code.set, None, None)

    _ElementMap.update({

    })
    _AttributeMap.update({
        __label.name(): __label,
        __code.name(): __code
    })


_module_typeBindings.CTD_ANON_3 = CTD_ANON_3


# Complex type varInfo with content type EMPTY
class varInfo(pyxb.binding.basis.complexTypeDefinition):
    """Complex type varInfo with content type EMPTY"""
    _TypeDefinition = None
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_EMPTY
    _Abstract = False
    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'varInfo')
    _XSDLocation = pyxb.utils.utility.Location(
        '/home/bbrighttaer/PycharmProjects/fuzzrl_pkg/fuzzrl/core/res/gftlv1.0.0.xsd', 80, 1)
    _ElementMap = {}
    _AttributeMap = {}
    # Base type is pyxb.binding.datatypes.anyType

    # Attribute name uses Python identifier name
    __name = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'name'), 'name',
                                               '__AbsentNamespace0_varInfo_name', pyxb.binding.datatypes.anySimpleType,
                                               required=True)
    __name._DeclarationLocation = pyxb.utils.utility.Location(
        '/home/bbrighttaer/PycharmProjects/fuzzrl_pkg/fuzzrl/core/res/gftlv1.0.0.xsd', 81, 2)
    __name._UseLocation = pyxb.utils.utility.Location(
        '/home/bbrighttaer/PycharmProjects/fuzzrl_pkg/fuzzrl/core/res/gftlv1.0.0.xsd', 81, 2)

    name = property(__name.value, __name.set, None, None)

    # Attribute type uses Python identifier type
    __type = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'type'), 'type',
                                               '__AbsentNamespace0_varInfo_type', pyxb.binding.datatypes.anySimpleType,
                                               required=True)
    __type._DeclarationLocation = pyxb.utils.utility.Location(
        '/home/bbrighttaer/PycharmProjects/fuzzrl_pkg/fuzzrl/core/res/gftlv1.0.0.xsd', 82, 2)
    __type._UseLocation = pyxb.utils.utility.Location(
        '/home/bbrighttaer/PycharmProjects/fuzzrl_pkg/fuzzrl/core/res/gftlv1.0.0.xsd', 82, 2)

    type = property(__type.value, __type.set, None, None)

    _ElementMap.update({

    })
    _AttributeMap.update({
        __name.name(): __name,
        __type.name(): __type
    })


_module_typeBindings.varInfo = varInfo
Namespace.addCategoryObject('typeBinding', 'varInfo', varInfo)


# Complex type input_link with content type SIMPLE
class input_link(pyxb.binding.basis.complexTypeDefinition):
    """Complex type input_link with content type SIMPLE"""
    _TypeDefinition = pyxb.binding.datatypes.string
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_SIMPLE
    _Abstract = False
    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'input_link')
    _XSDLocation = pyxb.utils.utility.Location(
        '/home/bbrighttaer/PycharmProjects/fuzzrl_pkg/fuzzrl/core/res/gftlv1.0.0.xsd', 85, 1)
    _ElementMap = {}
    _AttributeMap = {}
    # Base type is pyxb.binding.datatypes.string

    # Attribute link uses Python identifier link
    __link = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'link'), 'link',
                                               '__AbsentNamespace0_input_link_link', pyxb.binding.datatypes.IDREF)
    __link._DeclarationLocation = pyxb.utils.utility.Location(
        '/home/bbrighttaer/PycharmProjects/fuzzrl_pkg/fuzzrl/core/res/gftlv1.0.0.xsd', 88, 4)
    __link._UseLocation = pyxb.utils.utility.Location(
        '/home/bbrighttaer/PycharmProjects/fuzzrl_pkg/fuzzrl/core/res/gftlv1.0.0.xsd', 88, 4)

    link = property(__link.value, __link.set, None, None)

    _ElementMap.update({

    })
    _AttributeMap.update({
        __link.name(): __link
    })


_module_typeBindings.input_link = input_link
Namespace.addCategoryObject('typeBinding', 'input_link', input_link)


# Complex type [anonymous] with content type ELEMENT_ONLY
class CTD_ANON_4(pyxb.binding.basis.complexTypeDefinition):
    """Complex type [anonymous] with content type ELEMENT_ONLY"""
    _TypeDefinition = None
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_ELEMENT_ONLY
    _Abstract = False
    _ExpandedName = None
    _XSDLocation = pyxb.utils.utility.Location(
        '/home/bbrighttaer/PycharmProjects/fuzzrl_pkg/fuzzrl/core/res/gftlv1.0.0.xsd', 18, 4)
    _ElementMap = {}
    _AttributeMap = {}
    # Base type is pyxb.binding.datatypes.anyType

    # Element outputGeneRange uses Python identifier outputGeneRange
    __outputGeneRange = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(None, 'outputGeneRange'),
                                                                'outputGeneRange',
                                                                '__AbsentNamespace0_CTD_ANON_4_outputGeneRange', False,
                                                                pyxb.utils.utility.Location(
                                                                    '/home/bbrighttaer/PycharmProjects/fuzzrl_pkg/fuzzrl/core/res/gftlv1.0.0.xsd',
                                                                    20, 6), )

    outputGeneRange = property(__outputGeneRange.value, __outputGeneRange.set, None, None)

    # Element rbSize uses Python identifier rbSize
    __rbSize = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(None, 'rbSize'), 'rbSize',
                                                       '__AbsentNamespace0_CTD_ANON_4_rbSize', False,
                                                       pyxb.utils.utility.Location(
                                                           '/home/bbrighttaer/PycharmProjects/fuzzrl_pkg/fuzzrl/core/res/gftlv1.0.0.xsd',
                                                           25, 6), )

    rbSize = property(__rbSize.value, __rbSize.set, None, None)

    # Element mfSize uses Python identifier mfSize
    __mfSize = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(None, 'mfSize'), 'mfSize',
                                                       '__AbsentNamespace0_CTD_ANON_4_mfSize', False,
                                                       pyxb.utils.utility.Location(
                                                           '/home/bbrighttaer/PycharmProjects/fuzzrl_pkg/fuzzrl/core/res/gftlv1.0.0.xsd',
                                                           26, 6), )

    mfSize = property(__mfSize.value, __mfSize.set, None, None)

    # Element position uses Python identifier position
    __position = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(None, 'position'), 'position',
                                                         '__AbsentNamespace0_CTD_ANON_4_position', False,
                                                         pyxb.utils.utility.Location(
                                                             '/home/bbrighttaer/PycharmProjects/fuzzrl_pkg/fuzzrl/core/res/gftlv1.0.0.xsd',
                                                             27, 6), )

    position = property(__position.value, __position.set, None, None)

    # Element description uses Python identifier description
    __description = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(None, 'description'),
                                                            'description', '__AbsentNamespace0_CTD_ANON_4_description',
                                                            False, pyxb.utils.utility.Location(
            '/home/bbrighttaer/PycharmProjects/fuzzrl_pkg/fuzzrl/core/res/gftlv1.0.0.xsd', 28, 6), )

    description = property(__description.value, __description.set, None, None)

    # Element inputVariables uses Python identifier inputVariables
    __inputVariables = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(None, 'inputVariables'),
                                                               'inputVariables',
                                                               '__AbsentNamespace0_CTD_ANON_4_inputVariables', False,
                                                               pyxb.utils.utility.Location(
                                                                   '/home/bbrighttaer/PycharmProjects/fuzzrl_pkg/fuzzrl/core/res/gftlv1.0.0.xsd',
                                                                   29, 6), )

    inputVariables = property(__inputVariables.value, __inputVariables.set, None, None)

    # Element outputVariable uses Python identifier outputVariable
    __outputVariable = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(None, 'outputVariable'),
                                                               'outputVariable',
                                                               '__AbsentNamespace0_CTD_ANON_4_outputVariable', False,
                                                               pyxb.utils.utility.Location(
                                                                   '/home/bbrighttaer/PycharmProjects/fuzzrl_pkg/fuzzrl/core/res/gftlv1.0.0.xsd',
                                                                   44, 6), )

    outputVariable = property(__outputVariable.value, __outputVariable.set, None, None)

    # Attribute name uses Python identifier name
    __name = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'name'), 'name',
                                               '__AbsentNamespace0_CTD_ANON_4_name', pyxb.binding.datatypes.ID,
                                               required=True)
    __name._DeclarationLocation = pyxb.utils.utility.Location(
        '/home/bbrighttaer/PycharmProjects/fuzzrl_pkg/fuzzrl/core/res/gftlv1.0.0.xsd', 46, 5)
    __name._UseLocation = pyxb.utils.utility.Location(
        '/home/bbrighttaer/PycharmProjects/fuzzrl_pkg/fuzzrl/core/res/gftlv1.0.0.xsd', 46, 5)

    name = property(__name.value, __name.set, None, None)

    # Attribute defuzz uses Python identifier defuzz
    __defuzz = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'defuzz'), 'defuzz',
                                                 '__AbsentNamespace0_CTD_ANON_4_defuzz',
                                                 _module_typeBindings.defuzz_method, required=True)
    __defuzz._DeclarationLocation = pyxb.utils.utility.Location(
        '/home/bbrighttaer/PycharmProjects/fuzzrl_pkg/fuzzrl/core/res/gftlv1.0.0.xsd', 47, 5)
    __defuzz._UseLocation = pyxb.utils.utility.Location(
        '/home/bbrighttaer/PycharmProjects/fuzzrl_pkg/fuzzrl/core/res/gftlv1.0.0.xsd', 47, 5)

    defuzz = property(__defuzz.value, __defuzz.set, None, None)

    _ElementMap.update({
        __outputGeneRange.name(): __outputGeneRange,
        __rbSize.name(): __rbSize,
        __mfSize.name(): __mfSize,
        __position.name(): __position,
        __description.name(): __description,
        __inputVariables.name(): __inputVariables,
        __outputVariable.name(): __outputVariable
    })
    _AttributeMap.update({
        __name.name(): __name,
        __defuzz.name(): __defuzz
    })


_module_typeBindings.CTD_ANON_4 = CTD_ANON_4

fuzzynet = pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'fuzzynet'), CTD_ANON,
                                      location=pyxb.utils.utility.Location(
                                          '/home/bbrighttaer/PycharmProjects/fuzzrl_pkg/fuzzrl/core/res/gftlv1.0.0.xsd',
                                          6, 1))
Namespace.addCategoryObject('elementBinding', fuzzynet.name().localName(), fuzzynet)

CTD_ANON._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(None, 'input'), layer, scope=CTD_ANON,
                                                location=pyxb.utils.utility.Location(
                                                    '/home/bbrighttaer/PycharmProjects/fuzzrl_pkg/fuzzrl/core/res/gftlv1.0.0.xsd',
                                                    9, 4)))

CTD_ANON._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(None, 'hidden'), layer, scope=CTD_ANON,
                                                location=pyxb.utils.utility.Location(
                                                    '/home/bbrighttaer/PycharmProjects/fuzzrl_pkg/fuzzrl/core/res/gftlv1.0.0.xsd',
                                                    10, 4)))

CTD_ANON._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(None, 'output'), layer, scope=CTD_ANON,
                                                location=pyxb.utils.utility.Location(
                                                    '/home/bbrighttaer/PycharmProjects/fuzzrl_pkg/fuzzrl/core/res/gftlv1.0.0.xsd',
                                                    11, 4)))


def _BuildAutomaton():
    # Remove this helper function from the namespace after it is invoked
    global _BuildAutomaton
    del _BuildAutomaton
    import pyxb.utils.fac as fac

    counters = set()
    cc_0 = fac.CounterCondition(min=0, max=1, metadata=pyxb.utils.utility.Location(
        '/home/bbrighttaer/PycharmProjects/fuzzrl_pkg/fuzzrl/core/res/gftlv1.0.0.xsd', 9, 4))
    counters.add(cc_0)
    cc_1 = fac.CounterCondition(min=0, max=None, metadata=pyxb.utils.utility.Location(
        '/home/bbrighttaer/PycharmProjects/fuzzrl_pkg/fuzzrl/core/res/gftlv1.0.0.xsd', 10, 4))
    counters.add(cc_1)
    states = []
    final_update = None
    symbol = pyxb.binding.content.ElementUse(CTD_ANON._UseForTag(pyxb.namespace.ExpandedName(None, 'input')),
                                             pyxb.utils.utility.Location(
                                                 '/home/bbrighttaer/PycharmProjects/fuzzrl_pkg/fuzzrl/core/res/gftlv1.0.0.xsd',
                                                 9, 4))
    st_0 = fac.State(symbol, is_initial=True, final_update=final_update, is_unordered_catenation=False)
    states.append(st_0)
    final_update = None
    symbol = pyxb.binding.content.ElementUse(CTD_ANON._UseForTag(pyxb.namespace.ExpandedName(None, 'hidden')),
                                             pyxb.utils.utility.Location(
                                                 '/home/bbrighttaer/PycharmProjects/fuzzrl_pkg/fuzzrl/core/res/gftlv1.0.0.xsd',
                                                 10, 4))
    st_1 = fac.State(symbol, is_initial=True, final_update=final_update, is_unordered_catenation=False)
    states.append(st_1)
    final_update = set()
    symbol = pyxb.binding.content.ElementUse(CTD_ANON._UseForTag(pyxb.namespace.ExpandedName(None, 'output')),
                                             pyxb.utils.utility.Location(
                                                 '/home/bbrighttaer/PycharmProjects/fuzzrl_pkg/fuzzrl/core/res/gftlv1.0.0.xsd',
                                                 11, 4))
    st_2 = fac.State(symbol, is_initial=True, final_update=final_update, is_unordered_catenation=False)
    states.append(st_2)
    transitions = []
    transitions.append(fac.Transition(st_0, [
        fac.UpdateInstruction(cc_0, True)]))
    transitions.append(fac.Transition(st_1, [
        fac.UpdateInstruction(cc_0, False)]))
    transitions.append(fac.Transition(st_2, [
        fac.UpdateInstruction(cc_0, False)]))
    st_0._set_transitionSet(transitions)
    transitions = []
    transitions.append(fac.Transition(st_1, [
        fac.UpdateInstruction(cc_1, True)]))
    transitions.append(fac.Transition(st_2, [
        fac.UpdateInstruction(cc_1, False)]))
    st_1._set_transitionSet(transitions)
    transitions = []
    st_2._set_transitionSet(transitions)
    return fac.Automaton(states, counters, False, containing_state=None)


CTD_ANON._Automaton = _BuildAutomaton()

layer._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(None, 'fis'), CTD_ANON_4, scope=layer,
                                             location=pyxb.utils.utility.Location(
                                                 '/home/bbrighttaer/PycharmProjects/fuzzrl_pkg/fuzzrl/core/res/gftlv1.0.0.xsd',
                                                 17, 3)))


def _BuildAutomaton_():
    # Remove this helper function from the namespace after it is invoked
    global _BuildAutomaton_
    del _BuildAutomaton_
    import pyxb.utils.fac as fac

    counters = set()
    states = []
    final_update = set()
    symbol = pyxb.binding.content.ElementUse(layer._UseForTag(pyxb.namespace.ExpandedName(None, 'fis')),
                                             pyxb.utils.utility.Location(
                                                 '/home/bbrighttaer/PycharmProjects/fuzzrl_pkg/fuzzrl/core/res/gftlv1.0.0.xsd',
                                                 17, 3))
    st_0 = fac.State(symbol, is_initial=True, final_update=final_update, is_unordered_catenation=False)
    states.append(st_0)
    transitions = []
    transitions.append(fac.Transition(st_0, [
    ]))
    st_0._set_transitionSet(transitions)
    return fac.Automaton(states, counters, False, containing_state=None)


layer._Automaton = _BuildAutomaton_()

CTD_ANON_._AddElement(
    pyxb.binding.basis.element(pyxb.namespace.ExpandedName(None, 'inputVar'), CTD_ANON_2, scope=CTD_ANON_,
                               location=pyxb.utils.utility.Location(
                                   '/home/bbrighttaer/PycharmProjects/fuzzrl_pkg/fuzzrl/core/res/gftlv1.0.0.xsd', 32,
                                   9)))


def _BuildAutomaton_2():
    # Remove this helper function from the namespace after it is invoked
    global _BuildAutomaton_2
    del _BuildAutomaton_2
    import pyxb.utils.fac as fac

    counters = set()
    states = []
    final_update = set()
    symbol = pyxb.binding.content.ElementUse(CTD_ANON_._UseForTag(pyxb.namespace.ExpandedName(None, 'inputVar')),
                                             pyxb.utils.utility.Location(
                                                 '/home/bbrighttaer/PycharmProjects/fuzzrl_pkg/fuzzrl/core/res/gftlv1.0.0.xsd',
                                                 32, 9))
    st_0 = fac.State(symbol, is_initial=True, final_update=final_update, is_unordered_catenation=False)
    states.append(st_0)
    transitions = []
    transitions.append(fac.Transition(st_0, [
    ]))
    st_0._set_transitionSet(transitions)
    return fac.Automaton(states, counters, False, containing_state=None)


CTD_ANON_._Automaton = _BuildAutomaton_2()

CTD_ANON_2._AddElement(
    pyxb.binding.basis.element(pyxb.namespace.ExpandedName(None, 'tune'), pyxb.binding.datatypes.boolean,
                               scope=CTD_ANON_2, location=pyxb.utils.utility.Location(
            '/home/bbrighttaer/PycharmProjects/fuzzrl_pkg/fuzzrl/core/res/gftlv1.0.0.xsd', 35, 12)))

CTD_ANON_2._AddElement(
    pyxb.binding.basis.element(pyxb.namespace.ExpandedName(None, 'identity'), varInfo, scope=CTD_ANON_2,
                               location=pyxb.utils.utility.Location(
                                   '/home/bbrighttaer/PycharmProjects/fuzzrl_pkg/fuzzrl/core/res/gftlv1.0.0.xsd', 36,
                                   12)))

CTD_ANON_2._AddElement(
    pyxb.binding.basis.element(pyxb.namespace.ExpandedName(None, 'input_fis'), input_link, scope=CTD_ANON_2,
                               location=pyxb.utils.utility.Location(
                                   '/home/bbrighttaer/PycharmProjects/fuzzrl_pkg/fuzzrl/core/res/gftlv1.0.0.xsd', 37,
                                   12)))


def _BuildAutomaton_3():
    # Remove this helper function from the namespace after it is invoked
    global _BuildAutomaton_3
    del _BuildAutomaton_3
    import pyxb.utils.fac as fac

    counters = set()
    cc_0 = fac.CounterCondition(min=0, max=1, metadata=pyxb.utils.utility.Location(
        '/home/bbrighttaer/PycharmProjects/fuzzrl_pkg/fuzzrl/core/res/gftlv1.0.0.xsd', 37, 12))
    counters.add(cc_0)
    states = []
    final_update = None
    symbol = pyxb.binding.content.ElementUse(CTD_ANON_2._UseForTag(pyxb.namespace.ExpandedName(None, 'tune')),
                                             pyxb.utils.utility.Location(
                                                 '/home/bbrighttaer/PycharmProjects/fuzzrl_pkg/fuzzrl/core/res/gftlv1.0.0.xsd',
                                                 35, 12))
    st_0 = fac.State(symbol, is_initial=True, final_update=final_update, is_unordered_catenation=False)
    states.append(st_0)
    final_update = set()
    symbol = pyxb.binding.content.ElementUse(CTD_ANON_2._UseForTag(pyxb.namespace.ExpandedName(None, 'identity')),
                                             pyxb.utils.utility.Location(
                                                 '/home/bbrighttaer/PycharmProjects/fuzzrl_pkg/fuzzrl/core/res/gftlv1.0.0.xsd',
                                                 36, 12))
    st_1 = fac.State(symbol, is_initial=False, final_update=final_update, is_unordered_catenation=False)
    states.append(st_1)
    final_update = set()
    final_update.add(fac.UpdateInstruction(cc_0, False))
    symbol = pyxb.binding.content.ElementUse(CTD_ANON_2._UseForTag(pyxb.namespace.ExpandedName(None, 'input_fis')),
                                             pyxb.utils.utility.Location(
                                                 '/home/bbrighttaer/PycharmProjects/fuzzrl_pkg/fuzzrl/core/res/gftlv1.0.0.xsd',
                                                 37, 12))
    st_2 = fac.State(symbol, is_initial=False, final_update=final_update, is_unordered_catenation=False)
    states.append(st_2)
    transitions = []
    transitions.append(fac.Transition(st_1, [
    ]))
    st_0._set_transitionSet(transitions)
    transitions = []
    transitions.append(fac.Transition(st_2, [
    ]))
    st_1._set_transitionSet(transitions)
    transitions = []
    transitions.append(fac.Transition(st_2, [
        fac.UpdateInstruction(cc_0, True)]))
    st_2._set_transitionSet(transitions)
    return fac.Automaton(states, counters, False, containing_state=None)


CTD_ANON_2._Automaton = _BuildAutomaton_3()

OutputVariableTerm._AddElement(
    pyxb.binding.basis.element(pyxb.namespace.ExpandedName(None, 'term'), CTD_ANON_3, scope=OutputVariableTerm,
                               location=pyxb.utils.utility.Location(
                                   '/home/bbrighttaer/PycharmProjects/fuzzrl_pkg/fuzzrl/core/res/gftlv1.0.0.xsd', 57,
                                   3)))


def _BuildAutomaton_4():
    # Remove this helper function from the namespace after it is invoked
    global _BuildAutomaton_4
    del _BuildAutomaton_4
    import pyxb.utils.fac as fac

    counters = set()
    states = []
    final_update = set()
    symbol = pyxb.binding.content.ElementUse(OutputVariableTerm._UseForTag(pyxb.namespace.ExpandedName(None, 'term')),
                                             pyxb.utils.utility.Location(
                                                 '/home/bbrighttaer/PycharmProjects/fuzzrl_pkg/fuzzrl/core/res/gftlv1.0.0.xsd',
                                                 57, 3))
    st_0 = fac.State(symbol, is_initial=True, final_update=final_update, is_unordered_catenation=False)
    states.append(st_0)
    transitions = []
    transitions.append(fac.Transition(st_0, [
    ]))
    st_0._set_transitionSet(transitions)
    return fac.Automaton(states, counters, False, containing_state=None)


OutputVariableTerm._Automaton = _BuildAutomaton_4()

CTD_ANON_4._AddElement(
    pyxb.binding.basis.element(pyxb.namespace.ExpandedName(None, 'outputGeneRange'), STD_ANON, scope=CTD_ANON_4,
                               location=pyxb.utils.utility.Location(
                                   '/home/bbrighttaer/PycharmProjects/fuzzrl_pkg/fuzzrl/core/res/gftlv1.0.0.xsd', 20,
                                   6)))

CTD_ANON_4._AddElement(
    pyxb.binding.basis.element(pyxb.namespace.ExpandedName(None, 'rbSize'), pyxb.binding.datatypes.int,
                               scope=CTD_ANON_4, location=pyxb.utils.utility.Location(
            '/home/bbrighttaer/PycharmProjects/fuzzrl_pkg/fuzzrl/core/res/gftlv1.0.0.xsd', 25, 6)))

CTD_ANON_4._AddElement(
    pyxb.binding.basis.element(pyxb.namespace.ExpandedName(None, 'mfSize'), pyxb.binding.datatypes.int,
                               scope=CTD_ANON_4, location=pyxb.utils.utility.Location(
            '/home/bbrighttaer/PycharmProjects/fuzzrl_pkg/fuzzrl/core/res/gftlv1.0.0.xsd', 26, 6)))

CTD_ANON_4._AddElement(
    pyxb.binding.basis.element(pyxb.namespace.ExpandedName(None, 'position'), pyxb.binding.datatypes.int,
                               scope=CTD_ANON_4, location=pyxb.utils.utility.Location(
            '/home/bbrighttaer/PycharmProjects/fuzzrl_pkg/fuzzrl/core/res/gftlv1.0.0.xsd', 27, 6)))

CTD_ANON_4._AddElement(
    pyxb.binding.basis.element(pyxb.namespace.ExpandedName(None, 'description'), pyxb.binding.datatypes.string,
                               scope=CTD_ANON_4, location=pyxb.utils.utility.Location(
            '/home/bbrighttaer/PycharmProjects/fuzzrl_pkg/fuzzrl/core/res/gftlv1.0.0.xsd', 28, 6)))

CTD_ANON_4._AddElement(
    pyxb.binding.basis.element(pyxb.namespace.ExpandedName(None, 'inputVariables'), CTD_ANON_, scope=CTD_ANON_4,
                               location=pyxb.utils.utility.Location(
                                   '/home/bbrighttaer/PycharmProjects/fuzzrl_pkg/fuzzrl/core/res/gftlv1.0.0.xsd', 29,
                                   6)))

CTD_ANON_4._AddElement(
    pyxb.binding.basis.element(pyxb.namespace.ExpandedName(None, 'outputVariable'), OutputVariableTerm,
                               scope=CTD_ANON_4, location=pyxb.utils.utility.Location(
            '/home/bbrighttaer/PycharmProjects/fuzzrl_pkg/fuzzrl/core/res/gftlv1.0.0.xsd', 44, 6)))


def _BuildAutomaton_5():
    # Remove this helper function from the namespace after it is invoked
    global _BuildAutomaton_5
    del _BuildAutomaton_5
    import pyxb.utils.fac as fac

    counters = set()
    states = []
    final_update = None
    symbol = pyxb.binding.content.ElementUse(
        CTD_ANON_4._UseForTag(pyxb.namespace.ExpandedName(None, 'outputGeneRange')),
        pyxb.utils.utility.Location('/home/bbrighttaer/PycharmProjects/fuzzrl_pkg/fuzzrl/core/res/gftlv1.0.0.xsd', 20,
                                    6))
    st_0 = fac.State(symbol, is_initial=True, final_update=final_update, is_unordered_catenation=False)
    states.append(st_0)
    final_update = None
    symbol = pyxb.binding.content.ElementUse(CTD_ANON_4._UseForTag(pyxb.namespace.ExpandedName(None, 'rbSize')),
                                             pyxb.utils.utility.Location(
                                                 '/home/bbrighttaer/PycharmProjects/fuzzrl_pkg/fuzzrl/core/res/gftlv1.0.0.xsd',
                                                 25, 6))
    st_1 = fac.State(symbol, is_initial=False, final_update=final_update, is_unordered_catenation=False)
    states.append(st_1)
    final_update = None
    symbol = pyxb.binding.content.ElementUse(CTD_ANON_4._UseForTag(pyxb.namespace.ExpandedName(None, 'mfSize')),
                                             pyxb.utils.utility.Location(
                                                 '/home/bbrighttaer/PycharmProjects/fuzzrl_pkg/fuzzrl/core/res/gftlv1.0.0.xsd',
                                                 26, 6))
    st_2 = fac.State(symbol, is_initial=False, final_update=final_update, is_unordered_catenation=False)
    states.append(st_2)
    final_update = None
    symbol = pyxb.binding.content.ElementUse(CTD_ANON_4._UseForTag(pyxb.namespace.ExpandedName(None, 'position')),
                                             pyxb.utils.utility.Location(
                                                 '/home/bbrighttaer/PycharmProjects/fuzzrl_pkg/fuzzrl/core/res/gftlv1.0.0.xsd',
                                                 27, 6))
    st_3 = fac.State(symbol, is_initial=False, final_update=final_update, is_unordered_catenation=False)
    states.append(st_3)
    final_update = None
    symbol = pyxb.binding.content.ElementUse(CTD_ANON_4._UseForTag(pyxb.namespace.ExpandedName(None, 'description')),
                                             pyxb.utils.utility.Location(
                                                 '/home/bbrighttaer/PycharmProjects/fuzzrl_pkg/fuzzrl/core/res/gftlv1.0.0.xsd',
                                                 28, 6))
    st_4 = fac.State(symbol, is_initial=False, final_update=final_update, is_unordered_catenation=False)
    states.append(st_4)
    final_update = None
    symbol = pyxb.binding.content.ElementUse(CTD_ANON_4._UseForTag(pyxb.namespace.ExpandedName(None, 'inputVariables')),
                                             pyxb.utils.utility.Location(
                                                 '/home/bbrighttaer/PycharmProjects/fuzzrl_pkg/fuzzrl/core/res/gftlv1.0.0.xsd',
                                                 29, 6))
    st_5 = fac.State(symbol, is_initial=False, final_update=final_update, is_unordered_catenation=False)
    states.append(st_5)
    final_update = set()
    symbol = pyxb.binding.content.ElementUse(CTD_ANON_4._UseForTag(pyxb.namespace.ExpandedName(None, 'outputVariable')),
                                             pyxb.utils.utility.Location(
                                                 '/home/bbrighttaer/PycharmProjects/fuzzrl_pkg/fuzzrl/core/res/gftlv1.0.0.xsd',
                                                 44, 6))
    st_6 = fac.State(symbol, is_initial=False, final_update=final_update, is_unordered_catenation=False)
    states.append(st_6)
    transitions = []
    transitions.append(fac.Transition(st_1, [
    ]))
    st_0._set_transitionSet(transitions)
    transitions = []
    transitions.append(fac.Transition(st_2, [
    ]))
    st_1._set_transitionSet(transitions)
    transitions = []
    transitions.append(fac.Transition(st_3, [
    ]))
    st_2._set_transitionSet(transitions)
    transitions = []
    transitions.append(fac.Transition(st_4, [
    ]))
    st_3._set_transitionSet(transitions)
    transitions = []
    transitions.append(fac.Transition(st_5, [
    ]))
    st_4._set_transitionSet(transitions)
    transitions = []
    transitions.append(fac.Transition(st_6, [
    ]))
    st_5._set_transitionSet(transitions)
    transitions = []
    st_6._set_transitionSet(transitions)
    return fac.Automaton(states, counters, False, containing_state=None)


CTD_ANON_4._Automaton = _BuildAutomaton_5()
