
import sys
if sys.version_info >= (3, 8):
    from typing import Protocol
else:
    from typing_extensions import Protocol

import java.lang
import jisa.maths.matrices
import jpype
import typing



class MatrixException(java.lang.RuntimeException):
    def __init__(self, string: str): ...

class DimensionException(MatrixException):
    @typing.overload
    def __init__(self, int: int, int2: int): ...
    @typing.overload
    def __init__(self, int: int, int2: int, int3: int, int4: int): ...
    @typing.overload
    def __init__(self, matrix: jisa.maths.matrices.Matrix, int: int, int2: int): ...
    @typing.overload
    def __init__(self, matrix: jisa.maths.matrices.Matrix, matrix2: jisa.maths.matrices.Matrix): ...

class IndexException(MatrixException):
    def __init__(self, int: int, int2: int, matrix: jisa.maths.matrices.Matrix): ...

class NonColException(MatrixException):
    def __init__(self): ...

class NonRowException(MatrixException):
    def __init__(self): ...

class NonSquareException(MatrixException):
    def __init__(self): ...

class SingularException(MatrixException):
    def __init__(self): ...

class SubMatrixException(MatrixException):
    @typing.overload
    def __init__(self, matrix: jisa.maths.matrices.Matrix, intArray: typing.Union[typing.List[int], jpype.JArray], intArray2: typing.Union[typing.List[int], jpype.JArray]): ...
    @typing.overload
    def __init__(self, matrix: jisa.maths.matrices.Matrix, matrix2: jisa.maths.matrices.Matrix, int: int, int2: int): ...


class __module_protocol__(Protocol):
    # A module protocol which reflects the result of ``jp.JPackage("jisa.maths.matrices.exceptions")``.

    DimensionException: typing.Type[DimensionException]
    IndexException: typing.Type[IndexException]
    MatrixException: typing.Type[MatrixException]
    NonColException: typing.Type[NonColException]
    NonRowException: typing.Type[NonRowException]
    NonSquareException: typing.Type[NonSquareException]
    SingularException: typing.Type[SingularException]
    SubMatrixException: typing.Type[SubMatrixException]
