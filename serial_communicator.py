import serial
import logging
import time
from typing import Optional
from serial.tools import list_ports

# Настройка уровня логирования (можно настроить извне)
logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')

class SerialCommunicator:
    def __init__(self, port: str, baudrate: int = 9600, timeout: int = 3000):
        """
        Инициализирует последовательный порт.

        :param port: Порт, к которому подключено устройство (например, 'COM3' или '/dev/ttyUSB0')
        :param baudrate: Скорость передачи данных
        :param timeout: Таймаут чтения в секундах
        """
        self.port = port
        self.baudrate = baudrate
        self.timeout = timeout
        self.ser: Optional[serial.Serial] = None

        self._open_serial_port()

    def _open_serial_port(self):
        """Открывает последовательный порт с обработкой исключений."""
        try:
            self.ser = serial.Serial(
                port=self.port,
                baudrate=self.baudrate,
                timeout=self.timeout,
                write_timeout=self.timeout  # Таймаут для записи
            )
            logging.info(f"Открыт последовательный порт {self.port} со скоростью {self.baudrate} бод")
        except serial.SerialException as e:
            logging.error(f"Не удалось открыть порт {self.port}: {e}")
            self.ser = None

    def send_command(
            self,
            command: str,
            expected_response: Optional[str] = None,
            retries: int = 3,
            delay: float = 0.5
        ) -> bool:
        """
        Отправляет команду на устройство и проверяет ожидаемый ответ с повторными попытками.

        :param command: Команда для отправки
        :param expected_response: Ожидаемый ответ от устройства
        :param retries: Количество попыток отправки команды
        :param delay: Задержка между попытками в секундах
        :return: True, если команда успешно отправлена и получен ожидаемый ответ, иначе False
        """
        if not self.ser or not self.ser.is_open:
            logging.error("Последовательный порт не открыт")
            return False

        for attempt in range(1, retries + 1):
            try:
                # Очистка буферов перед отправкой команды
                self.ser.reset_input_buffer()
                self.ser.reset_output_buffer()

                # Отправка команды
                full_command = command.strip() + '\n'
                self.ser.write(full_command.encode('utf-8'))
                logging.debug(f"Отправлено (попытка {attempt}): {command}")

                # Ожидание ответа с использованием read_response
                response = self.read_response()

                if response is None:
                    logging.warning("Не получен ответ от устройства")
                elif expected_response is None:
                    logging.info("Команда отправлена без ожидания ответа")
                    return True
                elif expected_response.lower() in response.lower():
                    logging.info(f"Ожидаемый ответ получен: {response}")
                    return True
                else:
                    logging.warning(f"Неожиданный ответ от устройства: {response}")
            except Exception as e:
                logging.error(f"Необработанная ошибка: {e}")  # Дополнительная безопасность

            if attempt < retries:
                logging.debug(f"Повторная попытка через {delay} секунд...")
                time.sleep(delay)
            else:
                logging.error(f"Не удалось получить ожидаемый ответ после {retries} попыток")

        return False

    def read_response(self, timeout: Optional[float] = None) -> Optional[str]:
        """
        Читает ответ от устройства без отправки команды.

        :param  timeout: Временной лимит ожидания ответа. Если None, используется таймаут, установленный при инициализации
        :return: Полученный ответ или None в случае ошибки
        """
        if not self.ser or not self.ser.is_open:
            logging.error("Серийный порт не открыт")
            return None

        original_timeout = self.ser.timeout
        if timeout is not None:
            self.ser.timeout = timeout

        try:
            response = self.ser.readline().decode('utf-8').strip()
            if response:
                logging.debug(f"Получен ответ: {response}")
                return response
            else:
                logging.warning("Ответ не получен (таймаут)")
                return None
        except serial.SerialException as e:
            logging.error(f"Ошибка при чтении ответа: {e}")
            return None
        except UnicodeDecodeError as e:
            logging.error(f"Ошибка декодирования ответа: {e}")
            return None
        finally:
            # Восстановление оригинального таймаута
            if timeout is not None:
                self.ser.timeout = original_timeout

    def close(self):
        """Закрывает последовательный порт."""
        if self.ser and self.ser.is_open:
            self.ser.close()
            logging.info(f"Последовательный порт {self.port} закрыт")

    def __enter__(self):
        """Метод для использования класса в блоке with."""
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        """Гарантирует закрытие порта при выходе из блока with."""
        self.close()
    
    def __del__(self):
        self.close()
        """Гарантирует закрытие порта при удалении объекта."""
    
    @staticmethod
    def find_controller_port(
            command: str = "i",
            expected_response: str = "i",
            baudrate: int = 115200,
            timeout: float = 0.5,
            retries: int = 5,
            delay: float = 1,
            delay_between_ports: float = 1
        ) -> Optional[str]:
        """
        Перебирает все доступные COM-порты, отправляет команду и ищет ответ от контроллера.

        :param command: Команда для отправки на каждый порт
        :param expected_response: Ожидаемый ответ от контроллера
        :param baudrate: Скорость передачи данных для портов
        :param timeout: Таймаут для чтения ответа
        :param retries: Количество попыток отправки команды на каждый порт
        :param delay: Задержка между попытками внутри порта
        :param delay_between_ports: Задержка между перебором разных портов
        :return port: Строка с именем порта, если контроллер найден, иначе None
        """
        ports = list_ports.comports()
        logging.info(f"Доступные COM-порты: {[port.device for port in ports]}")

        for port_info in ports:
            port = port_info.device
            logging.info(f"Проверка порта: {port}")

            try:
                with SerialCommunicator(port, baudrate=baudrate, timeout=timeout) as device:
                    success = device.send_command(
                        command=command,
                        expected_response=expected_response,
                        retries=retries,
                        delay=delay
                    )
                    if success:
                        logging.info(f"Контроллер найден на порту: {port}")
                        return port
                    else:
                        logging.debug(f"Контроллер не найден на порту: {port}")
            except serial.SerialException as e:
                logging.error(f"Не удалось открыть порт {port}: {e}")
            except Exception as e:
                logging.error(f"Произошла ошибка при проверке порта {port}: {e}")

            logging.debug(f"Задержка перед проверкой следующего порта: {delay_between_ports} секунд")
            time.sleep(delay_between_ports)

        logging.critical("Контроллер не найден на доступных COM-портах")
        return None

# Примеры использования
if __name__ == "__main__":
    
    baudrate = 115200
    # Если порт заранее известен
    port = 'COM3'
    # Пример автопоиска нужного порта
    port = SerialCommunicator.find_controller_port()

    # Создаем экземпляр SerialCommunicator
    communicator = SerialCommunicator(port=port, baudrate=baudrate, timeout=2.0)

    # 1 пример отправки команды
    communicator.send_command('p76')
    
    # 2 пример отправки команды с ожидаемым ответом
    success = communicator.send_command('S', expected_response='S')
    if success:
        print("Команда 'S' выполнена успешно.")
    else:
        print("Не удалось выполнить команду 'S'.")

    # Закрываем последовательный порт
    communicator.close()

    # Удаляем экземпляр
    del communicator

    port = SerialCommunicator.find_controller_port()
    # Пример использования контекстного менеджера с блоком with
    with SerialCommunicator(port=port, baudrate=115200) as communicator:
        communicator.send_command('s')

