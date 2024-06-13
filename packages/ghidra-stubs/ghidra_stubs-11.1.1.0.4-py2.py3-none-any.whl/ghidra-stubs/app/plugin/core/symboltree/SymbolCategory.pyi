from typing import overload
import ghidra.program.model.symbol
import java.lang


class SymbolCategory(object):
    CLASS_CATEGORY: ghidra.app.plugin.core.symboltree.SymbolCategory
    EXPORTS_CATEGORY: ghidra.app.plugin.core.symboltree.SymbolCategory
    FUNCTION_CATEGORY: ghidra.app.plugin.core.symboltree.SymbolCategory
    IMPORTS_CATEGORY: ghidra.app.plugin.core.symboltree.SymbolCategory
    LABEL_CATEGORY: ghidra.app.plugin.core.symboltree.SymbolCategory
    NAMESPACE_CATEGORY: ghidra.app.plugin.core.symboltree.SymbolCategory
    ROOT_CATEGORY: ghidra.app.plugin.core.symboltree.SymbolCategory







    def equals(self, __a0: object) -> bool: ...

    def getClass(self) -> java.lang.Class: ...

    def getName(self) -> unicode: ...

    def getSymbolType(self) -> ghidra.program.model.symbol.SymbolType: ...

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
    def name(self) -> unicode: ...

    @property
    def symbolType(self) -> ghidra.program.model.symbol.SymbolType: ...