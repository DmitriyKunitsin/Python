from dataclasses import dataclass


@dataclass
class Dntk:
    data : bytes = b'\x00'
    _deviceId : hex = 51 