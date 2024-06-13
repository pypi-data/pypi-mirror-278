from typing import overload
import ghidra.app.cmd.data
import ghidra.framework.model
import ghidra.program.model.data
import ghidra.program.model.listing
import java.lang


class CreateStructureInStructureCmd(ghidra.app.cmd.data.AbstractCreateStructureCmd):
    """
    Command to create a structure inside of another structure.
    """





    @overload
    def __init__(self, address: ghidra.program.model.address.Address, fromPath: List[int], toPath: List[int]):
        """
        Constructs a new command for creating structures inside other structures.
        @param address the address of the outer-most structure.
        @param fromPath the componentPath of the first component to be consumed in 
         the new structure.
        @param toPath the componentPath of the second component to be consumed in the
         the new structure.
        """
        ...

    @overload
    def __init__(self, name: unicode, addr: ghidra.program.model.address.Address, fromPath: List[int], toPath: List[int]):
        """
        Constructs a new command for creating structures inside other structures.
        @param name The name of the structure.
        @param addr the address of the outer-most structure.
        @param fromPath the componentPath of the first component to be consumed in 
         the new structure.
        @param toPath the componentPath of the second component to be consumed in the
         the new structure.
        """
        ...

    @overload
    def __init__(self, newStructure: ghidra.program.model.data.Structure, address: ghidra.program.model.address.Address, fromPath: List[int], toPath: List[int]): ...



    @overload
    def applyTo(self, program: ghidra.program.model.listing.Program) -> bool: ...

    @overload
    def applyTo(self, __a0: ghidra.framework.model.DomainObject) -> bool: ...

    def equals(self, __a0: object) -> bool: ...

    def getClass(self) -> java.lang.Class: ...

    def getName(self) -> unicode: ...

    def getNewDataType(self) -> ghidra.program.model.data.DataType:
        """
        Get the new structure data type which was created.
        @return new structure.
        """
        ...

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

