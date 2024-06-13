from typing import List
from typing import overload
import java.lang


class OpcodeTable(object):
    """
    Abstract class used to represent the generic components of a Mach-O opcode table
    """





    def __init__(self): ...



    def equals(self, __a0: object) -> bool: ...

    def getClass(self) -> java.lang.Class: ...

    def getOpcodeOffsets(self) -> List[long]:
        """
        {@return opcode offsets from the start of the bind data}
        """
        ...

    def getSlebOffsets(self) -> List[long]:
        """
        {@return SLEB128 offsets from the start of the bind data}
        """
        ...

    def getStringOffsets(self) -> List[long]:
        """
        {@return string offsets from the start of the bind data}
        """
        ...

    def getUlebOffsets(self) -> List[long]:
        """
        {@return ULEB128 offsets from the start of the bind data}
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
    def opcodeOffsets(self) -> List[object]: ...

    @property
    def slebOffsets(self) -> List[object]: ...

    @property
    def stringOffsets(self) -> List[object]: ...

    @property
    def ulebOffsets(self) -> List[object]: ...