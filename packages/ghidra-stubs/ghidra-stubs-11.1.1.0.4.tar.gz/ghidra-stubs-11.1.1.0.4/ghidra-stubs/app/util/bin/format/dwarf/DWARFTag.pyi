from typing import List
from typing import overload
import ghidra.app.util.bin.format.dwarf
import ghidra.program.model.symbol
import java.lang
import java.util


class DWARFTag(java.lang.Enum):
    DW_TAG_APPLE_ptrauth_type: ghidra.app.util.bin.format.dwarf.DWARFTag
    DW_TAG_GNU_BINCL: ghidra.app.util.bin.format.dwarf.DWARFTag
    DW_TAG_GNU_EINCL: ghidra.app.util.bin.format.dwarf.DWARFTag
    DW_TAG_GNU_formal_parameter_pack: ghidra.app.util.bin.format.dwarf.DWARFTag
    DW_TAG_GNU_template_parameter_pack: ghidra.app.util.bin.format.dwarf.DWARFTag
    DW_TAG_GNU_template_template_param: ghidra.app.util.bin.format.dwarf.DWARFTag
    DW_TAG_HP_Bliss_field: ghidra.app.util.bin.format.dwarf.DWARFTag
    DW_TAG_HP_Bliss_field_set: ghidra.app.util.bin.format.dwarf.DWARFTag
    DW_TAG_HP_array_descriptor: ghidra.app.util.bin.format.dwarf.DWARFTag
    DW_TAG_MIPS_loop: ghidra.app.util.bin.format.dwarf.DWARFTag
    DW_TAG_UNKNOWN: ghidra.app.util.bin.format.dwarf.DWARFTag
    DW_TAG_access_declaration: ghidra.app.util.bin.format.dwarf.DWARFTag
    DW_TAG_array_type: ghidra.app.util.bin.format.dwarf.DWARFTag
    DW_TAG_atomic_type: ghidra.app.util.bin.format.dwarf.DWARFTag
    DW_TAG_base_type: ghidra.app.util.bin.format.dwarf.DWARFTag
    DW_TAG_call_site: ghidra.app.util.bin.format.dwarf.DWARFTag
    DW_TAG_call_site_parameter: ghidra.app.util.bin.format.dwarf.DWARFTag
    DW_TAG_catch_block: ghidra.app.util.bin.format.dwarf.DWARFTag
    DW_TAG_class_template: ghidra.app.util.bin.format.dwarf.DWARFTag
    DW_TAG_class_type: ghidra.app.util.bin.format.dwarf.DWARFTag
    DW_TAG_coarray_type: ghidra.app.util.bin.format.dwarf.DWARFTag
    DW_TAG_common_block: ghidra.app.util.bin.format.dwarf.DWARFTag
    DW_TAG_common_inclusion: ghidra.app.util.bin.format.dwarf.DWARFTag
    DW_TAG_compile_unit: ghidra.app.util.bin.format.dwarf.DWARFTag
    DW_TAG_condition: ghidra.app.util.bin.format.dwarf.DWARFTag
    DW_TAG_const_type: ghidra.app.util.bin.format.dwarf.DWARFTag
    DW_TAG_constant: ghidra.app.util.bin.format.dwarf.DWARFTag
    DW_TAG_dwarf_procedure: ghidra.app.util.bin.format.dwarf.DWARFTag
    DW_TAG_dynamic_type: ghidra.app.util.bin.format.dwarf.DWARFTag
    DW_TAG_entry_point: ghidra.app.util.bin.format.dwarf.DWARFTag
    DW_TAG_enumeration_type: ghidra.app.util.bin.format.dwarf.DWARFTag
    DW_TAG_enumerator: ghidra.app.util.bin.format.dwarf.DWARFTag
    DW_TAG_file_type: ghidra.app.util.bin.format.dwarf.DWARFTag
    DW_TAG_formal_parameter: ghidra.app.util.bin.format.dwarf.DWARFTag
    DW_TAG_format_label: ghidra.app.util.bin.format.dwarf.DWARFTag
    DW_TAG_friend: ghidra.app.util.bin.format.dwarf.DWARFTag
    DW_TAG_function_template: ghidra.app.util.bin.format.dwarf.DWARFTag
    DW_TAG_generic_subrange: ghidra.app.util.bin.format.dwarf.DWARFTag
    DW_TAG_gnu_call_site: ghidra.app.util.bin.format.dwarf.DWARFTag
    DW_TAG_gnu_call_site_parameter: ghidra.app.util.bin.format.dwarf.DWARFTag
    DW_TAG_hi_user: ghidra.app.util.bin.format.dwarf.DWARFTag
    DW_TAG_immutable_type: ghidra.app.util.bin.format.dwarf.DWARFTag
    DW_TAG_imported_declaration: ghidra.app.util.bin.format.dwarf.DWARFTag
    DW_TAG_imported_module: ghidra.app.util.bin.format.dwarf.DWARFTag
    DW_TAG_imported_unit: ghidra.app.util.bin.format.dwarf.DWARFTag
    DW_TAG_inheritance: ghidra.app.util.bin.format.dwarf.DWARFTag
    DW_TAG_inlined_subroutine: ghidra.app.util.bin.format.dwarf.DWARFTag
    DW_TAG_interface_type: ghidra.app.util.bin.format.dwarf.DWARFTag
    DW_TAG_label: ghidra.app.util.bin.format.dwarf.DWARFTag
    DW_TAG_lexical_block: ghidra.app.util.bin.format.dwarf.DWARFTag
    DW_TAG_lo_user: ghidra.app.util.bin.format.dwarf.DWARFTag
    DW_TAG_member: ghidra.app.util.bin.format.dwarf.DWARFTag
    DW_TAG_module: ghidra.app.util.bin.format.dwarf.DWARFTag
    DW_TAG_mutable_type: ghidra.app.util.bin.format.dwarf.DWARFTag
    DW_TAG_namelist: ghidra.app.util.bin.format.dwarf.DWARFTag
    DW_TAG_namelist_item: ghidra.app.util.bin.format.dwarf.DWARFTag
    DW_TAG_namespace: ghidra.app.util.bin.format.dwarf.DWARFTag
    DW_TAG_packed_type: ghidra.app.util.bin.format.dwarf.DWARFTag
    DW_TAG_partial_unit: ghidra.app.util.bin.format.dwarf.DWARFTag
    DW_TAG_pointer_type: ghidra.app.util.bin.format.dwarf.DWARFTag
    DW_TAG_ptr_to_member_type: ghidra.app.util.bin.format.dwarf.DWARFTag
    DW_TAG_reference_type: ghidra.app.util.bin.format.dwarf.DWARFTag
    DW_TAG_restrict_type: ghidra.app.util.bin.format.dwarf.DWARFTag
    DW_TAG_rvalue_reference_type: ghidra.app.util.bin.format.dwarf.DWARFTag
    DW_TAG_set_type: ghidra.app.util.bin.format.dwarf.DWARFTag
    DW_TAG_shared_type: ghidra.app.util.bin.format.dwarf.DWARFTag
    DW_TAG_skeleton_unit: ghidra.app.util.bin.format.dwarf.DWARFTag
    DW_TAG_string_type: ghidra.app.util.bin.format.dwarf.DWARFTag
    DW_TAG_structure_type: ghidra.app.util.bin.format.dwarf.DWARFTag
    DW_TAG_subprogram: ghidra.app.util.bin.format.dwarf.DWARFTag
    DW_TAG_subrange_type: ghidra.app.util.bin.format.dwarf.DWARFTag
    DW_TAG_subroutine_type: ghidra.app.util.bin.format.dwarf.DWARFTag
    DW_TAG_template_alias: ghidra.app.util.bin.format.dwarf.DWARFTag
    DW_TAG_template_type_param: ghidra.app.util.bin.format.dwarf.DWARFTag
    DW_TAG_template_value_param: ghidra.app.util.bin.format.dwarf.DWARFTag
    DW_TAG_thrown_type: ghidra.app.util.bin.format.dwarf.DWARFTag
    DW_TAG_try_block: ghidra.app.util.bin.format.dwarf.DWARFTag
    DW_TAG_type_unit: ghidra.app.util.bin.format.dwarf.DWARFTag
    DW_TAG_typedef: ghidra.app.util.bin.format.dwarf.DWARFTag
    DW_TAG_union_type: ghidra.app.util.bin.format.dwarf.DWARFTag
    DW_TAG_unspecified_parameters: ghidra.app.util.bin.format.dwarf.DWARFTag
    DW_TAG_unspecified_type: ghidra.app.util.bin.format.dwarf.DWARFTag
    DW_TAG_variable: ghidra.app.util.bin.format.dwarf.DWARFTag
    DW_TAG_variant: ghidra.app.util.bin.format.dwarf.DWARFTag
    DW_TAG_variant_part: ghidra.app.util.bin.format.dwarf.DWARFTag
    DW_TAG_volatile_type: ghidra.app.util.bin.format.dwarf.DWARFTag
    DW_TAG_with_stmt: ghidra.app.util.bin.format.dwarf.DWARFTag







    @overload
    def compareTo(self, __a0: java.lang.Enum) -> int: ...

    @overload
    def compareTo(self, __a0: object) -> int: ...

    def describeConstable(self) -> java.util.Optional: ...

    def equals(self, __a0: object) -> bool: ...

    def getClass(self) -> java.lang.Class: ...

    def getContainerTypeName(self) -> unicode: ...

    def getDeclaringClass(self) -> java.lang.Class: ...

    def getId(self) -> int: ...

    def getSymbolType(self) -> ghidra.program.model.symbol.SymbolType: ...

    def hashCode(self) -> int: ...

    def isFuncDefType(self) -> bool: ...

    def isNameSpaceContainer(self) -> bool: ...

    def isNamedType(self) -> bool: ...

    def isStructureType(self) -> bool: ...

    def isType(self) -> bool: ...

    @overload
    def name(self) -> unicode: ...

    @overload
    def name(self, __a0: int) -> unicode: ...

    def notify(self) -> None: ...

    def notifyAll(self) -> None: ...

    @staticmethod
    def of(__a0: int) -> ghidra.app.util.bin.format.dwarf.DWARFTag: ...

    def ordinal(self) -> int: ...

    def toString(self) -> unicode: ...

    @overload
    @staticmethod
    def valueOf(__a0: unicode) -> ghidra.app.util.bin.format.dwarf.DWARFTag: ...

    @overload
    @staticmethod
    def valueOf(__a0: java.lang.Class, __a1: unicode) -> java.lang.Enum: ...

    @staticmethod
    def values() -> List[ghidra.app.util.bin.format.dwarf.DWARFTag]: ...

    @overload
    def wait(self) -> None: ...

    @overload
    def wait(self, __a0: long) -> None: ...

    @overload
    def wait(self, __a0: long, __a1: int) -> None: ...

    @property
    def containerTypeName(self) -> unicode: ...

    @property
    def funcDefType(self) -> bool: ...

    @property
    def id(self) -> int: ...

    @property
    def nameSpaceContainer(self) -> bool: ...

    @property
    def namedType(self) -> bool: ...

    @property
    def structureType(self) -> bool: ...

    @property
    def symbolType(self) -> ghidra.program.model.symbol.SymbolType: ...

    @property
    def type(self) -> bool: ...