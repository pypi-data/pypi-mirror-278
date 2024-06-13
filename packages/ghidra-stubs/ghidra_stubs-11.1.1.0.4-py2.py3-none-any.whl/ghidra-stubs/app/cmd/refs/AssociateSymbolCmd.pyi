from typing import overload
import ghidra.framework.cmd
import ghidra.framework.model
import ghidra.program.model.listing
import java.lang


class AssociateSymbolCmd(object, ghidra.framework.cmd.Command):
    """
    Command class for associating a reference with a specific label
    """





    @overload
    def __init__(self, ref: ghidra.program.model.symbol.Reference, symbolName: unicode):
        """
        Create a associate symbol command for a global symbol
        @param ref the reference to associate with a symbol
        @param symbolName the name of the symbol with which to associate the reference.
        """
        ...

    @overload
    def __init__(self, ref: ghidra.program.model.symbol.Reference, scope: ghidra.program.model.symbol.Namespace):
        """
        Constructor.
        @param ref the reference to associate with a symbol
        @param scope scope that has the symbol to associate with the reference
        """
        ...

    @overload
    def __init__(self, ref: ghidra.program.model.symbol.Reference, symbolName: unicode, scope: ghidra.program.model.symbol.Namespace):
        """
        Constructor
        @param ref the reference to associate with a symbol
        @param symbolName the name of the symbol with which to associate the reference.
        @param scope scope of the symbol with the given symbolName
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