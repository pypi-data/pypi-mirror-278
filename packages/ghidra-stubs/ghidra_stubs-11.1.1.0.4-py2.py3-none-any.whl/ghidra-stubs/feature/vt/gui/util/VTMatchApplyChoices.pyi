from typing import List
from typing import overload
import ghidra.feature.vt.gui.util
import java.lang
import java.util


class VTMatchApplyChoices(object):





    class ParameterDataTypeChoices(java.lang.Enum):
        EXCLUDE: ghidra.feature.vt.gui.util.VTMatchApplyChoices.ParameterDataTypeChoices
        REPLACE: ghidra.feature.vt.gui.util.VTMatchApplyChoices.ParameterDataTypeChoices
        REPLACE_UNDEFINED_DATA_TYPES_ONLY: ghidra.feature.vt.gui.util.VTMatchApplyChoices.ParameterDataTypeChoices







        @overload
        def compareTo(self, __a0: java.lang.Enum) -> int: ...

        @overload
        def compareTo(self, __a0: object) -> int: ...

        def describeConstable(self) -> java.util.Optional: ...

        def equals(self, __a0: object) -> bool: ...

        def getClass(self) -> java.lang.Class: ...

        def getDeclaringClass(self) -> java.lang.Class: ...

        def hashCode(self) -> int: ...

        def name(self) -> unicode: ...

        def notify(self) -> None: ...

        def notifyAll(self) -> None: ...

        def ordinal(self) -> int: ...

        def toString(self) -> unicode: ...

        @overload
        @staticmethod
        def valueOf(__a0: unicode) -> ghidra.feature.vt.gui.util.VTMatchApplyChoices.ParameterDataTypeChoices: ...

        @overload
        @staticmethod
        def valueOf(__a0: java.lang.Class, __a1: unicode) -> java.lang.Enum: ...

        @staticmethod
        def values() -> List[ghidra.feature.vt.gui.util.VTMatchApplyChoices.ParameterDataTypeChoices]: ...

        @overload
        def wait(self) -> None: ...

        @overload
        def wait(self, __a0: long) -> None: ...

        @overload
        def wait(self, __a0: long, __a1: int) -> None: ...






    class HighestSourcePriorityChoices(java.lang.Enum):
        IMPORT_PRIORITY_HIGHEST: ghidra.feature.vt.gui.util.VTMatchApplyChoices.HighestSourcePriorityChoices
        USER_PRIORITY_HIGHEST: ghidra.feature.vt.gui.util.VTMatchApplyChoices.HighestSourcePriorityChoices







        @overload
        def compareTo(self, __a0: java.lang.Enum) -> int: ...

        @overload
        def compareTo(self, __a0: object) -> int: ...

        def describeConstable(self) -> java.util.Optional: ...

        def equals(self, __a0: object) -> bool: ...

        def getClass(self) -> java.lang.Class: ...

        def getDeclaringClass(self) -> java.lang.Class: ...

        def hashCode(self) -> int: ...

        def name(self) -> unicode: ...

        def notify(self) -> None: ...

        def notifyAll(self) -> None: ...

        def ordinal(self) -> int: ...

        def toString(self) -> unicode: ...

        @overload
        @staticmethod
        def valueOf(__a0: unicode) -> ghidra.feature.vt.gui.util.VTMatchApplyChoices.HighestSourcePriorityChoices: ...

        @overload
        @staticmethod
        def valueOf(__a0: java.lang.Class, __a1: unicode) -> java.lang.Enum: ...

        @staticmethod
        def values() -> List[ghidra.feature.vt.gui.util.VTMatchApplyChoices.HighestSourcePriorityChoices]: ...

        @overload
        def wait(self) -> None: ...

        @overload
        def wait(self, __a0: long) -> None: ...

        @overload
        def wait(self, __a0: long, __a1: int) -> None: ...






    class FunctionAttributeChoices(java.lang.Enum):
        EXCLUDE: ghidra.feature.vt.gui.util.VTMatchApplyChoices.FunctionAttributeChoices
        REPLACE: ghidra.feature.vt.gui.util.VTMatchApplyChoices.FunctionAttributeChoices
        WHEN_TAKING_SIGNATURE: ghidra.feature.vt.gui.util.VTMatchApplyChoices.FunctionAttributeChoices







        @overload
        def compareTo(self, __a0: java.lang.Enum) -> int: ...

        @overload
        def compareTo(self, __a0: object) -> int: ...

        def describeConstable(self) -> java.util.Optional: ...

        def equals(self, __a0: object) -> bool: ...

        def getClass(self) -> java.lang.Class: ...

        def getDeclaringClass(self) -> java.lang.Class: ...

        def hashCode(self) -> int: ...

        def name(self) -> unicode: ...

        def notify(self) -> None: ...

        def notifyAll(self) -> None: ...

        def ordinal(self) -> int: ...

        def toString(self) -> unicode: ...

        @overload
        @staticmethod
        def valueOf(__a0: unicode) -> ghidra.feature.vt.gui.util.VTMatchApplyChoices.FunctionAttributeChoices: ...

        @overload
        @staticmethod
        def valueOf(__a0: java.lang.Class, __a1: unicode) -> java.lang.Enum: ...

        @staticmethod
        def values() -> List[ghidra.feature.vt.gui.util.VTMatchApplyChoices.FunctionAttributeChoices]: ...

        @overload
        def wait(self) -> None: ...

        @overload
        def wait(self, __a0: long) -> None: ...

        @overload
        def wait(self, __a0: long, __a1: int) -> None: ...






    class CallingConventionChoices(java.lang.Enum):
        EXCLUDE: ghidra.feature.vt.gui.util.VTMatchApplyChoices.CallingConventionChoices
        NAME_MATCH: ghidra.feature.vt.gui.util.VTMatchApplyChoices.CallingConventionChoices
        SAME_LANGUAGE: ghidra.feature.vt.gui.util.VTMatchApplyChoices.CallingConventionChoices







        @overload
        def compareTo(self, __a0: java.lang.Enum) -> int: ...

        @overload
        def compareTo(self, __a0: object) -> int: ...

        def describeConstable(self) -> java.util.Optional: ...

        def equals(self, __a0: object) -> bool: ...

        def getClass(self) -> java.lang.Class: ...

        def getDeclaringClass(self) -> java.lang.Class: ...

        def hashCode(self) -> int: ...

        def name(self) -> unicode: ...

        def notify(self) -> None: ...

        def notifyAll(self) -> None: ...

        def ordinal(self) -> int: ...

        def toString(self) -> unicode: ...

        @overload
        @staticmethod
        def valueOf(__a0: unicode) -> ghidra.feature.vt.gui.util.VTMatchApplyChoices.CallingConventionChoices: ...

        @overload
        @staticmethod
        def valueOf(__a0: java.lang.Class, __a1: unicode) -> java.lang.Enum: ...

        @staticmethod
        def values() -> List[ghidra.feature.vt.gui.util.VTMatchApplyChoices.CallingConventionChoices]: ...

        @overload
        def wait(self) -> None: ...

        @overload
        def wait(self, __a0: long) -> None: ...

        @overload
        def wait(self, __a0: long, __a1: int) -> None: ...






    class ReplaceChoices(java.lang.Enum):
        EXCLUDE: ghidra.feature.vt.gui.util.VTMatchApplyChoices.ReplaceChoices
        REPLACE: ghidra.feature.vt.gui.util.VTMatchApplyChoices.ReplaceChoices







        @overload
        def compareTo(self, __a0: java.lang.Enum) -> int: ...

        @overload
        def compareTo(self, __a0: object) -> int: ...

        def describeConstable(self) -> java.util.Optional: ...

        def equals(self, __a0: object) -> bool: ...

        def getClass(self) -> java.lang.Class: ...

        def getDeclaringClass(self) -> java.lang.Class: ...

        def hashCode(self) -> int: ...

        def name(self) -> unicode: ...

        def notify(self) -> None: ...

        def notifyAll(self) -> None: ...

        def ordinal(self) -> int: ...

        def toString(self) -> unicode: ...

        @overload
        @staticmethod
        def valueOf(__a0: unicode) -> ghidra.feature.vt.gui.util.VTMatchApplyChoices.ReplaceChoices: ...

        @overload
        @staticmethod
        def valueOf(__a0: java.lang.Class, __a1: unicode) -> java.lang.Enum: ...

        @staticmethod
        def values() -> List[ghidra.feature.vt.gui.util.VTMatchApplyChoices.ReplaceChoices]: ...

        @overload
        def wait(self) -> None: ...

        @overload
        def wait(self, __a0: long) -> None: ...

        @overload
        def wait(self, __a0: long, __a1: int) -> None: ...






    class FunctionSignatureChoices(java.lang.Enum):
        EXCLUDE: ghidra.feature.vt.gui.util.VTMatchApplyChoices.FunctionSignatureChoices
        REPLACE: ghidra.feature.vt.gui.util.VTMatchApplyChoices.FunctionSignatureChoices
        WHEN_SAME_PARAMETER_COUNT: ghidra.feature.vt.gui.util.VTMatchApplyChoices.FunctionSignatureChoices







        @overload
        def compareTo(self, __a0: java.lang.Enum) -> int: ...

        @overload
        def compareTo(self, __a0: object) -> int: ...

        def describeConstable(self) -> java.util.Optional: ...

        def equals(self, __a0: object) -> bool: ...

        def getClass(self) -> java.lang.Class: ...

        def getDeclaringClass(self) -> java.lang.Class: ...

        def hashCode(self) -> int: ...

        def name(self) -> unicode: ...

        def notify(self) -> None: ...

        def notifyAll(self) -> None: ...

        def ordinal(self) -> int: ...

        def toString(self) -> unicode: ...

        @overload
        @staticmethod
        def valueOf(__a0: unicode) -> ghidra.feature.vt.gui.util.VTMatchApplyChoices.FunctionSignatureChoices: ...

        @overload
        @staticmethod
        def valueOf(__a0: java.lang.Class, __a1: unicode) -> java.lang.Enum: ...

        @staticmethod
        def values() -> List[ghidra.feature.vt.gui.util.VTMatchApplyChoices.FunctionSignatureChoices]: ...

        @overload
        def wait(self) -> None: ...

        @overload
        def wait(self, __a0: long) -> None: ...

        @overload
        def wait(self, __a0: long, __a1: int) -> None: ...






    class ReplaceDefaultChoices(java.lang.Enum):
        EXCLUDE: ghidra.feature.vt.gui.util.VTMatchApplyChoices.ReplaceDefaultChoices
        REPLACE_ALWAYS: ghidra.feature.vt.gui.util.VTMatchApplyChoices.ReplaceDefaultChoices
        REPLACE_DEFAULT_ONLY: ghidra.feature.vt.gui.util.VTMatchApplyChoices.ReplaceDefaultChoices







        @overload
        def compareTo(self, __a0: java.lang.Enum) -> int: ...

        @overload
        def compareTo(self, __a0: object) -> int: ...

        def describeConstable(self) -> java.util.Optional: ...

        def equals(self, __a0: object) -> bool: ...

        def getClass(self) -> java.lang.Class: ...

        def getDeclaringClass(self) -> java.lang.Class: ...

        def hashCode(self) -> int: ...

        def name(self) -> unicode: ...

        def notify(self) -> None: ...

        def notifyAll(self) -> None: ...

        def ordinal(self) -> int: ...

        def toString(self) -> unicode: ...

        @overload
        @staticmethod
        def valueOf(__a0: unicode) -> ghidra.feature.vt.gui.util.VTMatchApplyChoices.ReplaceDefaultChoices: ...

        @overload
        @staticmethod
        def valueOf(__a0: java.lang.Class, __a1: unicode) -> java.lang.Enum: ...

        @staticmethod
        def values() -> List[ghidra.feature.vt.gui.util.VTMatchApplyChoices.ReplaceDefaultChoices]: ...

        @overload
        def wait(self) -> None: ...

        @overload
        def wait(self, __a0: long) -> None: ...

        @overload
        def wait(self, __a0: long, __a1: int) -> None: ...






    class SourcePriorityChoices(java.lang.Enum):
        EXCLUDE: ghidra.feature.vt.gui.util.VTMatchApplyChoices.SourcePriorityChoices
        PRIORITY_REPLACE: ghidra.feature.vt.gui.util.VTMatchApplyChoices.SourcePriorityChoices
        REPLACE: ghidra.feature.vt.gui.util.VTMatchApplyChoices.SourcePriorityChoices
        REPLACE_DEFAULTS_ONLY: ghidra.feature.vt.gui.util.VTMatchApplyChoices.SourcePriorityChoices







        @overload
        def compareTo(self, __a0: java.lang.Enum) -> int: ...

        @overload
        def compareTo(self, __a0: object) -> int: ...

        def describeConstable(self) -> java.util.Optional: ...

        def equals(self, __a0: object) -> bool: ...

        def getClass(self) -> java.lang.Class: ...

        def getDeclaringClass(self) -> java.lang.Class: ...

        def hashCode(self) -> int: ...

        def name(self) -> unicode: ...

        def notify(self) -> None: ...

        def notifyAll(self) -> None: ...

        def ordinal(self) -> int: ...

        def toString(self) -> unicode: ...

        @overload
        @staticmethod
        def valueOf(__a0: unicode) -> ghidra.feature.vt.gui.util.VTMatchApplyChoices.SourcePriorityChoices: ...

        @overload
        @staticmethod
        def valueOf(__a0: java.lang.Class, __a1: unicode) -> java.lang.Enum: ...

        @staticmethod
        def values() -> List[ghidra.feature.vt.gui.util.VTMatchApplyChoices.SourcePriorityChoices]: ...

        @overload
        def wait(self) -> None: ...

        @overload
        def wait(self, __a0: long) -> None: ...

        @overload
        def wait(self, __a0: long, __a1: int) -> None: ...






    class ReplaceDataChoices(java.lang.Enum):
        EXCLUDE: ghidra.feature.vt.gui.util.VTMatchApplyChoices.ReplaceDataChoices
        REPLACE_ALL_DATA: ghidra.feature.vt.gui.util.VTMatchApplyChoices.ReplaceDataChoices
        REPLACE_FIRST_DATA_ONLY: ghidra.feature.vt.gui.util.VTMatchApplyChoices.ReplaceDataChoices
        REPLACE_UNDEFINED_DATA_ONLY: ghidra.feature.vt.gui.util.VTMatchApplyChoices.ReplaceDataChoices







        @overload
        def compareTo(self, __a0: java.lang.Enum) -> int: ...

        @overload
        def compareTo(self, __a0: object) -> int: ...

        def describeConstable(self) -> java.util.Optional: ...

        def equals(self, __a0: object) -> bool: ...

        def getClass(self) -> java.lang.Class: ...

        def getDeclaringClass(self) -> java.lang.Class: ...

        def hashCode(self) -> int: ...

        def name(self) -> unicode: ...

        def notify(self) -> None: ...

        def notifyAll(self) -> None: ...

        def ordinal(self) -> int: ...

        def toString(self) -> unicode: ...

        @overload
        @staticmethod
        def valueOf(__a0: unicode) -> ghidra.feature.vt.gui.util.VTMatchApplyChoices.ReplaceDataChoices: ...

        @overload
        @staticmethod
        def valueOf(__a0: java.lang.Class, __a1: unicode) -> java.lang.Enum: ...

        @staticmethod
        def values() -> List[ghidra.feature.vt.gui.util.VTMatchApplyChoices.ReplaceDataChoices]: ...

        @overload
        def wait(self) -> None: ...

        @overload
        def wait(self, __a0: long) -> None: ...

        @overload
        def wait(self, __a0: long, __a1: int) -> None: ...






    class ParameterSourceChoices(java.lang.Enum):
        ENTIRE_PARAMETER_SIGNATURE_MARKUP: ghidra.feature.vt.gui.util.VTMatchApplyChoices.ParameterSourceChoices
        INDIVIDUAL_PARAMETER_MARKUP: ghidra.feature.vt.gui.util.VTMatchApplyChoices.ParameterSourceChoices







        @overload
        def compareTo(self, __a0: java.lang.Enum) -> int: ...

        @overload
        def compareTo(self, __a0: object) -> int: ...

        def describeConstable(self) -> java.util.Optional: ...

        def equals(self, __a0: object) -> bool: ...

        def getClass(self) -> java.lang.Class: ...

        def getDeclaringClass(self) -> java.lang.Class: ...

        def hashCode(self) -> int: ...

        def name(self) -> unicode: ...

        def notify(self) -> None: ...

        def notifyAll(self) -> None: ...

        def ordinal(self) -> int: ...

        def toString(self) -> unicode: ...

        @overload
        @staticmethod
        def valueOf(__a0: unicode) -> ghidra.feature.vt.gui.util.VTMatchApplyChoices.ParameterSourceChoices: ...

        @overload
        @staticmethod
        def valueOf(__a0: java.lang.Class, __a1: unicode) -> java.lang.Enum: ...

        @staticmethod
        def values() -> List[ghidra.feature.vt.gui.util.VTMatchApplyChoices.ParameterSourceChoices]: ...

        @overload
        def wait(self) -> None: ...

        @overload
        def wait(self, __a0: long) -> None: ...

        @overload
        def wait(self, __a0: long, __a1: int) -> None: ...






    class LabelChoices(java.lang.Enum):
        ADD: ghidra.feature.vt.gui.util.VTMatchApplyChoices.LabelChoices
        ADD_AS_PRIMARY: ghidra.feature.vt.gui.util.VTMatchApplyChoices.LabelChoices
        EXCLUDE: ghidra.feature.vt.gui.util.VTMatchApplyChoices.LabelChoices
        REPLACE_ALL: ghidra.feature.vt.gui.util.VTMatchApplyChoices.LabelChoices
        REPLACE_DEFAULT_ONLY: ghidra.feature.vt.gui.util.VTMatchApplyChoices.LabelChoices







        @overload
        def compareTo(self, __a0: java.lang.Enum) -> int: ...

        @overload
        def compareTo(self, __a0: object) -> int: ...

        def describeConstable(self) -> java.util.Optional: ...

        def equals(self, __a0: object) -> bool: ...

        def getClass(self) -> java.lang.Class: ...

        def getDeclaringClass(self) -> java.lang.Class: ...

        def hashCode(self) -> int: ...

        def name(self) -> unicode: ...

        def notify(self) -> None: ...

        def notifyAll(self) -> None: ...

        def ordinal(self) -> int: ...

        def toString(self) -> unicode: ...

        @overload
        @staticmethod
        def valueOf(__a0: unicode) -> ghidra.feature.vt.gui.util.VTMatchApplyChoices.LabelChoices: ...

        @overload
        @staticmethod
        def valueOf(__a0: java.lang.Class, __a1: unicode) -> java.lang.Enum: ...

        @staticmethod
        def values() -> List[ghidra.feature.vt.gui.util.VTMatchApplyChoices.LabelChoices]: ...

        @overload
        def wait(self) -> None: ...

        @overload
        def wait(self, __a0: long) -> None: ...

        @overload
        def wait(self, __a0: long, __a1: int) -> None: ...






    class FunctionNameChoices(java.lang.Enum):
        ADD: ghidra.feature.vt.gui.util.VTMatchApplyChoices.FunctionNameChoices
        ADD_AS_PRIMARY: ghidra.feature.vt.gui.util.VTMatchApplyChoices.FunctionNameChoices
        EXCLUDE: ghidra.feature.vt.gui.util.VTMatchApplyChoices.FunctionNameChoices
        REPLACE_ALWAYS: ghidra.feature.vt.gui.util.VTMatchApplyChoices.FunctionNameChoices
        REPLACE_DEFAULT_ONLY: ghidra.feature.vt.gui.util.VTMatchApplyChoices.FunctionNameChoices







        @overload
        def compareTo(self, __a0: java.lang.Enum) -> int: ...

        @overload
        def compareTo(self, __a0: object) -> int: ...

        def describeConstable(self) -> java.util.Optional: ...

        def equals(self, __a0: object) -> bool: ...

        def getClass(self) -> java.lang.Class: ...

        def getDeclaringClass(self) -> java.lang.Class: ...

        def hashCode(self) -> int: ...

        def name(self) -> unicode: ...

        def notify(self) -> None: ...

        def notifyAll(self) -> None: ...

        def ordinal(self) -> int: ...

        def toString(self) -> unicode: ...

        @overload
        @staticmethod
        def valueOf(__a0: unicode) -> ghidra.feature.vt.gui.util.VTMatchApplyChoices.FunctionNameChoices: ...

        @overload
        @staticmethod
        def valueOf(__a0: java.lang.Class, __a1: unicode) -> java.lang.Enum: ...

        @staticmethod
        def values() -> List[ghidra.feature.vt.gui.util.VTMatchApplyChoices.FunctionNameChoices]: ...

        @overload
        def wait(self) -> None: ...

        @overload
        def wait(self, __a0: long) -> None: ...

        @overload
        def wait(self, __a0: long, __a1: int) -> None: ...






    class CommentChoices(java.lang.Enum):
        APPEND_TO_EXISTING: ghidra.feature.vt.gui.util.VTMatchApplyChoices.CommentChoices
        EXCLUDE: ghidra.feature.vt.gui.util.VTMatchApplyChoices.CommentChoices
        OVERWRITE_EXISTING: ghidra.feature.vt.gui.util.VTMatchApplyChoices.CommentChoices







        @overload
        def compareTo(self, __a0: java.lang.Enum) -> int: ...

        @overload
        def compareTo(self, __a0: object) -> int: ...

        def describeConstable(self) -> java.util.Optional: ...

        def equals(self, __a0: object) -> bool: ...

        def getClass(self) -> java.lang.Class: ...

        def getDeclaringClass(self) -> java.lang.Class: ...

        def hashCode(self) -> int: ...

        def name(self) -> unicode: ...

        def notify(self) -> None: ...

        def notifyAll(self) -> None: ...

        def ordinal(self) -> int: ...

        def toString(self) -> unicode: ...

        @overload
        @staticmethod
        def valueOf(__a0: unicode) -> ghidra.feature.vt.gui.util.VTMatchApplyChoices.CommentChoices: ...

        @overload
        @staticmethod
        def valueOf(__a0: java.lang.Class, __a1: unicode) -> java.lang.Enum: ...

        @staticmethod
        def values() -> List[ghidra.feature.vt.gui.util.VTMatchApplyChoices.CommentChoices]: ...

        @overload
        def wait(self) -> None: ...

        @overload
        def wait(self, __a0: long) -> None: ...

        @overload
        def wait(self, __a0: long, __a1: int) -> None: ...



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

