from typing import overload
import ghidra.framework.cmd
import ghidra.framework.model
import ghidra.program.model.listing
import java.lang


class AddExternalNameCmd(object, ghidra.framework.cmd.Command):
    """
    Command to update the name for an external program.
    """





    def __init__(self, name: unicode, source: ghidra.program.model.symbol.SourceType):
        """
        Constructs a new command for adding the name of an external program.
        @param name the new name to be used for the external program link.
        @param source the source of this external name
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