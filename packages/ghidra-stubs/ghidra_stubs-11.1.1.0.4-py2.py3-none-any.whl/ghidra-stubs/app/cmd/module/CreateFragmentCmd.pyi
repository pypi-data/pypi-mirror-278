from typing import overload
import ghidra.framework.cmd
import ghidra.framework.model
import ghidra.program.model.listing
import java.lang


class CreateFragmentCmd(object, ghidra.framework.cmd.Command):
    """
    Command to create a Fragment.
    """





    def __init__(self, treeName: unicode, name: unicode, parentName: unicode):
        """
        Construct a new CreateFragmentCmd.
        @param treeName name of the tree where the fragment will reside
        @param name name of the new Fragment
        @param parentName name of the module that is the parent of the fragment
        """
        ...



    @overload
    def applyTo(self, program: ghidra.program.model.listing.Program) -> bool:
        """
        Apply the command; if the name already exists, then the fragment 
         will not be created.
        @return false if the fragment was not created
        @see ghidra.framework.cmd.Command#applyTo(ghidra.framework.model.DomainObject)
        """
        ...

    @overload
    def applyTo(self, __a0: ghidra.framework.model.DomainObject) -> bool: ...

    def equals(self, __a0: object) -> bool: ...

    def getClass(self) -> java.lang.Class: ...

    def getName(self) -> unicode: ...

    def getStatusMsg(self) -> unicode: ...

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
    def name(self) -> unicode: ...

    @property
    def statusMsg(self) -> unicode: ...