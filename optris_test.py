import sys
import numpy as np
import ctypes as ct
import time
from PySide6.QtWidgets import (QApplication, QMainWindow, QLabel, 
                               QComboBox, QVBoxLayout, QWidget)
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
        self.setGeometry(100, 100, 700, 650)
        
        # Создаем центральный виджет и макет
        central_widget = QWidget(self)
        self.setCentralWidget(central_widget)
        layout = QVBoxLayout(central_widget)
        
        # Создаем виджет для отображения
        self.image_label = QLabel(self)
        self.image_label.setScaledContents(True)
        layout.addWidget(self.image_label)
        
        # Создаем QLabel для отображения разрешения
        self.resolution_label = QLabel(self)
        self.resolution_label.setText("Resolution: ")
        layout.addWidget(self.resolution_label)
        
        # Создаем QLabel для отображения FPS
        self.fps_label = QLabel(self)
        self.fps_label.setText("FPS: 0.0")
        layout.addWidget(self.fps_label)
        
        # Создаем QLabel для отображения температуры в центре
        self.temp_label = QLabel(self)
        self.temp_label.setText("Центральная точка: -- °C (RAW: --)")
        layout.addWidget(self.temp_label)
        
        # Создаем выпадающий список для выбора палитры
        self.palette_label = QLabel("Цветовая палитра:", self)
        layout.addWidget(self.palette_label)
        
        self.palette_combo = QComboBox(self)
        # Список доступных палитр
        self.palette_combo.addItems([
            "Alarm Blue",
            "Alarm Red",
            "Alarm Green",
            "Rainbow",
            "Iron",
            "Bone",
            "Medical", 
            "Orange",
            "Rain",
            "Pinkblue",
            "Grayblack"
        ])
        self.palette_combo.setCurrentText("Iron")  # Установка палитры по умолчанию
        self.palette_combo.currentTextChanged.connect(self.set_palette)
        layout.addWidget(self.palette_combo)
        
        # Переменные для расчета FPS
        self.frame_count = 0
        self.fps = 0.0
        self.last_time = time.time()
        self.last_update_time = time.time()
        
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
            
            # Добавляем функцию для установки палитры
            self.libir.evo_irimager_set_palette.argtypes = [ct.c_int]
            self.libir.evo_irimager_set_palette.restype = ct.c_int
            
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
            
            # Обновляем лейбл с разрешением
            self.resolution_label.setText(
                f"Resolution: {self.thermal_width.value}x{self.thermal_height.value} "
                f"(Palette: {self.palette_width.value}x{self.palette_height.value})"
            )
            
            # Буферы для данных
            self.np_thermal = np.zeros([self.thermal_width.value * self.thermal_height.value], dtype=np.uint16)
            self.np_img = np.zeros([self.palette_width.value * self.palette_height.value * 3], dtype=np.uint8)
            self.metadata = EvoIRFrameMetadata()
            
            # Установка начальной палитры
            self.set_palette(self.palette_combo.currentText())
            
            return True
            
        except Exception as e:
            print(f"Ошибка инициализации: {e}")
            return False

    def set_palette(self, palette_name):
        """Устанавливает цветовую палитру для камеры"""
        if not hasattr(self, 'libir'):
            return
            
        # Соответствие имен палитр их ID
        palette_map = {
            "Alarm Blue": 1,
            "Pinkblue": 2,
            "Bone": 3,
            "Grayblack": 4,
            "Alarm Green": 5,
            "Iron": 6, # 0 и больше 11 - тоже Iron
            "Orange": 7, 
            "Medical": 8,
            "Rain": 9,
            "Rainbow": 10, 
            "Alarm Red": 11,
        }
        
        palette_id = palette_map.get(palette_name, 6)
        ret = self.libir.evo_irimager_set_palette(palette_id)
        if ret != 0:
            print(f"Ошибка установки палитры '{palette_name}' (ID={palette_id}): {ret}")
        else:
            print(f"Установлена палитра: {palette_name} (ID={palette_id})")

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
            
            # Расчет FPS
            self.frame_count += 1
            current_time = time.time()
            elapsed = current_time - self.last_update_time
            
            # Обновляем FPS каждые 0.5 секунд для плавности
            if elapsed > 0.5:
                self.fps = self.frame_count / elapsed
                self.fps_label.setText(f"FPS: {self.fps:.1f}")
                self.last_update_time = current_time
                self.frame_count = 0
            
            # Получение температуры в центре кадра
            center_index = (self.thermal_height.value // 2) * self.thermal_width.value + (self.thermal_width.value // 2)
            raw_temp = self.np_thermal[center_index]
            
            # Преобразование сырого значения в температуру (°C)
            # Формула для камер Optris PI: температура (°C) = (сырое значение / 10) - 100
            temp_c = (raw_temp / 10.0) - 100.0
            
            # Обновление QLabel с температурой
            self.temp_label.setText(f"Центральная точка: {temp_c:.2f} °C (RAW: {raw_temp})")
            
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