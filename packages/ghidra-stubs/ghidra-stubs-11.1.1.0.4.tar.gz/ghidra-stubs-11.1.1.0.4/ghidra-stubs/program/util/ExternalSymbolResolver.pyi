from typing import overload
import ghidra.program.model.listing
import java.io
import java.lang
import java.util.function


class ExternalSymbolResolver(object, java.io.Closeable):
    """
    Moves dangling external function symbols found in the Library#UNKNOWN
     namespace into the namespace of the external library that publishes a matching symbol.
 
     This uses an ordered list of external library names that was attached to the program during
     import by the Elf or Macho loader (see #REQUIRED_LIBRARY_PROPERTY_PREFIX).
    """





    def __init__(self, projectData: ghidra.framework.model.ProjectData, monitor: ghidra.util.task.TaskMonitor): ...



    def addLoadedProgram(self, programPath: unicode, program: ghidra.program.model.listing.Program) -> None:
        """
        Adds an already opened program to this session, allowing it to be used as an external
         library without needing to look it up in the current project.
        @param programPath project path to already opened program
        @param program {@link Program}
        """
        ...

    @overload
    def addProgramToFixup(self, program: ghidra.program.model.listing.Program) -> None:
        """
        Queues a program into this session that will be fixed when {@link #fixUnresolvedExternalSymbols()}
         is called.
         <p>
         The program should be fully persisted to the project if using this method, otherwise use
         {@link #addProgramToFixup(String, Program)} and specify the pathname the program will 
         be saved to.
        @param program {@link Program} to fix
        """
        ...

    @overload
    def addProgramToFixup(self, programPath: unicode, program: ghidra.program.model.listing.Program) -> None:
        """
        Queues a program into this session that will be fixed when {@link #fixUnresolvedExternalSymbols()}
         is called.
        @param programPath string project path to the program
        @param program {@link Program} to fix
        """
        ...

    def close(self) -> None: ...

    def equals(self, __a0: object) -> bool: ...

    def fixUnresolvedExternalSymbols(self) -> None:
        """
        Resolves any unresolved external symbols in each program that has been queued up via
         {@link #addProgramToFixup(String, Program)}.
        @throws CancelledException if cancelled
        """
        ...

    def getClass(self) -> java.lang.Class: ...

    @staticmethod
    def getRequiredLibraryProperty(libraryIndex: int) -> unicode:
        """
        Gets a program property name to represent the ordered required library of the given index
        @param libraryIndex The index of the required library
        @return A program property name to represent the ordered required library of the given index
        """
        ...

    def hasProblemLibraries(self) -> bool:
        """
        Returns true if there was an error encountered when trying to open an external library.
        @return boolean flag, true if there was a problem opening an external library
        """
        ...

    def hashCode(self) -> int: ...

    def logInfo(self, logger: java.util.function.Consumer, shortSummary: bool) -> None:
        """
        Logs information about the libraries and symbols that were found during the fixup.
        @param logger consumer that will log a string
        @param shortSummary boolean flag, if true individual symbol names will be omitted
        """
        ...

    def notify(self) -> None: ...

    def notifyAll(self) -> None: ...

    def toString(self) -> unicode: ...

    @overload
    def wait(self) -> None: ...

    @overload
    def wait(self, __a0: long) -> None: ...

    @overload
    def wait(self, __a0: long, __a1: int) -> None: ...

