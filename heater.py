import logging
from serial_communicator import SerialCommunicator

class Heater(SerialCommunicator):
    """
    Класс для управления нагревателем через последовательный порт.
    """

    def __init__(self, com_port_number, baud_rate):
        super().__init__(com_port_number, baud_rate)
        self.state = False

    def turn_on(self) -> None:
        command = 'COMMAND1'
        expected_response = 'ACK1'

        if self.send_command(command, expected_response):
            self.state = True
            logging.info("Нагреватель включен")
        else:
            logging.error("Не удалось включить нагреватель")

    def turn_off(self) -> None:
        command = 'COMMAND2'
        expected_response = 'ACK2'

        if self.send_command(command, expected_response):
            self.state = False
            logging.info("Нагреватель выключен")
        else:
            logging.error("Не удалось выключить нагреватель")

class MockHeater:
    
    def __init__(self, com_port_number, baud_rate):
        self.com_port_number = com_port_number
        self.baud_rate = baud_rate
        self.state = False
        logging.info(f"СИМУЛЯЦИЯ: MockHeater инициализирован (Порт: {com_port_number}, Бод: {baud_rate})")

    def turn_on(self) -> None:
        self.state = True
        logging.info("СИМУЛЯЦИЯ: Нагреватель включен")
        return True

    def turn_off(self) -> None:
        self.state = False
        logging.info("СИМУЛЯЦИЯ: Нагреватель выключен")
        return False