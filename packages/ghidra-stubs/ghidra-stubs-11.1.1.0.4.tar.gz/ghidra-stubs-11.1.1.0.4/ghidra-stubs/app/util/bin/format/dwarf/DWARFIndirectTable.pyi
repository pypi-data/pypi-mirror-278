from typing import overload
import ghidra.app.util.bin.format.dwarf
import ghidra.app.util.bin.format.dwarf.DWARFIndirectTable
import ghidra.util.task
import java.lang


class DWARFIndirectTable(object):
    """
    Handles a grouping of DWARFIndirectTableHeaders that specify how to look up a
     certain type of item (per CU).
    """






    class CheckedIOFunction(object):








        def apply(self, __a0: object) -> object: ...

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



    def __init__(self, reader: ghidra.app.util.bin.BinaryReader, baseOffsetFunc: java.util.function.Function):
        """
        Creates a {@link DWARFIndirectTable}
        @param reader {@link BinaryReader} containing the {@link DWARFIndirectTableHeader}s
        @param baseOffsetFunc a function that will return the baseoffset value for a
         {@link DWARFCompilationUnit}.
        """
        ...



    def bootstrap(self, msg: unicode, headerReader: ghidra.app.util.bin.format.dwarf.DWARFIndirectTable.CheckedIOFunction, monitor: ghidra.util.task.TaskMonitor) -> None:
        """
        Populates this instance will all {@link DWARFIndirectTableHeader} instances that can be
         read from the stream.
        @param msg String message to use for the taskmonitor
        @param headerReader a function that reads the specific table header type from the stream
        @param monitor {@link TaskMonitor}
        @throws CancelledException if cancelled
        @throws IOException if error reading a header
        """
        ...

    def clear(self) -> None: ...

    def equals(self, __a0: object) -> bool: ...

    def getClass(self) -> java.lang.Class: ...

    def getOffset(self, index: int, cu: ghidra.app.util.bin.format.dwarf.DWARFCompilationUnit) -> long:
        """
        Returns the offset of an item, based on its index in a particular header (which is found
         by the controlling CU)
        @param index index of the item
        @param cu {@link DWARFCompilationUnit}
        @return long offset of the item.  Caller responsible for reading the item themselves
        @throws IOException if error reading table data
        """
        ...

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

