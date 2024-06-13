from typing import overload
import ghidra.framework.cmd
import ghidra.framework.model
import ghidra.program.model.listing
import java.lang


class UpdateFunctionCommand(object, ghidra.framework.cmd.Command):
    """
    A command to update Function signature in its entirety including optional
     custom storage.
 
     If the function does not rely on custom storage the use of ApplyFunctionSignatureCmd
     may be more appropriate.
    """





    def __init__(self, __a0: ghidra.program.model.listing.Function, __a1: ghidra.program.model.listing.Function.FunctionUpdateType, __a2: unicode, __a3: ghidra.program.model.listing.Variable, __a4: List[object], __a5: ghidra.program.model.symbol.SourceType, __a6: bool): ...



    @overload
    def applyTo(self, obj: ghidra.program.model.listing.Program) -> bool: ...

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