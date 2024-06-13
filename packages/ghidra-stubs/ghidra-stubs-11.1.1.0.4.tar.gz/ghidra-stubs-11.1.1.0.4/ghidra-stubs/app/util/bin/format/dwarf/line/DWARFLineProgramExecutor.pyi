from typing import List
from typing import overload
import ghidra.app.util.bin.format.dwarf.line
import java.io
import java.lang


class DWARFLineProgramExecutor(object, java.io.Closeable):
    """
    Handles executing, step-by-step, the address-to-sourcefile mapping instructions found at the
     end of a DWARFLine structure.
    """





    def __init__(self, reader: ghidra.app.util.bin.BinaryReader, streamEnd: long, pointerSize: int, opcodeBase: int, lineBase: int, lineRange: int, minInstrLen: int, defaultIsStatement: bool): ...



    def allRows(self) -> List[ghidra.app.util.bin.format.dwarf.line.DWARFLineProgramState]: ...

    def close(self) -> None: ...

    def currentState(self) -> ghidra.app.util.bin.format.dwarf.line.DWARFLineProgramState: ...

    def equals(self, __a0: object) -> bool: ...

    def getClass(self) -> java.lang.Class: ...

    def hasNext(self) -> bool: ...

    def hashCode(self) -> int: ...

    def nextRow(self) -> ghidra.app.util.bin.format.dwarf.line.DWARFLineProgramState: ...

    def notify(self) -> None: ...

    def notifyAll(self) -> None: ...

    def step(self) -> ghidra.app.util.bin.format.dwarf.line.DWARFLineProgramInstruction:
        """
        Read the next instruction and executes it
        @return 
        @throws IOException if an i/o error occurs
        """
        ...

    def toString(self) -> unicode: ...

    @overload
    def wait(self) -> None: ...

    @overload
    def wait(self, __a0: long) -> None: ...

    @overload
    def wait(self, __a0: long, __a1: int) -> None: ...

