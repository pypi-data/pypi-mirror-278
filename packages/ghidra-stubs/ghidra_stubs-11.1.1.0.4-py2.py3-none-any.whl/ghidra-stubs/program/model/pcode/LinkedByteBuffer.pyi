from typing import List
from typing import overload
import ghidra.program.model.pcode
import ghidra.program.model.pcode.LinkedByteBuffer
import java.io
import java.lang


class LinkedByteBuffer(object):
    """
    A byte buffer that is stored as a linked list of pages.  Each page holds BUFFER_SIZE bytes.
     A Position object acts as an iterator over the whole buffer.  The buffer can be populated
     from a stream, either all at once or "as needed" when a Position object iterates past
     the current cached set of bytes.
    """

    BUFFER_SIZE: int = 1024




    class ArrayIter(object):
        array: List[int]
        next: ghidra.program.model.pcode.LinkedByteBuffer.ArrayIter



        def __init__(self): ...



        def equals(self, __a0: object) -> bool: ...

        def getClass(self) -> java.lang.Class: ...

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






    class Position(object):
        array: List[int]
        buffer: ghidra.program.model.pcode.LinkedByteBuffer
        current: int
        seqIter: ghidra.program.model.pcode.LinkedByteBuffer.ArrayIter



        def __init__(self): ...



        def advancePosition(self, __a0: int) -> None: ...

        def copy(self, __a0: ghidra.program.model.pcode.LinkedByteBuffer.Position) -> None: ...

        def equals(self, __a0: object) -> bool: ...

        def getByte(self) -> int: ...

        def getBytePlus1(self) -> int: ...

        def getClass(self) -> java.lang.Class: ...

        def getNextByte(self) -> int: ...

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
        def byte(self) -> int: ...

        @property
        def bytePlus1(self) -> int: ...

        @property
        def nextByte(self) -> int: ...

    def __init__(self, max: int, pad: int, desc: unicode): ...



    def close(self) -> None:
        """
        Close the "as needed" stream, if configure.
        @throws IOException for problems closing the stream
        """
        ...

    def equals(self, __a0: object) -> bool: ...

    def getClass(self) -> java.lang.Class: ...

    def getStartPosition(self, position: ghidra.program.model.pcode.LinkedByteBuffer.Position) -> None: ...

    def hashCode(self) -> int: ...

    def ingestBytes(self, byteArray: List[int], off: int, sz: int) -> None:
        """
        Ingest bytes directly from a byte array.
         If these bytes would cause the total number of bytes ingested to exceed
         the maximum (maxCount) bytes set for this buffer, an exception is thrown.
         This can be called multiple times to read in different chunks.
        @param byteArray is the array of bytes
        @param off is the index of the first byte to ingest
        @param sz is the number of bytes to ingest
        @throws IOException if the max number of bytes to ingest is exceeded
        """
        ...

    def ingestStream(self, stream: java.io.InputStream) -> None:
        """
        Read the stream until the end of stream is encountered or until maxCount bytes is reached.
         Store the bytes on the heap in BUFFER_SIZE chunks.
        @param stream is the input
        @throws IOException for errors reading from the stream
        """
        ...

    def ingestStreamAsNeeded(self, stream: java.io.InputStream, start: ghidra.program.model.pcode.LinkedByteBuffer.Position) -> None:
        """
        Set up this buffer so that it reads in pages as needed.  The initial page is read
         immediately.  Additional pages are read via readNextPage() through the Position methods.
        @param stream is the stream to read from
        @param start will hold the initial buffer
        @throws IOException for problems reading data from the stream
        """
        ...

    def ingestStreamToNextTerminator(self, stream: java.io.InputStream) -> None:
        """
        Ingest stream up to the first 0 byte or until maxCount bytes is reached.
         Store the bytes on the heap in BUFFER_SIZE chunks.
        @param stream is the input
        @throws IOException for errors reading from the stream
        """
        ...

    def notify(self) -> None: ...

    def notifyAll(self) -> None: ...

    def pad(self) -> None:
        """
        Add the padValue to the end of the buffer
        """
        ...

    def toString(self) -> unicode: ...

    @overload
    def wait(self) -> None: ...

    @overload
    def wait(self, __a0: long) -> None: ...

    @overload
    def wait(self, __a0: long, __a1: int) -> None: ...

