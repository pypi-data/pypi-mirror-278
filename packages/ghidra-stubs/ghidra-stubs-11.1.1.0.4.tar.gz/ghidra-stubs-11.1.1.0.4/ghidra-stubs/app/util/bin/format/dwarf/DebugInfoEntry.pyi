from typing import List
from typing import overload
import ghidra.app.util.bin
import ghidra.app.util.bin.format.dwarf
import ghidra.app.util.bin.format.dwarf.attribs
import java.lang


class DebugInfoEntry(object):
    """
    A DWARF Debug Info Entry is a collection of DWARFAttributeValue
     in a hierarchical structure (see #getParent(), #getChildren()).
 
     This class is a lower-level class and DIEAggregate should be used instead in most
     cases when examining information from the DWARF system.
    """





    def __init__(self, cu: ghidra.app.util.bin.format.dwarf.DWARFCompilationUnit, offset: long, dieIndex: int, abbreviation: ghidra.app.util.bin.format.dwarf.DWARFAbbreviation, attrOffsets: List[int]):
        """
        Creates a DIE.
        @param cu compunit containing the DIE
        @param offset offset of the DIE
        @param dieIndex index of the DIE
        @param abbreviation that defines the schema of this DIE record
        @param attrOffsets offset (from the die offset) of each attribute value
        """
        ...



    def equals(self, obj: object) -> bool: ...

    def findAttribute(self, attributeId: ghidra.app.util.bin.format.dwarf.attribs.DWARFAttribute) -> ghidra.app.util.bin.format.dwarf.attribs.DWARFAttributeValue:
        """
        Searches the list of attributes for a specific attribute, by id.
        @param attributeId {@link DWARFAttribute}
        @return {@link DWARFAttributeValue}, or null if not found
        """
        ...

    def getAbbreviation(self) -> ghidra.app.util.bin.format.dwarf.DWARFAbbreviation:
        """
        Get the abbreviation of this DIE.
        @return the abbreviation of this DIE
        """
        ...

    def getAttributeCount(self) -> int:
        """
        Returns the number of attributes in this DIE.
        @return number of attribute values in this DIE
        """
        ...

    def getAttributeValue(self, attribIndex: int) -> ghidra.app.util.bin.format.dwarf.attribs.DWARFAttributeValue:
        """
        Returns the indexed attribute value.
        @param attribIndex index (0..count)
        @return {@link DWARFAttributeValue}
        @throws IOException if error reading the value
        """
        ...

    @overload
    def getChildren(self) -> List[ghidra.app.util.bin.format.dwarf.DebugInfoEntry]:
        """
        Return a list of the child DIE's.
        @return list of child DIE's
        """
        ...

    @overload
    def getChildren(self, childTag: ghidra.app.util.bin.format.dwarf.DWARFTag) -> List[ghidra.app.util.bin.format.dwarf.DebugInfoEntry]:
        """
        Return a list of children that are of a specific DWARF type.
         <p>
        @param childTag DIE tag used to filter the child DIEs
        @return list of matching child DIE records
        """
        ...

    def getClass(self) -> java.lang.Class: ...

    def getCompilationUnit(self) -> ghidra.app.util.bin.format.dwarf.DWARFCompilationUnit: ...

    def getDepth(self) -> int: ...

    def getIndex(self) -> int:
        """
        Returns the index of this DIE in the entire dwarf program.
        @return index of this DIE
        """
        ...

    def getOffset(self) -> long:
        """
        Get the offset of this DIE from the beginning of the debug_info section.
        @return the offset of this DIE from the beginning of the debug_info section
        """
        ...

    def getParent(self) -> ghidra.app.util.bin.format.dwarf.DebugInfoEntry:
        """
        Get the parent DIE of this DIE.
        @return the parent DIE, or null if this DIE is the root of the compilation unit
        """
        ...

    def getPositionInParent(self) -> int:
        """
        Returns the ordinal position of this DIE record in its parent's list of children.
        @return index of ourself in our parent, or -1 if root DIE
        """
        ...

    def getProgram(self) -> ghidra.app.util.bin.format.dwarf.DWARFProgram: ...

    def getTag(self) -> ghidra.app.util.bin.format.dwarf.DWARFTag:
        """
        Get the DWARFTag value of this DIE.
        @return the DWARFTag value of this DIE
        """
        ...

    def hashCode(self) -> int: ...

    def isTerminator(self) -> bool:
        """
        Check to see if the DIE is a terminator.
        @return true if the DIE is a terminator and false otherwise
        """
        ...

    def notify(self) -> None: ...

    def notifyAll(self) -> None: ...

    @staticmethod
    def read(reader: ghidra.app.util.bin.BinaryReader, cu: ghidra.app.util.bin.format.dwarf.DWARFCompilationUnit, dieIndex: int) -> ghidra.app.util.bin.format.dwarf.DebugInfoEntry:
        """
        Read a DIE record.
        @param reader {@link BinaryReader} positioned at the start of a DIE record
        @param cu the compunit that contains the DIE
        @param dieIndex the index of the DIE
        @return new DIE instance
        @throws IOException if error reading data, or bad DWARF
        """
        ...

    def setAttributeValue(self, index: int, attrVal: ghidra.app.util.bin.format.dwarf.attribs.DWARFAttributeValue) -> None: ...

    def toString(self) -> unicode: ...

    @overload
    def wait(self) -> None: ...

    @overload
    def wait(self, __a0: long) -> None: ...

    @overload
    def wait(self, __a0: long, __a1: int) -> None: ...

    @property
    def abbreviation(self) -> ghidra.app.util.bin.format.dwarf.DWARFAbbreviation: ...

    @property
    def attributeCount(self) -> int: ...

    @property
    def children(self) -> List[object]: ...

    @property
    def compilationUnit(self) -> ghidra.app.util.bin.format.dwarf.DWARFCompilationUnit: ...

    @property
    def depth(self) -> int: ...

    @property
    def index(self) -> int: ...

    @property
    def offset(self) -> long: ...

    @property
    def parent(self) -> ghidra.app.util.bin.format.dwarf.DebugInfoEntry: ...

    @property
    def positionInParent(self) -> int: ...

    @property
    def program(self) -> ghidra.app.util.bin.format.dwarf.DWARFProgram: ...

    @property
    def tag(self) -> ghidra.app.util.bin.format.dwarf.DWARFTag: ...

    @property
    def terminator(self) -> bool: ...