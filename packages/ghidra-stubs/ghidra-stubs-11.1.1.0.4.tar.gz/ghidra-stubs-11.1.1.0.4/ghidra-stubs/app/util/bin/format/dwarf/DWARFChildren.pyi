from typing import overload
import java.lang


class DWARFChildren(object):
    """
    DWARF child determination consts from www.dwarfstd.org/doc/DWARF4.pdf.
 
     Yes, its a direct equiv to a boolean, but its in the spec.
    """

    DW_CHILDREN_no: int = 0
    DW_CHILDREN_yes: int = 1



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

