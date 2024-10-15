import serial

class Heater:
    """
    Класс для управления нагревателем через последовательный порт.
    """

    def __init__(self, com_port_number, baud_rate):
        """
        Инициализация подключения к нагревателю.

        :param com_port_number: Строка с номером COM-порта (например, 'COM3', '/dev/ttyUSB0').
        :param baud_rate: Скорость передачи данных в бодах (например, 115200).
        """
        self.state = False  # Текущее состояние нагревателя (включен/выключен)
        self.ser = None     # Объект serial.Serial
        self.com_port_number = com_port_number
        self.baud_rate = baud_rate  # Скорость передачи данных

    def connect(self) -> bool:
        """
        Подключается к заданному COM-порту с текущей скоростью передачи данных.
        """
        # Закрываем существующее соединение, если оно открыто
        if self.ser and self.ser.is_open:
            self.ser.close()

        try:
            # Открываем новый порт с заданной скоростью
            self.ser = serial.Serial(self.com_port_number, self.baud_rate, timeout=1)
            print(f"Подключено к {self.com_port_number} со скоростью {self.baud_rate} бод")
            return True
        except serial.SerialException as e:
            print(f"Не удалось открыть порт {self.com_port_number}: {e}")
            self.ser = None  # Если подключение не удалось, устанавливаем ser в None
            return False

    def disconnect(self) -> None:
        """
        Разрывает текущее соединение с COM-портом.
        """
        if self.ser and self.ser.is_open:
            self.ser.close()
            print("Соединение с COM-портом разорвано")
        self.ser = None

    def send_command(self, command, expected_response) -> bool:
        """
        Отправляет команду на устройство и проверяет ожидаемый ответ.

        :param command: Строка с командой для отправки.
        :param expected_response: Строка с ожидаемым ответом от устройства.
        :return: True, если получен ожидаемый ответ, иначе False.
        """
        if not self.ser or not self.ser.is_open:
            print("Серийный порт не открыт")
            return False

        try:
            # Отправляем команду, добавляя перевод строки
            self.ser.write((command + '\n').encode('utf-8'))
            print(f"Отправлено: {command}")

            # Читаем ответ от устройства
            response = self.ser.readline().decode('utf-8').strip()
            print(f"Получено: {response}")

            if response == expected_response:
                return True
            else:
                print(f"Неожиданный ответ от устройства: {response}")
                return False
        except serial.SerialException as e:
            print(f"Ошибка при обмене данными: {e}")
            return False

    def turn_on(self) -> None:
        """
        Включает нагреватель, отправляя соответствующую команду.
        """
        # Заменить 'COMMAND1' и 'ACK1' реальными командой и ответом МК
        if self.send_command('COMMAND1', 'ACK1'):
            self.state = True
            print("Нагреватель включен")
        else:
            print("Не удалось включить нагреватель")

    def turn_off(self) -> None:
        """
        Выключает нагреватель, отправляя соответствующую команду.
        """
        # Заменить 'COMMAND2' и 'ACK2' реальными командой и ответом МК
        if self.send_command('COMMAND2', 'ACK2'):
            self.state = False
            print("Нагреватель выключен")
        else:
            print("Не удалось выключить нагреватель")

    def __del__(self):
        """
        Деструктор класса, вызывается при удалении объекта.
        """
        self.disconnect()