import pytest

from src.interface_ascii_parser.interface_ascii_parser import parse_response, SerialCommunicator
from src.interface_ascii_parser import interface_ascii_parser as dut_module
import serial
from unittest.mock import MagicMock


class TestInterfaceAsciiParser:
    @pytest.mark.parametrize("raw_resp, expected_resp", [
        ("A_10V", {'parameter': 'A', 'value': 10, 'unit': 'V'}),
        ("B_5V", {'parameter': 'B', 'value': 5, 'unit': 'V'}),
        ("C_15A", {'parameter': 'C', 'value': 15, 'unit': 'A'}),
        ("D_255Hz", {'parameter': 'D', 'value': 255, 'unit': 'Hz'}),
        ("INVALID_STRING", None)
    ])
    def test_parse_response(self, raw_resp, expected_resp):
        actual_resp = parse_response(raw_resp)
        assert actual_resp == expected_resp, f"Actual: {actual_resp}, Expected: {expected_resp}"


class TestSerialCommunicator:
    # Фикстура для создания экземпляра SerialCommunicator
    @pytest.fixture
    def serial_comm(self):
        # Используем фиктивные значения для порта и скорости
        return SerialCommunicator(port='COM_VIRTUAL', baudrate=9600, timeout=1.0)

    @pytest.fixture
    def mock_serial_port(self, mocker):
        """
        Фикстура для мокирования serial.Serial.
        Возвращает кортеж: (mock_constructor, mock_instance)
        """
        # Сохраняем ссылку на оригинальный класс serial.Serial ПЕРЕД его мокированием.
        # Это важно, так как mocker.patch.object(dut_module.serial, 'Serial')
        # может изменить то, на что ссылается `serial.Serial` в этом файле,
        # если `dut_module.serial` и `serial` (импортированный здесь)
        # являются одним и тем же объектом модуля.
        original_serial_class = serial.Serial

        # Мокируем конструктор класса serial.Serial в dut_module
        mock_constructor = mocker.patch.object(dut_module.serial, 'Serial')

        # Используем original_serial_class для spec, чтобы mock_instance
        # имел правильный интерфейс, основанный на реальном классе.
        mock_instance = MagicMock(spec=original_serial_class)

        # Настраиваем мокированный конструктор так, чтобы при вызове он возвращал наш мок-экземпляр
        mock_constructor.return_value = mock_instance
        yield mock_constructor, mock_instance

    # Тест успешного подключения
    def test_connect_success(self, serial_comm, mock_serial_port):
        # Получаем моки из фикстуры
        mock_constructor, mock_connection = mock_serial_port

        # Вызываем метод connect
        connected = serial_comm.connect()

        # Проверяем, что метод connect вернул True
        assert connected is True
        # Проверяем, что класс serial.Serial был вызван с правильными параметрами
        mock_constructor.assert_called_once_with(serial_comm.port, serial_comm.baudrate,
                                                              timeout=serial_comm.timeout)
        # Проверяем, что внутреннее соединение установлено
        assert serial_comm.connection is mock_connection
