from typing import overload
import ghidra.framework.cmd
import ghidra.framework.model
import ghidra.program.model.listing
import java.lang


class RenameTreeCmd(object, ghidra.framework.cmd.Command):
    """
    Command to rename a tree in a program; this does not affect
     the root module of the tree.
    """





    def __init__(self, oldName: unicode, newName: unicode):
        """
        Constructor for RenameTreeCmd.
        @param oldName old name of the tree
        @param newName new name of the tree
        """
        ...



    @overload
    def applyTo(self, p: ghidra.program.model.listing.Program) -> bool: ...

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