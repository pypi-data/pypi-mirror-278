from typing import overload
import java.lang


class PluginCategoryNames(object):
    """
    A listing of commonly used PluginDescription category names.
 
     Note - the Front End tool automatically include plugins that: 1) implement 
     ApplicationLevelPlugin, have the PluginStatus#RELEASED, and do not have the 
     #EXAMPLES category.  If you wish to create an ApplicationLevelPlugin that is not
     automatically included in the Front End, the easiest way to do that is to mark its status as
     PluginStatus#STABLE.
    """

    ANALYSIS: unicode = u'Analysis'
    CODE_VIEWER: unicode = u'Code Viewer'
    COMMON: unicode = u'Common'
    DEBUGGER: unicode = u'Debugger'
    DIAGNOSTIC: unicode = u'Diagnostic'
    EXAMPLES: unicode = u'Examples'
    FRAMEWORK: unicode = u'Framework'
    GRAPH: unicode = u'Graph'
    NAVIGATION: unicode = u'Navigation'
    PROGRAM_ORGANIZATION: unicode = u'Program Organization'
    SEARCH: unicode = u'Search'
    SELECTION: unicode = u'Selection'







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

