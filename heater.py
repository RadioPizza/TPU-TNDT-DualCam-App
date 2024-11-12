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