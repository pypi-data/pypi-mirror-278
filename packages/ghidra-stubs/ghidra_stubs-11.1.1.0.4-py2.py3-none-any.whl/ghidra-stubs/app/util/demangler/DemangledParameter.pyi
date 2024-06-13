from typing import overload
import ghidra.app.util.demangler
import java.lang


class DemangledParameter(object):
    """
    A class to represent a demangled function parameter.
 
     This extends DemangledDataType in order to associate an optional parameter label with
     its data type.
    """





    def __init__(self, type: ghidra.app.util.demangler.DemangledDataType):
        """
        Creates a new {@link DemangledParameter} with the given type and no label
        @param type The parameter type
        """
        ...



    def equals(self, __a0: object) -> bool: ...

    def getClass(self) -> java.lang.Class: ...

    def getLabel(self) -> unicode:
        """
        {@return the parameter's label (could be null)}
        """
        ...

    def getType(self) -> ghidra.app.util.demangler.DemangledDataType:
        """
        {@return the parameter's type}
        """
        ...

    def hashCode(self) -> int: ...

    def notify(self) -> None: ...

    def notifyAll(self) -> None: ...

    def setLabel(self, label: unicode) -> None:
        """
        Sets the parameter's label
        @param label The label (null for no label)
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
    def label(self) -> unicode: ...

    @label.setter
    def label(self, value: unicode) -> None: ...

    @property
    def type(self) -> ghidra.app.util.demangler.DemangledDataType: ...