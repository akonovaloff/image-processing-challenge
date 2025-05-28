import re
from abc import ABC, abstractmethod
import serial

def parse_response(response_string):
    """
    Парсит строку ответа от прибора.
    Формат ответа: "ИМЯ_ЗНАЧЕНИЕЕДИНИЦА" (например, "A_10V").
    Возвращает словарь {'parameter': ИМЯ, 'value': ЗНАЧЕНИЕ, 'unit': ЕДИНИЦА}
    или None, если строка не соответствует формату.
    """
    match = re.match(r"([A-Z])_(\d+)([A-Z]+[a-z]*)", response_string)
    if match:
        parameter = match.group(1)
        value = match.group(2)
        unit = match.group(3)
        return {"parameter": parameter, "value": int(value), "unit": unit}
    return None


class CommunicationInterface(ABC):
    """
    Абстрактный базовый класс для интерфейсов связи с прибором.
    """

    @abstractmethod
    def connect(self) -> bool:
        """Устанавливает соединение с прибором."""
        pass

    @abstractmethod
    def disconnect(self) -> None:
        """Разрывает соединение с прибором."""
        pass

    @abstractmethod
    def send_request(self, request_string: str) -> bool:
        """Отправляет строку запроса прибору."""
        pass

    @abstractmethod
    def receive_response(self) -> str | None:
        """Получает строку ответа от прибора."""
        pass


class SerialCommunicator(CommunicationInterface):
    """
    Реализация интерфейса связи для Serial порта.
    """
    def __init__(self, port: str, baudrate: int = 9600, timeout: float = 1.0):
        self.port = port
        self.baudrate = baudrate
        self.timeout = timeout
        self.connection: serial.Serial | None = None

    def connect(self) -> bool:
        try:
            self.connection = serial.Serial(self.port, self.baudrate, timeout=self.timeout)
            return True
        except serial.SerialException:
            self.connection = None
            return False

    def disconnect(self) -> None:
        if self.connection and self.connection.is_open:
            self.connection.close()
        self.connection = None

    def send_request(self, request_string: str) -> bool:
        if self.connection and self.connection.is_open:
            try:
                # Предполагается, что команды должны завершаться CR+LF
                self.connection.write(request_string.encode('ascii') + b'\r\n')
                return True
            except serial.SerialException:
                return False
        return False

    def receive_response(self) -> str | None:
        if self.connection and self.connection.is_open:
            try:
                # readline() читает до '\n' (LF)
                response_bytes = self.connection.readline()
                return response_bytes.decode('ascii').strip()
            except serial.SerialTimeoutException:
                return None # Таймаут чтения
            except UnicodeDecodeError:
                return None # Ошибка декодирования
            except serial.SerialException:
                return None # Ошибка чтения
        return None