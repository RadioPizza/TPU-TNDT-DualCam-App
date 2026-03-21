# Стандартные библиотеки
import logging
import sys

# Сторонние библиотеки
from PySide6.QtWidgets import QApplication, QDialog

# Локальные модули
from heater_interface import Heater
from MainWindow import MainWindow
from settings import PreviewSettings, Settings, UserData
from StartDialog import StartDialog
from diagnostics import run_flir_diagnostics

# Настройка базового конфигуратора логирования
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.StreamHandler()
    ]
)

logger = logging.getLogger(__name__)

# Загрузка настроек из файла (глобальная переменная)
settings = Settings.load_from_file()

# Глобальные объекты, которые будут использоваться в MainWindow
user_data = UserData.get_instance()
preview_settings = PreviewSettings.get_instance()

# Инициализация нагревателя
if settings.mock_heater:
    class MockHeater:
        def turn_on(self):
            logger.info("СИМУЛЯЦИЯ: Нагреватель включен")
        
        def turn_off(self):
            logger.info("СИМУЛЯЦИЯ: Нагреватель выключен")
    
    heater = MockHeater()
else:
    heater = Heater(settings.heater_COM_port_number, settings.heater_baud_rate)

    # Диагностика PySpin и камер FLIR
if __name__ == '__main__':
    success, camera_count = run_flir_diagnostics()
    if not success or camera_count == 0:
        logger.warning("Внимание: Активных камер FLIR нет.")
    
    # Инициализация приложения Qt
    app = QApplication(sys.argv)
    
    start_window = StartDialog()
    result = start_window.exec()
    
    if result == QDialog.Accepted:
        # Пользователь нажал "Начать"
        main_window = MainWindow(heater=heater, settings=settings)
        main_window.show()
        sys.exit(app.exec())
    else:
        # Пользователь нажал "Выход" или закрыл окно
        sys.exit(0)