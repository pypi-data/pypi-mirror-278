from typing import overload
import java.lang


class SquashConstants(object):
    ALWAYS_FRAGMENT: int = 32
    COMPRESSION_OPTIONS_EXIST: int = 1024
    COMPRESSION_TYPE_GZIP: int = 1
    COMPRESSION_TYPE_LZ4: int = 5
    COMPRESSION_TYPE_LZMA: int = 2
    COMPRESSION_TYPE_LZO: int = 3
    COMPRESSION_TYPE_XZ: int = 4
    COMPRESSION_TYPE_ZSTD: int = 6
    DATABLOCK_COMPRESSED_MASK: int = 16777216
    EXPORT_TABLE_EXISTS: int = 128
    FRAGMENT_COMPRESSED_MASK: int = 16777216
    FRAGMENT_ENTRY_LENGTH: int = 16
    INODE_NO_FRAGMENTS: int = -1
    INODE_TYPE_BASIC_BLOCK_DEVICE: int = 4
    INODE_TYPE_BASIC_CHAR_DEVICE: int = 5
    INODE_TYPE_BASIC_DIRECTORY: int = 1
    INODE_TYPE_BASIC_FIFO: int = 6
    INODE_TYPE_BASIC_FILE: int = 2
    INODE_TYPE_BASIC_SOCKET: int = 7
    INODE_TYPE_BASIC_SYMLINK: int = 3
    INODE_TYPE_EXTENDED_BLOCK_DEVICE: int = 11
    INODE_TYPE_EXTENDED_CHAR_DEVICE: int = 12
    INODE_TYPE_EXTENDED_DIRECTORY: int = 8
    INODE_TYPE_EXTENDED_FIFO: int = 13
    INODE_TYPE_EXTENDED_FILE: int = 9
    INODE_TYPE_EXTENDED_SOCKET: int = 14
    INODE_TYPE_EXTENDED_SYMLINK: int = 10
    MAGIC: List[int]
    MAX_SYMLINK_DEPTH: int = 100
    MAX_UNIT_BLOCK_SIZE: int = 8192
    METABLOCK_UNCOMPRESSED_MASK: int = 32768
    NO_DUPLICATE_DATE: int = 64
    NO_FRAGMENTS: int = 16
    NO_XATTRS: int = 512
    SECTION_OMITTED: int = -1
    UNCOMPRESSED_DATA_BLOCKS: int = 2
    UNCOMPRESSED_FRAGMENTS: int = 8
    UNCOMPRESSED_IDS: int = 2048
    UNCOMPRESSED_INODES: int = 1
    UNCOMPRESSED_XATTRS: int = 256
    UNUSED_FLAG: int = 4



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

