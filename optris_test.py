import sys
import numpy as np
import ctypes as ct
from PySide6.QtWidgets import QApplication, QMainWindow, QLabel
from PySide6.QtGui import QImage, QPixmap
from PySide6.QtCore import QTimer

# Define EvoIRFrameMetadata structure
class EvoIRFrameMetadata(ct.Structure):
    _fields_ = [
        ("counter", ct.c_uint),
        ("counterHW", ct.c_uint),
        ("timestamp", ct.c_longlong),
        ("timestampMedia", ct.c_longlong),
        ("flagState", ct.c_int),
        ("tempChip", ct.c_float),
        ("tempFlag", ct.c_float),
        ("tempBox", ct.c_float),    
    ]

class ThermalCameraApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Optris PI 640 Viewer")
        self.setGeometry(100, 100, 700, 600)
        
        # Создаем виджет для отображения
        self.image_label = QLabel(self)
        self.image_label.setGeometry(10, 10, 640, 480)
        self.image_label.setScaledContents(True)
        
        # Инициализация камеры
        if not self.init_camera():
            print("Ошибка инициализации камеры")
            sys.exit(1)
        
        # Таймер для обновления кадров
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.update_frame)
        self.timer.start(100)  # 10 FPS

    def init_camera(self):
        try:
            # Загрузка библиотеки
            self.libir = ct.CDLL('.\libirimager.dll')
            
            # Определение типов аргументов и возвращаемых значений
            self.libir.evo_irimager_usb_init.argtypes = [ct.c_char_p, ct.c_char_p, ct.c_char_p]
            self.libir.evo_irimager_usb_init.restype = ct.c_int
            
            self.libir.evo_irimager_get_thermal_image_size.argtypes = [ct.POINTER(ct.c_int), ct.POINTER(ct.c_int)]
            self.libir.evo_irimager_get_thermal_image_size.restype = None
            
            self.libir.evo_irimager_get_palette_image_size.argtypes = [ct.POINTER(ct.c_int), ct.POINTER(ct.c_int)]
            self.libir.evo_irimager_get_palette_image_size.restype = None
            
            self.libir.evo_irimager_get_thermal_palette_image_metadata.argtypes = [
                ct.c_int, ct.c_int, ct.POINTER(ct.c_ushort),
                ct.c_int, ct.c_int, ct.POINTER(ct.c_ubyte),
                ct.POINTER(EvoIRFrameMetadata)
            ]
            self.libir.evo_irimager_get_thermal_palette_image_metadata.restype = ct.c_int
            
            self.libir.evo_irimager_terminate.argtypes = []
            self.libir.evo_irimager_terminate.restype = None
            
            # Инициализация камеры
            pathXml = b'generic.xml'  # Убедитесь что файл в той же директории
            pathFormat = b''
            pathLog = b''
            
            ret = self.libir.evo_irimager_usb_init(pathXml, pathFormat, pathLog)
            if ret != 0:
                print(f"Ошибка инициализации: {ret}")
                return False
            
            # Получение размеров изображения
            self.thermal_width = ct.c_int()
            self.thermal_height = ct.c_int()
            self.libir.evo_irimager_get_thermal_image_size(ct.byref(self.thermal_width), ct.byref(self.thermal_height))
            print(f"Thermal size: {self.thermal_width.value}x{self.thermal_height.value}")
            
            self.palette_width = ct.c_int()
            self.palette_height = ct.c_int()
            self.libir.evo_irimager_get_palette_image_size(ct.byref(self.palette_width), ct.byref(self.palette_height))
            print(f"Palette size: {self.palette_width.value}x{self.palette_height.value}")
            
            # Буферы для данных
            self.np_thermal = np.zeros([self.thermal_width.value * self.thermal_height.value], dtype=np.uint16)
            self.np_img = np.zeros([self.palette_width.value * self.palette_height.value * 3], dtype=np.uint8)
            self.metadata = EvoIRFrameMetadata()
            
            return True
            
        except Exception as e:
            print(f"Ошибка инициализации: {e}")
            return False

    def update_frame(self):
        try:
            # Получение изображения
            ret = self.libir.evo_irimager_get_thermal_palette_image_metadata(
                self.thermal_width, 
                self.thermal_height, 
                self.np_thermal.ctypes.data_as(ct.POINTER(ct.c_ushort)), 
                self.palette_width, 
                self.palette_height, 
                self.np_img.ctypes.data_as(ct.POINTER(ct.c_ubyte)), 
                ct.byref(self.metadata)
            )
            
            if ret != 0:
                print(f"Ошибка получения кадра: {ret}")
                return
            
            # Преобразование в RGB
            img_rgb = self.np_img.reshape(
                self.palette_height.value, 
                self.palette_width.value, 
                3
            )[:, :, ::-1].copy()  # BGR -> RGB
            
            # Конвертация в QImage
            height, width, _ = img_rgb.shape
            bytes_per_line = 3 * width
            qimg = QImage(
                img_rgb.data, 
                width, 
                height, 
                bytes_per_line, 
                QImage.Format_RGB888
            )
            
            # Отображение в интерфейсе
            self.image_label.setPixmap(QPixmap.fromImage(qimg))
            
        except Exception as e:
            print(f"Ошибка обновления кадра: {e}")

    def closeEvent(self, event):
        """Очистка ресурсов при закрытии"""
        self.timer.stop()
        if hasattr(self, 'libir'):
            self.libir.evo_irimager_terminate()
        super().closeEvent(event)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = ThermalCameraApp()
    window.show()
    sys.exit(app.exec())