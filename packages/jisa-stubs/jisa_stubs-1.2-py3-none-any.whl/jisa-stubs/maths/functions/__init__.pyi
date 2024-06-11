
import sys
if sys.version_info >= (3, 8):
    from typing import Protocol
else:
    from typing_extensions import Protocol

import jisa
import jisa.maths.matrices
import jpype
import org.apache.commons.math.analysis
import org.apache.commons.math.complex
import typing



class ComplexFunction:
    def value(self, complex: org.apache.commons.math.complex.Complex) -> org.apache.commons.math.complex.Complex: ...

_GFunction__U = typing.TypeVar('_GFunction__U')  # <U>
_GFunction__V = typing.TypeVar('_GFunction__V')  # <V>
class GFunction(typing.Generic[_GFunction__U, _GFunction__V]):
    def value(self, v: _GFunction__V) -> _GFunction__U: ...

class MultiFunction(org.apache.commons.math.analysis.MultivariateRealFunction):
    def value(self, *double: float) -> float: ...

class PFunction:
    def calculate(self, double: float, *double2: float) -> float: ...

class XYFunction(MultiFunction):
    @typing.overload
    def value(self, double: float, double2: float) -> float: ...
    @typing.overload
    def value(self, doubleArray: typing.Union[typing.List[float], jpype.JArray]) -> float: ...

class XYZFunction(MultiFunction):
    @typing.overload
    def value(self, double: float, double2: float, double3: float) -> float: ...
    @typing.overload
    def value(self, doubleArray: typing.Union[typing.List[float], jpype.JArray]) -> float: ...

class Function(org.apache.commons.math.analysis.DifferentiableUnivariateRealFunction):
    def add(self, function: typing.Union['Function', typing.Callable]) -> 'Function': ...
    def derivative(self) -> 'Function': ...
    def divide(self, function: typing.Union['Function', typing.Callable]) -> 'Function': ...
    def getNormalisedChiSquared(self, matrix: jisa.maths.matrices.Matrix, matrix2: jisa.maths.matrices.Matrix) -> float: ...
    def multiply(self, function: typing.Union['Function', typing.Callable]) -> 'Function': ...
    def subtract(self, function: typing.Union['Function', typing.Callable]) -> 'Function': ...
    @typing.overload
    def value(self, double: float) -> float: ...
    @typing.overload
    def value(self, matrix: jisa.maths.matrices.Matrix[float]) -> jisa.maths.matrices.Matrix[float]: ...
    class WrappedFunction(jisa.maths.functions.Function):
        def __init__(self, differentiableUnivariateRealFunction: org.apache.commons.math.analysis.DifferentiableUnivariateRealFunction): ...
        def derivative(self) -> 'Function': ...
        @typing.overload
        def value(self, matrix: jisa.maths.matrices.Matrix[float]) -> jisa.maths.matrices.Matrix[float]: ...
        @typing.overload
        def value(self, double: float) -> float: ...


class __module_protocol__(Protocol):
    # A module protocol which reflects the result of ``jp.JPackage("jisa.maths.functions")``.

    ComplexFunction: typing.Type[ComplexFunction]
    Function: typing.Type[Function]
    GFunction: typing.Type[GFunction]
    MultiFunction: typing.Type[MultiFunction]
    PFunction: typing.Type[PFunction]
    XYFunction: typing.Type[XYFunction]
    XYZFunction: typing.Type[XYZFunction]
