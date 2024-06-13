from typing import overload
import ghidra.pty
import ghidra.pty.unix
import ghidra.pty.unix.PosixC
import java.lang


class UnixPty(object, ghidra.pty.Pty):








    def close(self) -> None: ...

    def equals(self, __a0: object) -> bool: ...

    def getChild(self) -> ghidra.pty.unix.UnixPtyChild: ...

    def getClass(self) -> java.lang.Class: ...

    def getParent(self) -> ghidra.pty.unix.UnixPtyParent: ...

    def hashCode(self) -> int: ...

    def notify(self) -> None: ...

    def notifyAll(self) -> None: ...

    @staticmethod
    def openpty(ioctls: ghidra.pty.unix.PosixC.Ioctls) -> ghidra.pty.unix.UnixPty: ...

    def toString(self) -> unicode: ...

    @overload
    def wait(self) -> None: ...

    @overload
    def wait(self, __a0: long) -> None: ...

    @overload
    def wait(self, __a0: long, __a1: int) -> None: ...

    @property
    def child(self) -> ghidra.pty.unix.UnixPtyChild: ...

    @property
    def parent(self) -> ghidra.pty.unix.UnixPtyParent: ...