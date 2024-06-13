from typing import overload
import ghidra.app.util.bin
import ghidra.app.util.bin.format.dwarf
import ghidra.app.util.bin.format.dwarf.line
import ghidra.util.task
import java.lang
import java.util


class DWARFCompilationUnit(ghidra.app.util.bin.format.dwarf.DWARFUnitHeader):
    """
    A DWARF CompilationUnit is a contiguous block of DebugInfoEntry records found
     in a .debug_info section of an program.  The compilation unit block starts with a
     header that has a few important values and flags, and is followed by the DIE records.
 
     The first DIE record must be a DW_TAG_compile_unit.
 
     DIE records are identified by their byte offset in the .debug_info section.
 
    """





    def __init__(self, dwarfProgram: ghidra.app.util.bin.format.dwarf.DWARFProgram, startOffset: long, endOffset: long, intSize: int, dwarfVersion: int, pointerSize: int, unitNumber: int, firstDIEOffset: long, codeToAbbreviationMap: java.util.Map):
        """
        This ctor is public only for junit tests.  Do not use directly.
        @param dwarfProgram {@link DWARFProgram}
        @param startOffset offset in provider where it starts
        @param endOffset offset in provider where it ends
        @param intSize 4 (DWARF_32) or 8 (DWARF_64)
        @param dwarfVersion 2-5
        @param pointerSize default size of pointers
        @param unitNumber this compunits ordinal in the file
        @param firstDIEOffset start of DIEs in the provider
        @param codeToAbbreviationMap map of abbreviation numbers to {@link DWARFAbbreviation} instances
        """
        ...



    def equals(self, __a0: object) -> bool: ...

    def getAbbreviation(self, ac: int) -> ghidra.app.util.bin.format.dwarf.DWARFAbbreviation: ...

    def getAddrTableBase(self) -> long: ...

    def getClass(self) -> java.lang.Class: ...

    def getCodeToAbbreviationMap(self) -> java.util.Map: ...

    def getCompUnitDIEA(self) -> ghidra.app.util.bin.format.dwarf.DIEAggregate:
        """
        Returns this comp unit's root DIE as a DIE Aggregate.
        @return the aggregate containing the root element of this comp unit
        """
        ...

    def getCompileDirectory(self) -> unicode:
        """
        Get the compile directory of the compile unit
        @return the compile directory of the compile unit
        """
        ...

    def getDWARFVersion(self) -> int: ...

    def getEndOffset(self) -> long:
        """
        Returns the byte offset to the end of this unit.
        @return the byte offset to the end of this unit
        """
        ...

    def getFirstDIEOffset(self) -> long: ...

    def getIntSize(self) -> int:
        """
        Returns either 4 (for DWARF_32) or 8 (for DWARF_64) depending on the current unit format
        @return size of ints in this unit (4 or 8)
        """
        ...

    def getLanguage(self) -> int:
        """
        Get the source language of the compile unit.
         <p>
         See {@link DWARFSourceLanguage} for values.
        @return the source language of the compile unit, or -1 if not set
        """
        ...

    def getLine(self) -> ghidra.app.util.bin.format.dwarf.line.DWARFLine: ...

    def getLocListsBase(self) -> long: ...

    def getName(self) -> unicode:
        """
        Get the filename that produced the compile unit
        @return the filename that produced the compile unit
        """
        ...

    def getPCRange(self) -> ghidra.app.util.bin.format.dwarf.DWARFRange:
        """
        Returns the range covered by this CU, as defined by the lo_pc and high_pc attribute values,
         defaulting to (0,0] if missing.
        @return {@link DWARFRange} that this CU covers, never null
        """
        ...

    def getPointerSize(self) -> int:
        """
        Returns the size of pointers in this compUnit.
        @return the size in bytes of pointers
        """
        ...

    def getProducer(self) -> unicode:
        """
        Get the producer of the compile unit
        @return the producer of the compile unit
        """
        ...

    def getProgram(self) -> ghidra.app.util.bin.format.dwarf.DWARFProgram: ...

    def getRangeListsBase(self) -> long: ...

    def getStartOffset(self) -> long:
        """
        Returns the byte offset to the start of this unit.
        @return the byte offset to the start of this unit
        """
        ...

    def getStrOffsetsBase(self) -> long: ...

    def getUnitNumber(self) -> int:
        """
        Return the ordinal number of this unit
        @return ordinal of this unit
        """
        ...

    def hasDWO(self) -> bool: ...

    def hashCode(self) -> int: ...

    def init(self, rootDIE: ghidra.app.util.bin.format.dwarf.DebugInfoEntry) -> None:
        """
        Initializes this compunit with the root DIE (first DIE) of the compunit.  This comp unit
         isn't usable until this has happened.
        @param rootDIE {@link DebugInfoEntry}
        @throws IOException if error reading data from the DIE
        """
        ...

    def notify(self) -> None: ...

    def notifyAll(self) -> None: ...

    @staticmethod
    def read(dprog: ghidra.app.util.bin.format.dwarf.DWARFProgram, reader: ghidra.app.util.bin.BinaryReader, abbrReader: ghidra.app.util.bin.BinaryReader, unitNumber: int, monitor: ghidra.util.task.TaskMonitor) -> ghidra.app.util.bin.format.dwarf.DWARFUnitHeader:
        """
        Reads the initial fields found in a unit header.
        @param dprog {@link DWARFProgram}
        @param reader {@link BinaryReader} stream
        @param abbrReader {@link BinaryReader} .debug_abbr stream
        @param unitNumber ordinal of this item
        @param monitor {@link TaskMonitor}
        @return a unit header (only comp units for now), or null if at end-of-list
        @throws DWARFException if invalid dwarf data
        @throws IOException if error reading data
        @throws CancelledException if cancelled
        """
        ...

    @staticmethod
    def readV4(partial: ghidra.app.util.bin.format.dwarf.DWARFUnitHeader, reader: ghidra.app.util.bin.BinaryReader, abbrReader: ghidra.app.util.bin.BinaryReader, monitor: ghidra.util.task.TaskMonitor) -> ghidra.app.util.bin.format.dwarf.DWARFCompilationUnit:
        """
        Creates a new {@link DWARFCompilationUnit} by reading a compilationUnit's header data
         from the debug_info section and the debug_abbr section and its compileUnit DIE (ie.
         the first DIE right after the header).
         <p>
         Returns {@code NULL} if there was an ignorable error while reading the compilation unit (and
         leaves the input stream at the next compilation unit to read), otherwise throws
         an IOException if there was an unrecoverable error.
         <p>
         Also returns {@code NULL} (and leaves the stream at EOF) if the remainder of the stream 
         is filled with null bytes.
        @param partial already read partial unit header
        @param reader .debug_info BinaryReader
        @param abbrReader .debug_abbr BinaryReader
        @param monitor the current task monitor
        @return the read compilation unit, or null if the compilation unit was bad/empty and should 
         be ignored
        @throws DWARFException if an invalid or unsupported DWARF version is read.
        @throws IOException if the length of the compilation unit is invalid.
        @throws CancelledException if the task has been canceled.
        """
        ...

    @staticmethod
    def readV5(partial: ghidra.app.util.bin.format.dwarf.DWARFUnitHeader, reader: ghidra.app.util.bin.BinaryReader, abbrReader: ghidra.app.util.bin.BinaryReader, monitor: ghidra.util.task.TaskMonitor) -> ghidra.app.util.bin.format.dwarf.DWARFCompilationUnit:
        """
        Creates a new {@link DWARFCompilationUnit} by reading a compilationUnit's header data
         from the debug_info section and the debug_abbr section and its compileUnit DIE (ie.
         the first DIE right after the header).
         <p>
         Returns {@code NULL} if there was an ignorable error while reading the compilation unit (and
         leaves the input stream at the next compilation unit to read), otherwise throws
         an IOException if there was an unrecoverable error.
         <p>
         Also returns {@code NULL} (and leaves the stream at EOF) if the remainder of the stream 
         is filled with null bytes.
        @param partial already read partial unit header
        @param reader .debug_info BinaryReader
        @param abbrReader .debug_abbr BinaryReader
        @param monitor the current task monitor
        @return the read compilation unit, or null if the compilation unit was bad/empty and should 
         be ignored
        @throws DWARFException if an invalid or unsupported DWARF version is read.
        @throws IOException if the length of the compilation unit is invalid.
        @throws CancelledException if the task has been canceled.
        """
        ...

    def toString(self) -> unicode: ...

    @overload
    def wait(self) -> None: ...

    @overload
    def wait(self, __a0: long) -> None: ...

    @overload
    def wait(self, __a0: long, __a1: int) -> None: ...

    @property
    def PCRange(self) -> ghidra.app.util.bin.format.dwarf.DWARFRange: ...

    @property
    def addrTableBase(self) -> long: ...

    @property
    def codeToAbbreviationMap(self) -> java.util.Map: ...

    @property
    def compUnitDIEA(self) -> ghidra.app.util.bin.format.dwarf.DIEAggregate: ...

    @property
    def compileDirectory(self) -> unicode: ...

    @property
    def firstDIEOffset(self) -> long: ...

    @property
    def language(self) -> int: ...

    @property
    def line(self) -> ghidra.app.util.bin.format.dwarf.line.DWARFLine: ...

    @property
    def locListsBase(self) -> long: ...

    @property
    def name(self) -> unicode: ...

    @property
    def pointerSize(self) -> int: ...

    @property
    def producer(self) -> unicode: ...

    @property
    def rangeListsBase(self) -> long: ...

    @property
    def strOffsetsBase(self) -> long: ...