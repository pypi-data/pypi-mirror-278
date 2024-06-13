from typing import List
from typing import overload
import ghidra.framework.model
import ghidra.program.model.address
import ghidra.program.model.listing
import ghidra.program.util
import ghidra.program.util.FunctionChangeRecord
import java.lang
import java.util


class FunctionChangeRecord(ghidra.program.util.ProgramChangeRecord):





    class FunctionChangeType(java.lang.Enum):
        CALL_FIXUP_CHANGED: ghidra.program.util.FunctionChangeRecord.FunctionChangeType
        INLINE_CHANGED: ghidra.program.util.FunctionChangeRecord.FunctionChangeType
        NO_RETURN_CHANGED: ghidra.program.util.FunctionChangeRecord.FunctionChangeType
        PARAMETERS_CHANGED: ghidra.program.util.FunctionChangeRecord.FunctionChangeType
        PURGE_CHANGED: ghidra.program.util.FunctionChangeRecord.FunctionChangeType
        RETURN_TYPE_CHANGED: ghidra.program.util.FunctionChangeRecord.FunctionChangeType
        THUNK_CHANGED: ghidra.program.util.FunctionChangeRecord.FunctionChangeType
        UNSPECIFIED: ghidra.program.util.FunctionChangeRecord.FunctionChangeType







        @overload
        def compareTo(self, __a0: java.lang.Enum) -> int: ...

        @overload
        def compareTo(self, __a0: object) -> int: ...

        def describeConstable(self) -> java.util.Optional: ...

        def equals(self, __a0: object) -> bool: ...

        def getClass(self) -> java.lang.Class: ...

        def getDeclaringClass(self) -> java.lang.Class: ...

        def hashCode(self) -> int: ...

        def name(self) -> unicode: ...

        def notify(self) -> None: ...

        def notifyAll(self) -> None: ...

        def ordinal(self) -> int: ...

        def toString(self) -> unicode: ...

        @overload
        @staticmethod
        def valueOf(__a0: unicode) -> ghidra.program.util.FunctionChangeRecord.FunctionChangeType: ...

        @overload
        @staticmethod
        def valueOf(__a0: java.lang.Class, __a1: unicode) -> java.lang.Enum: ...

        @staticmethod
        def values() -> List[ghidra.program.util.FunctionChangeRecord.FunctionChangeType]: ...

        @overload
        def wait(self) -> None: ...

        @overload
        def wait(self, __a0: long) -> None: ...

        @overload
        def wait(self, __a0: long, __a1: int) -> None: ...



    def __init__(self, function: ghidra.program.model.listing.Function, changeType: ghidra.program.util.FunctionChangeRecord.FunctionChangeType):
        """
        Constructs a new Function change record.
        @param function the function that was changed
        @param changeType the specific type of change that was applied to the function
        """
        ...



    def equals(self, __a0: object) -> bool: ...

    def getClass(self) -> java.lang.Class: ...

    def getEnd(self) -> ghidra.program.model.address.Address:
        """
        Get the end address of the affected addresses of this change or null if not applicable.
        @return the end address of the effected address of this change
        """
        ...

    def getEventType(self) -> ghidra.framework.model.EventType:
        """
        Returns the event type for this change.
        @return the event type for this change
        """
        ...

    def getFunction(self) -> ghidra.program.model.listing.Function:
        """
        Returns the function that was changed.
        @return the function that was changed
        """
        ...

    def getNewValue(self) -> object:
        """
        Return the new value for this event or null if not applicable.
        @return the old value or null if not applicable for this event.
        """
        ...

    def getObject(self) -> object:
        """
        Return the object that is the subject of this change record.
        @return the object affected or null if not applicable
        """
        ...

    def getOldValue(self) -> object:
        """
        Return the old value for this event or null if not applicable.
        @return the old value or null if not applicable
        """
        ...

    def getSpecificChangeType(self) -> ghidra.program.util.FunctionChangeRecord.FunctionChangeType:
        """
        Returns the specific type of function change.
        @return the specific type of function change
        """
        ...

    def getStart(self) -> ghidra.program.model.address.Address:
        """
        Get the start address of the affected addresses of this change or null if not applicable.
        @return the start address of the effected address of this change
        """
        ...

    def hashCode(self) -> int: ...

    def isFunctionModifierChange(self) -> bool:
        """
        Returns true if the specific change was to one of the function's modifier properties.
        @return true if the specific change was to one of the function's modifier properties
        """
        ...

    def isFunctionSignatureChange(self) -> bool:
        """
        Returns true if the specific change was related to the function signature.
        @return true if the specific change was related to the function signature
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

    @property
    def function(self) -> ghidra.program.model.listing.Function: ...

    @property
    def functionModifierChange(self) -> bool: ...

    @property
    def functionSignatureChange(self) -> bool: ...

    @property
    def specificChangeType(self) -> ghidra.program.util.FunctionChangeRecord.FunctionChangeType: ...