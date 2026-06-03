from dataclasses import dataclass
from construct import Struct, Byte

@dataclass
class PacketHeader:
    """
    Заголовок бинарного пакета.

    Поля:
        format (bytes): Версия формата пакета (1 байт).
        deviceId (bytes): Идентификатор устройства (1 байт).
        token (bytes): Токен сессии или команды (1 байт).
        count (bytes): Счётчик пакетов (1 байт).
        payloadSize (bytes): Размер полезной нагрузки в байтах (1 байт).
    """
    format: bytes = b'\x00'
    deviceId: bytes = b'\x00'
    token: bytes = b'\x00'
    count: bytes = b'\x00'
    payloadSize: bytes = b'\x00'

    # Декларативное описание структуры (оцените читаемость!)
    _STRUCT = Struct(
        "format" / Byte,
        "deviceId" / Byte,
        "token" / Byte,
        "count" / Byte,
        "payloadSize" / Byte,
    )

    @classmethod
    def from_bytes(cls, data: bytes) -> 'PacketHeader':
        """Создаёт заголовок из байтовой посылки, используя construct."""
        # Парсинг возвращает Container (как словарь) с целыми числами
        parsed = cls._STRUCT.parse(data)
        # Преобразуем целые в однобайтовые строки, чтобы сохранить аннотации полей
        return cls(
            format=bytes([parsed.format]),
            deviceId=bytes([parsed.deviceId]),
            token=bytes([parsed.token]),
            count=bytes([parsed.count]),
            payloadSize=bytes([parsed.payloadSize]),
        )

    def to_bytes(self) -> bytes:
        """Упаковывает заголовок обратно в байты."""
        # build принимает словарь, поля должны быть целыми числами
        return self._STRUCT.build({
            "format": self.format[0],
            "deviceId": self.deviceId[0],
            "token": self.token[0],
            "count": self.count[0],
            "payloadSize": self.payloadSize[0],
        })