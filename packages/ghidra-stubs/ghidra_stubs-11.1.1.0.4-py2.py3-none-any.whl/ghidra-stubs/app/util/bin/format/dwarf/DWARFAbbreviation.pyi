from typing import List
from typing import overload
import ghidra.app.util.bin
import ghidra.app.util.bin.format.dwarf
import ghidra.app.util.bin.format.dwarf.attribs
import ghidra.app.util.bin.format.dwarf.attribs.DWARFAttribute
import ghidra.util.task
import java.lang
import java.util


class DWARFAbbreviation(object):
    """
    This class represents the 'schema' for a DWARF DIE record.
 
     A raw DWARF DIE record specifies its abbreviation code (pointing to an instance of
     this class) and the corresponding DWARFAbbreviation instance has the information
     about how the raw DIE is laid out.
    """





    def __init__(self, abbreviationCode: int, tagId: int, hasChildren: bool, attributes: List[ghidra.app.util.bin.format.dwarf.attribs.DWARFAttribute.AttrDef]): ...



    def equals(self, __a0: object) -> bool: ...

    def findAttribute(self, attributeId: ghidra.app.util.bin.format.dwarf.attribs.DWARFAttribute) -> ghidra.app.util.bin.format.dwarf.attribs.DWARFAttribute.AttrDef:
        """
        Get the attribute with the given attribute key.
        @param attributeId attribute key
        @return attribute specification
        """
        ...

    def getAbbreviationCode(self) -> int:
        """
        Get the abbreviation code.
        @return the abbreviation code
        """
        ...

    def getAttributeAt(self, index: int) -> ghidra.app.util.bin.format.dwarf.attribs.DWARFAttribute.AttrDef:
        """
        Get the attribute at the given index.
        @param index index of the attribute
        @return attribute specification
        """
        ...

    def getAttributeCount(self) -> int:
        """
        Return number of attribute values.
        @return number of attribute values
        """
        ...

    def getAttributes(self) -> List[ghidra.app.util.bin.format.dwarf.attribs.DWARFAttribute.AttrDef]:
        """
        Return a live list of the attributes.
        @return list of attributes
        """
        ...

    def getClass(self) -> java.lang.Class: ...

    def getTag(self) -> ghidra.app.util.bin.format.dwarf.DWARFTag:
        """
        Get the tag value.
        @return the tag value
        """
        ...

    def getTagName(self) -> unicode: ...

    def hasChildren(self) -> bool:
        """
        Checks to see if this abbreviation has any DIE children.
        @return true if this abbreviation has DIE children
        """
        ...

    def hashCode(self) -> int: ...

    def notify(self) -> None: ...

    def notifyAll(self) -> None: ...

    @staticmethod
    def read(reader: ghidra.app.util.bin.BinaryReader, prog: ghidra.app.util.bin.format.dwarf.DWARFProgram, monitor: ghidra.util.task.TaskMonitor) -> ghidra.app.util.bin.format.dwarf.DWARFAbbreviation:
        """
        Reads a {@link DWARFAbbreviation} from the stream.
        @param reader {@link BinaryReader} stream
        @param prog {@link DWARFProgram}
        @param monitor {@link TaskMonitor}
        @return {@link DWARFAbbreviation}, or null if the stream was at a end-of-list marker
        @throws IOException if error reading
        @throws CancelledException if canceled
        """
        ...

    @staticmethod
    def readAbbreviations(reader: ghidra.app.util.bin.BinaryReader, prog: ghidra.app.util.bin.format.dwarf.DWARFProgram, monitor: ghidra.util.task.TaskMonitor) -> java.util.Map:
        """
        Reads a list of {@link DWARFAbbreviation}, stopping when the end-of-list marker is
         encountered.
        @param reader {@link BinaryReader} .debug_abbr stream
        @param prog {@link DWARFProgram}
        @param monitor {@link TaskMonitor}
        @return map of abbrCode -> abbr instance
        @throws IOException if error reading
        @throws CancelledException if cancelled
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
    def abbreviationCode(self) -> int: ...

    @property
    def attributeCount(self) -> int: ...

    @property
    def attributes(self) -> List[ghidra.app.util.bin.format.dwarf.attribs.DWARFAttribute.AttrDef]: ...

    @property
    def tag(self) -> ghidra.app.util.bin.format.dwarf.DWARFTag: ...

    @property
    def tagName(self) -> unicode: ...