from typing import overload
import ghidra.framework.cmd
import ghidra.framework.model
import ghidra.program.model.listing
import java.lang


class DeleteLabelCmd(object, ghidra.framework.cmd.Command):
    """
    Command to delete a label
    """





    @overload
    def __init__(self, addr: ghidra.program.model.address.Address, name: unicode):
        """
        Constructs a new command for deleting a global symbol
        @param addr address of the label to be deleted.
        @param name name of the label to be deleted.
        """
        ...

    @overload
    def __init__(self, addr: ghidra.program.model.address.Address, name: unicode, scope: ghidra.program.model.symbol.Namespace):
        """
        Constructs a new command for deleting a label or function variable.
        @param addr address of the label to be deleted.
        @param name name of the label to be deleted.
        @param scope the scope of the label to delete. (i.e. the namespace the label to delete is associated with)
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