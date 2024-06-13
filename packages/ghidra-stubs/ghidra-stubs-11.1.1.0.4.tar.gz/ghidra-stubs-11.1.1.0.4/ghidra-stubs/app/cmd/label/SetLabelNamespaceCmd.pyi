from typing import overload
import ghidra.framework.cmd
import ghidra.framework.model
import ghidra.program.model.listing
import java.lang


class SetLabelNamespaceCmd(object, ghidra.framework.cmd.Command):
    """
    Command for changing the scope of a label.
     The scope is the namespace that the label is associated with.
    """





    def __init__(self, addr: ghidra.program.model.address.Address, name: unicode, oldNamespace: ghidra.program.model.symbol.Namespace, newNamespace: ghidra.program.model.symbol.Namespace):
        """
        Constructs a new command for changing the scope of a label.
        @param addr the address of the label to be changed.
        @param name the name of the label to be changed.
        @param oldNamespace the current scope of the label that will be changed.
        @param newNamespace the new scope of the label.
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