from typing import List
from typing import overload
import ghidra.app.plugin.assembler.sleigh.sem
import java.lang
import java.util


class AssemblyResolution(java.lang.Comparable, object):








    def collectAllRight(self, into: java.util.Collection) -> None: ...

    def compareTo(self, __a0: object) -> int: ...

    def equals(self, __a0: object) -> bool: ...

    def getChildren(self) -> List[ghidra.app.plugin.assembler.sleigh.sem.AssemblyResolution]: ...

    def getClass(self) -> java.lang.Class: ...

    def getDescription(self) -> unicode: ...

    def getRight(self) -> ghidra.app.plugin.assembler.sleigh.sem.AssemblyResolution: ...

    def hasChildren(self) -> bool:
        """
        Check if this record has children
 
         <p>
         If a subclass has another, possibly additional, notion of children that it would like to
         include in {@link #toString()}, it must override this method to return true when such
         children are present.
        @return true if this record has children
        """
        ...

    def hashCode(self) -> int: ...

    def isBackfill(self) -> bool:
        """
        Check if this record describes a backfill
        @return true if the record is a backfill
        """
        ...

    def isError(self) -> bool:
        """
        Check if this record describes an error
        @return true if the record is an error
        """
        ...

    def lineToString(self) -> unicode:
        """
        Display the resolution result in one line (omitting child details)
        @return the display description
        """
        ...

    def notify(self) -> None: ...

    def notifyAll(self) -> None: ...

    def parent(self, description: unicode, opCount: int) -> ghidra.app.plugin.assembler.sleigh.sem.AssemblyResolution:
        """
        Get this same resolution, pushing its right siblings down to its children
        """
        ...

    def shift(self, amt: int) -> ghidra.app.plugin.assembler.sleigh.sem.AssemblyResolution:
        """
        Shift the resolution's instruction pattern to the right, if applicable
 
         <p>
         This also shifts any backfill and forbidden pattern records.
        @param amt the number of bytes to shift.
        @return the result
        """
        ...

    @overload
    def toString(self) -> unicode:
        """
        {@inheritDoc}
 
         <p>
         Describe this record including indented children, grandchildren, etc., each on its own line.
        """
        ...

    @overload
    def toString(self, indent: unicode) -> unicode:
        """
        Used only by parents: get a multi-line description of this record, indented
        @param indent the current indentation
        @return the indented description
        """
        ...

    @overload
    def wait(self) -> None: ...

    @overload
    def wait(self, __a0: long) -> None: ...

    @overload
    def wait(self, __a0: long, __a1: int) -> None: ...

    @property
    def backfill(self) -> bool: ...

    @property
    def children(self) -> List[object]: ...

    @property
    def description(self) -> unicode: ...

    @property
    def error(self) -> bool: ...

    @property
    def right(self) -> ghidra.app.plugin.assembler.sleigh.sem.AssemblyResolution: ...