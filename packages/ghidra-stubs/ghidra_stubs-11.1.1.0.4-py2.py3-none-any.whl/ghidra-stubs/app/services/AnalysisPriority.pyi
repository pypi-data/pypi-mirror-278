from typing import overload
import ghidra.app.services
import java.lang


class AnalysisPriority(object):
    """
    Class to specify priority within the Automated Analysis pipeline.
    """

    BLOCK_ANALYSIS: ghidra.app.services.AnalysisPriority
    CODE_ANALYSIS: ghidra.app.services.AnalysisPriority
    DATA_ANALYSIS: ghidra.app.services.AnalysisPriority
    DATA_TYPE_PROPOGATION: ghidra.app.services.AnalysisPriority
    DISASSEMBLY: ghidra.app.services.AnalysisPriority
    FORMAT_ANALYSIS: ghidra.app.services.AnalysisPriority
    FUNCTION_ANALYSIS: ghidra.app.services.AnalysisPriority
    FUNCTION_ID_ANALYSIS: ghidra.app.services.AnalysisPriority
    HIGHEST_PRIORITY: ghidra.app.services.AnalysisPriority
    LOW_PRIORITY: ghidra.app.services.AnalysisPriority
    REFERENCE_ANALYSIS: ghidra.app.services.AnalysisPriority



    @overload
    def __init__(self, priority: int): ...

    @overload
    def __init__(self, name: unicode, priority: int):
        """
        Construct a new priority object.
        @param priority priority to use
        """
        ...



    def after(self) -> ghidra.app.services.AnalysisPriority:
        """
        Get a piority that is a little lower than this one.
        @return a lower priority
        """
        ...

    def before(self) -> ghidra.app.services.AnalysisPriority:
        """
        Get a priority that is a little higher than this one.
        @return a higher priority
        """
        ...

    def equals(self, __a0: object) -> bool: ...

    def getClass(self) -> java.lang.Class: ...

    @staticmethod
    def getInitial(name: unicode) -> ghidra.app.services.AnalysisPriority:
        """
        Return first gross priority.
        @return first gross priority
        """
        ...

    def getNext(self, nextName: unicode) -> ghidra.app.services.AnalysisPriority:
        """
        Get the next gross priority.
        @return return next gross priority
        """
        ...

    def hashCode(self) -> int: ...

    def notify(self) -> None: ...

    def notifyAll(self) -> None: ...

    def priority(self) -> int:
        """
        Return the priority specified for this analysis priority.
        """
        ...

    def toString(self) -> unicode: ...

    @overload
    def wait(self) -> None: ...

    @overload
    def wait(self, __a0: long) -> None: ...

    @overload
    def wait(self, __a0: long, __a1: int) -> None: ...

