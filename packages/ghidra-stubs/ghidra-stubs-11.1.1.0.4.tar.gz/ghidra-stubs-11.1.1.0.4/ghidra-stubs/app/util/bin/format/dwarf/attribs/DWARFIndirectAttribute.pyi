from typing import overload
import ghidra.app.util.bin.format.dwarf
import ghidra.app.util.bin.format.dwarf.attribs
import java.lang


class DWARFIndirectAttribute(ghidra.app.util.bin.format.dwarf.attribs.DWARFNumericAttribute):
    """
    DWARF numeric attribute value that is an index into a lookup table
    """





    def __init__(self, index: long, def_: ghidra.app.util.bin.format.dwarf.attribs.DWARFAttributeDef): ...



    def equals(self, __a0: object) -> bool: ...

    def getAttributeForm(self) -> ghidra.app.util.bin.format.dwarf.attribs.DWARFForm: ...

    def getAttributeName(self) -> unicode: ...

    def getClass(self) -> java.lang.Class: ...

    def getIndex(self) -> int: ...

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
    def index(self) -> int: ...