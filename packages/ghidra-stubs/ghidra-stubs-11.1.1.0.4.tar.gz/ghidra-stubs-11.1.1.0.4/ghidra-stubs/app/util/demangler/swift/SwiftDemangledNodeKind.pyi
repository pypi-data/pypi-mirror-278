from typing import List
from typing import overload
import ghidra.app.util.demangler.swift
import java.lang
import java.util


class SwiftDemangledNodeKind(java.lang.Enum):
    Allocator: ghidra.app.util.demangler.swift.SwiftDemangledNodeKind
    AnonymousDescriptor: ghidra.app.util.demangler.swift.SwiftDemangledNodeKind
    ArgumentTuple: ghidra.app.util.demangler.swift.SwiftDemangledNodeKind
    BoundGenericStructure: ghidra.app.util.demangler.swift.SwiftDemangledNodeKind
    BuiltinTypeName: ghidra.app.util.demangler.swift.SwiftDemangledNodeKind
    Class: ghidra.app.util.demangler.swift.SwiftDemangledNodeKind
    Constructor: ghidra.app.util.demangler.swift.SwiftDemangledNodeKind
    Deallocator: ghidra.app.util.demangler.swift.SwiftDemangledNodeKind
    DefaultArgumentInitializer: ghidra.app.util.demangler.swift.SwiftDemangledNodeKind
    DependentGenericParamType: ghidra.app.util.demangler.swift.SwiftDemangledNodeKind
    DependentGenericType: ghidra.app.util.demangler.swift.SwiftDemangledNodeKind
    Destructor: ghidra.app.util.demangler.swift.SwiftDemangledNodeKind
    DispatchThunk: ghidra.app.util.demangler.swift.SwiftDemangledNodeKind
    Enum: ghidra.app.util.demangler.swift.SwiftDemangledNodeKind
    Extension: ghidra.app.util.demangler.swift.SwiftDemangledNodeKind
    FirstElementMarker: ghidra.app.util.demangler.swift.SwiftDemangledNodeKind
    Function: ghidra.app.util.demangler.swift.SwiftDemangledNodeKind
    FunctionType: ghidra.app.util.demangler.swift.SwiftDemangledNodeKind
    GenericSpecialization: ghidra.app.util.demangler.swift.SwiftDemangledNodeKind
    Getter: ghidra.app.util.demangler.swift.SwiftDemangledNodeKind
    Global: ghidra.app.util.demangler.swift.SwiftDemangledNodeKind
    GlobalVariableOnceDeclList: ghidra.app.util.demangler.swift.SwiftDemangledNodeKind
    GlobalVariableOnceFunction: ghidra.app.util.demangler.swift.SwiftDemangledNodeKind
    Identifier: ghidra.app.util.demangler.swift.SwiftDemangledNodeKind
    InOut: ghidra.app.util.demangler.swift.SwiftDemangledNodeKind
    InfixOperator: ghidra.app.util.demangler.swift.SwiftDemangledNodeKind
    Initializer: ghidra.app.util.demangler.swift.SwiftDemangledNodeKind
    LabelList: ghidra.app.util.demangler.swift.SwiftDemangledNodeKind
    LazyProtocolWitnessTableAccessor: ghidra.app.util.demangler.swift.SwiftDemangledNodeKind
    LocalDeclName: ghidra.app.util.demangler.swift.SwiftDemangledNodeKind
    MergedFunction: ghidra.app.util.demangler.swift.SwiftDemangledNodeKind
    ModifyAccessor: ghidra.app.util.demangler.swift.SwiftDemangledNodeKind
    Module: ghidra.app.util.demangler.swift.SwiftDemangledNodeKind
    ModuleDescriptor: ghidra.app.util.demangler.swift.SwiftDemangledNodeKind
    NominalTypeDescriptor: ghidra.app.util.demangler.swift.SwiftDemangledNodeKind
    Number: ghidra.app.util.demangler.swift.SwiftDemangledNodeKind
    ObjCAttribute: ghidra.app.util.demangler.swift.SwiftDemangledNodeKind
    OutlinedConsume: ghidra.app.util.demangler.swift.SwiftDemangledNodeKind
    OutlinedCopy: ghidra.app.util.demangler.swift.SwiftDemangledNodeKind
    Owned: ghidra.app.util.demangler.swift.SwiftDemangledNodeKind
    PrivateDeclName: ghidra.app.util.demangler.swift.SwiftDemangledNodeKind
    Protocol: ghidra.app.util.demangler.swift.SwiftDemangledNodeKind
    ProtocolConformance: ghidra.app.util.demangler.swift.SwiftDemangledNodeKind
    ProtocolConformanceDescriptor: ghidra.app.util.demangler.swift.SwiftDemangledNodeKind
    ProtocolDescriptor: ghidra.app.util.demangler.swift.SwiftDemangledNodeKind
    ProtocolWitness: ghidra.app.util.demangler.swift.SwiftDemangledNodeKind
    ReflectionMetadataBuiltinDescriptor: ghidra.app.util.demangler.swift.SwiftDemangledNodeKind
    ReflectionMetadataFieldDescriptor: ghidra.app.util.demangler.swift.SwiftDemangledNodeKind
    ReturnType: ghidra.app.util.demangler.swift.SwiftDemangledNodeKind
    Setter: ghidra.app.util.demangler.swift.SwiftDemangledNodeKind
    Static: ghidra.app.util.demangler.swift.SwiftDemangledNodeKind
    Structure: ghidra.app.util.demangler.swift.SwiftDemangledNodeKind
    Subscript: ghidra.app.util.demangler.swift.SwiftDemangledNodeKind
    Suffix: ghidra.app.util.demangler.swift.SwiftDemangledNodeKind
    Tuple: ghidra.app.util.demangler.swift.SwiftDemangledNodeKind
    TupleElement: ghidra.app.util.demangler.swift.SwiftDemangledNodeKind
    TupleElementName: ghidra.app.util.demangler.swift.SwiftDemangledNodeKind
    Type: ghidra.app.util.demangler.swift.SwiftDemangledNodeKind
    TypeAlias: ghidra.app.util.demangler.swift.SwiftDemangledNodeKind
    TypeList: ghidra.app.util.demangler.swift.SwiftDemangledNodeKind
    TypeMetadataAccessFunction: ghidra.app.util.demangler.swift.SwiftDemangledNodeKind
    UnsafeMutableAddressor: ghidra.app.util.demangler.swift.SwiftDemangledNodeKind
    Unsupported: ghidra.app.util.demangler.swift.SwiftDemangledNodeKind
    Variable: ghidra.app.util.demangler.swift.SwiftDemangledNodeKind







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
    def valueOf(__a0: unicode) -> ghidra.app.util.demangler.swift.SwiftDemangledNodeKind: ...

    @overload
    @staticmethod
    def valueOf(__a0: java.lang.Class, __a1: unicode) -> java.lang.Enum: ...

    @staticmethod
    def values() -> List[ghidra.app.util.demangler.swift.SwiftDemangledNodeKind]: ...

    @overload
    def wait(self) -> None: ...

    @overload
    def wait(self, __a0: long) -> None: ...

    @overload
    def wait(self, __a0: long, __a1: int) -> None: ...

