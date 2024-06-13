from typing import overload
import java.lang


class RustConstants(object):
    RUST_CATEGORYPATH: ghidra.program.model.data.CategoryPath
    RUST_COMPILER: unicode = u'rustc'
    RUST_EXTENSIONS_PATH: unicode = u'extensions/rust/'
    RUST_EXTENSIONS_UNIX: unicode = u'unix'
    RUST_EXTENSIONS_WINDOWS: unicode = u'windows'
    RUST_SIGNATURE_1: List[int]
    RUST_SIGNATURE_2: List[int]



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

