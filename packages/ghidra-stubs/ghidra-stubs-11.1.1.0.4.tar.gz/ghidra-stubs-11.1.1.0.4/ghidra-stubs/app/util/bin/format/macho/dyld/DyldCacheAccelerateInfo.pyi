from typing import overload
import ghidra.app.util.bin
import ghidra.app.util.importer
import ghidra.program.model.address
import ghidra.program.model.data
import ghidra.program.model.listing
import ghidra.util.task
import java.lang


class DyldCacheAccelerateInfo(object, ghidra.app.util.bin.StructConverter):
    """
    Represents a dyld_cache_accelerator_info structure.
    """

    ASCII: ghidra.program.model.data.DataType
    BYTE: ghidra.program.model.data.DataType
    DWORD: ghidra.program.model.data.DataType
    IBO32: ghidra.program.model.data.DataType
    IBO64: ghidra.program.model.data.DataType
    POINTER: ghidra.program.model.data.DataType
    QWORD: ghidra.program.model.data.DataType
    SLEB128: ghidra.program.model.data.SignedLeb128DataType
    STRING: ghidra.program.model.data.DataType
    ULEB128: ghidra.program.model.data.UnsignedLeb128DataType
    UTF16: ghidra.program.model.data.DataType
    UTF8: ghidra.program.model.data.DataType
    VOID: ghidra.program.model.data.DataType
    WORD: ghidra.program.model.data.DataType



    def __init__(self, reader: ghidra.app.util.bin.BinaryReader):
        """
        Create a new {@link DyldCacheAccelerateInfo}.
        @param reader A {@link BinaryReader} positioned at the start of a DYLD accelerate info
        @throws IOException if there was an IO-related problem creating the DYLD accelerate info
        """
        ...



    def equals(self, __a0: object) -> bool: ...

    def getClass(self) -> java.lang.Class: ...

    def hashCode(self) -> int: ...

    def markup(self, program: ghidra.program.model.listing.Program, accelerateInfoAddr: ghidra.program.model.address.Address, monitor: ghidra.util.task.TaskMonitor, log: ghidra.app.util.importer.MessageLog) -> None:
        """
        Marks up this {@link DyldCacheAccelerateInfo} with data structures and comments.
        @param program The {@link Program} to mark up
        @param accelerateInfoAddr The {@link Address} of the {@link DyldCacheAccelerateInfo}
        @param monitor A cancellable task monitor
        @param log The log
        @throws CancelledException if the user cancelled the operation
        """
        ...

    def notify(self) -> None: ...

    def notifyAll(self) -> None: ...

    def parse(self, program: ghidra.program.model.listing.Program, accelerateInfoAddr: ghidra.program.model.address.Address, log: ghidra.app.util.importer.MessageLog, monitor: ghidra.util.task.TaskMonitor) -> None:
        """
        Parses the structures referenced by this {@link DyldCacheAccelerateInfo}.
        @param program The {@link Program} to parse.
        @param accelerateInfoAddr The {@link Address} of the {@link DyldCacheAccelerateInfo}
        @param log The log
        @param monitor A cancellable task monitor
        @throws CancelledException if the user cancelled the operation
        """
        ...

    def toDataType(self) -> ghidra.program.model.data.DataType: ...

    def toString(self) -> unicode: ...

    @overload
    def wait(self) -> None: ...

    @overload
    def wait(self, __a0: long) -> None: ...

    @overload
    def wait(self, __a0: long, __a1: int) -> None: ...

