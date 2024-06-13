from typing import overload
import ghidra.app.plugin.processors.sleigh
import ghidra.pcode.emu.sys
import ghidra.pcode.exec
import ghidra.pcode.exec.PcodeUseropLibrary
import ghidra.program.model.lang
import ghidra.program.model.listing
import java.lang
import java.lang.annotation
import java.lang.reflect
import java.util


class AnnotatedEmuSyscallUseropLibrary(ghidra.pcode.exec.AnnotatedPcodeUseropLibrary, ghidra.pcode.emu.sys.EmuSyscallLibrary):
    """
    A syscall library wherein Java methods are exported via a special annotated
 
 
     This library is both a system call and a sleigh userop library. To export a system call, it must
     also be exported as a sleigh userop. This is more conventional, as the system call dispatcher
     does not require it, however, this library uses a wrapping technique that does require it. In
     general, exporting system calls as userops will make developers and users lives easier. To avoid
     naming collisions, system calls can be exported with customized names.
    """

    SYSCALL_SPACE_NAME: unicode = u'syscall'




    class EmuSyscall(java.lang.annotation.Annotation, object):








        def annotationType(self) -> java.lang.Class: ...

        def equals(self, __a0: object) -> bool: ...

        def getClass(self) -> java.lang.Class: ...

        def hashCode(self) -> int: ...

        def notify(self) -> None: ...

        def notifyAll(self) -> None: ...

        def toString(self) -> unicode: ...

        def value(self) -> unicode: ...

        @overload
        def wait(self) -> None: ...

        @overload
        def wait(self, __a0: long) -> None: ...

        @overload
        def wait(self, __a0: long, __a1: int) -> None: ...



    def __init__(self, machine: ghidra.pcode.emu.PcodeMachine, program: ghidra.program.model.listing.Program):
        """
        Construct a new library including the "syscall" userop
        @param machine the machine using this library
        @param program a program from which to derive syscall configuration, conventions, etc.
        """
        ...



    def compose(self, __a0: ghidra.pcode.exec.PcodeUseropLibrary) -> ghidra.pcode.exec.PcodeUseropLibrary: ...

    def equals(self, __a0: object) -> bool: ...

    def getClass(self) -> java.lang.Class: ...

    @staticmethod
    def getOperandType(__a0: java.lang.Class) -> java.lang.reflect.Type: ...

    def getSymbols(self, __a0: ghidra.app.plugin.processors.sleigh.SleighLanguage) -> java.util.Map: ...

    def getSyscallUserop(self) -> ghidra.pcode.exec.PcodeUseropLibrary.PcodeUseropDefinition: ...

    def getSyscalls(self) -> java.util.Map: ...

    def getUserops(self) -> java.util.Map: ...

    def handleError(self, __a0: ghidra.pcode.exec.PcodeExecutor, __a1: ghidra.pcode.exec.PcodeExecutionException) -> bool: ...

    def hashCode(self) -> int: ...

    @staticmethod
    def loadSyscallConventionMap(__a0: ghidra.program.model.listing.Program) -> java.util.Map: ...

    @staticmethod
    def loadSyscallFunctionMap(__a0: ghidra.program.model.listing.Program) -> java.util.Map: ...

    @overload
    @staticmethod
    def loadSyscallNumberMap(__a0: unicode) -> java.util.Map: ...

    @overload
    @staticmethod
    def loadSyscallNumberMap(__a0: ghidra.program.model.listing.Program) -> java.util.Map: ...

    def newBoundSyscall(self, opdef: ghidra.pcode.exec.PcodeUseropLibrary.PcodeUseropDefinition, convention: ghidra.program.model.lang.PrototypeModel) -> ghidra.pcode.emu.sys.UseropEmuSyscallDefinition:
        """
        Export a userop as a system call
        @param opdef the userop
        @return the syscall definition
        """
        ...

    @staticmethod
    def nil() -> ghidra.pcode.exec.PcodeUseropLibrary: ...

    def notify(self) -> None: ...

    def notifyAll(self) -> None: ...

    def readSyscallNumber(self, __a0: ghidra.pcode.exec.PcodeExecutorState, __a1: ghidra.pcode.exec.PcodeExecutorStatePiece.Reason) -> long: ...

    def syscall(self, __a0: ghidra.pcode.exec.PcodeExecutor, __a1: ghidra.pcode.exec.PcodeUseropLibrary) -> None: ...

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