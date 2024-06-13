from typing import overload
import ghidra.program.model.address
import ghidra.util.task
import java.lang


class ReDisassembler(object):
    """
    A class that re-disassembles where necessary
 
 
     Given a seed address, this will (re-)disassemble the instruction at that address. If it indicates
     any context changes, whether via  or fall-through, the affected addresses are
     considered for re-disassembly as well. If no instruction exists at the address, or an off-cut
     instruction exists at the address, the address is dropped, but the outgoing context is recorded.
     If one does exist, but its context is already the same, the address is dropped. Otherwise, it is
     queued up and the process repeats.
    """





    def __init__(self, program: ghidra.program.model.listing.Program): ...



    def disasemble(self, seed: ghidra.program.model.address.Address, monitor: ghidra.util.task.TaskMonitor) -> ghidra.program.model.address.AddressSetView: ...

    def equals(self, __a0: object) -> bool: ...

    def getClass(self) -> java.lang.Class: ...

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

