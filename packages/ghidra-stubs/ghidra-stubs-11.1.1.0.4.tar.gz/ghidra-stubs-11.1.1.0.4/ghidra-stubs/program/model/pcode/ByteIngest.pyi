from typing import List
from typing import overload
import java.io
import java.lang


class ByteIngest(object):
    """
    An object that can ingest bytes from a stream in preparation for decoding
    """









    def clear(self) -> None:
        """
        Clear any previous cached bytes.
        """
        ...

    def endIngest(self) -> None:
        """
        Formal indicator that ingesting of bytes is complete and processing can begin
        @throws IOException for errors processing the underlying stream
        """
        ...

    def equals(self, __a0: object) -> bool: ...

    def getClass(self) -> java.lang.Class: ...

    def hashCode(self) -> int: ...

    def ingestBytes(self, byteArray: List[int], off: int, sz: int) -> None:
        """
        Ingest bytes directly from a byte array.
         If these bytes would cause the total number of bytes ingested to exceed
         the maximum (as set by the call to open()), an exception is thrown.
         This can be called multiple times to read in different chunks.
        @param byteArray is the array of bytes
        @param off is the index of the first byte to ingest
        @param sz is the number of bytes to ingest
        @throws IOException if the max number of bytes to ingest is exceeded
        """
        ...

    def ingestStream(self, inStream: java.io.InputStream) -> None:
        """
        Ingest bytes from the stream until the end of stream is encountered.
         An absolute limit is set on the number of bytes that can be ingested via the max parameter
         to a previous call to open(). If this limit is exceeded, an exception is thrown.
        @param inStream is the input stream to read from
        @throws IOException for errors reading from the stream
        """
        ...

    def ingestStreamToNextTerminator(self, inStream: java.io.InputStream) -> None:
        """
        Ingest bytes from the stream up to (and including) the first 0 byte.  This can be called
         multiple times to read in bytes in different chunks.
         An absolute limit is set on the number of bytes that can be ingested via the max parameter
         to a previous call to open(). If this limit is exceeded, an exception is thrown.
        @param inStream is the input stream to read from
        @throws IOException for errors reading from the stream
        """
        ...

    def isEmpty(self) -> bool:
        """
        @return true if no bytes have yet been ingested via ingestStream()
        """
        ...

    def notify(self) -> None: ...

    def notifyAll(self) -> None: ...

    def open(self, max: int, desc: unicode) -> None:
        """
        Open the ingester for receiving bytes.  This establishes the description of the source of
         the bytes and maximum number of bytes that can be read
        @param max is the maximum number of bytes that can be read
        @param desc is the description of the byte source
        """
        ...

    def toString(self) -> unicode: ...

    @overload
    def wait(self) -> None: ...

    @overload
    def wait(self, __a0: long) -> None: ...

    @overload
    def wait(self, __a0: long, __a1: int) -> None: ...

    @property
    def empty(self) -> bool: ...