from typing import overload
import ghidra.framework.cmd
import ghidra.framework.model
import ghidra.program.model.listing
import java.lang


class ReorderModuleCmd(object, ghidra.framework.cmd.Command):
    """
    Command to reorder children in a module.
    """





    def __init__(self, treeName: unicode, parentModuleName: unicode, childName: unicode, index: int):
        """
        Constructor for ReorderModuleCmd.
        @param treeName tree that contains the parent module identified by
         the parentModuleName
        @param parentModuleName name of the module with the children to reorder
        @param childName name of the child to move to the new index
        @param index new index for the child
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