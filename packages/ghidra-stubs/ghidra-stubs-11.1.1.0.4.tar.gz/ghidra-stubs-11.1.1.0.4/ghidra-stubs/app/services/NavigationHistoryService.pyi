from typing import List
from typing import overload
import ghidra.app.nav
import ghidra.program.model.listing
import java.lang


class NavigationHistoryService(object):
    """
    The NavigationHistoryService maintains a stack of locations that the user has visited via a
     navigation plugin. It provides methods querying and manipulating this list.
    """









    def addNewLocation(self, navigatable: ghidra.app.nav.Navigatable) -> None:
        """
        Adds the current location memento to the list of previous locations for the given
         navigatable. Clears the list of next locations.
        @param navigatable the navigatable to be navigated
        """
        ...

    @overload
    def clear(self, navigatable: ghidra.app.nav.Navigatable) -> None:
        """
        Removes all visited locations from the history list for the given navigatable
        @param navigatable the navigatable whose list to be cleared
        """
        ...

    @overload
    def clear(self, program: ghidra.program.model.listing.Program) -> None:
        """
        Removes all entries for the given program from all history lists
        @param program the program whose entries to be cleared
        """
        ...

    def equals(self, __a0: object) -> bool: ...

    def getClass(self) -> java.lang.Class: ...

    def getNextLocations(self, navigatable: ghidra.app.nav.Navigatable) -> List[ghidra.app.nav.LocationMemento]:
        """
        Returns the {@link LocationMemento} objects in the "next" list
        @param navigatable the navigatable to be navigated
        @return the LocationMemento objects in the "next" list
        """
        ...

    def getPreviousLocations(self, navigatable: ghidra.app.nav.Navigatable) -> List[ghidra.app.nav.LocationMemento]:
        """
        Returns the {@link LocationMemento} objects in the "previous" list
        @param navigatable the navigatable to be navigated
        @return the LocationMemento objects in the "previous" list
        """
        ...

    def hasNext(self, navigatable: ghidra.app.nav.Navigatable) -> bool:
        """
        Returns true if there is a valid "next" location in the history list.
        @param navigatable the navigatable to be navigated
        @return true if there is a "next" location
        """
        ...

    def hasNextFunction(self, navigatable: ghidra.app.nav.Navigatable) -> bool:
        """
        Returns true if there is a valid "next" function location in the history list
        @param navigatable Navigatable object we are looking at
        @return true if there is a valid "next" function location
        """
        ...

    def hasPrevious(self, navigatable: ghidra.app.nav.Navigatable) -> bool:
        """
        Returns true if there is a valid "previous" location in the history list
        @param navigatable the navigatable to be navigated
        @return true if there is a "previous" location
        """
        ...

    def hasPreviousFunction(self, navigatable: ghidra.app.nav.Navigatable) -> bool:
        """
        Returns true if there is a valid "previous" function location in the history list
        @param navigatable Navigatable object we are looking at
        @return true if there is a valid "previous" function location
        """
        ...

    def hashCode(self) -> int: ...

    @overload
    def next(self, navigatable: ghidra.app.nav.Navigatable) -> None:
        """
        Positions the current location to the next location in the history list. If there is no
         "next" location, the history list remains unchanged.
        @param navigatable the navigatable to be navigated
        """
        ...

    @overload
    def next(self, navigatable: ghidra.app.nav.Navigatable, location: ghidra.app.nav.LocationMemento) -> None:
        """
        Navigates to the given location in the "next" list. If the location is not in the list, then
         nothing will happen.
        @param navigatable the navigatable to be navigated
        @param location The location within the "next" list to which to go
        """
        ...

    def nextFunction(self, navigatable: ghidra.app.nav.Navigatable) -> None:
        """
        Positions the "current" location to the next location which is in a different function from
         current one or previous non-code location. If we are not inside any function, performs like
         "next".
        @param navigatable the navigatable to be navigated
        """
        ...

    def notify(self) -> None: ...

    def notifyAll(self) -> None: ...

    @overload
    def previous(self, navigatable: ghidra.app.nav.Navigatable) -> None:
        """
        Positions the "current" location to the previous location in the history list. If there is no
         "previous" location, the history list remains unchanged.
        @param navigatable the navigatable to be navigated
        """
        ...

    @overload
    def previous(self, navigatable: ghidra.app.nav.Navigatable, location: ghidra.app.nav.LocationMemento) -> None:
        """
        Navigates to the given location in the "previous" list. If the location is not in the list,
         then nothing will happen
        @param navigatable the navigatable to be navigated
        @param location The location within the "previous" list to which to go.
        """
        ...

    def previousFunction(self, navigatable: ghidra.app.nav.Navigatable) -> None:
        """
        Positions the "previous" location to the next location which is in a different function from
         current one or previous non-code location. If we are not inside any function, performs like
         "next".
        @param navigatable the navigatable to be navigated
        """
        ...

    def toString(self) -> unicode: ...

    @overload
    def wait(self) -> None: ...

    @overload
    def wait(self, __a0: long) -> None: ...

    @overload
    def wait(self, __a0: long, __a1: int) -> None: ...

