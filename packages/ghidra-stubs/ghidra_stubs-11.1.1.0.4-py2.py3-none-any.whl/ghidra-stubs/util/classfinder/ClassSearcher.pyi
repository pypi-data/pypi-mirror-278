from typing import List
from typing import overload
import ghidra.util.classfinder
import ghidra.util.task
import java.lang
import java.util
import java.util.function
import javax.swing.event


class ClassSearcher(object):
    """
    This class is a collection of static methods used to discover classes that implement a
     particular interface or extend a particular base class.
 
     Warning: Using the search feature of this class will trigger other classes to be loaded.
     Thus, clients should not make calls to this class inside of static initializer blocks

     Note: if your application is not using a module structure for its release build, then
     your application must create the following file, with the required entries,
     in order to find extension points:
 
     	install dir/data/ExtensionPoint.manifest
 
    """

    SEARCH_ALL_JARS_PROPERTY: unicode = u'class.searcher.search.all.jars'







    @staticmethod
    def addChangeListener(l: javax.swing.event.ChangeListener) -> None:
        """
        Add a change listener that will be notified when the classpath
         is searched for new classes.
         <p><strong>Note:</strong> The listener list is implemented
         using WeakReferences. Therefore, the caller must maintain a handle to
         the listener being added, or else it will be garbage collected and
         never called.</p>
        @param l the listener to add
        """
        ...

    def equals(self, __a0: object) -> bool: ...

    def getClass(self) -> java.lang.Class: ...

    @overload
    @staticmethod
    def getClasses(ancestorClass: java.lang.Class) -> List[java.lang.Class]:
        """
        Get {@link ExtensionPointProperties#priority() priority-sorted} classes that implement or
         derive from the given ancestor class
        @param ancestorClass the ancestor class
        @return set of classes that implement or extend T
        """
        ...

    @overload
    @staticmethod
    def getClasses(ancestorClass: java.lang.Class, classFilter: java.util.function.Predicate) -> List[java.lang.Class]:
        """
        Get {@link ExtensionPointProperties#priority() priority-sorted} classes that
         implement or derive from the given ancestor class
        @param ancestorClass the ancestor class
        @param classFilter A Predicate that tests class objects (that are already of type T)
         			for further filtering, {@code null} is equivalent to "return true"
        @return {@link ExtensionPointProperties#priority() priority-sorted} list of
         			classes that implement or extend T and pass the filtering test performed by the
         			predicate
        """
        ...

    @staticmethod
    def getExtensionPointInfo() -> java.util.Set:
        """
        Gets class information about each discovered potential extension point.
         <p>
         NOTE: A discovered potential extension point may end up not getting loaded if it is not
         "of interest" (see {@link #isClassOfInterest(Class)}. These are referred to as false
         positives.
        @return A {@link Set} of class information about each discovered potential extension point
        """
        ...

    @staticmethod
    def getExtensionPointSuffix(className: unicode) -> unicode:
        """
        Gets the given class's extension point suffix.
         <p>
         Note that if multiple suffixes match, the smallest will be chosen. For a detailed
         explanation, see the comment inside {@link #loadExtensionPointSuffixes()}.
        @param className The name of the potential extension point class
        @return The given class's extension point suffix, or null if it is not an extension point or
           {@link #search(TaskMonitor)} has not been called yet
        """
        ...

    @staticmethod
    def getFalsePositives() -> java.util.Set:
        """
        Gets class information about discovered potential extension points that end up not getting
         loaded.
         <p>
         NOTE: Ghidra may load more classes as it runs. Therefore, repeated calls to this method may
         return more results, as more potential extension points are identified as false positives.
        @return A {@link Set} of class information about each loaded extension point
        """
        ...

    @overload
    @staticmethod
    def getInstances(c: java.lang.Class) -> List[object]:
        """
        Gets all {@link ExtensionPointProperties#priority() priority-sorted} class instances that 
         implement or derive from the given filter class
        @param c the filter class
        @return {@link ExtensionPointProperties#priority() priority-sorted} {@link List} of 
           class instances that implement or extend T
        """
        ...

    @overload
    @staticmethod
    def getInstances(c: java.lang.Class, filter: ghidra.util.classfinder.ClassFilter) -> List[object]:
        """
        Get {@link ExtensionPointProperties#priority() priority-sorted} classes instances that 
         implement or derive from the given filter class and pass the given filter predicate
        @param c the filter class
        @param filter A filter predicate that tests class objects (that are already of type T).
           {@code null} is equivalent to "return true".
        @return {@link ExtensionPointProperties#priority() priority-sorted} {@link List} of class 
           instances that implement or extend T and pass the filtering test performed by the predicate
        """
        ...

    @staticmethod
    def getLoaded() -> java.util.Set:
        """
        Gets class information about each loaded extension point.
         <p>
         NOTE: Ghidra may load more classes as it runs. Therefore, repeated calls to this method may
         return more results, as more extension points are loaded.
        @return A {@link Set} of class information about each loaded extension point
        """
        ...

    def hashCode(self) -> int: ...

    @staticmethod
    def isClassOfInterest(c: java.lang.Class) -> bool:
        """
        Checks to see if the given class is an extension point of interest.
        @param c The class to check.
        @return True if the given class is an extension point of interest; otherwise, false.
        """
        ...

    @staticmethod
    def logStatistics() -> None:
        """
        Writes the current class searcher statistics to the info log
        """
        ...

    def notify(self) -> None: ...

    def notifyAll(self) -> None: ...

    @staticmethod
    def removeChangeListener(l: javax.swing.event.ChangeListener) -> None:
        """
        Remove the change listener
        @param l the listener to remove
        """
        ...

    @staticmethod
    def search(monitor: ghidra.util.task.TaskMonitor) -> None:
        """
        Searches the classpath and updates the list of available classes which satisfies the 
         internal class filter. When the search completes (and was not cancelled), any registered 
         change listeners are notified.
        @param monitor the progress monitor for the search
        @throws CancelledException if the operation was cancelled
        """
        ...

    def toString(self) -> unicode: ...

    @overload
    def wait(self) -> None: ...

    @overload
    def wait(self, __a0: long) -> None: ...

    @overload
    def wait(self, __a0: long, __a1: int) -> None: ...

