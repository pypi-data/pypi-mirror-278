from typing import List
from typing import overload
import java.lang


class ElfLoaderOptionsFactory(object):
    APPLY_UNDEFINED_SYMBOL_DATA_NAME: unicode = u'Apply Undefined Symbol Data'
    DISCARDABLE_SEGMENT_SIZE_OPTION_NAME: unicode = u'Max Zero-Segment Discard Size'
    IMAGE16_BASE_DEFAULT: long = 0x1000L
    IMAGE32_BASE_DEFAULT: long = 0x10000L
    IMAGE64_BASE_DEFAULT: long = 0x100000L
    IMAGE_BASE_OPTION_NAME: unicode = u'Image Base'
    IMAGE_DATA_IMAGE_BASE_OPTION_NAME: unicode = u'Data Image Base'
    INCLUDE_OTHER_BLOCKS: unicode = u'Import Non-Loaded Data'
    PERFORM_RELOCATIONS_NAME: unicode = u'Perform Symbol Relocations'







    @staticmethod
    def applyUndefinedSymbolData(__a0: List[object]) -> bool: ...

    def equals(self, __a0: object) -> bool: ...

    def getClass(self) -> java.lang.Class: ...

    @staticmethod
    def getDataImageBaseOption(__a0: List[object]) -> unicode: ...

    @staticmethod
    def getImageBaseOption(__a0: List[object]) -> unicode: ...

    @staticmethod
    def getMaxSegmentDiscardSize(__a0: List[object]) -> int: ...

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

