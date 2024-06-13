from typing import overload
import ghidra.app.util.bin.format.dwarf
import ghidra.app.util.bin.format.dwarf.attribs
import java.lang


class DWARFNumericAttribute(ghidra.app.util.bin.format.dwarf.attribs.DWARFAttributeValue):
    """
    DWARF numeric attribute.
    """





    @overload
    def __init__(self, value: long, def_: ghidra.app.util.bin.format.dwarf.attribs.DWARFAttributeDef):
        """
        Creates a new numeric value, using 64 bits and marked as signed
        @param value long 64 bit value
        @param def attribute id and form of this value
        """
        ...

    @overload
    def __init__(self, bitLength: int, value: long, signed: bool, def_: ghidra.app.util.bin.format.dwarf.attribs.DWARFAttributeDef):
        """
        Creates a new numeric value, using the specific bitLength and value.
        @param bitLength number of bits, valid values are 1..64, or 0 if value is also 0
        @param value value of the scalar, any bits that are set above bitLength will be ignored
        @param signed true for a signed value, false for an unsigned value.
        @param def attribute id and form of this value
        """
        ...

    @overload
    def __init__(self, bitLength: int, value: long, signed: bool, ambiguous: bool, def_: ghidra.app.util.bin.format.dwarf.attribs.DWARFAttributeDef):
        """
        Creates a new numeric value, using the specific bitLength and value.
        @param bitLength number of bits, valid values are 1..64, or 0 if value is also 0
        @param value value of the scalar, any bits that are set above bitLength will be ignored
        @param signed true for a signed value, false for an unsigned value.
        @param ambiguous true for value with ambiguous signedness ({@code signed} parameter should
         not be trusted), false for value where the {@code signed} parameter is known to be correct
        @param def attribute id and form of this value
        """
        ...



    def equals(self, __a0: object) -> bool: ...

    def getAttributeForm(self) -> ghidra.app.util.bin.format.dwarf.attribs.DWARFForm: ...

    def getAttributeName(self) -> unicode: ...

    def getClass(self) -> java.lang.Class: ...

    def getUnsignedIntExact(self) -> int: ...

    def getUnsignedValue(self) -> long: ...

    def getValue(self) -> long: ...

    def getValueWithSignednessHint(self, signednessHint: bool) -> long:
        """
        {@return the value, forcing the signedness of ambiguous values using the specified hint}
        @param signednessHint true to default to a signed value, false to default to an 
         unsigned value
        """
        ...

    def hashCode(self) -> int: ...

    def isAmbiguousSignedness(self) -> bool:
        """
        {@return boolean flag, if true this value's signedness is up to the user of the value,
         if false the signedness was determined when the value was constructed}
        """
        ...

    def isHighbitSet(self) -> bool: ...

    def notify(self) -> None: ...

    def notifyAll(self) -> None: ...

    def toElementLocationString(self, elementType: unicode, sectionName: unicode, index: int, offset: long, ver: int) -> unicode: ...

    @overload
    def toString(self) -> unicode: ...

    @overload
    def toString(self, cu: ghidra.app.util.bin.format.dwarf.DWARFCompilationUnit) -> unicode: ...

    @overload
    def wait(self) -> None: ...

    @overload
    def wait(self, __a0: long) -> None: ...

    @overload
    def wait(self, __a0: long, __a1: int) -> None: ...

    @property
    def ambiguousSignedness(self) -> bool: ...

    @property
    def highbitSet(self) -> bool: ...

    @property
    def unsignedIntExact(self) -> int: ...

    @property
    def unsignedValue(self) -> long: ...

    @property
    def value(self) -> long: ...