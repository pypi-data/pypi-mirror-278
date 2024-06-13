from typing import List
from typing import overload
import ghidra.program.model.data
import ghidra.program.model.lang
import ghidra.program.model.lang.protorules
import ghidra.program.model.pcode
import ghidra.xml
import java.lang


class MultiSlotDualAssign(ghidra.program.model.lang.protorules.AssignAction):
    """
    Consume multiple registers from different storage classes to pass a data-type
 
     This action is for calling conventions that can use both floating-point and general purpose registers
     when assigning storage for a single composite data-type, such as the X86-64 System V ABI
    """





    def __init__(self, baseStore: ghidra.program.model.lang.StorageClass, altStore: ghidra.program.model.lang.StorageClass, mostSig: bool, justRight: bool, res: ghidra.program.model.lang.ParamListStandard): ...



    def assignAddress(self, dt: ghidra.program.model.data.DataType, proto: ghidra.program.model.lang.PrototypePieces, pos: int, dtManager: ghidra.program.model.data.DataTypeManager, status: List[int], res: ghidra.program.model.lang.ParameterPieces) -> int: ...

    def clone(self, newResource: ghidra.program.model.lang.ParamListStandard) -> ghidra.program.model.lang.protorules.AssignAction: ...

    def encode(self, encoder: ghidra.program.model.pcode.Encoder) -> None: ...

    def equals(self, __a0: object) -> bool: ...

    def getClass(self) -> java.lang.Class: ...

    def hashCode(self) -> int: ...

    def isEquivalent(self, op: ghidra.program.model.lang.protorules.AssignAction) -> bool: ...

    def notify(self) -> None: ...

    def notifyAll(self) -> None: ...

    @staticmethod
    def restoreActionXml(parser: ghidra.xml.XmlPullParser, res: ghidra.program.model.lang.ParamListStandard) -> ghidra.program.model.lang.protorules.AssignAction:
        """
        Read the next action element from the stream and return the new configured
         AssignAction object.  If the next element is not an action, throw an exception.
        @param parser is the stream parser
        @param res is the resource set for the new action
        @return the new action
        @throws XmlParseException for problems parsing the stream
        """
        ...

    @staticmethod
    def restoreSideeffectXml(parser: ghidra.xml.XmlPullParser, res: ghidra.program.model.lang.ParamListStandard) -> ghidra.program.model.lang.protorules.AssignAction:
        """
        Read the next sideeffect element from the stream and return the new configured
         AssignAction object.  If the next element is not a sideeffect, throw an exception.
        @param parser is the stream parser
        @param res is the resource set for the new sideeffect
        @return the new sideeffect
        @throws XmlParseException for problems parsing the stream
        """
        ...

    def restoreXml(self, parser: ghidra.xml.XmlPullParser) -> None: ...

    def toString(self) -> unicode: ...

    @overload
    def wait(self) -> None: ...

    @overload
    def wait(self, __a0: long) -> None: ...

    @overload
    def wait(self, __a0: long, __a1: int) -> None: ...

