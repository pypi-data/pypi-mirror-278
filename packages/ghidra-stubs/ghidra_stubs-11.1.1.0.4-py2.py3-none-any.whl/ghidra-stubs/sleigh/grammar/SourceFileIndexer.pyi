from typing import overload
import ghidra.program.model.pcode
import ghidra.sleigh.grammar
import java.lang


class SourceFileIndexer(object):
    """
    This class is used to index source files in a SLEIGH language module.
     The SLEIGH compiler records the index of the source file for a constructor rather
     than the file name.  This is an optimization to avoid repeating the file name in
     the .sla files.
    """





    def __init__(self):
        """
        Creates a {code SourceFileIndexer} object with an empty index.
        """
        ...



    def decode(self, decoder: ghidra.program.model.pcode.Decoder) -> None:
        """
        Decode an index from a stream
        @param decoder is the stream
        @throws DecoderException for errors in the encoding
        """
        ...

    def encode(self, encoder: ghidra.program.model.pcode.Encoder) -> None:
        """
        Encode the index to a stream
        @param encoder stream to write to
        @throws IOException for errors writing to the stream
        """
        ...

    def equals(self, __a0: object) -> bool: ...

    def getClass(self) -> java.lang.Class: ...

    def getFileName(self, index: int) -> unicode:
        """
        Returns the file name at a given index
        @param index index
        @return file name or {@code null} if there is no file with that index
        """
        ...

    def getIndex(self, filename: unicode) -> int:
        """
        Returns the index for a filename
        @param filename file
        @return index or {@code null} if {@code filename} is not in the index.
        """
        ...

    def hashCode(self) -> int: ...

    def index(self, loc: ghidra.sleigh.grammar.Location) -> int:
        """
        Adds the filename of a location to the index if it is not already present.
        @param loc location containing filename to add
        @return index associated with filename, or {@code null} if a {@code null} {@link Location}
         or a {@link Location} with a {@code null} filename was provided as input.
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

