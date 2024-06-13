from typing import overload
import java.lang


class EmuUnixUser(object):
    """
    A simulated UNIX user
    """

    DEFAULT_USER: ghidra.pcode.emu.unix.EmuUnixUser
    gids: java.util.Collection
    uid: int



    def __init__(self, uid: int, gids: java.util.Collection):
        """
        Construct a new user
        @param uid the user's uid
        @param gids the user's gids
        """
        ...



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

