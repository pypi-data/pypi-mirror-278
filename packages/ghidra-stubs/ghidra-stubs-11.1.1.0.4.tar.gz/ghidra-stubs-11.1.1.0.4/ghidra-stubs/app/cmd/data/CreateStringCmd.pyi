from typing import overload
import ghidra.framework.cmd
import ghidra.framework.model
import ghidra.program.model.listing
import java.lang


class CreateStringCmd(object, ghidra.framework.cmd.Command):
    """
    Command to create a String and optionally label it.
    """





    @overload
    def __init__(self, addr: ghidra.program.model.address.Address):
        """
        Construct command for creating null-terminated ASCII string Data.
         Current Data at addr will be cleared if it already exists.
        @param addr address where string should be created.
        """
        ...

    @overload
    def __init__(self, addr: ghidra.program.model.address.Address, length: int):
        """
        Construct command for creating fixed-length ASCII string Data.
         Current Data at addr will be cleared if it already exists.
        @param addr address where string should be created.
        @param length byte-length of string
        """
        ...

    @overload
    def __init__(self, addr: ghidra.program.model.address.Address, length: int, unicode: bool):
        """
        Construct command for creating fixed-length ASCII or Unicode string Data.
         Current Data at addr will be cleared if it already exists.
        @param addr address where string should be created.
        @param length byte-length of string
        @param unicode if true Unicode string will be created, else ASCII
        """
        ...

    @overload
    def __init__(self, addr: ghidra.program.model.address.Address, stringDataType: ghidra.program.model.data.AbstractStringDataType, length: int, clearMode: ghidra.program.model.data.DataUtilities.ClearDataMode):
        """
        Construct command for creating string Data
        @param addr address where string should be created.
        @param stringDataType string datatype
        @param length maximum string length (treatment is specific to specified datatype).
        @param clearMode {@link ClearDataMode} which indicates how existing Data conflicts
         should be handled.
        """
        ...

    @overload
    def __init__(self, addr: ghidra.program.model.address.Address, length: int, unicode: bool, clearMode: ghidra.program.model.data.DataUtilities.ClearDataMode):
        """
        Construct command for creating fixed-length ASCII or Unicode string Data
        @param addr address where string should be created.
        @param length byte-length of string
        @param unicode if true Unicode string will be created, else ASCII
        @param clearMode {@link ClearDataMode} which indicates how existing Data conflicts
         should be handled.
        """
        ...



    @overload
    def applyTo(self, program: ghidra.program.model.listing.Program) -> bool: ...

    @overload
    def applyTo(self, __a0: ghidra.framework.model.DomainObject) -> bool: ...

    def equals(self, __a0: object) -> bool: ...

    def getClass(self) -> java.lang.Class: ...

    def getName(self) -> unicode: ...

    def getStatusMsg(self) -> unicode: ...

    def hashCode(self) -> int: ...

    def notify(self) -> None: ...

    def notifyAll(self) -> None: ...

    def toString(self) -> unicode: ...

    @overload
    def wait(self) -> None: ...

    @overload
    def wait(self, __a0: long) -> None: ...

    @overload
    def wait(self, __a0: long, __a1: int) -> None: ...

    @property
    def name(self) -> unicode: ...

    @property
    def statusMsg(self) -> unicode: ...