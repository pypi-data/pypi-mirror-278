from typing import List
from typing import overload
import ghidra.app.util.bin
import ghidra.app.util.bin.format.dwarf.attribs
import java.lang
import java.util
import java.util.function


class DWARFAttribute(java.lang.Enum):
    DW_AT_APPLE_omit_frame_ptr: ghidra.app.util.bin.format.dwarf.attribs.DWARFAttribute
    DW_AT_APPLE_optimized: ghidra.app.util.bin.format.dwarf.attribs.DWARFAttribute
    DW_AT_APPLE_ptrauth_address_discriminated: ghidra.app.util.bin.format.dwarf.attribs.DWARFAttribute
    DW_AT_APPLE_ptrauth_extra_discriminator: ghidra.app.util.bin.format.dwarf.attribs.DWARFAttribute
    DW_AT_APPLE_ptrauth_key: ghidra.app.util.bin.format.dwarf.attribs.DWARFAttribute
    DW_AT_GNU_addr_base: ghidra.app.util.bin.format.dwarf.attribs.DWARFAttribute
    DW_AT_GNU_dwo_id: ghidra.app.util.bin.format.dwarf.attribs.DWARFAttribute
    DW_AT_GNU_dwo_name: ghidra.app.util.bin.format.dwarf.attribs.DWARFAttribute
    DW_AT_GNU_pubnames: ghidra.app.util.bin.format.dwarf.attribs.DWARFAttribute
    DW_AT_GNU_pubtypes: ghidra.app.util.bin.format.dwarf.attribs.DWARFAttribute
    DW_AT_GNU_ranges_base: ghidra.app.util.bin.format.dwarf.attribs.DWARFAttribute
    DW_AT_MIPS_linkage_name: ghidra.app.util.bin.format.dwarf.attribs.DWARFAttribute
    DW_AT_abstract_origin: ghidra.app.util.bin.format.dwarf.attribs.DWARFAttribute
    DW_AT_accessibility: ghidra.app.util.bin.format.dwarf.attribs.DWARFAttribute
    DW_AT_addr_base: ghidra.app.util.bin.format.dwarf.attribs.DWARFAttribute
    DW_AT_address_class: ghidra.app.util.bin.format.dwarf.attribs.DWARFAttribute
    DW_AT_alignment: ghidra.app.util.bin.format.dwarf.attribs.DWARFAttribute
    DW_AT_allocated: ghidra.app.util.bin.format.dwarf.attribs.DWARFAttribute
    DW_AT_artificial: ghidra.app.util.bin.format.dwarf.attribs.DWARFAttribute
    DW_AT_associated: ghidra.app.util.bin.format.dwarf.attribs.DWARFAttribute
    DW_AT_base_types: ghidra.app.util.bin.format.dwarf.attribs.DWARFAttribute
    DW_AT_binary_scale: ghidra.app.util.bin.format.dwarf.attribs.DWARFAttribute
    DW_AT_bit_offset: ghidra.app.util.bin.format.dwarf.attribs.DWARFAttribute
    DW_AT_bit_size: ghidra.app.util.bin.format.dwarf.attribs.DWARFAttribute
    DW_AT_bit_stride: ghidra.app.util.bin.format.dwarf.attribs.DWARFAttribute
    DW_AT_byte_size: ghidra.app.util.bin.format.dwarf.attribs.DWARFAttribute
    DW_AT_byte_stride: ghidra.app.util.bin.format.dwarf.attribs.DWARFAttribute
    DW_AT_call_all_calls: ghidra.app.util.bin.format.dwarf.attribs.DWARFAttribute
    DW_AT_call_all_source_calls: ghidra.app.util.bin.format.dwarf.attribs.DWARFAttribute
    DW_AT_call_all_tail_calls: ghidra.app.util.bin.format.dwarf.attribs.DWARFAttribute
    DW_AT_call_column: ghidra.app.util.bin.format.dwarf.attribs.DWARFAttribute
    DW_AT_call_data_location: ghidra.app.util.bin.format.dwarf.attribs.DWARFAttribute
    DW_AT_call_data_value: ghidra.app.util.bin.format.dwarf.attribs.DWARFAttribute
    DW_AT_call_file: ghidra.app.util.bin.format.dwarf.attribs.DWARFAttribute
    DW_AT_call_line: ghidra.app.util.bin.format.dwarf.attribs.DWARFAttribute
    DW_AT_call_origin: ghidra.app.util.bin.format.dwarf.attribs.DWARFAttribute
    DW_AT_call_parameter: ghidra.app.util.bin.format.dwarf.attribs.DWARFAttribute
    DW_AT_call_pc: ghidra.app.util.bin.format.dwarf.attribs.DWARFAttribute
    DW_AT_call_return_pc: ghidra.app.util.bin.format.dwarf.attribs.DWARFAttribute
    DW_AT_call_tail_call: ghidra.app.util.bin.format.dwarf.attribs.DWARFAttribute
    DW_AT_call_target: ghidra.app.util.bin.format.dwarf.attribs.DWARFAttribute
    DW_AT_call_target_clobbered: ghidra.app.util.bin.format.dwarf.attribs.DWARFAttribute
    DW_AT_call_value: ghidra.app.util.bin.format.dwarf.attribs.DWARFAttribute
    DW_AT_calling_convention: ghidra.app.util.bin.format.dwarf.attribs.DWARFAttribute
    DW_AT_common_reference: ghidra.app.util.bin.format.dwarf.attribs.DWARFAttribute
    DW_AT_comp_dir: ghidra.app.util.bin.format.dwarf.attribs.DWARFAttribute
    DW_AT_const_expr: ghidra.app.util.bin.format.dwarf.attribs.DWARFAttribute
    DW_AT_const_value: ghidra.app.util.bin.format.dwarf.attribs.DWARFAttribute
    DW_AT_containing_type: ghidra.app.util.bin.format.dwarf.attribs.DWARFAttribute
    DW_AT_count: ghidra.app.util.bin.format.dwarf.attribs.DWARFAttribute
    DW_AT_data_bit_offset: ghidra.app.util.bin.format.dwarf.attribs.DWARFAttribute
    DW_AT_data_location: ghidra.app.util.bin.format.dwarf.attribs.DWARFAttribute
    DW_AT_data_member_location: ghidra.app.util.bin.format.dwarf.attribs.DWARFAttribute
    DW_AT_decimal_scale: ghidra.app.util.bin.format.dwarf.attribs.DWARFAttribute
    DW_AT_decimal_sign: ghidra.app.util.bin.format.dwarf.attribs.DWARFAttribute
    DW_AT_decl_column: ghidra.app.util.bin.format.dwarf.attribs.DWARFAttribute
    DW_AT_decl_file: ghidra.app.util.bin.format.dwarf.attribs.DWARFAttribute
    DW_AT_decl_line: ghidra.app.util.bin.format.dwarf.attribs.DWARFAttribute
    DW_AT_declaration: ghidra.app.util.bin.format.dwarf.attribs.DWARFAttribute
    DW_AT_default_value: ghidra.app.util.bin.format.dwarf.attribs.DWARFAttribute
    DW_AT_defaulted: ghidra.app.util.bin.format.dwarf.attribs.DWARFAttribute
    DW_AT_deleted: ghidra.app.util.bin.format.dwarf.attribs.DWARFAttribute
    DW_AT_description: ghidra.app.util.bin.format.dwarf.attribs.DWARFAttribute
    DW_AT_digit_count: ghidra.app.util.bin.format.dwarf.attribs.DWARFAttribute
    DW_AT_discr: ghidra.app.util.bin.format.dwarf.attribs.DWARFAttribute
    DW_AT_discr_list: ghidra.app.util.bin.format.dwarf.attribs.DWARFAttribute
    DW_AT_discr_value: ghidra.app.util.bin.format.dwarf.attribs.DWARFAttribute
    DW_AT_dwo_name: ghidra.app.util.bin.format.dwarf.attribs.DWARFAttribute
    DW_AT_elemental: ghidra.app.util.bin.format.dwarf.attribs.DWARFAttribute
    DW_AT_encoding: ghidra.app.util.bin.format.dwarf.attribs.DWARFAttribute
    DW_AT_endianity: ghidra.app.util.bin.format.dwarf.attribs.DWARFAttribute
    DW_AT_entry_pc: ghidra.app.util.bin.format.dwarf.attribs.DWARFAttribute
    DW_AT_enum_class: ghidra.app.util.bin.format.dwarf.attribs.DWARFAttribute
    DW_AT_explicit: ghidra.app.util.bin.format.dwarf.attribs.DWARFAttribute
    DW_AT_export_symbols: ghidra.app.util.bin.format.dwarf.attribs.DWARFAttribute
    DW_AT_extension: ghidra.app.util.bin.format.dwarf.attribs.DWARFAttribute
    DW_AT_external: ghidra.app.util.bin.format.dwarf.attribs.DWARFAttribute
    DW_AT_frame_base: ghidra.app.util.bin.format.dwarf.attribs.DWARFAttribute
    DW_AT_friend: ghidra.app.util.bin.format.dwarf.attribs.DWARFAttribute
    DW_AT_go_dict_index: ghidra.app.util.bin.format.dwarf.attribs.DWARFAttribute
    DW_AT_go_elem: ghidra.app.util.bin.format.dwarf.attribs.DWARFAttribute
    DW_AT_go_embedded_field: ghidra.app.util.bin.format.dwarf.attribs.DWARFAttribute
    DW_AT_go_key: ghidra.app.util.bin.format.dwarf.attribs.DWARFAttribute
    DW_AT_go_kind: ghidra.app.util.bin.format.dwarf.attribs.DWARFAttribute
    DW_AT_go_package_name: ghidra.app.util.bin.format.dwarf.attribs.DWARFAttribute
    DW_AT_go_runtime_type: ghidra.app.util.bin.format.dwarf.attribs.DWARFAttribute
    DW_AT_hi_user: ghidra.app.util.bin.format.dwarf.attribs.DWARFAttribute
    DW_AT_high_pc: ghidra.app.util.bin.format.dwarf.attribs.DWARFAttribute
    DW_AT_identifier_case: ghidra.app.util.bin.format.dwarf.attribs.DWARFAttribute
    DW_AT_import: ghidra.app.util.bin.format.dwarf.attribs.DWARFAttribute
    DW_AT_inline: ghidra.app.util.bin.format.dwarf.attribs.DWARFAttribute
    DW_AT_is_optional: ghidra.app.util.bin.format.dwarf.attribs.DWARFAttribute
    DW_AT_language: ghidra.app.util.bin.format.dwarf.attribs.DWARFAttribute
    DW_AT_linkage_name: ghidra.app.util.bin.format.dwarf.attribs.DWARFAttribute
    DW_AT_lo_user: ghidra.app.util.bin.format.dwarf.attribs.DWARFAttribute
    DW_AT_location: ghidra.app.util.bin.format.dwarf.attribs.DWARFAttribute
    DW_AT_loclists_base: ghidra.app.util.bin.format.dwarf.attribs.DWARFAttribute
    DW_AT_low_pc: ghidra.app.util.bin.format.dwarf.attribs.DWARFAttribute
    DW_AT_lower_bound: ghidra.app.util.bin.format.dwarf.attribs.DWARFAttribute
    DW_AT_macro_info: ghidra.app.util.bin.format.dwarf.attribs.DWARFAttribute
    DW_AT_macros: ghidra.app.util.bin.format.dwarf.attribs.DWARFAttribute
    DW_AT_main_subprogram: ghidra.app.util.bin.format.dwarf.attribs.DWARFAttribute
    DW_AT_mutable: ghidra.app.util.bin.format.dwarf.attribs.DWARFAttribute
    DW_AT_name: ghidra.app.util.bin.format.dwarf.attribs.DWARFAttribute
    DW_AT_namelist_item: ghidra.app.util.bin.format.dwarf.attribs.DWARFAttribute
    DW_AT_noreturn: ghidra.app.util.bin.format.dwarf.attribs.DWARFAttribute
    DW_AT_object_pointer: ghidra.app.util.bin.format.dwarf.attribs.DWARFAttribute
    DW_AT_ordering: ghidra.app.util.bin.format.dwarf.attribs.DWARFAttribute
    DW_AT_picture_string: ghidra.app.util.bin.format.dwarf.attribs.DWARFAttribute
    DW_AT_priority: ghidra.app.util.bin.format.dwarf.attribs.DWARFAttribute
    DW_AT_producer: ghidra.app.util.bin.format.dwarf.attribs.DWARFAttribute
    DW_AT_prototyped: ghidra.app.util.bin.format.dwarf.attribs.DWARFAttribute
    DW_AT_pure: ghidra.app.util.bin.format.dwarf.attribs.DWARFAttribute
    DW_AT_ranges: ghidra.app.util.bin.format.dwarf.attribs.DWARFAttribute
    DW_AT_rank: ghidra.app.util.bin.format.dwarf.attribs.DWARFAttribute
    DW_AT_recursive: ghidra.app.util.bin.format.dwarf.attribs.DWARFAttribute
    DW_AT_reference: ghidra.app.util.bin.format.dwarf.attribs.DWARFAttribute
    DW_AT_return_addr: ghidra.app.util.bin.format.dwarf.attribs.DWARFAttribute
    DW_AT_rnglists_base: ghidra.app.util.bin.format.dwarf.attribs.DWARFAttribute
    DW_AT_rvalue_reference: ghidra.app.util.bin.format.dwarf.attribs.DWARFAttribute
    DW_AT_segment: ghidra.app.util.bin.format.dwarf.attribs.DWARFAttribute
    DW_AT_sibling: ghidra.app.util.bin.format.dwarf.attribs.DWARFAttribute
    DW_AT_signature: ghidra.app.util.bin.format.dwarf.attribs.DWARFAttribute
    DW_AT_small: ghidra.app.util.bin.format.dwarf.attribs.DWARFAttribute
    DW_AT_specification: ghidra.app.util.bin.format.dwarf.attribs.DWARFAttribute
    DW_AT_start_scope: ghidra.app.util.bin.format.dwarf.attribs.DWARFAttribute
    DW_AT_static_link: ghidra.app.util.bin.format.dwarf.attribs.DWARFAttribute
    DW_AT_stmt_list: ghidra.app.util.bin.format.dwarf.attribs.DWARFAttribute
    DW_AT_str_offsets_base: ghidra.app.util.bin.format.dwarf.attribs.DWARFAttribute
    DW_AT_string_length: ghidra.app.util.bin.format.dwarf.attribs.DWARFAttribute
    DW_AT_string_length_bit_size: ghidra.app.util.bin.format.dwarf.attribs.DWARFAttribute
    DW_AT_string_length_byte_size: ghidra.app.util.bin.format.dwarf.attribs.DWARFAttribute
    DW_AT_threads_scaled: ghidra.app.util.bin.format.dwarf.attribs.DWARFAttribute
    DW_AT_trampoline: ghidra.app.util.bin.format.dwarf.attribs.DWARFAttribute
    DW_AT_type: ghidra.app.util.bin.format.dwarf.attribs.DWARFAttribute
    DW_AT_upper_bound: ghidra.app.util.bin.format.dwarf.attribs.DWARFAttribute
    DW_AT_use_UTF8: ghidra.app.util.bin.format.dwarf.attribs.DWARFAttribute
    DW_AT_use_location: ghidra.app.util.bin.format.dwarf.attribs.DWARFAttribute
    DW_AT_variable_parameter: ghidra.app.util.bin.format.dwarf.attribs.DWARFAttribute
    DW_AT_virtuality: ghidra.app.util.bin.format.dwarf.attribs.DWARFAttribute
    DW_AT_visibility: ghidra.app.util.bin.format.dwarf.attribs.DWARFAttribute
    DW_AT_vtable_elem_location: ghidra.app.util.bin.format.dwarf.attribs.DWARFAttribute
    EOL: int = 0




    class AttrDef(ghidra.app.util.bin.format.dwarf.attribs.DWARFAttributeDef):




        def __init__(self, __a0: ghidra.app.util.bin.format.dwarf.attribs.DWARFAttribute, __a1: int, __a2: ghidra.app.util.bin.format.dwarf.attribs.DWARFForm, __a3: long): ...



        def equals(self, __a0: object) -> bool: ...

        def getAttributeForm(self) -> ghidra.app.util.bin.format.dwarf.attribs.DWARFForm: ...

        def getAttributeId(self) -> java.lang.Enum: ...

        def getAttributeName(self) -> unicode: ...

        def getClass(self) -> java.lang.Class: ...

        def getImplicitValue(self) -> long: ...

        def getRawAttributeId(self) -> int: ...

        def hashCode(self) -> int: ...

        def isImplicit(self) -> bool: ...

        def notify(self) -> None: ...

        def notifyAll(self) -> None: ...

        @overload
        @staticmethod
        def read(__a0: ghidra.app.util.bin.BinaryReader) -> ghidra.app.util.bin.format.dwarf.attribs.DWARFAttribute.AttrDef: ...

        @overload
        @staticmethod
        def read(__a0: ghidra.app.util.bin.BinaryReader, __a1: java.util.function.Function) -> ghidra.app.util.bin.format.dwarf.attribs.DWARFAttributeDef: ...

        def toString(self) -> unicode: ...

        @overload
        def wait(self) -> None: ...

        @overload
        def wait(self, __a0: long) -> None: ...

        @overload
        def wait(self, __a0: long, __a1: int) -> None: ...

        def withForm(self, __a0: ghidra.app.util.bin.format.dwarf.attribs.DWARFForm) -> ghidra.app.util.bin.format.dwarf.attribs.DWARFAttribute.AttrDef: ...







    @overload
    def compareTo(self, __a0: java.lang.Enum) -> int: ...

    @overload
    def compareTo(self, __a0: object) -> int: ...

    def describeConstable(self) -> java.util.Optional: ...

    def equals(self, __a0: object) -> bool: ...

    def getAttributeClass(self) -> java.util.Set: ...

    def getClass(self) -> java.lang.Class: ...

    def getDeclaringClass(self) -> java.lang.Class: ...

    def getId(self) -> int: ...

    def hashCode(self) -> int: ...

    def name(self) -> unicode: ...

    def notify(self) -> None: ...

    def notifyAll(self) -> None: ...

    @staticmethod
    def of(__a0: int) -> ghidra.app.util.bin.format.dwarf.attribs.DWARFAttribute: ...

    def ordinal(self) -> int: ...

    def toString(self) -> unicode: ...

    @overload
    @staticmethod
    def valueOf(__a0: unicode) -> ghidra.app.util.bin.format.dwarf.attribs.DWARFAttribute: ...

    @overload
    @staticmethod
    def valueOf(__a0: java.lang.Class, __a1: unicode) -> java.lang.Enum: ...

    @staticmethod
    def values() -> List[ghidra.app.util.bin.format.dwarf.attribs.DWARFAttribute]: ...

    @overload
    def wait(self) -> None: ...

    @overload
    def wait(self, __a0: long) -> None: ...

    @overload
    def wait(self, __a0: long, __a1: int) -> None: ...

    @property
    def attributeClass(self) -> java.util.Set: ...

    @property
    def id(self) -> int: ...