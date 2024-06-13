from typing import overload
import ghidra.app.util.bin
import ghidra.app.util.bin.format.dwarf.attribs
import java.lang
import java.util.function


class DWARFAttributeDef(object):
    """
    Information about a single DWARF attribute, as specified in a 
     DWARFAbbreviation.
 
     This class handles the case where a specified attribute id is unknown to us (therefore not
     listed in the attribute enum class), as well as the case where the form is customized with
     an implicitValue.
 
     Unknown forms are not supported and cause an exception.
    """





    def __init__(self, __a0: java.lang.Enum, __a1: int, __a2: ghidra.app.util.bin.format.dwarf.attribs.DWARFForm, __a3: long): ...



    def equals(self, obj: object) -> bool: ...

    def getAttributeForm(self) -> ghidra.app.util.bin.format.dwarf.attribs.DWARFForm:
        """
        Get the form of the attribute specification.
        @return the form value
        """
        ...

    def getAttributeId(self) -> E:
        """
        Get the attribute id of the attribute specification.
        @return the attribute value
        """
        ...

    def getAttributeName(self) -> unicode: ...

    def getClass(self) -> java.lang.Class: ...

    def getImplicitValue(self) -> long: ...

    def getRawAttributeId(self) -> int: ...

    def hashCode(self) -> int: ...

    def isImplicit(self) -> bool: ...

    def notify(self) -> None: ...

    def notifyAll(self) -> None: ...

    @staticmethod
    def read(reader: ghidra.app.util.bin.BinaryReader, mapper: java.util.function.Function) -> ghidra.app.util.bin.format.dwarf.attribs.DWARFAttributeDef:
        """
        Reads a {@link DWARFAttributeDef} instance from the {@link BinaryReader reader}.
         <p>
         Returns a null if its a end-of-list marker (which is only used by an attributespec list).
         <p>
        @param <E> attribute id enum type
        @param reader {@link BinaryReader}
        @param mapper func that converts an attribute id int into its enum
        @return DWARFAttributeDef instance, or null if EOL marker was read from the stream
        @throws IOException if error reading
        """
        ...

    def toString(self) -> unicode: ...

    @overload
    def wait(self) -> None: ...

    @overload
    def wait(self, __a0: long) -> None: ...

    @overload
    def wait(self, __a0: long, __a1: int) -> None: ...

    def withForm(self, newForm: ghidra.app.util.bin.format.dwarf.attribs.DWARFForm) -> ghidra.app.util.bin.format.dwarf.attribs.DWARFAttributeDef: ...

    @property
    def attributeForm(self) -> ghidra.app.util.bin.format.dwarf.attribs.DWARFForm: ...

    @property
    def attributeId(self) -> java.lang.Enum: ...

    @property
    def attributeName(self) -> unicode: ...

    @property
    def implicit(self) -> bool: ...

    @property
    def implicitValue(self) -> long: ...

    @property
    def rawAttributeId(self) -> int: ...