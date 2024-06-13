from typing import overload
import ghidra.framework.cmd
import ghidra.framework.model
import ghidra.program.model.data
import ghidra.program.model.listing
import java.lang


class AbstractCreateStructureCmd(object, ghidra.framework.cmd.Command):
    """
    A base class to hold duplicate information for commands that create 
     structures.  This class implements the logic of the 
     #applyTo(Program) method so that child implementations need 
     only to implement the abstract methods.
    """









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

    @property
    def name(self) -> unicode: ...

    @property
    def newDataType(self) -> ghidra.program.model.data.DataType: ...

    @property
    def statusMsg(self) -> unicode: ...