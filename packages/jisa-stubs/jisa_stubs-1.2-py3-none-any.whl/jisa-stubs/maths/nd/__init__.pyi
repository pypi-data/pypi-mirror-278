
import sys
if sys.version_info >= (3, 8):
    from typing import Protocol
else:
    from typing_extensions import Protocol

import typing



_ND__T = typing.TypeVar('_ND__T')  # <T>
class ND(typing.Generic[_ND__T]):
    def __init__(self): ...


class __module_protocol__(Protocol):
    # A module protocol which reflects the result of ``jp.JPackage("jisa.maths.nd")``.

    ND: typing.Type[ND]
