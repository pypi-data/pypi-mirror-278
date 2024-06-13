from typing import overload
import ghidra.program.model.data.RenderUnicodeSettingsDefinition
import java.lang
import java.nio


class StringRenderBuilder(object):
    """
    Helper class used to build up a formatted (for human consumption) string representation returned
     by Unicode and String data types.
 
     Call #build() to retrieve the formatted string.
 
     Example (quotes are part of result): 
    """

    DOUBLE_QUOTE: int = '"'
    SINGLE_QUOTE: int = "'"



    @overload
    def __init__(self, cs: java.nio.charset.Charset, charSize: int): ...

    @overload
    def __init__(self, cs: java.nio.charset.Charset, charSize: int, quoteChar: int): ...



    def addEscapedCodePoint(self, codePoint: int) -> None:
        """
        Add a unicode codepoint as its escaped hex value, with a escape character
         prefix of 'x', 'u' or 'U' depending on the magnitude of the codePoint value.
         <p>
         {@literal codePoint 15 -> '\' 'x' "0F"}<br>
         {@literal codePoint 65535 -> '\' 'u' "FFFF"}<br>
         {@literal codePoint 65536 -> '\' 'U' "00010000"}<br>
        @param codePoint int value
        """
        ...

    def build(self) -> unicode: ...

    def decodeBytesUsingCharset(self, bb: java.nio.ByteBuffer, renderSetting: ghidra.program.model.data.RenderUnicodeSettingsDefinition.RENDER_ENUM, trimTrailingNulls: bool) -> None:
        """
        Adds the characters found in the supplied {@link ByteBuffer} to the result.
         <p>
         Any portions of the byte buffer that cause problems for the charset codec will be added
         as a {@link #addByteSeq(ByteBuffer, int) byte sequence}.
         <p>
         Characters that are outside the traditional ASCII range will be rendered as-is or as
         escape sequences, depending on the RENDER_ENUM setting.
        @param bb {@link ByteBuffer} containing bytes of a string
        @param renderSetting {@link RENDER_ENUM}
        @param trimTrailingNulls boolean flag, if true trailing null bytes will not be included
         in the rendered output
        """
        ...

    def equals(self, __a0: object) -> bool: ...

    def getClass(self) -> java.lang.Class: ...

    def hashCode(self) -> int: ...

    def notify(self) -> None: ...

    def notifyAll(self) -> None: ...

    def toString(self) -> unicode:
        """
        Example (quotes are part of result): {@code "Test\tstring",01,02,"Second\npart",00}
         <p>
        @return Formatted string
        """
        ...

    @overload
    def wait(self) -> None: ...

    @overload
    def wait(self, __a0: long) -> None: ...

    @overload
    def wait(self, __a0: long, __a1: int) -> None: ...

