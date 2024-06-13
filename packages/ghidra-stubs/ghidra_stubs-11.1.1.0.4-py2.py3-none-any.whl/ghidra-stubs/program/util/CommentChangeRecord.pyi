from typing import overload
import ghidra.framework.model
import ghidra.program.model.address
import ghidra.program.util
import java.lang


class CommentChangeRecord(ghidra.program.util.ProgramChangeRecord):
    """
    Change record for comment changes
    """





    def __init__(self, commentType: int, address: ghidra.program.model.address.Address, oldValue: unicode, newValue: unicode):
        """
        Constructor
        @param commentType the type of comment (as defined in {@link CodeUnit})
        @param address the address of the comment change
        @param oldValue the old comment (may be null for a new comment)
        @param newValue the new comment (may be null if the comment was deleted)
        """
        ...



    def equals(self, __a0: object) -> bool: ...

    def getClass(self) -> java.lang.Class: ...

    def getCommentType(self) -> int:
        """
        Returns the comment type as defined in {@link CodeUnit}.
        @return the comment type
        """
        ...

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

    def getNewComment(self) -> unicode:
        """
        Returns the new comment or null if this is a result of deleting the comment.
        @return the new comment or null if this is a result of deleting the comment
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

    def getOldComment(self) -> unicode:
        """
        Returns the previous comment or null if there was no previous comment.
        @return the previous comment or null if there was no previous comment.
        """
        ...

    def getOldValue(self) -> object:
        """
        Return the old value for this event or null if not applicable.
        @return the old value or null if not applicable
        """
        ...

    def getStart(self) -> ghidra.program.model.address.Address:
        """
        Get the start address of the affected addresses of this change or null if not applicable.
        @return the start address of the effected address of this change
        """
        ...

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
    def commentType(self) -> int: ...

    @property
    def newComment(self) -> unicode: ...

    @property
    def oldComment(self) -> unicode: ...