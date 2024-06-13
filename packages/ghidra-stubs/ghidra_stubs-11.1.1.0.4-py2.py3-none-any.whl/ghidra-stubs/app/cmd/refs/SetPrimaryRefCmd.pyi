from typing import overload
import ghidra.framework.cmd
import ghidra.framework.model
import ghidra.program.model.listing
import java.lang


class SetPrimaryRefCmd(object, ghidra.framework.cmd.Command):
    """
    Command class for setting a reference to be primary.  Any other
     reference that was primary at that address will no longer be primary.
    """





    @overload
    def __init__(self, ref: ghidra.program.model.symbol.Reference, isPrimary: bool):
        """
        Creates a command for setting whether or not a reference is the primary reference.
         If isPrimary is true, any other reference that was primary at that 
         address will no longer be primary.
        @param ref the reference
        @param isPrimary true to make the reference primary, false to make it non-primary
        """
        ...

    @overload
    def __init__(self, fromAddr: ghidra.program.model.address.Address, opIndex: int, toAddr: ghidra.program.model.address.Address, isPrimary: bool):
        """
        Creates a command for setting whether or not a reference is the primary reference.
         If isPrimary is true, any other reference that was primary at that 
         address will no longer be primary.
        @param fromAddr the address of the codeunit making the reference.
        @param opIndex the operand index.
        @param toAddr the address being referred to.
        @param isPrimary true to make the reference primary, false to make it non-primary
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