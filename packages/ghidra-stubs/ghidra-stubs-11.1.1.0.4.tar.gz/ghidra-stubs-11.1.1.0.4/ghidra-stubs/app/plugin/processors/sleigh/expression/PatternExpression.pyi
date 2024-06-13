from typing import overload
import ghidra.app.plugin.processors.sleigh
import ghidra.app.plugin.processors.sleigh.expression
import ghidra.program.model.pcode
import java.lang


class PatternExpression(object):
    """
    An expression which results in a pattern for a specific InstructionContext
    """





    def __init__(self): ...



    def decode(self, decoder: ghidra.program.model.pcode.Decoder, lang: ghidra.app.plugin.processors.sleigh.SleighLanguage) -> None: ...

    @staticmethod
    def decodeExpression(decoder: ghidra.program.model.pcode.Decoder, lang: ghidra.app.plugin.processors.sleigh.SleighLanguage) -> ghidra.app.plugin.processors.sleigh.expression.PatternExpression: ...

    def equals(self, __a0: object) -> bool: ...

    def getClass(self) -> java.lang.Class: ...

    def getValue(self, walker: ghidra.app.plugin.processors.sleigh.ParserWalker) -> long: ...

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

