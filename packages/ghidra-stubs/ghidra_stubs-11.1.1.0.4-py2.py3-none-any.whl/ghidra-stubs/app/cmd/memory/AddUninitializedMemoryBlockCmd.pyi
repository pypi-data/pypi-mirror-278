from typing import overload
import ghidra.app.cmd.memory
import ghidra.framework.model
import ghidra.program.model.listing
import java.lang


class AddUninitializedMemoryBlockCmd(ghidra.app.cmd.memory.AbstractAddMemoryBlockCmd):
    """
    Command for adding uninitialized memory blocks
    """





    def __init__(self, name: unicode, comment: unicode, source: unicode, start: ghidra.program.model.address.Address, length: long, read: bool, write: bool, execute: bool, isVolatile: bool, isOverlay: bool):
        """
        Create a new AddUninitializedMemoryBlockCmd
        @param name the name for the new memory block.
        @param comment the comment for the block
        @param source indicates what is creating the block
        @param start the start address for the the block
        @param length the length of the new block
        @param read sets the block's read permission flag
        @param write sets the block's write permission flag
        @param execute sets the block's execute permission flag
        @param isVolatile sets the block's volatile flag
        @param isOverlay if true, the block will be created in a new overlay address space.
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

    def setArtificial(self, a: bool) -> None:
        """
        Prior to command execution the block's artificial attribute state may be specified
         and will be applied to the new memory block.
        @param a block artificial attribute state
        """
        ...

    def toString(self) -> unicode: ...

    @overload
    def wait(self) -> None: ...

    @overload
    def wait(self, __a0: long) -> None: ...

    @overload
    def wait(self, __a0: long, __a1: int) -> None: ...

