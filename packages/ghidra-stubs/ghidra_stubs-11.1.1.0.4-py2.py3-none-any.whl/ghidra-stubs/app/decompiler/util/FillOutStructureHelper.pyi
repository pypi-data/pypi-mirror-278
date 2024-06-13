from typing import List
from typing import overload
import ghidra.app.decompiler.util.FillOutStructureHelper
import ghidra.program.model.address
import ghidra.program.model.data
import ghidra.program.model.listing
import ghidra.program.model.pcode
import java.lang


class FillOutStructureHelper(object):
    """
    Automatically creates a structure definition based on the references found by the decompiler.

     If the parameter is already a structure pointer, any new references found will be added
     to the structure, even if the structure must grow.
    """






    class OffsetPcodeOpPair(object):




        def __init__(self, __a0: long, __a1: ghidra.program.model.pcode.PcodeOp): ...



        def equals(self, __a0: object) -> bool: ...

        def getClass(self) -> java.lang.Class: ...

        def getOffset(self) -> long: ...

        def getPcodeOp(self) -> ghidra.program.model.pcode.PcodeOp: ...

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
        def offset(self) -> long: ...

        @property
        def pcodeOp(self) -> ghidra.program.model.pcode.PcodeOp: ...

    def __init__(self, program: ghidra.program.model.listing.Program, decompileOptions: ghidra.app.decompiler.DecompileOptions, monitor: ghidra.util.task.TaskMonitor):
        """
        Constructor.
        @param program the current program
        @param decompileOptions decompiler options 
           (see {@link DecompilerUtils#getDecompileOptions(ServiceProvider, Program)})
        @param monitor task monitor
        """
        ...



    def computeHighVariable(self, storageAddress: ghidra.program.model.address.Address, function: ghidra.program.model.listing.Function) -> ghidra.program.model.pcode.HighVariable:
        """
        Decompile a function and return the resulting HighVariable associated with a storage address
        @param storageAddress the storage address of the variable
        @param function is the function
        @return the corresponding HighVariable or null
        """
        ...

    def equals(self, __a0: object) -> bool: ...

    def getClass(self) -> java.lang.Class: ...

    def getComponentMap(self) -> ghidra.program.model.data.NoisyStructureBuilder:
        """
        Retrieve the component map that was generated when structure was created using decompiler 
         info. Results are not valid until 
         {@link #processStructure(HighVariable, Function, boolean, boolean)} is invoked.
        @return componentMap
        """
        ...

    def getLoadPcodeOps(self) -> List[ghidra.app.decompiler.util.FillOutStructureHelper.OffsetPcodeOpPair]:
        """
        Retrieve the offset/pcodeOp pairs that are used to load data from the variable
         used to fill-out structure.
         Results are not valid until 
         {@link #processStructure(HighVariable, Function, boolean, boolean)} is invoked.
        @return the pcodeOps doing the loading from the associated variable
        """
        ...

    def getStorePcodeOps(self) -> List[ghidra.app.decompiler.util.FillOutStructureHelper.OffsetPcodeOpPair]:
        """
        Retrieve the offset/pcodeOp pairs that are used to store data into the variable
         used to fill-out structure.
         Results are not valid until 
         {@link #processStructure(HighVariable, Function, boolean, boolean)} is invoked.
        @return the pcodeOps doing the storing to the associated variable
        """
        ...

    @staticmethod
    def getStructureForExtending(dt: ghidra.program.model.data.DataType) -> ghidra.program.model.data.Structure:
        """
        Check if a variable has a data-type that is suitable for being extended.
         If so return the structure data-type, otherwise return null.
         Modulo typedefs, the data-type of the variable must be exactly a
         "pointer to a structure".  Not a "structure" itself, or a
         "pointer to a pointer to ... a structure".
        @param dt is the data-type of the variable to test
        @return the extendable structure data-type or null
        """
        ...

    def hashCode(self) -> int: ...

    def notify(self) -> None: ...

    def notifyAll(self) -> None: ...

    def processStructure(self, var: ghidra.program.model.pcode.HighVariable, function: ghidra.program.model.listing.Function, createNewStructure: bool, createClassIfNeeded: bool) -> ghidra.program.model.data.Structure:
        """
        Method to create a structure data type for a variable in the given function.
         Unlike the applyTo() action, this method will not modify the function, its variables,
         or any existing data-types. A new structure is always created.
        @param var a parameter, local variable, or global variable used in the given function
        @param function the function to process
        @param createNewStructure if true a new structure with a unique name will always be generated,
         if false and variable corresponds to a structure pointer the existing structure will be 
         updated instead.
        @param createClassIfNeeded if true and variable corresponds to a <B>this</B> pointer without 
         an assigned Ghidra Class (i.e., {@code void * this}), the function will be assigned to a 
         new unique Ghidra Class namespace with a new identically named structure returned.  If false,
         a new uniquely structure will be created.
        @return a filled-in structure or null if one could not be created
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
    def componentMap(self) -> ghidra.program.model.data.NoisyStructureBuilder: ...

    @property
    def loadPcodeOps(self) -> List[object]: ...

    @property
    def storePcodeOps(self) -> List[object]: ...