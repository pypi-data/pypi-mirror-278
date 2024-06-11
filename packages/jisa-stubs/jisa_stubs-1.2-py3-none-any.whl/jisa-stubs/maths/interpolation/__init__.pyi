
import sys
if sys.version_info >= (3, 8):
    from typing import Protocol
else:
    from typing_extensions import Protocol

import java.lang
import java.util
import jisa.maths.functions
import jisa.maths.matrices
import typing



class Interpolation:
    def __init__(self): ...
    @typing.overload
    @staticmethod
    def interpolate1D(iterable: typing.Union[java.lang.Iterable[float], typing.Sequence[float], typing.Set[float], typing.Callable[[], java.util.Iterator[typing.Any]]], iterable2: typing.Union[java.lang.Iterable[float], typing.Sequence[float], typing.Set[float], typing.Callable[[], java.util.Iterator[typing.Any]]]) -> jisa.maths.functions.Function: ...
    @typing.overload
    @staticmethod
    def interpolate1D(matrix: jisa.maths.matrices.Matrix[float]) -> jisa.maths.functions.Function: ...
    @typing.overload
    @staticmethod
    def interpolate2D(iterable: typing.Union[java.lang.Iterable[float], typing.Sequence[float], typing.Set[float], typing.Callable[[], java.util.Iterator[typing.Any]]], iterable2: typing.Union[java.lang.Iterable[float], typing.Sequence[float], typing.Set[float], typing.Callable[[], java.util.Iterator[typing.Any]]], iterable3: typing.Union[java.lang.Iterable[float], typing.Sequence[float], typing.Set[float], typing.Callable[[], java.util.Iterator[typing.Any]]]) -> jisa.maths.functions.XYFunction: ...
    @typing.overload
    @staticmethod
    def interpolate2D(matrix: jisa.maths.matrices.Matrix[float]) -> jisa.maths.functions.XYFunction: ...
    @typing.overload
    @staticmethod
    def interpolate3D(iterable: typing.Union[java.lang.Iterable[float], typing.Sequence[float], typing.Set[float], typing.Callable[[], java.util.Iterator[typing.Any]]], iterable2: typing.Union[java.lang.Iterable[float], typing.Sequence[float], typing.Set[float], typing.Callable[[], java.util.Iterator[typing.Any]]], iterable3: typing.Union[java.lang.Iterable[float], typing.Sequence[float], typing.Set[float], typing.Callable[[], java.util.Iterator[typing.Any]]], iterable4: typing.Union[java.lang.Iterable[float], typing.Sequence[float], typing.Set[float], typing.Callable[[], java.util.Iterator[typing.Any]]]) -> jisa.maths.functions.XYZFunction: ...
    @typing.overload
    @staticmethod
    def interpolate3D(matrix: jisa.maths.matrices.Matrix[float]) -> jisa.maths.functions.XYZFunction: ...
    @typing.overload
    @staticmethod
    def interpolateND(iterable: typing.Union[java.lang.Iterable[float], typing.Sequence[float], typing.Set[float], typing.Callable[[], java.util.Iterator[typing.Any]]], *iterable2: typing.Union[java.lang.Iterable[float], typing.Sequence[float], typing.Set[float], typing.Callable[[], java.util.Iterator[typing.Any]]]) -> jisa.maths.functions.MultiFunction: ...
    @typing.overload
    @staticmethod
    def interpolateND(matrix: jisa.maths.matrices.Matrix[float]) -> jisa.maths.functions.MultiFunction: ...
    @staticmethod
    def interpolateSmooth(iterable: typing.Union[java.lang.Iterable[float], typing.Sequence[float], typing.Set[float], typing.Callable[[], java.util.Iterator[typing.Any]]], iterable2: typing.Union[java.lang.Iterable[float], typing.Sequence[float], typing.Set[float], typing.Callable[[], java.util.Iterator[typing.Any]]]) -> jisa.maths.functions.Function: ...
    class MultiIterable(java.lang.Iterable[typing.MutableSequence[float]]):
        def __init__(self, *iterable: typing.Union[java.lang.Iterable[float], typing.Sequence[float], typing.Set[float], typing.Callable[[], java.util.Iterator[typing.Any]]]): ...
        def iterator(self) -> java.util.Iterator[typing.MutableSequence[float]]: ...


class __module_protocol__(Protocol):
    # A module protocol which reflects the result of ``jp.JPackage("jisa.maths.interpolation")``.

    Interpolation: typing.Type[Interpolation]
