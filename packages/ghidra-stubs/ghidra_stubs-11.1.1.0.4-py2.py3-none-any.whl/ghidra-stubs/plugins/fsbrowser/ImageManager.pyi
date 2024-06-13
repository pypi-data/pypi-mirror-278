from typing import overload
import java.lang


class ImageManager(object):
    """
    Static helper to register and load Icons for the file system browser plugin and its
     child windows.
 
     Visible to just this package.
    """

    CLOSE: javax.swing.Icon
    COLLAPSE_ALL: javax.swing.Icon
    COMPRESS: javax.swing.Icon
    COPY: javax.swing.Icon
    CREATE_FIRMWARE: javax.swing.Icon
    CUT: javax.swing.Icon
    DELETE: javax.swing.Icon
    ECLIPSE: javax.swing.Icon
    EXPAND_ALL: javax.swing.Icon
    EXTRACT: javax.swing.Icon
    FONT: javax.swing.Icon
    IMPORT: javax.swing.Icon
    INFO: javax.swing.Icon
    JAR: javax.swing.Icon
    LIST_MOUNTED: javax.swing.Icon
    LOCKED: javax.swing.Icon
    NEW: javax.swing.Icon
    OPEN: javax.swing.Icon
    OPEN_ALL: javax.swing.Icon
    OPEN_AS_BINARY: javax.swing.Icon
    OPEN_FILE_SYSTEM: javax.swing.Icon
    OPEN_IN_LISTING: javax.swing.Icon
    PASTE: javax.swing.Icon
    PHOTO: javax.swing.Icon
    REDO: javax.swing.Icon
    REFRESH: javax.swing.Icon
    RENAME: javax.swing.Icon
    SAVE: javax.swing.Icon
    SAVE_AS: javax.swing.Icon
    UNDO: javax.swing.Icon
    UNLOCKED: javax.swing.Icon
    VIEW_AS_IMAGE: javax.swing.Icon
    VIEW_AS_TEXT: javax.swing.Icon
    iOS: javax.swing.Icon



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

