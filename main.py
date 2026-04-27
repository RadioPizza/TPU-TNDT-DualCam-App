# Стандартные библиотеки
import logging
import sys

# Сторонние библиотеки
from PySide6.QtWidgets import QApplication, QDialog

# Локальные модули
from MainWindow import MainWindow
from settings import PreviewSettings, Settings, UserData
from StartDialog import StartDialog
from heater import MockHeater, Heater
from cameras import detect_flir_cameras

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
    heater = MockHeater(settings.heater_COM_port_number, settings.heater_baud_rate)
else:
    heater = Heater(settings.heater_COM_port_number, settings.heater_baud_rate)


if __name__ == "__main__":
    try:
        camera_count = detect_flir_cameras()
        if camera_count == 0:
            logger.warning("Внимание: Активных камер FLIR нет.")
    except Exception as e:
        logger.error(f"Ошибка при вызове диагностики: {e}")
    
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