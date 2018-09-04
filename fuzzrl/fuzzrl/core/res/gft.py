# ./gft.py
# -*- coding: utf-8 -*-
# PyXB bindings for NM:e92452c8d3e28a9e27abfc9994d2007779e7f4c9
# Generated 2018-09-04 07:16:44.657175 by PyXB version 1.2.6 using Python 3.6.5.final.0
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
_GenerationUID = pyxb.utils.utility.UniqueIdentifier('urn:uuid:6c5d7ac0-afcf-11e8-a6e8-1c3e846a7922')

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

def CreateFromDocument (xml_text, default_namespace=None, location_base=None):
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

def CreateFromDOM (node, default_namespace=None):
    """Create a Python instance from the given DOM node.
    The node tag must correspond to an element declaration in this module.

    @deprecated: Forcing use of DOM interface is unnecessary; use L{CreateFromDocument}."""
    if default_namespace is None:
        default_namespace = Namespace.fallbackNamespace()
    return pyxb.binding.basis.element.AnyCreateFromDOM(node, default_namespace)


# List simple type: [anonymous]
# superclasses pyxb.binding.datatypes.anySimpleType
class STD_ANON (pyxb.binding.basis.STD_list):

    """Simple type that is a list of pyxb.binding.datatypes.float."""

    _ExpandedName = None
    _XSDLocation = pyxb.utils.utility.Location('/home/bbrighttaer/PycharmProjects/fuzzrl/fuzzrl/fuzzrl/core/res/gftlv0.1.1.xsd', 13, 32)
    _Documentation = None

    _ItemType = pyxb.binding.datatypes.float
STD_ANON._InitializeFacetMap()
_module_typeBindings.STD_ANON = STD_ANON

# List simple type: PartialChromOffsets
# superclasses pyxb.binding.datatypes.anySimpleType
class PartialChromOffsets (pyxb.binding.basis.STD_list):

    """Simple type that is a list of pyxb.binding.datatypes.int."""

    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'PartialChromOffsets')
    _XSDLocation = pyxb.utils.utility.Location('/home/bbrighttaer/PycharmProjects/fuzzrl/fuzzrl/fuzzrl/core/res/gftlv0.1.1.xsd', 46, 4)
    _Documentation = None

    _ItemType = pyxb.binding.datatypes.int
PartialChromOffsets._InitializeFacetMap()
Namespace.addCategoryObject('typeBinding', 'PartialChromOffsets', PartialChromOffsets)
_module_typeBindings.PartialChromOffsets = PartialChromOffsets

# Atomic simple type: outputTargetType
class outputTargetType (pyxb.binding.datatypes.string, pyxb.binding.basis.enumeration_mixin):

    """An atomic simple type."""

    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'outputTargetType')
    _XSDLocation = pyxb.utils.utility.Location('/home/bbrighttaer/PycharmProjects/fuzzrl/fuzzrl/fuzzrl/core/res/gftlv0.1.1.xsd', 68, 4)
    _Documentation = None
outputTargetType._CF_enumeration = pyxb.binding.facets.CF_enumeration(value_datatype=outputTargetType, enum_prefix=None)
outputTargetType.fis = outputTargetType._CF_enumeration.addEnumeration(unicode_value='fis', tag='fis')
outputTargetType.action = outputTargetType._CF_enumeration.addEnumeration(unicode_value='action', tag='action')
outputTargetType._InitializeFacetMap(outputTargetType._CF_enumeration)
Namespace.addCategoryObject('typeBinding', 'outputTargetType', outputTargetType)
_module_typeBindings.outputTargetType = outputTargetType

# Complex type [anonymous] with content type ELEMENT_ONLY
class CTD_ANON (pyxb.binding.basis.complexTypeDefinition):
    """Complex type [anonymous] with content type ELEMENT_ONLY"""
    _TypeDefinition = None
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_ELEMENT_ONLY
    _Abstract = False
    _ExpandedName = None
    _XSDLocation = pyxb.utils.utility.Location('/home/bbrighttaer/PycharmProjects/fuzzrl/fuzzrl/fuzzrl/core/res/gftlv0.1.1.xsd', 7, 8)
    _ElementMap = {}
    _AttributeMap = {}
    # Base type is pyxb.binding.datatypes.anyType
    
    # Element fuzzyInferenceSystem uses Python identifier fuzzyInferenceSystem
    __fuzzyInferenceSystem = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(None, 'fuzzyInferenceSystem'), 'fuzzyInferenceSystem', '__AbsentNamespace0_CTD_ANON_fuzzyInferenceSystem', True, pyxb.utils.utility.Location('/home/bbrighttaer/PycharmProjects/fuzzrl/fuzzrl/fuzzrl/core/res/gftlv0.1.1.xsd', 9, 16), )

    
    fuzzyInferenceSystem = property(__fuzzyInferenceSystem.value, __fuzzyInferenceSystem.set, None, None)

    
    # Attribute rootInfSystem uses Python identifier rootInfSystem
    __rootInfSystem = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'rootInfSystem'), 'rootInfSystem', '__AbsentNamespace0_CTD_ANON_rootInfSystem', pyxb.binding.datatypes.string, required=True)
    __rootInfSystem._DeclarationLocation = pyxb.utils.utility.Location('/home/bbrighttaer/PycharmProjects/fuzzrl/fuzzrl/fuzzrl/core/res/gftlv0.1.1.xsd', 43, 12)
    __rootInfSystem._UseLocation = pyxb.utils.utility.Location('/home/bbrighttaer/PycharmProjects/fuzzrl/fuzzrl/fuzzrl/core/res/gftlv0.1.1.xsd', 43, 12)
    
    rootInfSystem = property(__rootInfSystem.value, __rootInfSystem.set, None, None)

    _ElementMap.update({
        __fuzzyInferenceSystem.name() : __fuzzyInferenceSystem
    })
    _AttributeMap.update({
        __rootInfSystem.name() : __rootInfSystem
    })
_module_typeBindings.CTD_ANON = CTD_ANON


# Complex type [anonymous] with content type ELEMENT_ONLY
class CTD_ANON_ (pyxb.binding.basis.complexTypeDefinition):
    """Complex type [anonymous] with content type ELEMENT_ONLY"""
    _TypeDefinition = None
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_ELEMENT_ONLY
    _Abstract = False
    _ExpandedName = None
    _XSDLocation = pyxb.utils.utility.Location('/home/bbrighttaer/PycharmProjects/fuzzrl/fuzzrl/fuzzrl/core/res/gftlv0.1.1.xsd', 10, 20)
    _ElementMap = {}
    _AttributeMap = {}
    # Base type is pyxb.binding.datatypes.anyType
    
    # Element outputGeneRange uses Python identifier outputGeneRange
    __outputGeneRange = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(None, 'outputGeneRange'), 'outputGeneRange', '__AbsentNamespace0_CTD_ANON__outputGeneRange', False, pyxb.utils.utility.Location('/home/bbrighttaer/PycharmProjects/fuzzrl/fuzzrl/fuzzrl/core/res/gftlv0.1.1.xsd', 12, 28), )

    
    outputGeneRange = property(__outputGeneRange.value, __outputGeneRange.set, None, None)

    
    # Element rbSize uses Python identifier rbSize
    __rbSize = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(None, 'rbSize'), 'rbSize', '__AbsentNamespace0_CTD_ANON__rbSize', False, pyxb.utils.utility.Location('/home/bbrighttaer/PycharmProjects/fuzzrl/fuzzrl/fuzzrl/core/res/gftlv0.1.1.xsd', 17, 28), )

    
    rbSize = property(__rbSize.value, __rbSize.set, None, None)

    
    # Element mfSize uses Python identifier mfSize
    __mfSize = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(None, 'mfSize'), 'mfSize', '__AbsentNamespace0_CTD_ANON__mfSize', False, pyxb.utils.utility.Location('/home/bbrighttaer/PycharmProjects/fuzzrl/fuzzrl/fuzzrl/core/res/gftlv0.1.1.xsd', 18, 28), )

    
    mfSize = property(__mfSize.value, __mfSize.set, None, None)

    
    # Element position uses Python identifier position
    __position = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(None, 'position'), 'position', '__AbsentNamespace0_CTD_ANON__position', False, pyxb.utils.utility.Location('/home/bbrighttaer/PycharmProjects/fuzzrl/fuzzrl/fuzzrl/core/res/gftlv0.1.1.xsd', 19, 28), )

    
    position = property(__position.value, __position.set, None, None)

    
    # Element rbOffset uses Python identifier rbOffset
    __rbOffset = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(None, 'rbOffset'), 'rbOffset', '__AbsentNamespace0_CTD_ANON__rbOffset', False, pyxb.utils.utility.Location('/home/bbrighttaer/PycharmProjects/fuzzrl/fuzzrl/fuzzrl/core/res/gftlv0.1.1.xsd', 20, 28), )

    
    rbOffset = property(__rbOffset.value, __rbOffset.set, None, None)

    
    # Element mfOffset uses Python identifier mfOffset
    __mfOffset = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(None, 'mfOffset'), 'mfOffset', '__AbsentNamespace0_CTD_ANON__mfOffset', False, pyxb.utils.utility.Location('/home/bbrighttaer/PycharmProjects/fuzzrl/fuzzrl/fuzzrl/core/res/gftlv0.1.1.xsd', 21, 28), )

    
    mfOffset = property(__mfOffset.value, __mfOffset.set, None, None)

    
    # Element description uses Python identifier description
    __description = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(None, 'description'), 'description', '__AbsentNamespace0_CTD_ANON__description', False, pyxb.utils.utility.Location('/home/bbrighttaer/PycharmProjects/fuzzrl/fuzzrl/fuzzrl/core/res/gftlv0.1.1.xsd', 22, 28), )

    
    description = property(__description.value, __description.set, None, None)

    
    # Element inputVariables uses Python identifier inputVariables
    __inputVariables = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(None, 'inputVariables'), 'inputVariables', '__AbsentNamespace0_CTD_ANON__inputVariables', False, pyxb.utils.utility.Location('/home/bbrighttaer/PycharmProjects/fuzzrl/fuzzrl/fuzzrl/core/res/gftlv0.1.1.xsd', 23, 28), )

    
    inputVariables = property(__inputVariables.value, __inputVariables.set, None, None)

    
    # Element outputVariable uses Python identifier outputVariable
    __outputVariable = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(None, 'outputVariable'), 'outputVariable', '__AbsentNamespace0_CTD_ANON__outputVariable', False, pyxb.utils.utility.Location('/home/bbrighttaer/PycharmProjects/fuzzrl/fuzzrl/fuzzrl/core/res/gftlv0.1.1.xsd', 37, 28), )

    
    outputVariable = property(__outputVariable.value, __outputVariable.set, None, None)

    
    # Attribute name uses Python identifier name
    __name = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'name'), 'name', '__AbsentNamespace0_CTD_ANON__name', pyxb.binding.datatypes.anySimpleType, required=True)
    __name._DeclarationLocation = pyxb.utils.utility.Location('/home/bbrighttaer/PycharmProjects/fuzzrl/fuzzrl/fuzzrl/core/res/gftlv0.1.1.xsd', 39, 24)
    __name._UseLocation = pyxb.utils.utility.Location('/home/bbrighttaer/PycharmProjects/fuzzrl/fuzzrl/fuzzrl/core/res/gftlv0.1.1.xsd', 39, 24)
    
    name = property(__name.value, __name.set, None, None)

    _ElementMap.update({
        __outputGeneRange.name() : __outputGeneRange,
        __rbSize.name() : __rbSize,
        __mfSize.name() : __mfSize,
        __position.name() : __position,
        __rbOffset.name() : __rbOffset,
        __mfOffset.name() : __mfOffset,
        __description.name() : __description,
        __inputVariables.name() : __inputVariables,
        __outputVariable.name() : __outputVariable
    })
    _AttributeMap.update({
        __name.name() : __name
    })
_module_typeBindings.CTD_ANON_ = CTD_ANON_


# Complex type [anonymous] with content type ELEMENT_ONLY
class CTD_ANON_2 (pyxb.binding.basis.complexTypeDefinition):
    """Complex type [anonymous] with content type ELEMENT_ONLY"""
    _TypeDefinition = None
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_ELEMENT_ONLY
    _Abstract = False
    _ExpandedName = None
    _XSDLocation = pyxb.utils.utility.Location('/home/bbrighttaer/PycharmProjects/fuzzrl/fuzzrl/fuzzrl/core/res/gftlv0.1.1.xsd', 24, 32)
    _ElementMap = {}
    _AttributeMap = {}
    # Base type is pyxb.binding.datatypes.anyType
    
    # Element inputVar uses Python identifier inputVar
    __inputVar = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(None, 'inputVar'), 'inputVar', '__AbsentNamespace0_CTD_ANON_2_inputVar', True, pyxb.utils.utility.Location('/home/bbrighttaer/PycharmProjects/fuzzrl/fuzzrl/fuzzrl/core/res/gftlv0.1.1.xsd', 26, 40), )

    
    inputVar = property(__inputVar.value, __inputVar.set, None, None)

    _ElementMap.update({
        __inputVar.name() : __inputVar
    })
    _AttributeMap.update({
        
    })
_module_typeBindings.CTD_ANON_2 = CTD_ANON_2


# Complex type [anonymous] with content type ELEMENT_ONLY
class CTD_ANON_3 (pyxb.binding.basis.complexTypeDefinition):
    """Complex type [anonymous] with content type ELEMENT_ONLY"""
    _TypeDefinition = None
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_ELEMENT_ONLY
    _Abstract = False
    _ExpandedName = None
    _XSDLocation = pyxb.utils.utility.Location('/home/bbrighttaer/PycharmProjects/fuzzrl/fuzzrl/fuzzrl/core/res/gftlv0.1.1.xsd', 27, 44)
    _ElementMap = {}
    _AttributeMap = {}
    # Base type is pyxb.binding.datatypes.anyType
    
    # Element tune uses Python identifier tune
    __tune = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(None, 'tune'), 'tune', '__AbsentNamespace0_CTD_ANON_3_tune', False, pyxb.utils.utility.Location('/home/bbrighttaer/PycharmProjects/fuzzrl/fuzzrl/fuzzrl/core/res/gftlv0.1.1.xsd', 29, 52), )

    
    tune = property(__tune.value, __tune.set, None, None)

    
    # Element identity uses Python identifier identity
    __identity = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(None, 'identity'), 'identity', '__AbsentNamespace0_CTD_ANON_3_identity', False, pyxb.utils.utility.Location('/home/bbrighttaer/PycharmProjects/fuzzrl/fuzzrl/fuzzrl/core/res/gftlv0.1.1.xsd', 30, 52), )

    
    identity = property(__identity.value, __identity.set, None, None)

    _ElementMap.update({
        __tune.name() : __tune,
        __identity.name() : __identity
    })
    _AttributeMap.update({
        
    })
_module_typeBindings.CTD_ANON_3 = CTD_ANON_3


# Complex type OutputVariableTerm with content type ELEMENT_ONLY
class OutputVariableTerm (pyxb.binding.basis.complexTypeDefinition):
    """Complex type OutputVariableTerm with content type ELEMENT_ONLY"""
    _TypeDefinition = None
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_ELEMENT_ONLY
    _Abstract = False
    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'OutputVariableTerm')
    _XSDLocation = pyxb.utils.utility.Location('/home/bbrighttaer/PycharmProjects/fuzzrl/fuzzrl/fuzzrl/core/res/gftlv0.1.1.xsd', 49, 4)
    _ElementMap = {}
    _AttributeMap = {}
    # Base type is pyxb.binding.datatypes.anyType
    
    # Element term uses Python identifier term
    __term = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(None, 'term'), 'term', '__AbsentNamespace0_OutputVariableTerm_term', True, pyxb.utils.utility.Location('/home/bbrighttaer/PycharmProjects/fuzzrl/fuzzrl/fuzzrl/core/res/gftlv0.1.1.xsd', 51, 12), )

    
    term = property(__term.value, __term.set, None, None)

    
    # Attribute type uses Python identifier type
    __type = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'type'), 'type', '__AbsentNamespace0_OutputVariableTerm_type', pyxb.binding.datatypes.string, required=True)
    __type._DeclarationLocation = pyxb.utils.utility.Location('/home/bbrighttaer/PycharmProjects/fuzzrl/fuzzrl/fuzzrl/core/res/gftlv0.1.1.xsd', 66, 8)
    __type._UseLocation = pyxb.utils.utility.Location('/home/bbrighttaer/PycharmProjects/fuzzrl/fuzzrl/fuzzrl/core/res/gftlv0.1.1.xsd', 66, 8)
    
    type = property(__type.value, __type.set, None, None)

    _ElementMap.update({
        __term.name() : __term
    })
    _AttributeMap.update({
        __type.name() : __type
    })
_module_typeBindings.OutputVariableTerm = OutputVariableTerm
Namespace.addCategoryObject('typeBinding', 'OutputVariableTerm', OutputVariableTerm)


# Complex type [anonymous] with content type ELEMENT_ONLY
class CTD_ANON_4 (pyxb.binding.basis.complexTypeDefinition):
    """Complex type [anonymous] with content type ELEMENT_ONLY"""
    _TypeDefinition = None
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_ELEMENT_ONLY
    _Abstract = False
    _ExpandedName = None
    _XSDLocation = pyxb.utils.utility.Location('/home/bbrighttaer/PycharmProjects/fuzzrl/fuzzrl/fuzzrl/core/res/gftlv0.1.1.xsd', 52, 16)
    _ElementMap = {}
    _AttributeMap = {}
    # Base type is pyxb.binding.datatypes.anyType
    
    # Element successOpTitle uses Python identifier successOpTitle
    __successOpTitle = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(None, 'successOpTitle'), 'successOpTitle', '__AbsentNamespace0_CTD_ANON_4_successOpTitle', False, pyxb.utils.utility.Location('/home/bbrighttaer/PycharmProjects/fuzzrl/fuzzrl/fuzzrl/core/res/gftlv0.1.1.xsd', 54, 24), )

    
    successOpTitle = property(__successOpTitle.value, __successOpTitle.set, None, None)

    
    # Element target uses Python identifier target
    __target = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(None, 'target'), 'target', '__AbsentNamespace0_CTD_ANON_4_target', False, pyxb.utils.utility.Location('/home/bbrighttaer/PycharmProjects/fuzzrl/fuzzrl/fuzzrl/core/res/gftlv0.1.1.xsd', 55, 24), )

    
    target = property(__target.value, __target.set, None, None)

    
    # Attribute code uses Python identifier code
    __code = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'code'), 'code', '__AbsentNamespace0_CTD_ANON_4_code', pyxb.binding.datatypes.float, required=True)
    __code._DeclarationLocation = pyxb.utils.utility.Location('/home/bbrighttaer/PycharmProjects/fuzzrl/fuzzrl/fuzzrl/core/res/gftlv0.1.1.xsd', 62, 20)
    __code._UseLocation = pyxb.utils.utility.Location('/home/bbrighttaer/PycharmProjects/fuzzrl/fuzzrl/fuzzrl/core/res/gftlv0.1.1.xsd', 62, 20)
    
    code = property(__code.value, __code.set, None, None)

    _ElementMap.update({
        __successOpTitle.name() : __successOpTitle,
        __target.name() : __target
    })
    _AttributeMap.update({
        __code.name() : __code
    })
_module_typeBindings.CTD_ANON_4 = CTD_ANON_4


# Complex type varInfo with content type EMPTY
class varInfo (pyxb.binding.basis.complexTypeDefinition):
    """Complex type varInfo with content type EMPTY"""
    _TypeDefinition = None
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_EMPTY
    _Abstract = False
    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'varInfo')
    _XSDLocation = pyxb.utils.utility.Location('/home/bbrighttaer/PycharmProjects/fuzzrl/fuzzrl/fuzzrl/core/res/gftlv0.1.1.xsd', 74, 4)
    _ElementMap = {}
    _AttributeMap = {}
    # Base type is pyxb.binding.datatypes.anyType
    
    # Attribute name uses Python identifier name
    __name = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'name'), 'name', '__AbsentNamespace0_varInfo_name', pyxb.binding.datatypes.anySimpleType, required=True)
    __name._DeclarationLocation = pyxb.utils.utility.Location('/home/bbrighttaer/PycharmProjects/fuzzrl/fuzzrl/fuzzrl/core/res/gftlv0.1.1.xsd', 75, 8)
    __name._UseLocation = pyxb.utils.utility.Location('/home/bbrighttaer/PycharmProjects/fuzzrl/fuzzrl/fuzzrl/core/res/gftlv0.1.1.xsd', 75, 8)
    
    name = property(__name.value, __name.set, None, None)

    
    # Attribute type uses Python identifier type
    __type = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'type'), 'type', '__AbsentNamespace0_varInfo_type', pyxb.binding.datatypes.anySimpleType, required=True)
    __type._DeclarationLocation = pyxb.utils.utility.Location('/home/bbrighttaer/PycharmProjects/fuzzrl/fuzzrl/fuzzrl/core/res/gftlv0.1.1.xsd', 76, 8)
    __type._UseLocation = pyxb.utils.utility.Location('/home/bbrighttaer/PycharmProjects/fuzzrl/fuzzrl/fuzzrl/core/res/gftlv0.1.1.xsd', 76, 8)
    
    type = property(__type.value, __type.set, None, None)

    _ElementMap.update({
        
    })
    _AttributeMap.update({
        __name.name() : __name,
        __type.name() : __type
    })
_module_typeBindings.varInfo = varInfo
Namespace.addCategoryObject('typeBinding', 'varInfo', varInfo)


# Complex type [anonymous] with content type EMPTY
class CTD_ANON_5 (pyxb.binding.basis.complexTypeDefinition):
    """Complex type [anonymous] with content type EMPTY"""
    _TypeDefinition = None
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_EMPTY
    _Abstract = False
    _ExpandedName = None
    _XSDLocation = pyxb.utils.utility.Location('/home/bbrighttaer/PycharmProjects/fuzzrl/fuzzrl/fuzzrl/core/res/gftlv0.1.1.xsd', 56, 28)
    _ElementMap = {}
    _AttributeMap = {}
    # Base type is pyxb.binding.datatypes.anyType
    
    # Attribute targetType uses Python identifier targetType
    __targetType = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'targetType'), 'targetType', '__AbsentNamespace0_CTD_ANON_5_targetType', _module_typeBindings.outputTargetType)
    __targetType._DeclarationLocation = pyxb.utils.utility.Location('/home/bbrighttaer/PycharmProjects/fuzzrl/fuzzrl/fuzzrl/core/res/gftlv0.1.1.xsd', 57, 32)
    __targetType._UseLocation = pyxb.utils.utility.Location('/home/bbrighttaer/PycharmProjects/fuzzrl/fuzzrl/fuzzrl/core/res/gftlv0.1.1.xsd', 57, 32)
    
    targetType = property(__targetType.value, __targetType.set, None, None)

    
    # Attribute name uses Python identifier name
    __name = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'name'), 'name', '__AbsentNamespace0_CTD_ANON_5_name', pyxb.binding.datatypes.string, required=True)
    __name._DeclarationLocation = pyxb.utils.utility.Location('/home/bbrighttaer/PycharmProjects/fuzzrl/fuzzrl/fuzzrl/core/res/gftlv0.1.1.xsd', 58, 32)
    __name._UseLocation = pyxb.utils.utility.Location('/home/bbrighttaer/PycharmProjects/fuzzrl/fuzzrl/fuzzrl/core/res/gftlv0.1.1.xsd', 58, 32)
    
    name = property(__name.value, __name.set, None, None)

    _ElementMap.update({
        
    })
    _AttributeMap.update({
        __targetType.name() : __targetType,
        __name.name() : __name
    })
_module_typeBindings.CTD_ANON_5 = CTD_ANON_5


fuzzyInferenceSystems = pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'fuzzyInferenceSystems'), CTD_ANON, location=pyxb.utils.utility.Location('/home/bbrighttaer/PycharmProjects/fuzzrl/fuzzrl/fuzzrl/core/res/gftlv0.1.1.xsd', 6, 4))
Namespace.addCategoryObject('elementBinding', fuzzyInferenceSystems.name().localName(), fuzzyInferenceSystems)



CTD_ANON._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(None, 'fuzzyInferenceSystem'), CTD_ANON_, scope=CTD_ANON, location=pyxb.utils.utility.Location('/home/bbrighttaer/PycharmProjects/fuzzrl/fuzzrl/fuzzrl/core/res/gftlv0.1.1.xsd', 9, 16)))

def _BuildAutomaton ():
    # Remove this helper function from the namespace after it is invoked
    global _BuildAutomaton
    del _BuildAutomaton
    import pyxb.utils.fac as fac

    counters = set()
    states = []
    final_update = set()
    symbol = pyxb.binding.content.ElementUse(CTD_ANON._UseForTag(pyxb.namespace.ExpandedName(None, 'fuzzyInferenceSystem')), pyxb.utils.utility.Location('/home/bbrighttaer/PycharmProjects/fuzzrl/fuzzrl/fuzzrl/core/res/gftlv0.1.1.xsd', 9, 16))
    st_0 = fac.State(symbol, is_initial=True, final_update=final_update, is_unordered_catenation=False)
    states.append(st_0)
    transitions = []
    transitions.append(fac.Transition(st_0, [
         ]))
    st_0._set_transitionSet(transitions)
    return fac.Automaton(states, counters, False, containing_state=None)
CTD_ANON._Automaton = _BuildAutomaton()




CTD_ANON_._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(None, 'outputGeneRange'), STD_ANON, scope=CTD_ANON_, location=pyxb.utils.utility.Location('/home/bbrighttaer/PycharmProjects/fuzzrl/fuzzrl/fuzzrl/core/res/gftlv0.1.1.xsd', 12, 28)))

CTD_ANON_._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(None, 'rbSize'), pyxb.binding.datatypes.int, scope=CTD_ANON_, location=pyxb.utils.utility.Location('/home/bbrighttaer/PycharmProjects/fuzzrl/fuzzrl/fuzzrl/core/res/gftlv0.1.1.xsd', 17, 28)))

CTD_ANON_._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(None, 'mfSize'), pyxb.binding.datatypes.int, scope=CTD_ANON_, location=pyxb.utils.utility.Location('/home/bbrighttaer/PycharmProjects/fuzzrl/fuzzrl/fuzzrl/core/res/gftlv0.1.1.xsd', 18, 28)))

CTD_ANON_._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(None, 'position'), pyxb.binding.datatypes.int, scope=CTD_ANON_, location=pyxb.utils.utility.Location('/home/bbrighttaer/PycharmProjects/fuzzrl/fuzzrl/fuzzrl/core/res/gftlv0.1.1.xsd', 19, 28)))

CTD_ANON_._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(None, 'rbOffset'), PartialChromOffsets, scope=CTD_ANON_, location=pyxb.utils.utility.Location('/home/bbrighttaer/PycharmProjects/fuzzrl/fuzzrl/fuzzrl/core/res/gftlv0.1.1.xsd', 20, 28)))

CTD_ANON_._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(None, 'mfOffset'), PartialChromOffsets, scope=CTD_ANON_, location=pyxb.utils.utility.Location('/home/bbrighttaer/PycharmProjects/fuzzrl/fuzzrl/fuzzrl/core/res/gftlv0.1.1.xsd', 21, 28)))

CTD_ANON_._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(None, 'description'), pyxb.binding.datatypes.string, scope=CTD_ANON_, location=pyxb.utils.utility.Location('/home/bbrighttaer/PycharmProjects/fuzzrl/fuzzrl/fuzzrl/core/res/gftlv0.1.1.xsd', 22, 28)))

CTD_ANON_._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(None, 'inputVariables'), CTD_ANON_2, scope=CTD_ANON_, location=pyxb.utils.utility.Location('/home/bbrighttaer/PycharmProjects/fuzzrl/fuzzrl/fuzzrl/core/res/gftlv0.1.1.xsd', 23, 28)))

CTD_ANON_._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(None, 'outputVariable'), OutputVariableTerm, scope=CTD_ANON_, location=pyxb.utils.utility.Location('/home/bbrighttaer/PycharmProjects/fuzzrl/fuzzrl/fuzzrl/core/res/gftlv0.1.1.xsd', 37, 28)))

def _BuildAutomaton_ ():
    # Remove this helper function from the namespace after it is invoked
    global _BuildAutomaton_
    del _BuildAutomaton_
    import pyxb.utils.fac as fac

    counters = set()
    states = []
    final_update = None
    symbol = pyxb.binding.content.ElementUse(CTD_ANON_._UseForTag(pyxb.namespace.ExpandedName(None, 'outputGeneRange')), pyxb.utils.utility.Location('/home/bbrighttaer/PycharmProjects/fuzzrl/fuzzrl/fuzzrl/core/res/gftlv0.1.1.xsd', 12, 28))
    st_0 = fac.State(symbol, is_initial=True, final_update=final_update, is_unordered_catenation=False)
    states.append(st_0)
    final_update = None
    symbol = pyxb.binding.content.ElementUse(CTD_ANON_._UseForTag(pyxb.namespace.ExpandedName(None, 'rbSize')), pyxb.utils.utility.Location('/home/bbrighttaer/PycharmProjects/fuzzrl/fuzzrl/fuzzrl/core/res/gftlv0.1.1.xsd', 17, 28))
    st_1 = fac.State(symbol, is_initial=False, final_update=final_update, is_unordered_catenation=False)
    states.append(st_1)
    final_update = None
    symbol = pyxb.binding.content.ElementUse(CTD_ANON_._UseForTag(pyxb.namespace.ExpandedName(None, 'mfSize')), pyxb.utils.utility.Location('/home/bbrighttaer/PycharmProjects/fuzzrl/fuzzrl/fuzzrl/core/res/gftlv0.1.1.xsd', 18, 28))
    st_2 = fac.State(symbol, is_initial=False, final_update=final_update, is_unordered_catenation=False)
    states.append(st_2)
    final_update = None
    symbol = pyxb.binding.content.ElementUse(CTD_ANON_._UseForTag(pyxb.namespace.ExpandedName(None, 'position')), pyxb.utils.utility.Location('/home/bbrighttaer/PycharmProjects/fuzzrl/fuzzrl/fuzzrl/core/res/gftlv0.1.1.xsd', 19, 28))
    st_3 = fac.State(symbol, is_initial=False, final_update=final_update, is_unordered_catenation=False)
    states.append(st_3)
    final_update = None
    symbol = pyxb.binding.content.ElementUse(CTD_ANON_._UseForTag(pyxb.namespace.ExpandedName(None, 'rbOffset')), pyxb.utils.utility.Location('/home/bbrighttaer/PycharmProjects/fuzzrl/fuzzrl/fuzzrl/core/res/gftlv0.1.1.xsd', 20, 28))
    st_4 = fac.State(symbol, is_initial=False, final_update=final_update, is_unordered_catenation=False)
    states.append(st_4)
    final_update = None
    symbol = pyxb.binding.content.ElementUse(CTD_ANON_._UseForTag(pyxb.namespace.ExpandedName(None, 'mfOffset')), pyxb.utils.utility.Location('/home/bbrighttaer/PycharmProjects/fuzzrl/fuzzrl/fuzzrl/core/res/gftlv0.1.1.xsd', 21, 28))
    st_5 = fac.State(symbol, is_initial=False, final_update=final_update, is_unordered_catenation=False)
    states.append(st_5)
    final_update = None
    symbol = pyxb.binding.content.ElementUse(CTD_ANON_._UseForTag(pyxb.namespace.ExpandedName(None, 'description')), pyxb.utils.utility.Location('/home/bbrighttaer/PycharmProjects/fuzzrl/fuzzrl/fuzzrl/core/res/gftlv0.1.1.xsd', 22, 28))
    st_6 = fac.State(symbol, is_initial=False, final_update=final_update, is_unordered_catenation=False)
    states.append(st_6)
    final_update = None
    symbol = pyxb.binding.content.ElementUse(CTD_ANON_._UseForTag(pyxb.namespace.ExpandedName(None, 'inputVariables')), pyxb.utils.utility.Location('/home/bbrighttaer/PycharmProjects/fuzzrl/fuzzrl/fuzzrl/core/res/gftlv0.1.1.xsd', 23, 28))
    st_7 = fac.State(symbol, is_initial=False, final_update=final_update, is_unordered_catenation=False)
    states.append(st_7)
    final_update = set()
    symbol = pyxb.binding.content.ElementUse(CTD_ANON_._UseForTag(pyxb.namespace.ExpandedName(None, 'outputVariable')), pyxb.utils.utility.Location('/home/bbrighttaer/PycharmProjects/fuzzrl/fuzzrl/fuzzrl/core/res/gftlv0.1.1.xsd', 37, 28))
    st_8 = fac.State(symbol, is_initial=False, final_update=final_update, is_unordered_catenation=False)
    states.append(st_8)
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
    transitions.append(fac.Transition(st_7, [
         ]))
    st_6._set_transitionSet(transitions)
    transitions = []
    transitions.append(fac.Transition(st_8, [
         ]))
    st_7._set_transitionSet(transitions)
    transitions = []
    st_8._set_transitionSet(transitions)
    return fac.Automaton(states, counters, False, containing_state=None)
CTD_ANON_._Automaton = _BuildAutomaton_()




CTD_ANON_2._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(None, 'inputVar'), CTD_ANON_3, scope=CTD_ANON_2, location=pyxb.utils.utility.Location('/home/bbrighttaer/PycharmProjects/fuzzrl/fuzzrl/fuzzrl/core/res/gftlv0.1.1.xsd', 26, 40)))

def _BuildAutomaton_2 ():
    # Remove this helper function from the namespace after it is invoked
    global _BuildAutomaton_2
    del _BuildAutomaton_2
    import pyxb.utils.fac as fac

    counters = set()
    states = []
    final_update = set()
    symbol = pyxb.binding.content.ElementUse(CTD_ANON_2._UseForTag(pyxb.namespace.ExpandedName(None, 'inputVar')), pyxb.utils.utility.Location('/home/bbrighttaer/PycharmProjects/fuzzrl/fuzzrl/fuzzrl/core/res/gftlv0.1.1.xsd', 26, 40))
    st_0 = fac.State(symbol, is_initial=True, final_update=final_update, is_unordered_catenation=False)
    states.append(st_0)
    transitions = []
    transitions.append(fac.Transition(st_0, [
         ]))
    st_0._set_transitionSet(transitions)
    return fac.Automaton(states, counters, False, containing_state=None)
CTD_ANON_2._Automaton = _BuildAutomaton_2()




CTD_ANON_3._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(None, 'tune'), pyxb.binding.datatypes.boolean, scope=CTD_ANON_3, location=pyxb.utils.utility.Location('/home/bbrighttaer/PycharmProjects/fuzzrl/fuzzrl/fuzzrl/core/res/gftlv0.1.1.xsd', 29, 52)))

CTD_ANON_3._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(None, 'identity'), varInfo, scope=CTD_ANON_3, location=pyxb.utils.utility.Location('/home/bbrighttaer/PycharmProjects/fuzzrl/fuzzrl/fuzzrl/core/res/gftlv0.1.1.xsd', 30, 52)))

def _BuildAutomaton_3 ():
    # Remove this helper function from the namespace after it is invoked
    global _BuildAutomaton_3
    del _BuildAutomaton_3
    import pyxb.utils.fac as fac

    counters = set()
    states = []
    final_update = None
    symbol = pyxb.binding.content.ElementUse(CTD_ANON_3._UseForTag(pyxb.namespace.ExpandedName(None, 'tune')), pyxb.utils.utility.Location('/home/bbrighttaer/PycharmProjects/fuzzrl/fuzzrl/fuzzrl/core/res/gftlv0.1.1.xsd', 29, 52))
    st_0 = fac.State(symbol, is_initial=True, final_update=final_update, is_unordered_catenation=False)
    states.append(st_0)
    final_update = set()
    symbol = pyxb.binding.content.ElementUse(CTD_ANON_3._UseForTag(pyxb.namespace.ExpandedName(None, 'identity')), pyxb.utils.utility.Location('/home/bbrighttaer/PycharmProjects/fuzzrl/fuzzrl/fuzzrl/core/res/gftlv0.1.1.xsd', 30, 52))
    st_1 = fac.State(symbol, is_initial=False, final_update=final_update, is_unordered_catenation=False)
    states.append(st_1)
    transitions = []
    transitions.append(fac.Transition(st_1, [
         ]))
    st_0._set_transitionSet(transitions)
    transitions = []
    st_1._set_transitionSet(transitions)
    return fac.Automaton(states, counters, False, containing_state=None)
CTD_ANON_3._Automaton = _BuildAutomaton_3()




OutputVariableTerm._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(None, 'term'), CTD_ANON_4, scope=OutputVariableTerm, location=pyxb.utils.utility.Location('/home/bbrighttaer/PycharmProjects/fuzzrl/fuzzrl/fuzzrl/core/res/gftlv0.1.1.xsd', 51, 12)))

def _BuildAutomaton_4 ():
    # Remove this helper function from the namespace after it is invoked
    global _BuildAutomaton_4
    del _BuildAutomaton_4
    import pyxb.utils.fac as fac

    counters = set()
    states = []
    final_update = set()
    symbol = pyxb.binding.content.ElementUse(OutputVariableTerm._UseForTag(pyxb.namespace.ExpandedName(None, 'term')), pyxb.utils.utility.Location('/home/bbrighttaer/PycharmProjects/fuzzrl/fuzzrl/fuzzrl/core/res/gftlv0.1.1.xsd', 51, 12))
    st_0 = fac.State(symbol, is_initial=True, final_update=final_update, is_unordered_catenation=False)
    states.append(st_0)
    transitions = []
    transitions.append(fac.Transition(st_0, [
         ]))
    st_0._set_transitionSet(transitions)
    return fac.Automaton(states, counters, False, containing_state=None)
OutputVariableTerm._Automaton = _BuildAutomaton_4()




CTD_ANON_4._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(None, 'successOpTitle'), pyxb.binding.datatypes.string, scope=CTD_ANON_4, location=pyxb.utils.utility.Location('/home/bbrighttaer/PycharmProjects/fuzzrl/fuzzrl/fuzzrl/core/res/gftlv0.1.1.xsd', 54, 24)))

CTD_ANON_4._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(None, 'target'), CTD_ANON_5, scope=CTD_ANON_4, location=pyxb.utils.utility.Location('/home/bbrighttaer/PycharmProjects/fuzzrl/fuzzrl/fuzzrl/core/res/gftlv0.1.1.xsd', 55, 24)))

def _BuildAutomaton_5 ():
    # Remove this helper function from the namespace after it is invoked
    global _BuildAutomaton_5
    del _BuildAutomaton_5
    import pyxb.utils.fac as fac

    counters = set()
    cc_0 = fac.CounterCondition(min=0, max=1, metadata=pyxb.utils.utility.Location('/home/bbrighttaer/PycharmProjects/fuzzrl/fuzzrl/fuzzrl/core/res/gftlv0.1.1.xsd', 55, 24))
    counters.add(cc_0)
    states = []
    final_update = set()
    symbol = pyxb.binding.content.ElementUse(CTD_ANON_4._UseForTag(pyxb.namespace.ExpandedName(None, 'successOpTitle')), pyxb.utils.utility.Location('/home/bbrighttaer/PycharmProjects/fuzzrl/fuzzrl/fuzzrl/core/res/gftlv0.1.1.xsd', 54, 24))
    st_0 = fac.State(symbol, is_initial=True, final_update=final_update, is_unordered_catenation=False)
    states.append(st_0)
    final_update = set()
    final_update.add(fac.UpdateInstruction(cc_0, False))
    symbol = pyxb.binding.content.ElementUse(CTD_ANON_4._UseForTag(pyxb.namespace.ExpandedName(None, 'target')), pyxb.utils.utility.Location('/home/bbrighttaer/PycharmProjects/fuzzrl/fuzzrl/fuzzrl/core/res/gftlv0.1.1.xsd', 55, 24))
    st_1 = fac.State(symbol, is_initial=False, final_update=final_update, is_unordered_catenation=False)
    states.append(st_1)
    transitions = []
    transitions.append(fac.Transition(st_1, [
         ]))
    st_0._set_transitionSet(transitions)
    transitions = []
    transitions.append(fac.Transition(st_1, [
        fac.UpdateInstruction(cc_0, True) ]))
    st_1._set_transitionSet(transitions)
    return fac.Automaton(states, counters, False, containing_state=None)
CTD_ANON_4._Automaton = _BuildAutomaton_5()

