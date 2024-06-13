from typing import List
from typing import overload
import ghidra.pcode.exec
import ghidra.pcode.struct
import ghidra.pcode.struct.StructuredSleigh
import java.io
import java.lang
import java.lang.reflect
import java.util


class StructuredSleigh(object):
    """
    The primary class for using the "structured sleigh" DSL
 
 
     This provides some conveniences for generating Sleigh source code, which is otherwise completely
     typeless and lacks basic control structure. In general, the types are not used so much for type
     checking as they are for easing access to fields of C structures, array indexing, etc.
     Furthermore, it becomes possible to re-use code when data types differ among platforms, so long
     as those variations are limited to field offsets and type sizes.
 
 
     Start by declaring an extension of StructuredSleigh. Then put any necessary "forward
     declarations" as fields of the class. Then declare methods annotated with
     StructuredUserop. Inside those methods, all the protected methods of this class are
     accessible, providing a DSL (as far as Java can provide :/ ) for writing Sleigh code. For
     example:
 
 
     class MyStructuredPart extends StructuredSleigh {
     	Var r0 = lang("r0", "/long");
 
     	protected MyStructuredPart() {
     		super(program);
     	}
 
     	StructuredUserop
     	public void my_userop() {
     		r0.set(0xdeadbeef);
     	}
     }
 
 
 
     This will simply generate the source "", but it also provides all the
     scaffolding to compile and invoke the userop as in a PcodeUseropLibrary. Internal methods
     -- which essentially behave like macros -- may be used, so only annotate methods to export as
     userops. For a more complete and practical example of using structured sleigh in a userop
     library, see AbstractEmuUnixSyscallUseropLibrary.
 
 
     Structured sleigh is also usable in a more standalone manner:
 
 
     StructuredSleigh ss = new StructuredSleigh(compilerSpec) {
     	StructuredUserop
     	public void my_userop() {
     		// Something interesting, I'm sure
     	}
     };
 
     SleighPcodeUseropDefinitionObject myUserop = ss.generate().get("my_userop");
     // To print source
     myUserop.getLines().forEach(System.out::print);
 
     // To compile for given parameters (none in this case) and print the p-code
     Register r0 = lang.getRegister("r0");
     System.out.println(myUserop.programFor(new Varnode(r0.getAddress(), r0.getNumBytes()), List.of(),
     	PcodeUseropLibrary.NIL));
 
 
 
     Known limitations:
 
     Recursion is not really possible. Currently, local variables of a userop do not actually get
     their own unique storage per invocation record. Furthermore, it's possible that local variable in
     different userop definition will be assigned the same storage location, meaning they could be
     unintentionally aliased if one invokes the other. Care should be taken when invoking one
     sleigh-based userop from another, or it should be avoided altogether until this limitation is
     addressed. It's generally safe to allow such invocations at the tail.
     Parameters are passed by reference. Essentially, the formal argument becomes an alias to its
     parameter. This is more a feature, but can be surprising if C semantics are expected.
     Calling one Structured Sleigh userop from another still requires a "external declaration" of
     the callee, despite being defined in the same "compilation unit."
 
    """






    class WrapIf(object):








        def _elif(self, __a0: ghidra.pcode.struct.Expr, __a1: java.lang.Runnable) -> ghidra.pcode.struct.StructuredSleigh.WrapIf: ...

        def _else(self, __a0: java.lang.Runnable) -> None: ...

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






    class StructuredSleighError(java.lang.RuntimeException):








        def addSuppressed(self, __a0: java.lang.Throwable) -> None: ...

        def equals(self, __a0: object) -> bool: ...

        def fillInStackTrace(self) -> java.lang.Throwable: ...

        def getCause(self) -> java.lang.Throwable: ...

        def getClass(self) -> java.lang.Class: ...

        def getLocalizedMessage(self) -> unicode: ...

        def getMessage(self) -> unicode: ...

        def getStackTrace(self) -> List[java.lang.StackTraceElement]: ...

        def getSuppressed(self) -> List[java.lang.Throwable]: ...

        def hashCode(self) -> int: ...

        def initCause(self, __a0: java.lang.Throwable) -> java.lang.Throwable: ...

        def notify(self) -> None: ...

        def notifyAll(self) -> None: ...

        @overload
        def printStackTrace(self) -> None: ...

        @overload
        def printStackTrace(self, __a0: java.io.PrintStream) -> None: ...

        @overload
        def printStackTrace(self, __a0: java.io.PrintWriter) -> None: ...

        def setStackTrace(self, __a0: List[java.lang.StackTraceElement]) -> None: ...

        def toString(self) -> unicode: ...

        @overload
        def wait(self) -> None: ...

        @overload
        def wait(self, __a0: long) -> None: ...

        @overload
        def wait(self, __a0: long, __a1: int) -> None: ...







    def e(self, rawExpr: unicode) -> ghidra.pcode.struct.Expr:
        """
        Generate a Sleigh expression
 
         <p>
         This is similar in concept to inline assembly, except it also has a value. It allows the
         embedding of Sleigh code into Structured Sleigh that is otherwise impossible or inconvenient
         to express. No effort is made to ensure the correctness of the given Sleigh expression nor
         its impact in context. The result is assigned a type of "void".
        @param rawExpr the Sleigh expression
        @return a handle to the value
        """
        ...

    def equals(self, __a0: object) -> bool: ...

    @overload
    def generate(self) -> java.util.Map:
        """
        Generate all the exported userops and return them in a map
 
         <p>
         This is typically only used when not part of a larger {@link PcodeUseropLibrary}, for example
         to aid in developing a Sleigh module or for generating injects.
        @param <T> the type of values used by the userop. For sleigh, this can be anything.
        @return the userop
        """
        ...

    @overload
    def generate(self, m: java.lang.reflect.Method) -> ghidra.pcode.exec.SleighPcodeUseropDefinition:
        """
        Generate the userop for a given Java method
        @param <T> the type of values used by the userop. For sleigh, this can be anything.
        @param m the method exported as a userop
        @return the userop
        """
        ...

    @overload
    def generate(self, into: java.util.Map) -> None:
        """
        Generate all the exported userops and place them into the given map
        @param <T> the type of values used by the userops. For sleigh, this can be anything.
        @param into the destination map, usually belonging to a {@link PcodeUseropLibrary}.
        """
        ...

    def getClass(self) -> java.lang.Class: ...

    def hashCode(self) -> int: ...

    def notify(self) -> None: ...

    def notifyAll(self) -> None: ...

    def s(self, rawStmt: unicode) -> ghidra.pcode.struct.StructuredSleigh.Stmt:
        """
        Generate Sleigh code
 
         <p>
         This is similar in concept to inline assembly. It allows the embedding of Sleigh code into
         Structured Sleigh that is otherwise impossible or inconvenient to state. No effort is made to
         ensure the correctness of the given Sleigh code nor its impact in context.
        @param rawStmt the Sleigh code
        @return a handle to the statement
        """
        ...

    def toString(self) -> unicode: ...

    @overload
    def wait(self) -> None: ...

    @overload
    def wait(self, __a0: long) -> None: ...

    @overload
    def wait(self, __a0: long, __a1: int) -> None: ...

