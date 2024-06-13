from typing import overload
import ghidra.app.cmd.data
import ghidra.framework.model
import ghidra.program.model.data
import ghidra.program.model.listing
import java.lang


class CreateStructureCmd(ghidra.app.cmd.data.AbstractCreateStructureCmd):
    """
    Command to create a structure.
    """





    @overload
    def __init__(self, address: ghidra.program.model.address.Address, length: int):
        """
        Constructs a new command for creating a new structure and applying it to
         the browser.  This method simply calls 
         {@link #CreateStructureCmd(String, Address, int)} with 
         {@link ghidra.program.model.data.StructureFactory#DEFAULT_STRUCTURE_NAME} as the name of the structure.
        @param address the address at which to create the new structure.
        @param length the number of undefined bytes to consume in the new 
                structure.
        """
        ...

    @overload
    def __init__(self, newStructure: ghidra.program.model.data.Structure, address: ghidra.program.model.address.Address):
        """
        Creates a new structure by using the provided structure and attaching
         it to the program passed in the {@link #applyTo(Program)} method.
        @param newStructure The new structure to attach to the program 
                provided in the {@link #applyTo(Program)} method.
        @param address the address at which to create the new structure.
        """
        ...

    @overload
    def __init__(self, name: unicode, address: ghidra.program.model.address.Address, length: int):
        """
        Constructs a new command for creating a new structure and applying it to
         the browser.
        @param name The name of the new structure to create.
        @param address the address at which to create the new structure.
        @param length the number of undefined bytes to consume in the new 
                structure.
        """
        ...



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

