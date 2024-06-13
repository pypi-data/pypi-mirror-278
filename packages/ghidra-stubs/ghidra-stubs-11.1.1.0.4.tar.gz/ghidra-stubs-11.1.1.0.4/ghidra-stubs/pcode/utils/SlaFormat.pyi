from typing import overload
import generic.jar
import ghidra.program.model.pcode
import java.io
import java.lang


class SlaFormat(object):
    """
    Encoding values for the .sla file format
    """

    ATTRIB_ALIGN: ghidra.program.model.pcode.AttributeId
    ATTRIB_BASE: ghidra.program.model.pcode.AttributeId
    ATTRIB_BIGENDIAN: ghidra.program.model.pcode.AttributeId
    ATTRIB_CODE: ghidra.program.model.pcode.AttributeId
    ATTRIB_CONTAIN: ghidra.program.model.pcode.AttributeId
    ATTRIB_CONTEXT: ghidra.program.model.pcode.AttributeId
    ATTRIB_CT: ghidra.program.model.pcode.AttributeId
    ATTRIB_DEFAULTSPACE: ghidra.program.model.pcode.AttributeId
    ATTRIB_DELAY: ghidra.program.model.pcode.AttributeId
    ATTRIB_ENDBIT: ghidra.program.model.pcode.AttributeId
    ATTRIB_ENDBYTE: ghidra.program.model.pcode.AttributeId
    ATTRIB_FIRST: ghidra.program.model.pcode.AttributeId
    ATTRIB_FLOW: ghidra.program.model.pcode.AttributeId
    ATTRIB_HIGH: ghidra.program.model.pcode.AttributeId
    ATTRIB_I: ghidra.program.model.pcode.AttributeId
    ATTRIB_ID: ghidra.program.model.pcode.AttributeId
    ATTRIB_INDEX: ghidra.program.model.pcode.AttributeId
    ATTRIB_LABELS: ghidra.program.model.pcode.AttributeId
    ATTRIB_LENGTH: ghidra.program.model.pcode.AttributeId
    ATTRIB_LINE: ghidra.program.model.pcode.AttributeId
    ATTRIB_LOW: ghidra.program.model.pcode.AttributeId
    ATTRIB_MASK: ghidra.program.model.pcode.AttributeId
    ATTRIB_MAXDELAY: ghidra.program.model.pcode.AttributeId
    ATTRIB_MINLEN: ghidra.program.model.pcode.AttributeId
    ATTRIB_NAME: ghidra.program.model.pcode.AttributeId
    ATTRIB_NONZERO: ghidra.program.model.pcode.AttributeId
    ATTRIB_NUMBER: ghidra.program.model.pcode.AttributeId
    ATTRIB_NUMCT: ghidra.program.model.pcode.AttributeId
    ATTRIB_NUMSECTIONS: ghidra.program.model.pcode.AttributeId
    ATTRIB_OFF: ghidra.program.model.pcode.AttributeId
    ATTRIB_PARENT: ghidra.program.model.pcode.AttributeId
    ATTRIB_PHYSICAL: ghidra.program.model.pcode.AttributeId
    ATTRIB_PIECE: ghidra.program.model.pcode.AttributeId
    ATTRIB_PLUS: ghidra.program.model.pcode.AttributeId
    ATTRIB_S: ghidra.program.model.pcode.AttributeId
    ATTRIB_SCOPE: ghidra.program.model.pcode.AttributeId
    ATTRIB_SCOPESIZE: ghidra.program.model.pcode.AttributeId
    ATTRIB_SECTION: ghidra.program.model.pcode.AttributeId
    ATTRIB_SHIFT: ghidra.program.model.pcode.AttributeId
    ATTRIB_SIGNBIT: ghidra.program.model.pcode.AttributeId
    ATTRIB_SIZE: ghidra.program.model.pcode.AttributeId
    ATTRIB_SOURCE: ghidra.program.model.pcode.AttributeId
    ATTRIB_SPACE: ghidra.program.model.pcode.AttributeId
    ATTRIB_STARTBIT: ghidra.program.model.pcode.AttributeId
    ATTRIB_STARTBYTE: ghidra.program.model.pcode.AttributeId
    ATTRIB_SUBSYM: ghidra.program.model.pcode.AttributeId
    ATTRIB_SYMBOLSIZE: ghidra.program.model.pcode.AttributeId
    ATTRIB_TABLE: ghidra.program.model.pcode.AttributeId
    ATTRIB_UNIQBASE: ghidra.program.model.pcode.AttributeId
    ATTRIB_UNIQMASK: ghidra.program.model.pcode.AttributeId
    ATTRIB_VAL: ghidra.program.model.pcode.AttributeId
    ATTRIB_VARNODE: ghidra.program.model.pcode.AttributeId
    ATTRIB_VERSION: ghidra.program.model.pcode.AttributeId
    ATTRIB_WORDSIZE: ghidra.program.model.pcode.AttributeId
    ELEM_AND_EXP: ghidra.program.model.pcode.ElementId
    ELEM_COMBINE_PAT: ghidra.program.model.pcode.ElementId
    ELEM_COMMIT: ghidra.program.model.pcode.ElementId
    ELEM_CONSTRUCTOR: ghidra.program.model.pcode.ElementId
    ELEM_CONSTRUCT_TPL: ghidra.program.model.pcode.ElementId
    ELEM_CONST_CURSPACE: ghidra.program.model.pcode.ElementId
    ELEM_CONST_CURSPACE_SIZE: ghidra.program.model.pcode.ElementId
    ELEM_CONST_FLOWDEST: ghidra.program.model.pcode.ElementId
    ELEM_CONST_FLOWDEST_SIZE: ghidra.program.model.pcode.ElementId
    ELEM_CONST_FLOWREF: ghidra.program.model.pcode.ElementId
    ELEM_CONST_FLOWREF_SIZE: ghidra.program.model.pcode.ElementId
    ELEM_CONST_HANDLE: ghidra.program.model.pcode.ElementId
    ELEM_CONST_NEXT: ghidra.program.model.pcode.ElementId
    ELEM_CONST_NEXT2: ghidra.program.model.pcode.ElementId
    ELEM_CONST_REAL: ghidra.program.model.pcode.ElementId
    ELEM_CONST_RELATIVE: ghidra.program.model.pcode.ElementId
    ELEM_CONST_SPACEID: ghidra.program.model.pcode.ElementId
    ELEM_CONST_START: ghidra.program.model.pcode.ElementId
    ELEM_CONTEXTFIELD: ghidra.program.model.pcode.ElementId
    ELEM_CONTEXT_OP: ghidra.program.model.pcode.ElementId
    ELEM_CONTEXT_PAT: ghidra.program.model.pcode.ElementId
    ELEM_CONTEXT_SYM: ghidra.program.model.pcode.ElementId
    ELEM_CONTEXT_SYM_HEAD: ghidra.program.model.pcode.ElementId
    ELEM_DECISION: ghidra.program.model.pcode.ElementId
    ELEM_DIV_EXP: ghidra.program.model.pcode.ElementId
    ELEM_END_EXP: ghidra.program.model.pcode.ElementId
    ELEM_END_SYM: ghidra.program.model.pcode.ElementId
    ELEM_END_SYM_HEAD: ghidra.program.model.pcode.ElementId
    ELEM_EPSILON_SYM: ghidra.program.model.pcode.ElementId
    ELEM_EPSILON_SYM_HEAD: ghidra.program.model.pcode.ElementId
    ELEM_HANDLE_TPL: ghidra.program.model.pcode.ElementId
    ELEM_INSTRUCT_PAT: ghidra.program.model.pcode.ElementId
    ELEM_INTB: ghidra.program.model.pcode.ElementId
    ELEM_LSHIFT_EXP: ghidra.program.model.pcode.ElementId
    ELEM_MASK_WORD: ghidra.program.model.pcode.ElementId
    ELEM_MINUS_EXP: ghidra.program.model.pcode.ElementId
    ELEM_MULT_EXP: ghidra.program.model.pcode.ElementId
    ELEM_NAMETAB: ghidra.program.model.pcode.ElementId
    ELEM_NAME_SYM: ghidra.program.model.pcode.ElementId
    ELEM_NAME_SYM_HEAD: ghidra.program.model.pcode.ElementId
    ELEM_NEXT2_EXP: ghidra.program.model.pcode.ElementId
    ELEM_NEXT2_SYM: ghidra.program.model.pcode.ElementId
    ELEM_NEXT2_SYM_HEAD: ghidra.program.model.pcode.ElementId
    ELEM_NOT_EXP: ghidra.program.model.pcode.ElementId
    ELEM_NULL: ghidra.program.model.pcode.ElementId
    ELEM_OPER: ghidra.program.model.pcode.ElementId
    ELEM_OPERAND_EXP: ghidra.program.model.pcode.ElementId
    ELEM_OPERAND_SYM: ghidra.program.model.pcode.ElementId
    ELEM_OPERAND_SYM_HEAD: ghidra.program.model.pcode.ElementId
    ELEM_OPPRINT: ghidra.program.model.pcode.ElementId
    ELEM_OP_TPL: ghidra.program.model.pcode.ElementId
    ELEM_OR_EXP: ghidra.program.model.pcode.ElementId
    ELEM_OR_PAT: ghidra.program.model.pcode.ElementId
    ELEM_PAIR: ghidra.program.model.pcode.ElementId
    ELEM_PAT_BLOCK: ghidra.program.model.pcode.ElementId
    ELEM_PLUS_EXP: ghidra.program.model.pcode.ElementId
    ELEM_PRINT: ghidra.program.model.pcode.ElementId
    ELEM_RSHIFT_EXP: ghidra.program.model.pcode.ElementId
    ELEM_SCOPE: ghidra.program.model.pcode.ElementId
    ELEM_SLEIGH: ghidra.program.model.pcode.ElementId
    ELEM_SOURCEFILE: ghidra.program.model.pcode.ElementId
    ELEM_SOURCEFILES: ghidra.program.model.pcode.ElementId
    ELEM_SPACE: ghidra.program.model.pcode.ElementId
    ELEM_SPACES: ghidra.program.model.pcode.ElementId
    ELEM_SPACE_OTHER: ghidra.program.model.pcode.ElementId
    ELEM_SPACE_UNIQUE: ghidra.program.model.pcode.ElementId
    ELEM_START_EXP: ghidra.program.model.pcode.ElementId
    ELEM_START_SYM: ghidra.program.model.pcode.ElementId
    ELEM_START_SYM_HEAD: ghidra.program.model.pcode.ElementId
    ELEM_SUBTABLE_SYM: ghidra.program.model.pcode.ElementId
    ELEM_SUBTABLE_SYM_HEAD: ghidra.program.model.pcode.ElementId
    ELEM_SUB_EXP: ghidra.program.model.pcode.ElementId
    ELEM_SYMBOL_TABLE: ghidra.program.model.pcode.ElementId
    ELEM_TOKENFIELD: ghidra.program.model.pcode.ElementId
    ELEM_USEROP: ghidra.program.model.pcode.ElementId
    ELEM_USEROP_HEAD: ghidra.program.model.pcode.ElementId
    ELEM_VALUEMAP_SYM: ghidra.program.model.pcode.ElementId
    ELEM_VALUEMAP_SYM_HEAD: ghidra.program.model.pcode.ElementId
    ELEM_VALUETAB: ghidra.program.model.pcode.ElementId
    ELEM_VALUE_SYM: ghidra.program.model.pcode.ElementId
    ELEM_VALUE_SYM_HEAD: ghidra.program.model.pcode.ElementId
    ELEM_VAR: ghidra.program.model.pcode.ElementId
    ELEM_VARLIST_SYM: ghidra.program.model.pcode.ElementId
    ELEM_VARLIST_SYM_HEAD: ghidra.program.model.pcode.ElementId
    ELEM_VARNODE_SYM: ghidra.program.model.pcode.ElementId
    ELEM_VARNODE_SYM_HEAD: ghidra.program.model.pcode.ElementId
    ELEM_VARNODE_TPL: ghidra.program.model.pcode.ElementId
    ELEM_XOR_EXP: ghidra.program.model.pcode.ElementId
    FORMAT_VERSION: int = 4
    MAX_FILE_SIZE: int = 16777216



    def __init__(self): ...



    @staticmethod
    def buildDecoder(sleighFile: generic.jar.ResourceFile) -> ghidra.program.model.pcode.PackedDecode:
        """
        Build the decoder for decompressing and decoding the .sla file (as a stream).
         The given file is opened and the header bytes are checked.  The returned
         decoder is immediately ready to read.
        @param sleighFile is the given .sla file
        @return the decoder
        @throws IOException if the header is invalid or there are problems reading the file
        """
        ...

    @staticmethod
    def buildEncoder(sleighFile: generic.jar.ResourceFile) -> ghidra.program.model.pcode.PackedEncode:
        """
        Build the encoder for compressing and encoding a .sla file (as a stream).
         The given file is opened and a header is immediately written.  The returned
         encoder is ready immediately to receive the .sla elements and attributes.
        @param sleighFile is the .sla file (to be created)
        @return the encoder
        @throws IOException for any problems opening or writing to the file
        """
        ...

    def equals(self, __a0: object) -> bool: ...

    def getClass(self) -> java.lang.Class: ...

    def hashCode(self) -> int: ...

    @staticmethod
    def isSlaFormat(stream: java.io.InputStream) -> bool:
        """
        Try to read the header bytes of the .sla format from the given stream. If the header bytes
         and the version byte match, \b true is returned, and the stream can be passed to the decoder.
        @param stream is the given stream
        @return true if the .sla header bytes are found
        @throws IOException for any errors reading from the stream
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

    @staticmethod
    def writeSlaHeader(stream: java.io.OutputStream) -> None:
        """
        Write a .sla file header,including the format version number to the given stream.
        @param stream is the given stream
        @throws IOException for problems writing to the stream
        """
        ...

