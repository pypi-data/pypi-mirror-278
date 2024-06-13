from typing import overload
import ghidra.program.model.listing
import java.lang


class VariableFilter(object):
    COMPOUND_STACK_VARIABLE_FILTER: ghidra.program.model.listing.VariableFilter
    LOCAL_VARIABLE_FILTER: ghidra.program.model.listing.VariableFilter
    MEMORY_VARIABLE_FILTER: ghidra.program.model.listing.VariableFilter
    NONAUTO_PARAMETER_FILTER: ghidra.program.model.listing.VariableFilter
    PARAMETER_FILTER: ghidra.program.model.listing.VariableFilter
    REGISTER_VARIABLE_FILTER: ghidra.program.model.listing.VariableFilter
    STACK_VARIABLE_FILTER: ghidra.program.model.listing.VariableFilter
    UNIQUE_VARIABLE_FILTER: ghidra.program.model.listing.VariableFilter




    class LocalVariableFilter(object, ghidra.program.model.listing.VariableFilter):
        COMPOUND_STACK_VARIABLE_FILTER: ghidra.program.model.listing.VariableFilter
        LOCAL_VARIABLE_FILTER: ghidra.program.model.listing.VariableFilter
        MEMORY_VARIABLE_FILTER: ghidra.program.model.listing.VariableFilter
        NONAUTO_PARAMETER_FILTER: ghidra.program.model.listing.VariableFilter
        PARAMETER_FILTER: ghidra.program.model.listing.VariableFilter
        REGISTER_VARIABLE_FILTER: ghidra.program.model.listing.VariableFilter
        STACK_VARIABLE_FILTER: ghidra.program.model.listing.VariableFilter
        UNIQUE_VARIABLE_FILTER: ghidra.program.model.listing.VariableFilter



        def __init__(self): ...



        def equals(self, __a0: object) -> bool: ...

        def getClass(self) -> java.lang.Class: ...

        def hashCode(self) -> int: ...

        def matches(self, __a0: ghidra.program.model.listing.Variable) -> bool: ...

        def notify(self) -> None: ...

        def notifyAll(self) -> None: ...

        def toString(self) -> unicode: ...

        @overload
        def wait(self) -> None: ...

        @overload
        def wait(self, __a0: long) -> None: ...

        @overload
        def wait(self, __a0: long, __a1: int) -> None: ...






    class ParameterFilter(object, ghidra.program.model.listing.VariableFilter):
        COMPOUND_STACK_VARIABLE_FILTER: ghidra.program.model.listing.VariableFilter
        LOCAL_VARIABLE_FILTER: ghidra.program.model.listing.VariableFilter
        MEMORY_VARIABLE_FILTER: ghidra.program.model.listing.VariableFilter
        NONAUTO_PARAMETER_FILTER: ghidra.program.model.listing.VariableFilter
        PARAMETER_FILTER: ghidra.program.model.listing.VariableFilter
        REGISTER_VARIABLE_FILTER: ghidra.program.model.listing.VariableFilter
        STACK_VARIABLE_FILTER: ghidra.program.model.listing.VariableFilter
        UNIQUE_VARIABLE_FILTER: ghidra.program.model.listing.VariableFilter



        def __init__(self, __a0: bool): ...



        def equals(self, __a0: object) -> bool: ...

        def getClass(self) -> java.lang.Class: ...

        def hashCode(self) -> int: ...

        def matches(self, __a0: ghidra.program.model.listing.Variable) -> bool: ...

        def notify(self) -> None: ...

        def notifyAll(self) -> None: ...

        def toString(self) -> unicode: ...

        @overload
        def wait(self) -> None: ...

        @overload
        def wait(self, __a0: long) -> None: ...

        @overload
        def wait(self, __a0: long, __a1: int) -> None: ...






    class CompoundStackVariableFilter(object, ghidra.program.model.listing.VariableFilter):
        COMPOUND_STACK_VARIABLE_FILTER: ghidra.program.model.listing.VariableFilter
        LOCAL_VARIABLE_FILTER: ghidra.program.model.listing.VariableFilter
        MEMORY_VARIABLE_FILTER: ghidra.program.model.listing.VariableFilter
        NONAUTO_PARAMETER_FILTER: ghidra.program.model.listing.VariableFilter
        PARAMETER_FILTER: ghidra.program.model.listing.VariableFilter
        REGISTER_VARIABLE_FILTER: ghidra.program.model.listing.VariableFilter
        STACK_VARIABLE_FILTER: ghidra.program.model.listing.VariableFilter
        UNIQUE_VARIABLE_FILTER: ghidra.program.model.listing.VariableFilter



        def __init__(self): ...



        def equals(self, __a0: object) -> bool: ...

        def getClass(self) -> java.lang.Class: ...

        def hashCode(self) -> int: ...

        def matches(self, __a0: ghidra.program.model.listing.Variable) -> bool: ...

        def notify(self) -> None: ...

        def notifyAll(self) -> None: ...

        def toString(self) -> unicode: ...

        @overload
        def wait(self) -> None: ...

        @overload
        def wait(self, __a0: long) -> None: ...

        @overload
        def wait(self, __a0: long, __a1: int) -> None: ...






    class StackVariableFilter(object, ghidra.program.model.listing.VariableFilter):
        COMPOUND_STACK_VARIABLE_FILTER: ghidra.program.model.listing.VariableFilter
        LOCAL_VARIABLE_FILTER: ghidra.program.model.listing.VariableFilter
        MEMORY_VARIABLE_FILTER: ghidra.program.model.listing.VariableFilter
        NONAUTO_PARAMETER_FILTER: ghidra.program.model.listing.VariableFilter
        PARAMETER_FILTER: ghidra.program.model.listing.VariableFilter
        REGISTER_VARIABLE_FILTER: ghidra.program.model.listing.VariableFilter
        STACK_VARIABLE_FILTER: ghidra.program.model.listing.VariableFilter
        UNIQUE_VARIABLE_FILTER: ghidra.program.model.listing.VariableFilter



        def __init__(self): ...



        def equals(self, __a0: object) -> bool: ...

        def getClass(self) -> java.lang.Class: ...

        def hashCode(self) -> int: ...

        def matches(self, __a0: ghidra.program.model.listing.Variable) -> bool: ...

        def notify(self) -> None: ...

        def notifyAll(self) -> None: ...

        def toString(self) -> unicode: ...

        @overload
        def wait(self) -> None: ...

        @overload
        def wait(self, __a0: long) -> None: ...

        @overload
        def wait(self, __a0: long, __a1: int) -> None: ...






    class UniqueVariableFilter(object, ghidra.program.model.listing.VariableFilter):
        COMPOUND_STACK_VARIABLE_FILTER: ghidra.program.model.listing.VariableFilter
        LOCAL_VARIABLE_FILTER: ghidra.program.model.listing.VariableFilter
        MEMORY_VARIABLE_FILTER: ghidra.program.model.listing.VariableFilter
        NONAUTO_PARAMETER_FILTER: ghidra.program.model.listing.VariableFilter
        PARAMETER_FILTER: ghidra.program.model.listing.VariableFilter
        REGISTER_VARIABLE_FILTER: ghidra.program.model.listing.VariableFilter
        STACK_VARIABLE_FILTER: ghidra.program.model.listing.VariableFilter
        UNIQUE_VARIABLE_FILTER: ghidra.program.model.listing.VariableFilter



        def __init__(self): ...



        def equals(self, __a0: object) -> bool: ...

        def getClass(self) -> java.lang.Class: ...

        def hashCode(self) -> int: ...

        def matches(self, __a0: ghidra.program.model.listing.Variable) -> bool: ...

        def notify(self) -> None: ...

        def notifyAll(self) -> None: ...

        def toString(self) -> unicode: ...

        @overload
        def wait(self) -> None: ...

        @overload
        def wait(self, __a0: long) -> None: ...

        @overload
        def wait(self, __a0: long, __a1: int) -> None: ...






    class MemoryVariableFilter(object, ghidra.program.model.listing.VariableFilter):
        COMPOUND_STACK_VARIABLE_FILTER: ghidra.program.model.listing.VariableFilter
        LOCAL_VARIABLE_FILTER: ghidra.program.model.listing.VariableFilter
        MEMORY_VARIABLE_FILTER: ghidra.program.model.listing.VariableFilter
        NONAUTO_PARAMETER_FILTER: ghidra.program.model.listing.VariableFilter
        PARAMETER_FILTER: ghidra.program.model.listing.VariableFilter
        REGISTER_VARIABLE_FILTER: ghidra.program.model.listing.VariableFilter
        STACK_VARIABLE_FILTER: ghidra.program.model.listing.VariableFilter
        UNIQUE_VARIABLE_FILTER: ghidra.program.model.listing.VariableFilter



        def __init__(self): ...



        def equals(self, __a0: object) -> bool: ...

        def getClass(self) -> java.lang.Class: ...

        def hashCode(self) -> int: ...

        def matches(self, __a0: ghidra.program.model.listing.Variable) -> bool: ...

        def notify(self) -> None: ...

        def notifyAll(self) -> None: ...

        def toString(self) -> unicode: ...

        @overload
        def wait(self) -> None: ...

        @overload
        def wait(self, __a0: long) -> None: ...

        @overload
        def wait(self, __a0: long, __a1: int) -> None: ...






    class RegisterVariableFilter(object, ghidra.program.model.listing.VariableFilter):
        COMPOUND_STACK_VARIABLE_FILTER: ghidra.program.model.listing.VariableFilter
        LOCAL_VARIABLE_FILTER: ghidra.program.model.listing.VariableFilter
        MEMORY_VARIABLE_FILTER: ghidra.program.model.listing.VariableFilter
        NONAUTO_PARAMETER_FILTER: ghidra.program.model.listing.VariableFilter
        PARAMETER_FILTER: ghidra.program.model.listing.VariableFilter
        REGISTER_VARIABLE_FILTER: ghidra.program.model.listing.VariableFilter
        STACK_VARIABLE_FILTER: ghidra.program.model.listing.VariableFilter
        UNIQUE_VARIABLE_FILTER: ghidra.program.model.listing.VariableFilter



        def __init__(self): ...



        def equals(self, __a0: object) -> bool: ...

        def getClass(self) -> java.lang.Class: ...

        def hashCode(self) -> int: ...

        def matches(self, __a0: ghidra.program.model.listing.Variable) -> bool: ...

        def notify(self) -> None: ...

        def notifyAll(self) -> None: ...

        def toString(self) -> unicode: ...

        @overload
        def wait(self) -> None: ...

        @overload
        def wait(self, __a0: long) -> None: ...

        @overload
        def wait(self, __a0: long, __a1: int) -> None: ...







    def equals(self, __a0: object) -> bool: ...

    def getClass(self) -> java.lang.Class: ...

    def hashCode(self) -> int: ...

    def matches(self, variable: ghidra.program.model.listing.Variable) -> bool:
        """
        Determine if the specified variable matches this filter criteria
        @param variable
        @return true if variable satisfies the criteria of this filter
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

