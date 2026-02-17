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

if __name__ == '__main__':
    # Диагностика PySpin и камер FLIR
    try:
        import PySpin
        logger.info("PySpin успешно импортирован")
        
        # Быстрая проверка камер без длительного удержания ресурсов
        system = PySpin.System.GetInstance()
        cam_list = system.GetCameras()
        num_cameras = cam_list.GetSize()
        logger.info(f"Количество обнаруженных камер FLIR: {num_cameras}")
        
        if num_cameras > 0:
            # Получаем информацию о первой камере
            camera = cam_list.GetByIndex(0)
            camera.Init()
            
            try:
                nodemap = camera.GetNodeMap()
                node_model = PySpin.CStringPtr(nodemap.GetNode("DeviceModelName"))
                if PySpin.IsAvailable(node_model):
                    logger.info(f"Модель камеры: {node_model.GetValue()}")
            finally:
                camera.DeInit()
                del camera
        
        cam_list.Clear()
        system.ReleaseInstance()
        
    except Exception as e:
        logger.error(f"Диагностика PySpin не удалась: {e}")
    
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