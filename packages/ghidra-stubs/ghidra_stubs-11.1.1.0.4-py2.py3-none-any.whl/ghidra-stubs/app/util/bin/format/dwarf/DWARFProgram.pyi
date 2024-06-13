from typing import List
from typing import overload
import ghidra.app.util.bin
import ghidra.app.util.bin.format.dwarf
import ghidra.app.util.bin.format.dwarf.attribs
import ghidra.app.util.bin.format.dwarf.attribs.DWARFAttribute
import ghidra.app.util.bin.format.dwarf.funcfixup
import ghidra.app.util.bin.format.dwarf.line
import ghidra.program.model.address
import ghidra.program.model.listing
import ghidra.util.datastruct
import ghidra.util.task
import java.io
import java.lang


class DWARFProgram(object, java.io.Closeable):
    """
    DWARFProgram encapsulates a Program with DWARF specific reference data
     used by DWARFDataTypeImporter and DWARFFunctionImporter, along with some
     helper functions.
    """

    DWARF_ROOT_CATPATH: ghidra.program.model.data.CategoryPath
    DWARF_ROOT_NAME: unicode = u'DWARF'
    UNCAT_CATPATH: ghidra.program.model.data.CategoryPath



    @overload
    def __init__(self, program: ghidra.program.model.listing.Program, importOptions: ghidra.app.util.bin.format.dwarf.DWARFImportOptions, monitor: ghidra.util.task.TaskMonitor):
        """
        Main constructor for DWARFProgram.
         <p>
         Auto-detects the DWARFSectionProvider and chains to the next constructor.
        @param program Ghidra {@link Program}.
        @param importOptions {@link DWARFImportOptions} to controls options during reading / parsing /importing.
        @param monitor {@link TaskMonitor} to control canceling and progress.
        @throws CancelledException if user cancels
        @throws IOException if error reading data
        @throws DWARFException if bad stuff happens.
        """
        ...

    @overload
    def __init__(self, program: ghidra.program.model.listing.Program, importOptions: ghidra.app.util.bin.format.dwarf.DWARFImportOptions, monitor: ghidra.util.task.TaskMonitor, sectionProvider: ghidra.app.util.bin.format.dwarf.sectionprovider.DWARFSectionProvider):
        """
        Constructor for DWARFProgram.
        @param program Ghidra {@link Program}.
        @param importOptions {@link DWARFImportOptions} to controls options during reading / parsing /importing.
        @param monitor {@link TaskMonitor} to control canceling and progress.
        @param sectionProvider {@link DWARFSectionProvider} factory that finds DWARF .debug_* sections
         wherever they live.
        @throws CancelledException if user cancels
        @throws IOException if error reading data
        @throws DWARFException if bad stuff happens.
        """
        ...



    def allAggregates(self) -> java.lang.Iterable:
        """
        Returns iterable that traverses all {@link DIEAggregate}s in the program.
        @return sequence of {@link DIEAggregate}es
        """
        ...

    def close(self) -> None: ...

    def dumpDIEs(self, ps: java.io.PrintStream) -> None: ...

    def equals(self, __a0: object) -> bool: ...

    def getAddress(self, form: ghidra.app.util.bin.format.dwarf.attribs.DWARFForm, value: long, cu: ghidra.app.util.bin.format.dwarf.DWARFCompilationUnit) -> long:
        """
        Returns an address value.
        @param form the format of the numeric value
        @param value raw offset or indirect address index (depending on the DWARFForm)
        @param cu {@link DWARFCompilationUnit}
        @return address
        @throws IOException if error reading indirect lookup tables
        """
        ...

    def getAddressRange(self, range: ghidra.app.util.bin.format.dwarf.DWARFRange, isCode: bool) -> ghidra.program.model.address.AddressRange: ...

    @overload
    def getAggregate(self, dieOffset: long) -> ghidra.app.util.bin.format.dwarf.DIEAggregate:
        """
        Returns the {@link DIEAggregate} that contains the {@link DebugInfoEntry} specified
         by the offset.
        @param dieOffset offset of a DIE record
        @return {@link DIEAggregate} that contains the DIE record specified, or null if bad
         offset.
        """
        ...

    @overload
    def getAggregate(self, die: ghidra.app.util.bin.format.dwarf.DebugInfoEntry) -> ghidra.app.util.bin.format.dwarf.DIEAggregate:
        """
        Returns the {@link DIEAggregate} that contains the specified {@link DebugInfoEntry}.
        @param die {@link DebugInfoEntry} or null
        @return {@link DIEAggregate} that contains the specified DIE, or null if DIE null or
         the aggregate was not found.
        """
        ...

    def getChildrenOf(self, dieIndex: int) -> List[ghidra.app.util.bin.format.dwarf.DebugInfoEntry]:
        """
        Returns the children of the specified DIE
        @param dieIndex index of a DIE record
        @return list of DIE instances that are children of the specified DIE
        """
        ...

    def getClass(self) -> java.lang.Class: ...

    def getCodeAddress(self, offset: long) -> ghidra.program.model.address.Address: ...

    def getCompilationUnits(self) -> List[ghidra.app.util.bin.format.dwarf.DWARFCompilationUnit]: ...

    def getDIEByOffset(self, dieOffset: long) -> ghidra.app.util.bin.format.dwarf.DebugInfoEntry:
        """
        Returns the specified DIE record.
        @param dieOffset offset of a DIE record
        @return {@link DebugInfoEntry} instance, or null if invalid offset
        """
        ...

    def getDIEChildIndexes(self, dieIndex: int) -> ghidra.util.datastruct.IntArrayList:
        """
        Returns list of indexes of the children of the specified DIE
        @param dieIndex index of a DIE record
        @return list of DIE indexes that are children of the specified DIE
        """
        ...

    def getDataAddress(self, offset: long) -> ghidra.program.model.address.Address: ...

    def getDebugLineBR(self) -> ghidra.app.util.bin.BinaryReader: ...

    def getDefaultIntSize(self) -> int: ...

    def getDwarfDTM(self) -> ghidra.app.util.bin.format.dwarf.DWARFDataTypeManager: ...

    def getEntryName(self, diea: ghidra.app.util.bin.format.dwarf.DIEAggregate) -> unicode: ...

    def getFunctionFixups(self) -> List[ghidra.app.util.bin.format.dwarf.funcfixup.DWARFFunctionFixup]: ...

    def getGhidraProgram(self) -> ghidra.program.model.listing.Program: ...

    def getImportOptions(self) -> ghidra.app.util.bin.format.dwarf.DWARFImportOptions: ...

    def getImportSummary(self) -> ghidra.app.util.bin.format.dwarf.DWARFImportSummary: ...

    def getLine(self, diea: ghidra.app.util.bin.format.dwarf.DIEAggregate, attribute: ghidra.app.util.bin.format.dwarf.attribs.DWARFAttribute) -> ghidra.app.util.bin.format.dwarf.line.DWARFLine:
        """
        Returns the DWARFLine info pointed to by the specified attribute.
        @param diea {@link DIEAggregate}
        @param attribute attribute id that points to the line info
        @return {@link DWARFLine}, never null, see {@link DWARFLine#empty()}
        @throws IOException if error reading line data
        """
        ...

    def getLocationList(self, diea: ghidra.app.util.bin.format.dwarf.DIEAggregate, attribute: ghidra.app.util.bin.format.dwarf.attribs.DWARFAttribute) -> ghidra.app.util.bin.format.dwarf.DWARFLocationList:
        """
        Returns the {@link DWARFLocationList} pointed to by the specified attribute value.
        @param diea {@link DIEAggregate}
        @param attribute attribute id that points to the location list
        @return {@link DWARFLocationList}, never null
        @throws IOException if specified attribute is not the correct type, or if other error reading
         data
        """
        ...

    def getName(self, diea: ghidra.app.util.bin.format.dwarf.DIEAggregate) -> ghidra.app.util.bin.format.dwarf.DWARFName:
        """
        Returns a {@link DWARFName} for a {@link DIEAggregate}.
        @param diea {@link DIEAggregate}
        @return {@link DWARFName}, never null
        """
        ...

    def getOffsetOfIndexedElement(self, form: ghidra.app.util.bin.format.dwarf.attribs.DWARFForm, index: int, cu: ghidra.app.util.bin.format.dwarf.DWARFCompilationUnit) -> long:
        """
        Returns the raw offset of an indexed item.  For DW_FORM_addrx values, the returned value
         is not fixed up with Ghidra load offset.
        @param form {@link DWARFForm} of the index
        @param index int index into a lookup table (see {@link #addressListTable}, 
         {@link #locationListTable}, {@link #rangeListTable}, {@link #stringsOffsetTable})
        @param cu {@link DWARFCompilationUnit}
        @return raw offset of indexed item
        @throws IOException if error reading index table
        """
        ...

    def getParentDepth(self, dieIndex: int) -> int:
        """
        Returns the depth of the specified DIE.
        @param dieIndex index of a DIE record
        @return parent/child depth of specified record, where 0 is the root DIE
        """
        ...

    def getParentIndex(self, dieIndex: int) -> int:
        """
        Returns the index of the parent of the specified DIE.
        @param dieIndex index of a DIE record
        @return index of the parent of specified DIE, or -1 if no parent (eg. root DIE)
        """
        ...

    def getParentOf(self, dieIndex: int) -> ghidra.app.util.bin.format.dwarf.DebugInfoEntry:
        """
        Returns the parent DIE of the specified (by index) DIE
        @param dieIndex index of a DIE record
        @return parent DIE, or null if no parent (eg. root DIE)
        """
        ...

    def getProgramBaseAddressFixup(self) -> long:
        """
        A fixup value that needs to be applied to static addresses of the program.
         <p>
         This value is necessary if the program's built-in base address is overridden at import time.
         <p>
        @return long value to add to static addresses discovered in DWARF to make it agree with
         Ghidra's imported program.
        """
        ...

    def getRangeList(self, diea: ghidra.app.util.bin.format.dwarf.DIEAggregate, attribute: ghidra.app.util.bin.format.dwarf.attribs.DWARFAttribute) -> ghidra.app.util.bin.format.dwarf.DWARFRangeList:
        """
        Returns the {@link DWARFRangeList} pointed at by the specified attribute.
        @param diea {@link DIEAggregate}
        @param attribute attribute id to find in the DIEA
        @return {@link DWARFRangeList}, or null if attribute is not present
        @throws IOException if error reading range list
        """
        ...

    def getReaderForCompUnit(self, cu: ghidra.app.util.bin.format.dwarf.DWARFCompilationUnit) -> ghidra.app.util.bin.BinaryReader: ...

    @staticmethod
    def getReferringTypedef(diea: ghidra.app.util.bin.format.dwarf.DIEAggregate) -> ghidra.app.util.bin.format.dwarf.DIEAggregate:
        """
        Returns the {@link DIEAggregate} of a typedef that points to the specified datatype.
         <p>
         Returns null if there is no typedef pointing to the specified DIEA or if there are
         multiple.
        @param diea {@link DIEAggregate} of a data type that might be the target of typedefs.
        @return {@link DIEAggregate} of the singular typedef that points to the arg, otherwise
         null if none or multiple found.
        """
        ...

    def getRegisterMappings(self) -> ghidra.app.util.bin.format.dwarf.DWARFRegisterMappings: ...

    def getRootDNI(self) -> ghidra.app.util.bin.format.dwarf.DWARFName: ...

    def getStackSpace(self) -> ghidra.program.model.address.AddressSpace: ...

    def getString(self, form: ghidra.app.util.bin.format.dwarf.attribs.DWARFForm, offset: long, cu: ghidra.app.util.bin.format.dwarf.DWARFCompilationUnit) -> unicode:
        """
        Returns a DWARF attribute string value, as specified by a form, offset/index, and the cu.
        @param form {@link DWARFForm}
        @param offset offset or index of the value
        @param cu {@link DWARFCompilationUnit}
        @return String value, never null
        @throws IOException if invalid form or bad offset/index
        """
        ...

    def getTotalAggregateCount(self) -> int:
        """
        Returns the total number of {@link DIEAggregate} objects in the entire program.
        @return the total number of {@link DIEAggregate} objects in the entire program.
        """
        ...

    def getTypeReferers(self, targetDIEA: ghidra.app.util.bin.format.dwarf.DIEAggregate, tag: ghidra.app.util.bin.format.dwarf.DWARFTag) -> List[ghidra.app.util.bin.format.dwarf.DIEAggregate]:
        """
        Returns a list of {@link DIEAggregate}s that refer to the targetDIEA via an
         attribute of the specified tag type.
        @param targetDIEA {@link DIEAggregate} that might be pointed to by other DIEAs.
        @param tag the {@link DWARFTag} attribute type that is pointing DIEAs are using
         to refer to the target DIEA.
        @return list of DIEAs that point to the target, empty list if nothing found.
        """
        ...

    def getUncategorizedRootDNI(self) -> ghidra.app.util.bin.format.dwarf.DWARFName: ...

    @staticmethod
    def hasDWARFData(program: ghidra.program.model.listing.Program, monitor: ghidra.util.task.TaskMonitor) -> bool:
        """
        Returns true if the specified {@link Program program} has DWARF information.
         <p>
         This is similar to {@link #isDWARF(Program)}, but is a stronger check that is more
         expensive as it could involve searching for external files.
         <p>
        @param program {@link Program} to test
        @param monitor {@link TaskMonitor} that can be used to cancel
        @return boolean true if the program has DWARF info, false if not
        """
        ...

    def hashCode(self) -> int: ...

    def init(self, monitor: ghidra.util.task.TaskMonitor) -> None:
        """
        Reads and indexes available DWARF information.
        @param monitor {@link TaskMonitor}
        @throws IOException if error reading data
        @throws DWARFException if bad or invalid DWARF information
        @throws CancelledException if cancelled
        """
        ...

    def internAttributeSpec(self, das: ghidra.app.util.bin.format.dwarf.attribs.DWARFAttribute.AttrDef) -> ghidra.app.util.bin.format.dwarf.attribs.DWARFAttribute.AttrDef: ...

    def isBigEndian(self) -> bool: ...

    @staticmethod
    def isDWARF(program: ghidra.program.model.listing.Program) -> bool:
        """
        Returns true if the {@link Program program} probably has DWARF information, without doing
         all the work that querying all registered DWARFSectionProviders would take.
         <p>
         If the program is an Elf binary, it must have (at least) ".debug_info" and ".debug_abbr",
         program sections, or their compressed "z" versions, or ExternalDebugInfo that would point
         to an external DWARF file.
         <p>
         If the program is a MachO binary (Mac), it must have a ".dSYM" directory co-located 
         next to the original binary file on the native filesystem (outside of Ghidra).  See the 
         DSymSectionProvider for more info.
         <p>
        @param program {@link Program} to test
        @return boolean true if program probably has DWARF info, false if not
        """
        ...

    def isLittleEndian(self) -> bool: ...

    def logWarningAt(self, addr: ghidra.program.model.address.Address, addrName: unicode, msg: unicode) -> None: ...

    def notify(self) -> None: ...

    def notifyAll(self) -> None: ...

    def setStringTable(self, st: ghidra.app.util.bin.format.dwarf.StringTable) -> None: ...

    def stackGrowsNegative(self) -> bool: ...

    def toString(self) -> unicode: ...

    @overload
    def wait(self) -> None: ...

    @overload
    def wait(self, __a0: long) -> None: ...

    @overload
    def wait(self, __a0: long, __a1: int) -> None: ...

    @property
    def bigEndian(self) -> bool: ...

    @property
    def compilationUnits(self) -> List[object]: ...

    @property
    def debugLineBR(self) -> ghidra.app.util.bin.BinaryReader: ...

    @property
    def defaultIntSize(self) -> int: ...

    @property
    def dwarfDTM(self) -> ghidra.app.util.bin.format.dwarf.DWARFDataTypeManager: ...

    @property
    def functionFixups(self) -> List[object]: ...

    @property
    def ghidraProgram(self) -> ghidra.program.model.listing.Program: ...

    @property
    def importOptions(self) -> ghidra.app.util.bin.format.dwarf.DWARFImportOptions: ...

    @property
    def importSummary(self) -> ghidra.app.util.bin.format.dwarf.DWARFImportSummary: ...

    @property
    def littleEndian(self) -> bool: ...

    @property
    def programBaseAddressFixup(self) -> long: ...

    @property
    def registerMappings(self) -> ghidra.app.util.bin.format.dwarf.DWARFRegisterMappings: ...

    @property
    def rootDNI(self) -> ghidra.app.util.bin.format.dwarf.DWARFName: ...

    @property
    def stackSpace(self) -> ghidra.program.model.address.AddressSpace: ...

    @property
    def stringTable(self) -> None: ...  # No getter available.

    @stringTable.setter
    def stringTable(self, value: ghidra.app.util.bin.format.dwarf.StringTable) -> None: ...

    @property
    def totalAggregateCount(self) -> int: ...

    @property
    def uncategorizedRootDNI(self) -> ghidra.app.util.bin.format.dwarf.DWARFName: ...