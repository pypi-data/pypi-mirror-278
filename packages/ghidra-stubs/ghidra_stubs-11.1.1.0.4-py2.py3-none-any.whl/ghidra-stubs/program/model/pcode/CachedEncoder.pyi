from typing import overload
import ghidra.program.model.address
import ghidra.program.model.pcode
import java.io
import java.lang


class CachedEncoder(ghidra.program.model.pcode.Encoder, object):
    """
    An Encoder that holds its bytes in memory (where they can possibly be edited) and
     can then finally write them all to an OutputStream via a call to writeTo()
    """









    def clear(self) -> None:
        """
        Clear any state associated with the encoder
         The encoder should be ready to write a new document after this call.
        """
        ...

    def closeElement(self, __a0: ghidra.program.model.pcode.ElementId) -> None: ...

    def equals(self, __a0: object) -> bool: ...

    def getClass(self) -> java.lang.Class: ...

    def hashCode(self) -> int: ...

    def isEmpty(self) -> bool:
        """
        The encoder is considered empty if the writeTo() method would output zero bytes
        @return true if there are no bytes in the encoder
        """
        ...

    def notify(self) -> None: ...

    def notifyAll(self) -> None: ...

    def openElement(self, __a0: ghidra.program.model.pcode.ElementId) -> None: ...

    def toString(self) -> unicode: ...

    @overload
    def wait(self) -> None: ...

    @overload
    def wait(self, __a0: long) -> None: ...

    @overload
    def wait(self, __a0: long, __a1: int) -> None: ...

    def writeBool(self, __a0: ghidra.program.model.pcode.AttributeId, __a1: bool) -> None: ...

    def writeOpcode(self, __a0: ghidra.program.model.pcode.AttributeId, __a1: int) -> None: ...

    def writeSignedInteger(self, __a0: ghidra.program.model.pcode.AttributeId, __a1: long) -> None: ...

    @overload
    def writeSpace(self, __a0: ghidra.program.model.pcode.AttributeId, __a1: ghidra.program.model.address.AddressSpace) -> None: ...

    @overload
    def writeSpace(self, __a0: ghidra.program.model.pcode.AttributeId, __a1: int, __a2: unicode) -> None: ...

    def writeString(self, __a0: ghidra.program.model.pcode.AttributeId, __a1: unicode) -> None: ...

    def writeStringIndexed(self, __a0: ghidra.program.model.pcode.AttributeId, __a1: int, __a2: unicode) -> None: ...

    def writeTo(self, stream: java.io.OutputStream) -> None:
        """
        Dump all the accumulated bytes in this encoder to the stream.
        @param stream is the output stream
        @throws IOException for errors during the write operation
        """
        ...

    def writeUnsignedInteger(self, __a0: ghidra.program.model.pcode.AttributeId, __a1: long) -> None: ...

    @property
    def empty(self) -> bool: ...