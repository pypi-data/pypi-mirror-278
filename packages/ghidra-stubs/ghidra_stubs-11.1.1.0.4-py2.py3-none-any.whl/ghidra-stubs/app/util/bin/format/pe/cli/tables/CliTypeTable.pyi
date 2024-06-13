from typing import List
from typing import overload
import ghidra.app.util.bin.format.pe.cli.tables
import java.lang
import java.util


class CliTypeTable(java.lang.Enum):
    Assembly: ghidra.app.util.bin.format.pe.cli.tables.CliTypeTable
    AssemblyOS: ghidra.app.util.bin.format.pe.cli.tables.CliTypeTable
    AssemblyProcessor: ghidra.app.util.bin.format.pe.cli.tables.CliTypeTable
    AssemblyRef: ghidra.app.util.bin.format.pe.cli.tables.CliTypeTable
    AssemblyRefOS: ghidra.app.util.bin.format.pe.cli.tables.CliTypeTable
    AssemblyRefProcessor: ghidra.app.util.bin.format.pe.cli.tables.CliTypeTable
    ClassLayout: ghidra.app.util.bin.format.pe.cli.tables.CliTypeTable
    Constant: ghidra.app.util.bin.format.pe.cli.tables.CliTypeTable
    CustomAttribute: ghidra.app.util.bin.format.pe.cli.tables.CliTypeTable
    DeclSecurity: ghidra.app.util.bin.format.pe.cli.tables.CliTypeTable
    Event: ghidra.app.util.bin.format.pe.cli.tables.CliTypeTable
    EventMap: ghidra.app.util.bin.format.pe.cli.tables.CliTypeTable
    ExportedType: ghidra.app.util.bin.format.pe.cli.tables.CliTypeTable
    Field: ghidra.app.util.bin.format.pe.cli.tables.CliTypeTable
    FieldLayout: ghidra.app.util.bin.format.pe.cli.tables.CliTypeTable
    FieldMarshal: ghidra.app.util.bin.format.pe.cli.tables.CliTypeTable
    FieldRVA: ghidra.app.util.bin.format.pe.cli.tables.CliTypeTable
    File: ghidra.app.util.bin.format.pe.cli.tables.CliTypeTable
    GenericParam: ghidra.app.util.bin.format.pe.cli.tables.CliTypeTable
    GenericParamConstraint: ghidra.app.util.bin.format.pe.cli.tables.CliTypeTable
    ImplMap: ghidra.app.util.bin.format.pe.cli.tables.CliTypeTable
    InterfaceImpl: ghidra.app.util.bin.format.pe.cli.tables.CliTypeTable
    ManifestResource: ghidra.app.util.bin.format.pe.cli.tables.CliTypeTable
    MemberRef: ghidra.app.util.bin.format.pe.cli.tables.CliTypeTable
    MethodDef: ghidra.app.util.bin.format.pe.cli.tables.CliTypeTable
    MethodImpl: ghidra.app.util.bin.format.pe.cli.tables.CliTypeTable
    MethodSemantics: ghidra.app.util.bin.format.pe.cli.tables.CliTypeTable
    MethodSpec: ghidra.app.util.bin.format.pe.cli.tables.CliTypeTable
    Module: ghidra.app.util.bin.format.pe.cli.tables.CliTypeTable
    ModuleRef: ghidra.app.util.bin.format.pe.cli.tables.CliTypeTable
    NestedClass: ghidra.app.util.bin.format.pe.cli.tables.CliTypeTable
    Param: ghidra.app.util.bin.format.pe.cli.tables.CliTypeTable
    Property: ghidra.app.util.bin.format.pe.cli.tables.CliTypeTable
    PropertyMap: ghidra.app.util.bin.format.pe.cli.tables.CliTypeTable
    StandAloneSig: ghidra.app.util.bin.format.pe.cli.tables.CliTypeTable
    TypeDef: ghidra.app.util.bin.format.pe.cli.tables.CliTypeTable
    TypeRef: ghidra.app.util.bin.format.pe.cli.tables.CliTypeTable
    TypeSpec: ghidra.app.util.bin.format.pe.cli.tables.CliTypeTable







    @overload
    def compareTo(self, __a0: java.lang.Enum) -> int: ...

    @overload
    def compareTo(self, __a0: object) -> int: ...

    def describeConstable(self) -> java.util.Optional: ...

    def equals(self, __a0: object) -> bool: ...

    @staticmethod
    def fromId(__a0: int) -> ghidra.app.util.bin.format.pe.cli.tables.CliTypeTable: ...

    def getClass(self) -> java.lang.Class: ...

    def getDeclaringClass(self) -> java.lang.Class: ...

    def hashCode(self) -> int: ...

    def id(self) -> int: ...

    def name(self) -> unicode: ...

    def notify(self) -> None: ...

    def notifyAll(self) -> None: ...

    def ordinal(self) -> int: ...

    def toString(self) -> unicode: ...

    @overload
    @staticmethod
    def valueOf(__a0: unicode) -> ghidra.app.util.bin.format.pe.cli.tables.CliTypeTable: ...

    @overload
    @staticmethod
    def valueOf(__a0: java.lang.Class, __a1: unicode) -> java.lang.Enum: ...

    @staticmethod
    def values() -> List[ghidra.app.util.bin.format.pe.cli.tables.CliTypeTable]: ...

    @overload
    def wait(self) -> None: ...

    @overload
    def wait(self, __a0: long) -> None: ...

    @overload
    def wait(self, __a0: long, __a1: int) -> None: ...

