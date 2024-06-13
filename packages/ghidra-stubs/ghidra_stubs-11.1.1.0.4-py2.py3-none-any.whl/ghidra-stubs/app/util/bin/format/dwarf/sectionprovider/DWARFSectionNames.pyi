from typing import overload
import java.lang


class DWARFSectionNames(object):
    DEBUG_ABBREV: unicode = u'debug_abbrev'
    DEBUG_ADDR: unicode = u'debug_addr'
    DEBUG_ARRANGES: unicode = u'debug_arranges'
    DEBUG_FRAME: unicode = u'debug_frame'
    DEBUG_INFO: unicode = u'debug_info'
    DEBUG_LINE: unicode = u'debug_line'
    DEBUG_LINE_STR: unicode = u'debug_line_str'
    DEBUG_LOC: unicode = u'debug_loc'
    DEBUG_LOCLISTS: unicode = u'debug_loclists'
    DEBUG_MACINFO: unicode = u'debug_macinfo'
    DEBUG_PUBNAMES: unicode = u'debug_pubnames'
    DEBUG_PUBTYPES: unicode = u'debug_pubtypes'
    DEBUG_RANGES: unicode = u'debug_ranges'
    DEBUG_RNGLISTS: unicode = u'debug_rnglists'
    DEBUG_STR: unicode = u'debug_str'
    DEBUG_STROFFSETS: unicode = u'debug_str_offsets'
    DEBUG_TYPES: unicode = u'debug_types'
    MINIMAL_DWARF_SECTIONS: List[unicode]



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

