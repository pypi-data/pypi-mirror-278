from typing import overload
import ghidra.app.plugin.processors.sleigh
import ghidra.pcode.emu.linux
import ghidra.pcode.emu.sys
import ghidra.pcode.emu.unix
import ghidra.pcode.exec
import ghidra.pcode.exec.PcodeExecutorStatePiece
import ghidra.pcode.exec.PcodeUseropLibrary
import ghidra.program.model.lang
import ghidra.program.model.listing
import java.lang
import java.lang.reflect
import java.util


class EmuLinuxAmd64SyscallUseropLibrary(ghidra.pcode.emu.linux.AbstractEmuLinuxSyscallUseropLibrary):
    """
    A system call library simulating Linux for amd64 / x86_64
    """





    @overload
    def __init__(self, machine: ghidra.pcode.emu.PcodeMachine, fs: ghidra.pcode.emu.unix.EmuUnixFileSystem, program: ghidra.program.model.listing.Program):
        """
        Construct the system call library for Linux-amd64
        @param machine the machine emulating the hardware
        @param fs the file system to export to the user-space program
        @param program a program containing syscall definitions and conventions, likely the target
                    program
        """
        ...

    @overload
    def __init__(self, machine: ghidra.pcode.emu.PcodeMachine, fs: ghidra.pcode.emu.unix.EmuUnixFileSystem, program: ghidra.program.model.listing.Program, user: ghidra.pcode.emu.unix.EmuUnixUser):
        """
        Construct the system call library for Linux-amd64
        @param machine the machine emulating the hardware
        @param fs the file system to export to the user-space program
        @param program a program containing syscall definitions and conventions, likely the target
                    program
        @param user the "current user" to simulate
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

    def handleError(self, executor: ghidra.pcode.exec.PcodeExecutor, err: ghidra.pcode.exec.PcodeExecutionException) -> bool: ...

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

    def putDescriptor(self, fd: int, desc: ghidra.pcode.emu.unix.EmuUnixFileDescriptor) -> ghidra.pcode.emu.unix.EmuUnixFileDescriptor:
        """
        Put a descriptor into the process' open file handles
        @param fd the file descriptor value
        @param desc the simulated descriptor (handle, console, etc.)
        @return the previous descriptor, which probably ought to be {@code null}
        """
        ...

    def readSyscallNumber(self, state: ghidra.pcode.exec.PcodeExecutorState, reason: ghidra.pcode.exec.PcodeExecutorStatePiece.Reason) -> long: ...

    def syscall(self, __a0: ghidra.pcode.exec.PcodeExecutor, __a1: ghidra.pcode.exec.PcodeUseropLibrary) -> None: ...

    def toString(self) -> unicode: ...

    def unix_close(self, fd: object) -> object:
        """
        The UNIX {@code close} system call
        @param fd the file descriptor
        @return 0 for success
        """
        ...

    def unix_exit(self, status: object) -> object:
        """
        The UNIX {@code exit} system call
 
         <p>
         This just throws an exception, which the overall simulator or script should catch.
        @param status the status code
        @return never
        @throws EmuProcessExitedException always
        """
        ...

    def unix_group_exit(self, status: object) -> None:
        """
        The UNIX {@code group_exit} system call
 
         <p>
         This just throws an exception, which the overall simulator or script should catch.
        @param status the status code
        @throws EmuProcessExitedException always
        """
        ...

    def unix_open(self, state: ghidra.pcode.exec.PcodeExecutorState, pathnamePtr: object, flags: object, mode: object) -> object:
        """
        The UNIX {@code open} system call
        @param state to receive the thread's state
        @param pathnamePtr the file's path (pointer to character string)
        @param flags the flags
        @param mode the mode
        @return the file descriptor
        """
        ...

    def unix_read(self, state: ghidra.pcode.exec.PcodeExecutorState, fd: object, bufPtr: object, count: object) -> object:
        """
        The UNIX {@code read} system call
        @param state to receive the thread's state
        @param fd the file descriptor
        @param bufPtr the pointer to the buffer to receive the data
        @param count the number of bytes to read
        @return the number of bytes successfully read
        """
        ...

    def unix_write(self, state: ghidra.pcode.exec.PcodeExecutorState, fd: object, bufPtr: object, count: object) -> object:
        """
        The UNIX {@code write} system call
        @param state to receive the thread's state
        @param fd the file descriptor
        @param bufPtr the pointer to the buffer of data to write
        @param count the number of bytes to write
        @return the number of bytes successfully written
        """
        ...

    @overload
    def wait(self) -> None: ...

    @overload
    def wait(self, __a0: long) -> None: ...

    @overload
    def wait(self, __a0: long, __a1: int) -> None: ...

