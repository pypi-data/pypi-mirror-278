from typing import List
from typing import overload
import ghidra.app.util.bin
import ghidra.program.model.data
import java.lang


class SecurityCertificate(object, ghidra.app.util.bin.StructConverter):
    """
    A class to represent the WIN_CERTIFICATE
     struct as defined in winbase.h.
 
     This structure encapsulates a signature used in verifying executables.
 
 
     typedef struct _WIN_CERTIFICATE {
         DWORD       dwLength;
         WORD        wRevision;
         WORD        wCertificateType;   // WIN_CERT_TYPE_xxx
         BYTE        bCertificate[ANYSIZE_ARRAY];
     } WIN_CERTIFICATE, *LPWIN_CERTIFICATE;
 
    """

    ASCII: ghidra.program.model.data.DataType
    BYTE: ghidra.program.model.data.DataType
    DWORD: ghidra.program.model.data.DataType
    IBO32: ghidra.program.model.data.DataType
    IBO64: ghidra.program.model.data.DataType
    NAME: unicode = u'WIN_CERTIFICATE'
    POINTER: ghidra.program.model.data.DataType
    QWORD: ghidra.program.model.data.DataType
    SLEB128: ghidra.program.model.data.SignedLeb128DataType
    STRING: ghidra.program.model.data.DataType
    ULEB128: ghidra.program.model.data.UnsignedLeb128DataType
    UTF16: ghidra.program.model.data.DataType
    UTF8: ghidra.program.model.data.DataType
    VOID: ghidra.program.model.data.DataType
    WIN_CERT_REVISION_1_0: int = 256
    WIN_CERT_REVISION_2_0: int = 512
    WIN_CERT_TYPE_PKCS1_SIGN: int = 9
    WIN_CERT_TYPE_PKCS_SIGNED_DATA: int = 2
    WIN_CERT_TYPE_RESERVED_1: int = 3
    WIN_CERT_TYPE_X509: int = 1
    WORD: ghidra.program.model.data.DataType



    def __init__(self): ...



    def equals(self, __a0: object) -> bool: ...

    def getClass(self) -> java.lang.Class: ...

    def getData(self) -> List[int]:
        """
        An array of certificates. The format of this member 
         depends on the value of wCertificateType.
        @return an array of certificates
        """
        ...

    def getLength(self) -> int:
        """
        Returns the length, in bytes, of the signature.
        @return the length, in bytes, of the signature
        """
        ...

    def getRevision(self) -> int:
        """
        Returns the certificate revision. Currently, 
         the only defined certificate revision is 
         WIN_CERT_REVISION_1_0 (0x0100).
        @return the certificate revision
        """
        ...

    def getType(self) -> int:
        """
        Returns the certificate type.
        @return the certificate type
        """
        ...

    def getTypeAsString(self) -> unicode:
        """
        Returns a string representation of the certificate type.
        @return a string representation of the certificate type
        """
        ...

    def hashCode(self) -> int: ...

    def notify(self) -> None: ...

    def notifyAll(self) -> None: ...

    def toDataType(self) -> ghidra.program.model.data.DataType:
        """
        @see ghidra.app.util.bin.StructConverter#toDataType()
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
    def data(self) -> List[int]: ...

    @property
    def length(self) -> int: ...

    @property
    def revision(self) -> int: ...

    @property
    def type(self) -> int: ...

    @property
    def typeAsString(self) -> unicode: ...