import time
from heater_interface import Heater

com_port = 'COM6'
baud_rate = 115200
heater = Heater(com_port, baud_rate=baud_rate)

if heater.connect():
    time.sleep(2)
    heater.turn_on()
    time.sleep(2)
    heater.turn_off()
    heater.disconnect()