
import sys
if sys.version_info >= (3, 8):
    from typing import Protocol
else:
    from typing_extensions import Protocol

import java.io
import java.lang
import java.util
import jisa.addresses
import jisa.visa.drivers
import typing



class VISAException(java.io.IOException):
    def __init__(self, string: str, *object: typing.Any): ...

class ConnectionFailedException(VISAException):
    def __init__(self, address: jisa.addresses.Address, map: typing.Union[java.util.Map[jisa.visa.drivers.Driver, java.lang.Exception], typing.Mapping[jisa.visa.drivers.Driver, java.lang.Exception]]): ...
    def getAddress(self) -> jisa.addresses.Address: ...
    def getErrors(self) -> java.util.Map[jisa.visa.drivers.Driver, java.lang.Exception]: ...

class DeviceLockedException(VISAException):
    def __init__(self, address: jisa.addresses.Address, driver: jisa.visa.drivers.Driver): ...

class DriverSpecificException(VISAException):
    def __init__(self, driver: jisa.visa.drivers.Driver, string: str): ...
    def getDriver(self) -> jisa.visa.drivers.Driver: ...

class IncompatibleAddressException(VISAException):
    def __init__(self, address: jisa.addresses.Address, driver: jisa.visa.drivers.Driver): ...

class InvalidAddressException(VISAException):
    def __init__(self, address: jisa.addresses.Address, driver: jisa.visa.drivers.Driver): ...

class NoCompatibleDriversException(VISAException):
    def __init__(self, address: jisa.addresses.Address): ...

class NoDeviceException(VISAException):
    def __init__(self, address: jisa.addresses.Address, driver: jisa.visa.drivers.Driver): ...
    def getAddress(self) -> jisa.addresses.Address: ...
    def getDriver(self) -> jisa.visa.drivers.Driver: ...


class __module_protocol__(Protocol):
    # A module protocol which reflects the result of ``jp.JPackage("jisa.visa.exceptions")``.

    ConnectionFailedException: typing.Type[ConnectionFailedException]
    DeviceLockedException: typing.Type[DeviceLockedException]
    DriverSpecificException: typing.Type[DriverSpecificException]
    IncompatibleAddressException: typing.Type[IncompatibleAddressException]
    InvalidAddressException: typing.Type[InvalidAddressException]
    NoCompatibleDriversException: typing.Type[NoCompatibleDriversException]
    NoDeviceException: typing.Type[NoDeviceException]
    VISAException: typing.Type[VISAException]
