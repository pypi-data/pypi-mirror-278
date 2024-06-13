from typing import overload
import ghidra.app.plugin.assembler.sleigh.grammars
import ghidra.app.plugin.assembler.sleigh.symbol
import ghidra.app.plugin.processors.sleigh.symbol
import java.lang
import java.util


class AssemblyStringTerminal(ghidra.app.plugin.assembler.sleigh.symbol.AssemblyTerminal):
    """
    A terminal that accepts only a particular string
    """





    def __init__(self, str: unicode, defsym: ghidra.app.plugin.processors.sleigh.symbol.VarnodeSymbol):
        """
        Construct a terminal that accepts only the given string
        @param str the string to accept
        """
        ...



    @overload
    def compareTo(self, that: ghidra.app.plugin.assembler.sleigh.symbol.AssemblySymbol) -> int: ...

    @overload
    def compareTo(self, __a0: object) -> int: ...

    def equals(self, that: object) -> bool: ...

    def getClass(self) -> java.lang.Class: ...

    def getDefiningSymbol(self) -> ghidra.app.plugin.processors.sleigh.symbol.VarnodeSymbol: ...

    def getName(self) -> unicode:
        """
        Get the name of this symbol
        @return the name
        """
        ...

    def getString(self) -> unicode: ...

    def getSuggestions(self, got: unicode, symbols: ghidra.app.plugin.assembler.sleigh.symbol.AssemblyNumericSymbols) -> java.util.Collection: ...

    def hashCode(self) -> int: ...

    def isWhiteSpace(self) -> bool: ...

    def match(self, buffer: unicode, pos: int, grammar: ghidra.app.plugin.assembler.sleigh.grammars.AssemblyGrammar, symbols: ghidra.app.plugin.assembler.sleigh.symbol.AssemblyNumericSymbols) -> java.util.Collection: ...

    def notify(self) -> None: ...

    def notifyAll(self) -> None: ...

    def takesOperandIndex(self) -> bool: ...

    def toString(self) -> unicode: ...

    @overload
    def wait(self) -> None: ...

    @overload
    def wait(self, __a0: long) -> None: ...

    @overload
    def wait(self, __a0: long, __a1: int) -> None: ...

    @property
    def definingSymbol(self) -> ghidra.app.plugin.processors.sleigh.symbol.VarnodeSymbol: ...

    @property
    def string(self) -> unicode: ...

    @property
    def whiteSpace(self) -> bool: ...