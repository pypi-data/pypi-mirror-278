from typing import List
from typing import overload
import ghidra.app.util.bin.format.dwarf
import ghidra.app.util.bin.format.dwarf.attribs
import java.lang


class DIEAggregate(object):
    """
    DIEAggregate groups related DebugInfoEntry records together in a single interface
     for querying attribute values.
 
     Information about program elements are written into the .debug_info as partial snapshots
     of the element, with later follow-up records that more fully specify the program element.
 
     (For instance, a declaration-only DIE that introduces the name of a structure type
     will be found at the beginning of a compilation unit, followed later by a DIE that
     specifies the contents of the structure type)
 
     A DIEAggregate groups these DebugInfoEntry records under one interface so a fully
     specified view of the program element can be presented.
    """









    @staticmethod
    def createFromHead(die: ghidra.app.util.bin.format.dwarf.DebugInfoEntry) -> ghidra.app.util.bin.format.dwarf.DIEAggregate:
        """
        Creates a {@link DIEAggregate} starting from a 'head' {@link DebugInfoEntry} instance.
         <p>
         DW_AT_abstract_origin and DW_AT_specification attributes are followed to find the previous
         {@link DebugInfoEntry} instances.
         <p>
        @param die starting DIE record
        @return new {@link DIEAggregate} made up of the starting DIE and all DIEs that it points
         to via abstract_origin and spec attributes.
        """
        ...

    @staticmethod
    def createSingle(die: ghidra.app.util.bin.format.dwarf.DebugInfoEntry) -> ghidra.app.util.bin.format.dwarf.DIEAggregate:
        """
        Create a {@link DIEAggregate} from a single {@link DebugInfoEntry DIE}.
         <p>
         Mainly useful early in the {@link DWARFCompilationUnit}'s bootstrapping process
         when it needs to read values from DIEs.
         <p>
        @param die {@link DebugInfoEntry}
        @return {@link DIEAggregate} containing a single DIE
        """
        ...

    @staticmethod
    def createSkipHead(source: ghidra.app.util.bin.format.dwarf.DIEAggregate) -> ghidra.app.util.bin.format.dwarf.DIEAggregate:
        """
        Creates a new {@link DIEAggregate} from the contents of the specified DIEA, using
         all the source's {@link DebugInfoEntry} fragments except for the head fragment
         which is skipped.
         <p>
         Used when a DIEA is composed of a head DIE with a different TAG type than the rest of
         the DIEs.  (ie. a dw_tag_call_site -&gt; dw_tag_sub DIEA)
        @param source {@link DIEAggregate} containing fragments
        @return {@link DIEAggregate} with the fragments of the source, skipping the first
        """
        ...

    def equals(self, obj: object) -> bool: ...

    def findAttributeInChildren(self, attribute: ghidra.app.util.bin.format.dwarf.attribs.DWARFAttribute, childTag: ghidra.app.util.bin.format.dwarf.DWARFTag, clazz: java.lang.Class) -> object:
        """
        Return an attribute that is present in this {@link DIEAggregate}, or in any of its
         direct children (of a specific type)
        @param <T> attribute value type
        @param attribute the attribute to find
        @param childTag the type of children to search
        @param clazz type of the attribute to return
        @return attribute value, or null if not found
        """
        ...

    def getAbstractInstance(self) -> ghidra.app.util.bin.format.dwarf.DIEAggregate:
        """
        Return a {@link DIEAggregate} that only contains the information present in the
         "abstract instance" (and lower) DIEs.
        @return a new {@link DIEAggregate}, or null if this DIEA was not split into a concrete and
         abstract portion
        """
        ...

    @overload
    def getAttribute(self, attribute: ghidra.app.util.bin.format.dwarf.attribs.DWARFAttribute) -> ghidra.app.util.bin.format.dwarf.attribs.DWARFAttributeValue:
        """
        Finds a {@link DWARFAttributeValue attribute} with a matching {@link DWARFAttribute} id.
         <p>
         Returns null if the attribute does not exist.
         <p>
         Attributes are searched for in each fragment in this aggregate, starting with the
         'head' fragment, progressing toward the 'decl' fragment.
         <p>
        @param attribute See {@link DWARFAttribute}
        @return DWARFAttributeValue, or null if not found
        """
        ...

    @overload
    def getAttribute(self, attribute: ghidra.app.util.bin.format.dwarf.attribs.DWARFAttribute, clazz: java.lang.Class) -> object:
        """
        Finds a {@link DWARFAttributeValue attribute} with a matching {@link DWARFAttribute} id.
         <p>
         Returns null if the attribute does not exist or is wrong java class type.
         <p>
         Attributes are searched for in each fragment in this aggregate, starting with the
         'head' fragment, progressing toward the 'decl' fragment.
         <p>
        @param attribute See {@link DWARFAttribute}
        @param clazz must be derived from {@link DWARFAttributeValue}
        @return DWARFAttributeValue or subclass as specified by the clazz, or null if not found
        """
        ...

    def getBool(self, attribute: ghidra.app.util.bin.format.dwarf.attribs.DWARFAttribute, defaultValue: bool) -> bool:
        """
        Returns the boolean value of the requested attribute, or -defaultValue- if
         the attribute is missing or not the correct type.
         <p>
        @param attribute {@link DWARFAttribute} id
        @param defaultValue value to return if attribute is not present
        @return boolean value, or the defaultValue if attribute is not present
        """
        ...

    def getChildren(self, childTag: ghidra.app.util.bin.format.dwarf.DWARFTag) -> List[ghidra.app.util.bin.format.dwarf.DebugInfoEntry]:
        """
        Return a list of children that are of a specific DWARF type.
         <p>
        @param childTag see {@link DWARFTag DWARFTag DW_TAG_* values}
        @return List of children DIEs that match the specified tag
        """
        ...

    def getClass(self) -> java.lang.Class: ...

    def getCompilationUnit(self) -> ghidra.app.util.bin.format.dwarf.DWARFCompilationUnit: ...

    def getContainingTypeRef(self) -> ghidra.app.util.bin.format.dwarf.DIEAggregate:
        """
        Returns the DIE pointed to by a DW_AT_containing_type attribute.
        @return DIEA pointed to by the DW_AT_containing_type attribute, or null if not present.
        """
        ...

    def getDeclOffset(self) -> long: ...

    def getDeclParent(self) -> ghidra.app.util.bin.format.dwarf.DIEAggregate: ...

    def getDepth(self) -> int:
        """
        Returns the depth of the head fragment, where depth is defined as
         the distance between the DIE and the root DIE of the owning compilation
         unit.
         <p>
         The root die would return 0, the children of the root will return 1, etc.
         <p>
         This value matches the nesting value shown when dumping DWARF
         info using 'readelf'.
        @return depth of this instance, from the root of its head DIE fragment, with 0 indicating
         that this instance was already the root of the compUnit
        """
        ...

    def getFragmentCount(self) -> int: ...

    def getFunctionParamList(self) -> List[ghidra.app.util.bin.format.dwarf.DIEAggregate]:
        """
        Returns a function's parameter list, taking care to ensure that the params
         are well ordered (to avoid issues with concrete instance param ordering)
        @return list of params for this function
        """
        ...

    def getHeadFragment(self) -> ghidra.app.util.bin.format.dwarf.DebugInfoEntry:
        """
        Returns the first {@link DebugInfoEntry DIE} fragment, ie. the spec or abstract_origin
         DIE.
        @return first DIE of this aggregate
        """
        ...

    def getHexOffset(self) -> unicode:
        """
        Returns {@link #getOffset()} as a hex string.
        @return string hex offset of the head DIE
        """
        ...

    def getLastFragment(self) -> ghidra.app.util.bin.format.dwarf.DebugInfoEntry:
        """
        Returns the last {@link DebugInfoEntry DIE} fragment, ie. the decl DIE.
        @return last DIE of this aggregate
        """
        ...

    def getLocation(self, attribute: ghidra.app.util.bin.format.dwarf.attribs.DWARFAttribute, pc: long) -> ghidra.app.util.bin.format.dwarf.DWARFLocation:
        """
        Parses a location attribute value, and returns the {@link DWARFLocation} instance that
         covers the specified pc.
        @param attribute typically {@link DWARFAttribute#DW_AT_location}
        @param pc program counter
        @return a {@link DWARFLocationList}, never null, possibly empty
        @throws IOException if error reading data
        """
        ...

    def getLocationList(self, attribute: ghidra.app.util.bin.format.dwarf.attribs.DWARFAttribute) -> ghidra.app.util.bin.format.dwarf.DWARFLocationList:
        """
        Parses a location attribute value, which can be a single expression that is valid for any
         PC, or a list of expressions that are tied to specific ranges.
        @param attribute typically {@link DWARFAttribute#DW_AT_location}
        @return a {@link DWARFLocationList}, never null, possibly empty
        @throws IOException if error reading data
        """
        ...

    def getLong(self, attribute: ghidra.app.util.bin.format.dwarf.attribs.DWARFAttribute, defaultValue: long) -> long:
        """
        Returns the value of the requested attribute, or -defaultValue- if the
         attribute is missing.
        @param attribute {@link DWARFAttribute} id
        @param defaultValue value to return if attribute is not present
        @return long value, or the defaultValue if attribute not present
        """
        ...

    def getName(self) -> unicode:
        """
        Returns the string value of the {@link DWARFAttribute#DW_AT_name dw_at_name} attribute,
         or null if it is missing.
         <p>
        @return name of this DIE aggregate, or null if missing
        """
        ...

    def getOffset(self) -> long: ...

    def getOffsets(self) -> List[long]: ...

    def getPCRange(self) -> ghidra.app.util.bin.format.dwarf.DWARFRange:
        """
        Return the range specified by the low_pc...high_pc attribute values.
        @return {@link DWARFRange} containing low_pc - high_pc, or empty range if the low_pc is 
         not present
        """
        ...

    def getParent(self) -> ghidra.app.util.bin.format.dwarf.DIEAggregate: ...

    def getProgram(self) -> ghidra.app.util.bin.format.dwarf.DWARFProgram: ...

    def getRangeList(self, attribute: ghidra.app.util.bin.format.dwarf.attribs.DWARFAttribute) -> ghidra.app.util.bin.format.dwarf.DWARFRangeList:
        """
        Parses a range list.
        @param attribute attribute eg {@link DWARFAttribute#DW_AT_ranges}
        @return list of ranges, or null if attribute is not present
        @throws IOException if an I/O error occurs
        """
        ...

    def getRef(self, attribute: ghidra.app.util.bin.format.dwarf.attribs.DWARFAttribute) -> ghidra.app.util.bin.format.dwarf.DIEAggregate:
        """
        Returns the {@link DIEAggregate diea} instance pointed to by the requested attribute,
         or null if the attribute does not exist.
         <p>
        @param attribute {@link DWARFAttribute} id
        @return {@link DIEAggregate}, or the null if attribute is not present
        """
        ...

    def getSourceFile(self) -> unicode:
        """
        Returns the name of the source file this item was declared in (DW_AT_decl_file)
        @return name of file this item was declared in, or null if info not available
        """
        ...

    def getString(self, attribute: ghidra.app.util.bin.format.dwarf.attribs.DWARFAttribute, defaultValue: unicode) -> unicode:
        """
        Returns the string value of the requested attribute, or -defaultValue- if
         the attribute is missing or not the correct type.
         <p>
        @param attribute {@link DWARFAttribute} id
        @param defaultValue value to return if attribute is not present
        @return String value, or the defaultValue if attribute is not present
        """
        ...

    def getTag(self) -> ghidra.app.util.bin.format.dwarf.DWARFTag: ...

    def getTypeRef(self) -> ghidra.app.util.bin.format.dwarf.DIEAggregate: ...

    def getUnsignedLong(self, attribute: ghidra.app.util.bin.format.dwarf.attribs.DWARFAttribute, defaultValue: long) -> long:
        """
        Returns the unsigned long integer value of the requested attribute, or -defaultValue-
         if the attribute is missing.
         <p>
         The 'unsigned'ness of this method refers to how the binary value is read from
         the dwarf information (ie. a value with the high bit set is not treated as signed).
         <p>
         The -defaultValue- parameter can accept a negative value.
        @param attribute {@link DWARFAttribute} id
        @param defaultValue value to return if attribute is not present
        @return unsigned long value, or the defaultValue if attribute is not present
        """
        ...

    def hasAttribute(self, attribute: ghidra.app.util.bin.format.dwarf.attribs.DWARFAttribute) -> bool:
        """
        Returns true if the specified attribute is present.
        @param attribute attribute id
        @return boolean true if value is present
        """
        ...

    def hasOffset(self, offset: long) -> bool:
        """
        Returns true if any of the {@link DebugInfoEntry DIEs} that makeup this aggregate
         have the specified offset.
        @param offset DIE offset to search for
        @return true if this {@link DIEAggregate} has a fragment DIE at that offset.
        """
        ...

    def hashCode(self) -> int: ...

    def isDanglingDeclaration(self) -> bool:
        """
        Returns true if this DIE has a DW_AT_declaration attribute and
         does NOT have a matching inbound DW_AT_specification reference.
         <p>
        @return boolean true if this DIE has a DW_AT_declaration attribute and
         does NOT have a matching inbound DW_AT_specification reference
        """
        ...

    def isPartialDeclaration(self) -> bool:
        """
        Returns true if this DIE has a DW_AT_declaration attribute.
        @return true if this DIE has a DW_AT_declaration attribute
        """
        ...

    def notify(self) -> None: ...

    def notifyAll(self) -> None: ...

    def parseDataMemberOffset(self, attribute: ghidra.app.util.bin.format.dwarf.attribs.DWARFAttribute, defaultValue: int) -> int:
        """
        Returns the unsigned integer value of the requested attribute after resolving
         any DWARF expression opcodes.
        @param attribute {@link DWARFAttribute} id
        @param defaultValue value to return if attribute is not present
        @return unsigned int value, or the defaultValue if attribute is not present
        @throws IOException if error reading value or invalid value type
        @throws DWARFExpressionException if error evaluating a DWARF expression
        """
        ...

    def parseInt(self, attribute: ghidra.app.util.bin.format.dwarf.attribs.DWARFAttribute, defaultValue: int) -> int:
        """
        Returns the signed integer value of the requested attribute after resolving
         any DWARF expression opcodes.
         <p>
        @param attribute {@link DWARFAttribute} id
        @param defaultValue value to return if attribute is not present
        @return int value, or the defaultValue if attribute is not present
        @throws IOException if error reading value or invalid value type
        @throws DWARFExpressionException if error evaluating a DWARF expression
        """
        ...

    def parseUnsignedLong(self, attribute: ghidra.app.util.bin.format.dwarf.attribs.DWARFAttribute, defaultValue: long) -> long:
        """
        Returns the unsigned integer value of the requested attribute after resolving
         any DWARF expression opcodes.
         <p>
        @param attribute {@link DWARFAttribute} id
        @param defaultValue value to return if attribute is not present
        @return unsigned long value, or the defaultValue if attribute is not present
        @throws IOException if error reading value or invalid value type
        @throws DWARFExpressionException if error evaluating a DWARF expression
        """
        ...

    def toString(self) -> unicode: ...

    @overload
    def wait(self) -> None: ...

    @overload
    def wait(self, __a0: long) -> None: ...

    @overload
    def wait(self, __a0: long, __a1: int) -> None: ...

    @property
    def PCRange(self) -> ghidra.app.util.bin.format.dwarf.DWARFRange: ...

    @property
    def abstractInstance(self) -> ghidra.app.util.bin.format.dwarf.DIEAggregate: ...

    @property
    def compilationUnit(self) -> ghidra.app.util.bin.format.dwarf.DWARFCompilationUnit: ...

    @property
    def containingTypeRef(self) -> ghidra.app.util.bin.format.dwarf.DIEAggregate: ...

    @property
    def danglingDeclaration(self) -> bool: ...

    @property
    def declOffset(self) -> long: ...

    @property
    def declParent(self) -> ghidra.app.util.bin.format.dwarf.DIEAggregate: ...

    @property
    def depth(self) -> int: ...

    @property
    def fragmentCount(self) -> int: ...

    @property
    def functionParamList(self) -> List[object]: ...

    @property
    def headFragment(self) -> ghidra.app.util.bin.format.dwarf.DebugInfoEntry: ...

    @property
    def hexOffset(self) -> unicode: ...

    @property
    def lastFragment(self) -> ghidra.app.util.bin.format.dwarf.DebugInfoEntry: ...

    @property
    def name(self) -> unicode: ...

    @property
    def offset(self) -> long: ...

    @property
    def offsets(self) -> List[long]: ...

    @property
    def parent(self) -> ghidra.app.util.bin.format.dwarf.DIEAggregate: ...

    @property
    def partialDeclaration(self) -> bool: ...

    @property
    def program(self) -> ghidra.app.util.bin.format.dwarf.DWARFProgram: ...

    @property
    def sourceFile(self) -> unicode: ...

    @property
    def tag(self) -> ghidra.app.util.bin.format.dwarf.DWARFTag: ...

    @property
    def typeRef(self) -> ghidra.app.util.bin.format.dwarf.DIEAggregate: ...