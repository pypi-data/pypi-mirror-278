from typing import overload
import ghidra.app.cmd.function
import ghidra.framework.model
import ghidra.program.model.listing
import java.lang


class AddRegisterParameterCommand(ghidra.app.cmd.function.AddParameterCommand):
    """
    A command to create a new function register parameter.
    """





    def __init__(self, function: ghidra.program.model.listing.Function, register: ghidra.program.model.lang.Register, name: unicode, dataType: ghidra.program.model.data.DataType, ordinal: int, source: ghidra.program.model.symbol.SourceType): ...



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