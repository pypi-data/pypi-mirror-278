from typing import List
from typing import overload
import ghidra.app.plugin.processors.sleigh
import ghidra.pcode.exec
import ghidra.pcode.exec.PcodeExecutorStatePiece
import ghidra.pcode.exec.PcodeUseropLibrary
import ghidra.program.model.listing
import ghidra.program.model.pcode
import java.lang
import java.lang.reflect
import java.util


class EmuSyscallLibrary(ghidra.pcode.exec.PcodeUseropLibrary, object):
    """
    A library of system calls

 
     A system call library is a collection of p-code executable routines, invoked by a system call
     dispatcher. That dispatcher is represented by
     #syscall(PcodeExecutor, PcodeUseropLibrary), and is exported as a sleigh userop. If this
     interface is "mixed in" with AnnotatedPcodeUseropLibrary, that userop is automatically
     included in the userop library. The simplest means of implementing a syscall library is probably
     via AnnotatedEmuSyscallUseropLibrary. It implements this interface and extends
     AnnotatedPcodeUseropLibrary. In addition, it provides its own annotation system for
     exporting userops as system calls.
    """

    NIL: ghidra.pcode.exec.PcodeUseropLibrary
    SYSCALL_CONVENTION_NAME: unicode = u'syscall'
    SYSCALL_SPACE_NAME: unicode = u'syscall'




    class EmuSyscallDefinition(object):








        def equals(self, __a0: object) -> bool: ...

        def getClass(self) -> java.lang.Class: ...

        def hashCode(self) -> int: ...

        def invoke(self, __a0: ghidra.pcode.exec.PcodeExecutor, __a1: ghidra.pcode.exec.PcodeUseropLibrary) -> None: ...

        def notify(self) -> None: ...

        def notifyAll(self) -> None: ...

        def toString(self) -> unicode: ...

        @overload
        def wait(self) -> None: ...

        @overload
        def wait(self, __a0: long) -> None: ...

        @overload
        def wait(self, __a0: long, __a1: int) -> None: ...






    class SyscallPcodeUseropDefinition(object, ghidra.pcode.exec.PcodeUseropLibrary.PcodeUseropDefinition):




        def __init__(self, __a0: ghidra.pcode.emu.sys.EmuSyscallLibrary): ...



        def equals(self, __a0: object) -> bool: ...

        def execute(self, __a0: ghidra.pcode.exec.PcodeExecutor, __a1: ghidra.pcode.exec.PcodeUseropLibrary, __a2: ghidra.program.model.pcode.Varnode, __a3: List[object]) -> None: ...

        def getClass(self) -> java.lang.Class: ...

        def getInputCount(self) -> int: ...

        def getName(self) -> unicode: ...

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
        def inputCount(self) -> int: ...

        @property
        def name(self) -> unicode: ...





    def compose(self, __a0: ghidra.pcode.exec.PcodeUseropLibrary) -> ghidra.pcode.exec.PcodeUseropLibrary: ...

    def equals(self, __a0: object) -> bool: ...

    def getClass(self) -> java.lang.Class: ...

    @staticmethod
    def getOperandType(__a0: java.lang.Class) -> java.lang.reflect.Type: ...

    def getSymbols(self, __a0: ghidra.app.plugin.processors.sleigh.SleighLanguage) -> java.util.Map: ...

    def getSyscallUserop(self) -> ghidra.pcode.exec.PcodeUseropLibrary.PcodeUseropDefinition:
        """
        In case this is not an {@link AnnotatedEmuSyscallUseropLibrary} or
         {@link AnnotatedPcodeUseropLibrary}, get the definition of the "syscall" userop for inclusion
         in the {@link PcodeUseropLibrary}.
 
         <p>
         Implementors may wish to override this to use a pre-constructed definition. That definition
         can be easily constructed using {@link SyscallPcodeUseropDefinition}.
        @return the syscall userop definition
        """
        ...

    def getSyscalls(self) -> java.util.Map:
        """
        Get the map of syscalls by number
 
         <p>
         Note this method will be invoked for every emulated syscall, so it should be a simple
         accessor. Any computations needed to create the map should be done ahead of time.
        @return the system call map
        """
        ...

    def getUserops(self) -> java.util.Map: ...

    def handleError(self, executor: ghidra.pcode.exec.PcodeExecutor, err: ghidra.pcode.exec.PcodeExecutionException) -> bool:
        """
        Try to handle an error, usually by returning it to the user program
 
         <p>
         If the particular error was not expected, it is best practice to return false, causing the
         emulator to interrupt. Otherwise, some state is set in the machine that, by convention,
         communicates the error back to the user program.
        @param executor the executor for the thread that caused the error
        @param err the error
        @return true if execution can continue uninterrupted
        """
        ...

    def hashCode(self) -> int: ...

    @staticmethod
    def loadSyscallConventionMap(program: ghidra.program.model.listing.Program) -> java.util.Map:
        """
        Derive a syscall number to calling convention map by scraping functions in the program's
         "syscall" space.
        @param program
        @return 
        """
        ...

    @staticmethod
    def loadSyscallFunctionMap(program: ghidra.program.model.listing.Program) -> java.util.Map:
        """
        Scrape functions from the given program's "syscall" space.
        @param program the program
        @return a map of syscall number to function
        """
        ...

    @overload
    @staticmethod
    def loadSyscallNumberMap(dataFileName: unicode) -> java.util.Map:
        """
        Derive a syscall number to name map from the specification in a given file.
        @param dataFileName the file name to be found in a modules data directory
        @return the map
        @throws IOException if the file could not be read
        """
        ...

    @overload
    @staticmethod
    def loadSyscallNumberMap(program: ghidra.program.model.listing.Program) -> java.util.Map:
        """
        Derive a syscall number to name map by scraping functions in the program's "syscall" space.
        @param program the program, likely analyzed for system calls already
        @return the map
        """
        ...

    @staticmethod
    def nil() -> ghidra.pcode.exec.PcodeUseropLibrary: ...

    def notify(self) -> None: ...

    def notifyAll(self) -> None: ...

    def readSyscallNumber(self, state: ghidra.pcode.exec.PcodeExecutorState, reason: ghidra.pcode.exec.PcodeExecutorStatePiece.Reason) -> long:
        """
        Retrieve the desired system call number according to the emulated system's conventions
 
         <p>
         TODO: This should go away in favor of some specification stored in the emulated program
         database. Until then, we require system-specific implementations.
        @param state the executor's state
        @param reason the reason for reading state, probably {@link Reason#EXECUTE_READ}, but should
                    be taken from the executor
        @return the system call number
        """
        ...

    def syscall(self, executor: ghidra.pcode.exec.PcodeExecutor, library: ghidra.pcode.exec.PcodeUseropLibrary) -> None:
        """
        The entry point for executing a system call on the given executor
 
         <p>
         The executor's state must already be prepared according to the relevant system calling
         conventions. This will determine the system call number, according to
         {@link #readSyscallNumber(PcodeExecutorState, Reason)}, retrieve the relevant system call
         definition, and invoke it.
        @param executor the executor
        @param library the library
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
    def syscallUserop(self) -> ghidra.pcode.exec.PcodeUseropLibrary.PcodeUseropDefinition: ...

    @property
    def syscalls(self) -> java.util.Map: ...

    @property
    def userops(self) -> java.util.Map: ...