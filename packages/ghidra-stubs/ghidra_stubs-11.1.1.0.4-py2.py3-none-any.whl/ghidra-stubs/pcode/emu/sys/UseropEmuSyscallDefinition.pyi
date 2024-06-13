from typing import overload
import ghidra.pcode.emu.sys
import ghidra.pcode.exec
import java.lang


class UseropEmuSyscallDefinition(object, ghidra.pcode.emu.sys.EmuSyscallLibrary.EmuSyscallDefinition):
    """
    A system call that is defined by delegating to a p-code userop
 
 
     This is essentially a wrapper of the p-code userop. Knowing the number of inputs to the userop
     and by applying the calling conventions of the platform, the wrapper aliases each parameter's
     storage to its respective parameter of the userop. The userop's output is also aliased to the
     system call's return storage, again as defined by the platform's conventions.
    """





    def __init__(self, opdef: ghidra.pcode.exec.PcodeUseropLibrary.PcodeUseropDefinition, program: ghidra.program.model.listing.Program, convention: ghidra.program.model.lang.PrototypeModel, dtMachineWord: ghidra.program.model.data.DataType):
        """
        Construct a syscall definition
        @see AnnotatedEmuSyscallUseropLibrary
        @param opdef the wrapped userop definition
        @param program the program, used for storage computation
        @param convention the "syscall" calling convention
        @param dtMachineWord the "pointer" data type
        """
        ...



    def equals(self, __a0: object) -> bool: ...

    def getClass(self) -> java.lang.Class: ...

    def hashCode(self) -> int: ...

    def invoke(self, executor: ghidra.pcode.exec.PcodeExecutor, library: ghidra.pcode.exec.PcodeUseropLibrary) -> None: ...

    def notify(self) -> None: ...

    def notifyAll(self) -> None: ...

    def toString(self) -> unicode: ...

    @overload
    def wait(self) -> None: ...

    @overload
    def wait(self, __a0: long) -> None: ...

    @overload
    def wait(self, __a0: long, __a1: int) -> None: ...

