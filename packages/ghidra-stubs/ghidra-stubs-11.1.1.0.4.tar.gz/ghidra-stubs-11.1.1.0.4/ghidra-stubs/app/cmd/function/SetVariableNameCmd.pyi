from typing import overload
import ghidra.framework.cmd
import ghidra.framework.model
import ghidra.program.model.listing
import java.lang


class SetVariableNameCmd(object, ghidra.framework.cmd.Command):
    """
    Command to rename a stack variable.
    """





    @overload
    def __init__(self, var: ghidra.program.model.listing.Variable, newName: unicode, source: ghidra.program.model.symbol.SourceType):
        """
        Constructs a new command to rename a stack/reg variable.
        @param var variable to rename
        @param newName the new name to give to the stack variable.
        @param source the source of this variable name
        """
        ...

    @overload
    def __init__(self, fnEntry: ghidra.program.model.address.Address, varName: unicode, newName: unicode, source: ghidra.program.model.symbol.SourceType):
        """
        Constructs a new command to rename a stack/reg variable.
        @param fnEntry
        @param varName
        @param newName
        @param source
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