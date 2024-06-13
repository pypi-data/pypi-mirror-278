from typing import List
from typing import overload
import generic.jar
import ghidra.app.util.bin.format.dwarf
import ghidra.program.model.address
import ghidra.program.model.data
import ghidra.program.model.lang
import ghidra.program.model.listing
import ghidra.program.model.pcode
import java.lang
import java.lang.reflect


class DWARFUtil(object):




    def __init__(self): ...



    @staticmethod
    def appendComment(program: ghidra.program.model.listing.Program, address: ghidra.program.model.address.Address, commentType: int, prefix: unicode, comment: unicode, sep: unicode) -> None: ...

    @overload
    @staticmethod
    def appendDescription(dt: ghidra.program.model.data.DataType, description: unicode, sep: unicode) -> None:
        """
        Append a string to a {@link DataType}'s description.
        @param dt {@link DataType}
        @param description string to append, if null or empty nothing happens.
        @param sep characters to place after previous description to separate it from the
         new portion.
        """
        ...

    @overload
    @staticmethod
    def appendDescription(dtc: ghidra.program.model.data.DataTypeComponent, description: unicode, sep: unicode) -> None:
        """
        Append a string to a description of a field in a structure.
        @param dtc the {@link DataTypeComponent field} in a struct
        @param description string to append, if null or empty nothing happens.
        @param sep characters to place after previous description to separate it from the
         new portion.
        """
        ...

    @staticmethod
    def convertRegisterListToVarnodeStorage(__a0: List[object], __a1: int) -> List[object]: ...

    def equals(self, __a0: object) -> bool: ...

    @staticmethod
    def findLinkageNameInChildren(die: ghidra.app.util.bin.format.dwarf.DebugInfoEntry) -> List[unicode]:
        """
        Try to find gnu mangled name nesting info in a DIE's children's linkage strings.
         <p>
        @param die
        @return a list of string of nesting names, ending with what should be the DIE parameter's
         name.
        """
        ...

    @staticmethod
    def getAnonNameForMeFromParentContext(diea: ghidra.app.util.bin.format.dwarf.DIEAggregate) -> unicode:
        """
        Creates a name for anon types based on their position in their parent's childList.
         <p>
        @param diea the die aggregate.
        @return the anonymous name of the die aggregate.
        """
        ...

    @staticmethod
    def getAnonNameForMeFromParentContext2(diea: ghidra.app.util.bin.format.dwarf.DIEAggregate) -> unicode:
        """
        Creates a name for anon types based on the names of sibling entries that are using the anon type.
         <p>
         Example: "anon_struct_for_field1_field2"
         <p>
         Falls back to {@link #getAnonNameForMeFromParentContext(DIEAggregate)} if no siblings found.
        @param diea the die aggregate.
        @return the anonymous name of the die aggregate.
        """
        ...

    def getClass(self) -> java.lang.Class: ...

    @staticmethod
    def getCodeUnitForComment(program: ghidra.program.model.listing.Program, address: ghidra.program.model.address.Address) -> ghidra.program.model.listing.CodeUnit: ...

    @staticmethod
    def getLanguageDefinitionDirectory(lang: ghidra.program.model.lang.Language) -> generic.jar.ResourceFile:
        """
        Returns the base directory of a language definition.
        @param lang {@link Language} to get base definition directory
        @return base directory for language definition files
        @throws IOException if not a sleigh lang
        """
        ...

    @staticmethod
    def getLanguageExternalFile(lang: ghidra.program.model.lang.Language, name: unicode) -> generic.jar.ResourceFile:
        """
        Returns a file that has been referenced in the specified {@link Language language's}
         ldefs description via a
         <pre>&lt;external_name tool="<b>name</b>" name="<b>value</b>"/&gt;</pre>
         entry.
        @param lang {@link Language} to query
        @param name name of the option in the ldefs file
        @return file pointed to by the specified external_name tool entry
        @throws IOException if not a sleigh lang
        """
        ...

    @staticmethod
    def getLanguageExternalNameValue(lang: ghidra.program.model.lang.Language, name: unicode) -> unicode:
        """
        Returns a value specified in a {@link Language} definition via a
         <pre>&lt;external_name tool="<b>name</b>" name="<b>value</b>"/&gt;</pre>
         entry.
         <p>
        @param lang {@link Language} to query
        @param name name of the value
        @return String value
        @throws IOException
        """
        ...

    @staticmethod
    def getStaticFinalFieldWithValue(clazz: java.lang.Class, value: long) -> java.lang.reflect.Field:
        """
        Searches a Class for a final static variable that has a specific numeric value.
        @param clazz Class to search.
        @param value numeric value to search for
        @return Java reflection {@link Field} that has the specified value or null
        """
        ...

    @staticmethod
    def getStructLayoutFingerprint(diea: ghidra.app.util.bin.format.dwarf.DIEAggregate) -> unicode:
        """
        Creates a fingerprint of the layout of an (anonymous) structure using its
         size, number of members, and the hashcode of the member field names.
        @param diea struct/union/class
        @return formatted string, example "80_5_73dc6de9" (80 bytes, 5 fields, hex hash of field names)
        """
        ...

    @staticmethod
    def getTemplateBaseName(name: unicode) -> unicode:
        """
        Determines if a name is a C++ style templated name.  If so, returns just
         the base portion of the name.
         The name must have a start and end angle bracket: '&lt;' and '&gt;'.
         <p>
         operator&lt;() and operator&lt;&lt;() are handled so their angle brackets
         don't trigger the template start/end angle bracket incorrectly.
         <p>
        @param name symbol name with C++ template portions
        @return base portion of the symbol name without template portion
        """
        ...

    def hashCode(self) -> int: ...

    @staticmethod
    def isEmptyArray(dt: ghidra.program.model.data.DataType) -> bool: ...

    @staticmethod
    def isPointerDataType(diea: ghidra.app.util.bin.format.dwarf.DIEAggregate) -> bool: ...

    @staticmethod
    def isPointerTo(targetDIEA: ghidra.app.util.bin.format.dwarf.DIEAggregate, testDIEA: ghidra.app.util.bin.format.dwarf.DIEAggregate) -> bool: ...

    @staticmethod
    def isStackVarnode(varnode: ghidra.program.model.pcode.Varnode) -> bool: ...

    @staticmethod
    def isThisParam(paramDIEA: ghidra.app.util.bin.format.dwarf.DIEAggregate) -> bool: ...

    @staticmethod
    def isVoid(dt: ghidra.program.model.data.DataType) -> bool: ...

    @staticmethod
    def isZeroByteDataType(dt: ghidra.program.model.data.DataType) -> bool: ...

    def notify(self) -> None: ...

    def notifyAll(self) -> None: ...

    @staticmethod
    def packCompositeIfPossible(original: ghidra.program.model.data.Composite, dtm: ghidra.program.model.data.DataTypeManager) -> None: ...

    @staticmethod
    def parseMangledNestings(s: unicode) -> List[unicode]:
        """
        A lightweight attempt to get nesting (ie. namespaces and such) information
         from gnu mangled name strings.
         <p>
         For example, "_ZN19class1_inline_funcs3fooEv" -&gt;
         [19 chars]'class1_inline_funcs', [3 chars]'foo'
         <p>
        @param s
        @return 
        """
        ...

    @overload
    def toString(self) -> unicode: ...

    @overload
    @staticmethod
    def toString(clazz: java.lang.Class, value: long) -> unicode:
        """
        Returns the field name of a final static variable in class <code>clazz</code>
         which holds a specific value.
         <p>
         Can be thought of as an enum numeric value to to name lookup.
         <p>
        @param clazz
        @param value
        @return 
        """
        ...

    @overload
    @staticmethod
    def toString(clazz: java.lang.Class, value: int) -> unicode:
        """
        Converts a integer value to its corresponding symbolic name from the set of
         "public static final" member variables in a class.
         <p>
         This is a bit of a hack and probably originated from pre-java Enum days.
        @param clazz The {@link Class} to search for the matching static value.
        @param value the integer value to search for
        @return the String name of the matching field.
        """
        ...

    @overload
    def wait(self) -> None: ...

    @overload
    def wait(self, __a0: long) -> None: ...

    @overload
    def wait(self, __a0: long, __a1: int) -> None: ...

