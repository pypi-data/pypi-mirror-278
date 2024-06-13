from typing import overload
import ghidra.framework.cmd
import ghidra.framework.model
import ghidra.program.model.listing
import java.lang


class DeleteFunctionCmd(object, ghidra.framework.cmd.Command):
    """
    Command for clearing a function at an address.
    """





    @overload
    def __init__(self, entry: ghidra.program.model.address.Address):
        """
        Constructs a new command for deleting a function.
        @param entry entry point address for the function to be deleted.
        """
        ...

    @overload
    def __init__(self, entry: ghidra.program.model.address.Address, ignoreMissingFunction: bool): ...



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