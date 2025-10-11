import sys
import numpy as np
import ctypes as ct
import time
import os
import re
from datetime import datetime
import cv2
from PySide6.QtWidgets import (QApplication, QMainWindow, QLabel, 
                               QComboBox, QVBoxLayout, QWidget, QCheckBox, 
                               QPushButton, QHBoxLayout, QGroupBox, QSplitter, 
                               QMessageBox)
from PySide6.QtGui import QImage, QPixmap
from PySide6.QtCore import QTimer, Qt

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

class FormatsDefParser:
    """Парсер файла Formats.def для получения информации о доступных форматах камер"""
    
    def __init__(self, def_file_path='Formats.def'):
        self.def_file_path = def_file_path
        self.formats = []
        self.parse_formats_file()
    
    def parse_formats_file(self):
        """Парсит файл Formats.def и извлекает информацию о форматах"""
        try:
            with open(self.def_file_path, 'r', encoding='utf-8') as f:
                content = f.read()
            
            # Ищем все блоки форматов
            format_blocks = re.findall(r'\[Format\](.*?)\[Format end\]', content, re.DOTALL)
            
            # Словарь для хранения форматов по GUID, чтобы отслеживать замены
            formats_by_guid = {}
            deprecated_guids = set()
            
            for block in format_blocks:
                format_info = {}
                
                # Извлекаем GUID
                guid_match = re.search(r'Guid\s*=\s*{([^}]+)}', block)
                if not guid_match:
                    continue
                    
                guid = guid_match.group(1)
                format_info['guid'] = guid
                
                # Проверяем, является ли формат устаревшим
                if "this format is deprecated" in block.lower():
                    deprecated_guids.add(guid)
                    continue
                
                # Проверяем, заменяет ли этот формат другой (устаревший)
                replace_match = re.search(r'replaces\s*{([^}]+)}', block, re.IGNORECASE)
                if replace_match:
                    replaced_guid = replace_match.group(1)
                    deprecated_guids.add(replaced_guid)
                
                # Извлекаем Name
                name_match = re.search(r'Name\s*=\s*"([^"]+)"', block)
                if name_match:
                    format_info['name'] = name_match.group(1)
                
                # Извлекаем Out (выходное разрешение)
                out_match = re.search(r'Out\s*=\s*(\d+)\s+(\d+)\s+([\d.]+)', block)
                if out_match:
                    format_info['width'] = int(out_match.group(1))
                    format_info['height'] = int(out_match.group(2))
                    format_info['fps'] = float(out_match.group(3))
                
                # Извлекаем HWRev
                hwrev_match = re.search(r'HWRev\s*=\s*\(([^)]+)\)', block)
                if hwrev_match:
                    format_info['hwrev'] = hwrev_match.group(1)
                
                # Извлекаем FWRev
                fwrev_match = re.search(r'FWRev\s*=\s*\(([^)]+)\)', block)
                if fwrev_match:
                    format_info['fwrev'] = fwrev_match.group(1)
                
                # Извлекаем DeviceRes если есть
                device_res_match = re.search(r'DeviceRes\s*=\s*(\d+)\s+(\d+)\s+([\d.]+)', block)
                if device_res_match:
                    format_info['device_width'] = int(device_res_match.group(1))
                    format_info['device_height'] = int(device_res_match.group(2))
                    format_info['device_fps'] = float(device_res_match.group(3))
                
                if format_info:
                    formats_by_guid[guid] = format_info
            
            # Фильтруем устаревшие форматы
            self.formats = [fmt for guid, fmt in formats_by_guid.items() if guid not in deprecated_guids]
            
            print(f"Загружено {len(self.formats)} форматов из {self.def_file_path}")
            
        except Exception as e:
            print(f"Ошибка загрузки файла Formats.def: {e}")
    
    def get_filtered_formats_info(self):
        """Возвращает информацию об отфильтрованных форматах для отладки"""
        try:
            with open(self.def_file_path, 'r', encoding='utf-8') as f:
                content = f.read()
            
            format_blocks = re.findall(r'\[Format\](.*?)\[Format end\]', content, re.DOTALL)
            
            all_formats = []
            deprecated_count = 0
            
            for block in format_blocks:
                format_info = {}
                
                # Извлекаем GUID и имя
                guid_match = re.search(r'Guid\s*=\s*{([^}]+)}', block)
                name_match = re.search(r'Name\s*=\s*"([^"]+)"', block)
                
                if guid_match and name_match:
                    format_info['guid'] = guid_match.group(1)
                    format_info['name'] = name_match.group(1)
                    format_info['deprecated'] = "this format is deprecated" in block.lower()
                    format_info['replaces'] = "replaces" in block.lower()
                    
                    if format_info['deprecated']:
                        deprecated_count += 1
                    
                    all_formats.append(format_info)
            
            return {
                'total_formats': len(all_formats),
                'deprecated_count': deprecated_count,
                'filtered_formats': len(self.formats),
                'details': all_formats
            }
            
        except Exception as e:
            return {'error': str(e)}
    
    def get_formats_by_resolution(self, width, height):
        """Возвращает форматы по заданному разрешению"""
        matching_formats = []
        for fmt in self.formats:
            if fmt.get('width') == width and fmt.get('height') == height:
                matching_formats.append(fmt)
        return matching_formats
    
    def get_all_formats(self):
        """Возвращает все доступные форматы"""
        return self.formats
    
    def get_formats_grouped_by_model(self):
        """Группирует форматы по моделям камер"""
        models = {}
        for fmt in self.formats:
            # Извлекаем название модели из имени формата
            name_parts = fmt['name'].split()
            if name_parts:
                model_name = name_parts[0]  # Первое слово - название модели
                if model_name not in models:
                    models[model_name] = []
                models[model_name].append(fmt)
        return models

class CameraManager:
    """Менеджер для работы с камерами через libirimager.dll"""
    
    def __init__(self):
        self.libir = None
        self.formats_parser = FormatsDefParser()
        self.current_format_index = 0
        self.available_formats = []
        
    def init_library(self):
        """Инициализирует библиотеку libirimager.dll"""
        try:
            self.libir = ct.CDLL('.\libirimager.dll')
            
            # Определяем прототипы функций
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
            
            self.libir.evo_irimager_set_palette.argtypes = [ct.c_int]
            self.libir.evo_irimager_set_palette.restype = ct.c_int
            
            self.libir.evo_irimager_set_shutter_mode.argtypes = [ct.c_int]
            self.libir.evo_irimager_set_shutter_mode.restype = ct.c_int
            
            self.libir.evo_irimager_trigger_shutter_flag.argtypes = []
            self.libir.evo_irimager_trigger_shutter_flag.restype = ct.c_int
            
            self.libir.evo_irimager_to_palette_save_png.argtypes = [
                ct.POINTER(ct.c_ushort), ct.c_int, ct.c_int,
                ct.c_char_p, ct.c_int, ct.c_int
            ]
            self.libir.evo_irimager_to_palette_save_png.restype = ct.c_int
            
            self.libir.evo_irimager_to_palette_save_png_high_precision.argtypes = [
                ct.POINTER(ct.c_ushort), ct.c_int, ct.c_int,
                ct.c_char_p, ct.c_int, ct.c_int, ct.c_short
            ]
            self.libir.evo_irimager_to_palette_save_png_high_precision.restype = ct.c_int
            
            self.libir.evo_irimager_terminate.argtypes = []
            self.libir.evo_irimager_terminate.restype = None
            
            # Новые функции для получения информации о камере
            self.libir.evo_irimager_get_serial.argtypes = [ct.POINTER(ct.c_uint)]
            self.libir.evo_irimager_get_serial.restype = ct.c_int
            
            return True
            
        except Exception as e:
            print(f"Ошибка загрузки libirimager.dll: {e}")
            return False
    
    def init_camera(self, xml_path='generic.xml'):
        """Инициализирует камеру с указанным XML-файлом"""
        if not self.libir:
            if not self.init_library():
                return False
        
        try:
            pathXml = xml_path.encode('utf-8')
            pathFormat = b''
            pathLog = b''
            
            ret = self.libir.evo_irimager_usb_init(pathXml, pathFormat, pathLog)
            if ret != 0:
                print(f"Ошибка инициализации камеры: {ret}")
                return False
            
            # Получаем размеры изображения
            thermal_width = ct.c_int()
            thermal_height = ct.c_int()
            self.libir.evo_irimager_get_thermal_image_size(ct.byref(thermal_width), ct.byref(thermal_height))
            
            palette_width = ct.c_int()
            palette_height = ct.c_int()
            self.libir.evo_irimager_get_palette_image_size(ct.byref(palette_width), ct.byref(palette_height))
            
            # Получаем серийный номер
            serial = ct.c_uint()
            ret = self.libir.evo_irimager_get_serial(ct.byref(serial))
            if ret == 0:
                print(f"Серийный номер камеры: {serial.value}")
            else:
                print("Не удалось получить серийный номер камеры")
            
            print(f"Thermal size: {thermal_width.value}x{thermal_height.value}")
            print(f"Palette size: {palette_width.value}x{palette_height.value}")
            
            # Определяем доступные форматы для этого разрешения
            self.available_formats = self.formats_parser.get_formats_by_resolution(
                thermal_width.value, thermal_height.value
            )
            
            # Если не нашли точного совпадения, используем все форматы
            if not self.available_formats:
                self.available_formats = self.formats_parser.get_all_formats()
                print("Точное совпадение не найдено, используются все доступные форматы")
            
            return {
                'thermal_width': thermal_width,
                'thermal_height': thermal_height,
                'palette_width': palette_width,
                'palette_height': palette_height,
                'serial': serial.value if ret == 0 else 0
            }
            
        except Exception as e:
            print(f"Ошибка инициализации камеры: {e}")
            return False
    
    def deinit_camera(self):
        """Освобождает ресурсы камеры"""
        if self.libir:
            self.libir.evo_irimager_terminate()

class PaletteManager:
    """Управление цветовыми палитрами камеры"""
    
    PALETTE_MAP = {
        "Alarm Blue": 1,
        "Pinkblue": 2,
        "Bone": 3,
        "Grayblack": 4,
        "Alarm Green": 5,
        "Iron": 6, # если 0 и больше 11 - тоже будет Ironй
        "Orange": 7, 
        "Medical": 8,
        "Rain": 9,
        "Rainbow": 10,
        "Alarm Red": 11,
    }
    
    DEFAULT_PALETTE_ID = 6
    SCALING_MODE_MINMAX = 2
    
    def __init__(self, camera_manager=None):
        self.camera_manager = camera_manager
    
    def get_palette_id(self, palette_name):
        """Возвращает ID палитры по имени"""
        return self.PALETTE_MAP.get(palette_name, self.DEFAULT_PALETTE_ID)
    
    def get_available_palettes(self):
        """Возвращает список доступных палитр"""
        return list(self.PALETTE_MAP.keys())
    
    def set_palette(self, palette_name):
        """Устанавливает цветовую палитру для камеры"""
        if not self.camera_manager or not self.camera_manager.libir:
            return False
            
        palette_id = self.get_palette_id(palette_name)
        ret = self.camera_manager.libir.evo_irimager_set_palette(palette_id)
        return ret == 0

class ThermalCameraApp(QMainWindow):
    SHUTTER_MODE_AUTO = 1
    SHUTTER_MODE_MANUAL = 0
    
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Optris Thermal Camera Viewer")
        self.setGeometry(100, 100, 1200, 700)
        
        # Инициализируем менеджеры
        self.camera_manager = CameraManager()
        self.palette_manager = PaletteManager(self.camera_manager)
        self.formats_parser = FormatsDefParser()
        
        debug_info = self.formats_parser.get_filtered_formats_info()
        if 'error' not in debug_info:
            print(f"Форматы: всего {debug_info['total_formats']}, "
                f"устаревших {debug_info['deprecated_count']}, "
                f"отфильтровано {debug_info['filtered_formats']}")
        
        # Загружаем шаблон XML при инициализации
        self.xml_template = self.load_xml_template()
        
        # Создаем центральный виджет и главный горизонтальный макет
        central_widget = QWidget(self)
        self.setCentralWidget(central_widget)
        main_layout = QHBoxLayout(central_widget)
        
        # Левая панель: только изображение
        left_panel = QWidget()
        left_layout = QVBoxLayout(left_panel)
        left_layout.setContentsMargins(0, 0, 0, 0)
        
        # Виджет для отображения изображения
        self.image_label = QLabel(self)
        self.image_label.setAlignment(Qt.AlignCenter)
        self.image_label.setScaledContents(False)
        self.image_label.setMinimumSize(100, 100)
        left_layout.addWidget(self.image_label, 1)
        
        # Правая панель: элементы управления и информация
        right_panel = QWidget()
        right_layout = QVBoxLayout(right_panel)
        right_layout.setAlignment(Qt.AlignTop)
        
        # Группа для управления камерой
        camera_group = QGroupBox("Управление камерой")
        camera_layout = QVBoxLayout()
        camera_group.setLayout(camera_layout)
        right_layout.addWidget(camera_group)
        
        # Информация о камере
        self.camera_info_label = QLabel("Камера: не определена")
        camera_layout.addWidget(self.camera_info_label)
        
        # Добавляем выбор формата видеопотока
        camera_layout.addWidget(QLabel("Формат видеопотока:", self))
        self.resolution_combo = QComboBox(self)
        camera_layout.addWidget(self.resolution_combo)
        
        # QCheckBox для управления автофлагом
        self.auto_calib_checkbox = QCheckBox("Разрешить автоматическую калибровку", self)
        self.auto_calib_checkbox.setChecked(True)
        self.auto_calib_checkbox.stateChanged.connect(self.toggle_auto_calib)
        camera_layout.addWidget(self.auto_calib_checkbox)
        
        # Кнопка для ручной калибровки
        self.manual_calib_button = QPushButton("Ручная калибровка", self)
        self.manual_calib_button.clicked.connect(self.trigger_calibration)
        camera_layout.addWidget(self.manual_calib_button)
        
        # Создаем выпадающий список для выбора палитры
        camera_layout.addWidget(QLabel("Цветовая палитра:", self))
        self.palette_combo = QComboBox(self)
        self.palette_combo.addItems(self.palette_manager.get_available_palettes())
        self.palette_combo.setCurrentText("Iron")
        self.palette_combo.currentTextChanged.connect(self.set_palette)
        camera_layout.addWidget(self.palette_combo)
        
        # Состояние флага внутри группы управления камерой
        self.flag_label = QLabel("Состояние флага: --")
        camera_layout.addWidget(self.flag_label)
        
        # Группа для метаданных
        meta_group = QGroupBox("Метаданные")
        meta_layout = QVBoxLayout()
        meta_group.setLayout(meta_layout)
        right_layout.addWidget(meta_group)
        
        # QLabel для отображения разрешения
        self.resolution_label = QLabel(self)
        self.resolution_label.setText("Разрешение: ")
        meta_layout.addWidget(self.resolution_label)
        
        # QLabel для отображения FPS
        self.fps_label = QLabel(self)
        self.fps_label.setText("FPS: 0.0")
        meta_layout.addWidget(self.fps_label)
        
        # QLabel для отображения температуры в центре
        self.temp_label = QLabel(self)
        self.temp_label.setText("Центральная точка: -- °C (RAW: --)")
        meta_layout.addWidget(self.temp_label)

        # QLabel для средней температуры по кадру
        self.avg_temp_label = QLabel(self)
        self.avg_temp_label.setText("Средняя температура кадра: -- °C")
        meta_layout.addWidget(self.avg_temp_label)
        
        # Температура чипа
        self.chip_temp_label = QLabel("Температура чипа: -- °C")
        meta_layout.addWidget(self.chip_temp_label)
        
        # Температура флага
        self.flag_temp_label = QLabel("Температура флага: -- °C")
        meta_layout.addWidget(self.flag_temp_label)
        
        # Температура корпуса
        self.box_temp_label = QLabel("Температура корпуса: -- °C")
        meta_layout.addWidget(self.box_temp_label)
        
        # Счетчик кадров
        self.frame_counter_label = QLabel("Счетчик кадров: --")
        meta_layout.addWidget(self.frame_counter_label)
        
        # Временная метка
        self.timestamp_label = QLabel("Временная метка: --")
        meta_layout.addWidget(self.timestamp_label)
        
        # Группа для сохранения данных
        save_group = QGroupBox("Сохранение данных")
        save_layout = QVBoxLayout()
        save_group.setLayout(save_layout)
        right_layout.addWidget(save_group)
        
        # Чекбоксы для выбора типов сохраняемых данных
        self.save_metadata_checkbox = QCheckBox("Сохранять метаданные (.txt)", self)
        self.save_metadata_checkbox.setChecked(True)
        save_layout.addWidget(self.save_metadata_checkbox)
        
        self.save_tempdata_checkbox = QCheckBox("Сохранять температурные данные (.npy)", self)
        self.save_tempdata_checkbox.setChecked(True)
        save_layout.addWidget(self.save_tempdata_checkbox)
        
        self.save_image_checkbox = QCheckBox("Сохранять снимок в текущей палитре (.png)", self)
        self.save_image_checkbox.setChecked(True)
        save_layout.addWidget(self.save_image_checkbox)
        
        # Выбор метода сохранения PNG
        save_layout.addWidget(QLabel("Метод сохранения PNG:"))
        self.png_method_combo = QComboBox()
        self.png_method_combo.addItems([
            "Оптимальный (через SDK)",
            "Высокоточный (через SDK)",
            "Исходный (через QPixmap)"
        ])
        save_layout.addWidget(self.png_method_combo)
        
        # Кнопка для сохранения данных
        self.save_button = QPushButton("Сделать снимок", self)
        self.save_button.clicked.connect(self.save_snapshot)
        save_layout.addWidget(self.save_button)
        
        # В группе для сохранения данных добавляем кнопку теста скорости
        self.speed_test_button = QPushButton("Тест скорости сохранения", self)
        self.speed_test_button.clicked.connect(self.run_save_speed_test)
        save_layout.addWidget(self.speed_test_button)
        
        # Группа для записи видео
        video_group = QGroupBox("Запись видео")
        video_layout = QVBoxLayout()
        video_group.setLayout(video_layout)
        right_layout.addWidget(video_group)
        
        # Кнопки записи видео
        button_layout = QHBoxLayout()
        video_layout.addLayout(button_layout)
        
        # Кнопка начала записи видео
        self.start_record_button = QPushButton("Начать запись", self)
        self.start_record_button.clicked.connect(self.start_video_recording)
        button_layout.addWidget(self.start_record_button)
        
        # Кнопка остановки записи видео
        self.stop_record_button = QPushButton("Остановить", self)
        self.stop_record_button.clicked.connect(self.stop_video_recording)
        self.stop_record_button.setEnabled(False)
        button_layout.addWidget(self.stop_record_button)
        
        # Метка для отображения времени записи
        self.record_time_label = QLabel("Время записи: 0 сек", self)
        video_layout.addWidget(self.record_time_label)
        
        # Добавляем разделитель между левой и правой панелями
        splitter = QSplitter(Qt.Horizontal)
        splitter.addWidget(left_panel)
        splitter.addWidget(right_panel)
        splitter.setSizes([800, 400])
        
        main_layout.addWidget(splitter)
        
        # Переменные для расчета FPS
        self.frame_count = 0
        self.fps = 0.0
        self.last_time = time.time()
        self.last_update_time = time.time()
        
        # Переменные для записи видео
        self.recording = False
        self.record_start_time = 0
        self.record_duration = 0
        self.video_writer = None
        
        # Таймер для обновления времени записи
        self.record_timer = QTimer(self)
        self.record_timer.timeout.connect(self.update_record_time)
        self.record_timer.setInterval(1000)
        
        # Инициализация камеры
        if not self.init_camera():
            print("Ошибка инициализации камеры")
            sys.exit(1)
        
        # Таймер для обновления кадров
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.update_frame)
        self.timer.start(100)

    def load_xml_template(self):
        """Загружает шаблон XML-файла для камеры"""
        try:
            with open('generic.xml', 'r') as f:
                return f.read()
        except Exception as e:
            print(f"Ошибка загрузки generic.xml: {e}")
            return '''<?xml version="1.0" encoding="UTF-8"?>
<imager xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xmlns:xsd="http://www.w3.org/2001/XMLSchema">
  <serial>0</serial>
  <videoformatindex>0</videoformatindex>
  <formatspath>.</formatspath>
  <framerate>32.0</framerate>
  <bispectral>0</bispectral>
  <autoflag>
    <enable>1</enable>
    <mininterval>15.0</mininterval>
    <maxinterval>0.0</maxinterval>
  </autoflag>
  <tchipmode>0</tchipmode>
  <tchipfixedvalue>40.0</tchipfixedvalue>
  <focus>-1</focus>
  <enable_extended_temp_range>0</enable_extended_temp_range>
  <buffer_queue_size>5</buffer_queue_size>
  <enable_high_precision>0</enable_high_precision>
  <radial_distortion_correction>0</radial_distortion_correction>
  <use_external_probe>0</use_external_probe>
</imager>'''

    def detect_camera_model(self):
        """Определяет модель камеры на основе разрешения и доступных форматов"""
        matching_formats = self.formats_parser.get_formats_by_resolution(
            self.thermal_width.value, self.thermal_height.value
        )
        
        if matching_formats:
            # Берем первую подходящую модель
            name_parts = matching_formats[0]['name'].split()
            return name_parts[0] if name_parts else "Неизвестная"
        
        return "Неизвестная модель"

    def update_available_formats(self):
        """Обновляет список доступных форматов в UI"""
        self.resolution_combo.clear()
        
        # Группируем форматы по моделям для лучшего отображения
        grouped_formats = self.formats_parser.get_formats_grouped_by_model()
        
        for model_name, formats in grouped_formats.items():
            for fmt in formats:
                display_name = f"{model_name}: {fmt['name'].split(' ', 1)[1] if ' ' in fmt['name'] else fmt['name']}"
                self.resolution_combo.addItem(display_name, fmt)
        
        # Подключаем обработчик изменения формата
        self.resolution_combo.currentIndexChanged.connect(self.on_format_changed)

    def on_format_changed(self, index):
        """Обработчик изменения формата видео"""
        if index < 0:
            return
            
        format_data = self.resolution_combo.itemData(index)
        if not format_data:
            return
        
        # Здесь должна быть логика переключения формата через XML
        print(f"Выбран формат: {format_data['name']}")

    def init_camera(self, xml_path='generic.xml'):
        """Инициализирует камеру и обновляет UI"""
        camera_info = self.camera_manager.init_camera(xml_path)
        if not camera_info:
            return False
        
        self.thermal_width = camera_info['thermal_width']
        self.thermal_height = camera_info['thermal_height']
        self.palette_width = camera_info['palette_width']
        self.palette_height = camera_info['palette_height']
        
        # Обновляем информацию о камере
        model_name = self.detect_camera_model()
        self.camera_info_label.setText(
            f"Модель: {model_name}\n"
            f"Разрешение: {self.thermal_width.value}x{self.thermal_height.value}\n"
            f"Серийный: {camera_info['serial']}"
        )
        
        # Обновляем доступные форматы
        self.update_available_formats()
        
        # Буферы для данных
        self.np_thermal = np.zeros([self.thermal_width.value * self.thermal_height.value], dtype=np.uint16)
        self.np_img = np.zeros([self.palette_width.value * self.palette_height.value * 3], dtype=np.uint8)
        self.metadata = EvoIRFrameMetadata()
        
        # Установка начальной палитры
        self.set_palette(self.palette_combo.currentText())
        
        # Установка начального режима затвора
        ret = self.camera_manager.libir.evo_irimager_set_shutter_mode(1)
        if ret != 0:
            print(f"Ошибка установки начального режима затвора: {ret}")
        
        return True

    def deinit_camera(self):
        """Освобождает ресурсы камеры"""
        self.camera_manager.deinit_camera()

    def set_palette(self, palette_name):
        """Устанавливает цветовую палитру для камеры"""
        success = self.palette_manager.set_palette(palette_name)
        if not success:
            print(f"Ошибка установки палитры '{palette_name}'")
        else:
            print(f"Установлена палитра: {palette_name}")

    def toggle_auto_calib(self, state):
        """Включает/выключает автоматическую калибровку"""
        if not hasattr(self, 'camera_manager') or not self.camera_manager.libir:
            return
            
        shutter_mode = self.SHUTTER_MODE_AUTO if state == 2 else self.SHUTTER_MODE_MANUAL
        
        ret = self.camera_manager.libir.evo_irimager_set_shutter_mode(shutter_mode)
        if ret != 0:
            print(f"Ошибка установки режима затвора: {ret}")
        else:
            mode = "Автоматический" if shutter_mode == 1 else "Ручной"
            print(f"Установлен режим затвора: {mode}")

    def trigger_calibration(self):
        """Ручной запуск калибровки"""
        ret = self.camera_manager.libir.evo_irimager_trigger_shutter_flag()
        if ret != 0:
            print(f"Ошибка запуска калибровки: {ret}")
        else:
            print("Запущена ручная калибровка")

    def run_save_speed_test(self):
        """Запускает тест скорости сохранения разными методами"""
        if not hasattr(self, 'camera_manager') or not self.camera_manager.libir:
            QMessageBox.warning(self, "Ошибка", "Камера не инициализирована")
            return
        
        try:
            ret = self.camera_manager.libir.evo_irimager_get_thermal_palette_image_metadata(
                self.thermal_width, self.thermal_height, 
                self.np_thermal.ctypes.data_as(ct.POINTER(ct.c_ushort)), 
                self.palette_width, self.palette_height, 
                self.np_img.ctypes.data_as(ct.POINTER(ct.c_ubyte)), 
                ct.byref(self.metadata)
            )
            
            if ret != 0:
                QMessageBox.warning(self, "Ошибка", "Не удалось получить кадр от камеры")
                return
        except Exception as e:
            QMessageBox.critical(self, "Ошибка", f"Ошибка получения кадра: {e}")
            return
        
        thermal_data = self.np_thermal.copy()
        palette_name = self.palette_combo.currentText()
        
        # Используем менеджер палитр для получения ID
        palette_id = self.palette_manager.get_palette_id(palette_name)
        
        test_filename = "speed_test_temp.png"
        results = []
        
        # Метод 1: Оптимальный (через SDK)
        times = []
        for _ in range(10):
            try:
                start_time = time.time()
                filename_bytes = test_filename.encode('utf-8')
                ret = self.camera_manager.libir.evo_irimager_to_palette_save_png(
                    thermal_data.ctypes.data_as(ct.POINTER(ct.c_ushort)),
                    self.thermal_width.value,
                    self.thermal_height.value,
                    filename_bytes,
                    palette_id,
                    self.palette_manager.SCALING_MODE_MINMAX
                )
                
                if ret == 0:
                    img = cv2.imread(test_filename)
                    if img is not None:
                        img_rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
                        cv2.imwrite(test_filename, img_rgb)
                    end_time = time.time()
                    times.append(end_time - start_time)
                else:
                    times = []
                    break
            except Exception as e:
                print(f"Ошибка при тестировании метода 1: {e}")
                times = []
                break
            finally:
                if os.path.exists(test_filename):
                    os.remove(test_filename)
        
        if times:
            avg_time = sum(times) / len(times)
            results.append(f"Оптимальный (через SDK): {avg_time:.4f} сек")
        
        # Метод 2: Высокоточный (через SDK)
        times = []
        for _ in range(10):
            try:
                start_time = time.time()
                filename_bytes = test_filename.encode('utf-8')
                ret = self.camera_manager.libir.evo_irimager_to_palette_save_png_high_precision(
                    thermal_data.ctypes.data_as(ct.POINTER(ct.c_ushort)),
                    self.thermal_width.value,
                    self.thermal_height.value,
                    filename_bytes,
                    palette_id,
                    2,
                    1
                )
                
                if ret == 0:
                    img = cv2.imread(test_filename)
                    if img is not None:
                        img_rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
                        cv2.imwrite(test_filename, img_rgb)
                    end_time = time.time()
                    times.append(end_time - start_time)
                else:
                    times = []
                    break
            except Exception as e:
                print(f"Ошибка при тестировании метода 2: {e}")
                times = []
                break
            finally:
                if os.path.exists(test_filename):
                    os.remove(test_filename)
        
        if times:
            avg_time = sum(times) / len(times)
            results.append(f"Высокоточный (через SDK): {avg_time:.4f} сек")
        
        # Метод 3: Исходный (через QPixmap)
        times = []
        for _ in range(10):
            try:
                img_rgb = self.np_img.reshape(
                    self.palette_height.value, 
                    self.palette_width.value, 
                    3
                )[:, :, ::-1].copy()
                
                height, width, _ = img_rgb.shape
                bytes_per_line = 3 * width
                qimg = QImage(img_rgb.data, width, height, bytes_per_line, QImage.Format_RGB888)
                
                start_time = time.time()
                pixmap = QPixmap.fromImage(qimg)
                pixmap.save(test_filename)
                end_time = time.time()
                times.append(end_time - start_time)
            except Exception as e:
                print(f"Ошибка при тестировании метода 3: {e}")
                times = []
                break
            finally:
                if os.path.exists(test_filename):
                    os.remove(test_filename)
        
        if times:
            avg_time = sum(times) / len(times)
            results.append(f"Исходный (через QPixmap): {avg_time:.4f} сек")
        
        if not results:
            result_text = "Все методы завершились с ошибкой"
        else:
            result_text = "Результаты теста скорости (среднее за 10 попыток):\n\n" + "\n".join(results)
        
        QMessageBox.information(self, "Результаты теста", result_text)

    def start_video_recording(self):
        """Начинает запись видео в формате AVI"""
        if self.recording:
            return
            
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"thermal_video_{timestamp}.avi"
        
        fps = max(1, int(self.fps))
        frame_size = (self.palette_width.value, self.palette_height.value)
        
        fourcc = cv2.VideoWriter_fourcc(*'MJPG')
        self.video_writer = cv2.VideoWriter(filename, fourcc, fps, frame_size)
        
        if not self.video_writer.isOpened():
            print("Ошибка создания видеофайла")
            self.video_writer = None
            return
        
        self.recording = True
        self.record_start_time = time.time()
        self.record_duration = 0
        self.record_time_label.setText("Время записи: 0 сек")
        self.record_timer.start()
        
        self.start_record_button.setEnabled(False)
        self.stop_record_button.setEnabled(True)
        print(f"Начата запись видео: {filename}")

    def stop_video_recording(self):
        """Останавливает запись видео и сохраняет файл"""
        if not self.recording:
            return
            
        self.recording = False
        self.record_timer.stop()
        
        if self.video_writer:
            self.video_writer.release()
            self.video_writer = None
            print(f"Видео сохранено, длительность: {self.record_duration} сек")
        
        self.start_record_button.setEnabled(True)
        self.stop_record_button.setEnabled(False)

    def update_record_time(self):
        """Обновляет время записи видео"""
        if self.recording:
            self.record_duration = int(time.time() - self.record_start_time)
            self.record_time_label.setText(f"Время записи: {self.record_duration} сек")

    def save_snapshot(self):
        """Сохраняет выбранные типы данных по нажатию кнопки"""
        try:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            base_filename = f"thermal_{timestamp}"
            saved_files = []
            
            if self.save_metadata_checkbox.isChecked():
                meta_filename = f"{base_filename}_metadata.txt"
                with open(meta_filename, 'w') as f:
                    f.write(f"Timestamp: {timestamp}\n")
                    f.write(f"Resolution: {self.thermal_width.value}x{self.thermal_height.value}\n")
                    f.write(f"Flag state: {self.metadata.flagState}\n")
                    f.write(f"Chip temperature: {self.metadata.tempChip:.2f} °C\n")
                    f.write(f"Flag temperature: {self.metadata.tempFlag:.2f} °C\n")
                    f.write(f"Box temperature: {self.metadata.tempBox:.2f} °C\n")
                    f.write(f"Central temperature: {self.temp_label.text()}\n")
                    f.write(f"Average temperature: {self.avg_temp_label.text()}\n")
                saved_files.append(meta_filename)
            
            if self.save_tempdata_checkbox.isChecked():
                temp_filename = f"{base_filename}_data.npy"
                data_2d = self.np_thermal.reshape(self.thermal_height.value, self.thermal_width.value)
                np.save(temp_filename, data_2d)
                saved_files.append(temp_filename)
            
            if self.save_image_checkbox.isChecked():
                img_filename = f"{base_filename}_image.png"
                method = self.png_method_combo.currentIndex()
                
                if method == 0:
                    filename_bytes = img_filename.encode('utf-8')
                    palette_name = self.palette_combo.currentText()
                    
                    # Используем менеджер палитр для получения ID
                    palette_id = self.palette_manager.get_palette_id(palette_name)
                    
                    ret = self.camera_manager.libir.evo_irimager_to_palette_save_png(
                        self.np_thermal.ctypes.data_as(ct.POINTER(ct.c_ushort)),
                        self.thermal_width.value,
                        self.thermal_height.value,
                        filename_bytes,
                        palette_id,
                        2
                    )
                    
                    if ret == 0:
                        img = cv2.imread(img_filename)
                        if img is not None:
                            img_rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
                            cv2.imwrite(img_filename, img_rgb)
                            saved_files.append(img_filename)
                            print(f"Сохранено PNG через SDK: {img_filename}")
                        else:
                            print(f"Ошибка загрузки изображения для конвертации: {img_filename}")
                    else:
                        print(f"Ошибка сохранения PNG через SDK: {ret}")
                
                elif method == 1:
                    filename_bytes = img_filename.encode('utf-8')
                    palette_name = self.palette_combo.currentText()
                    
                    # Используем менеджер палитр для получения ID
                    palette_id = self.palette_manager.get_palette_id(palette_name)
                    
                    ret = self.camera_manager.libir.evo_irimager_to_palette_save_png_high_precision(
                        self.np_thermal.ctypes.data_as(ct.POINTER(ct.c_ushort)),
                        self.thermal_width.value,
                        self.thermal_height.value,
                        filename_bytes,
                        palette_id,
                        2,
                        1
                    )
                    
                    if ret == 0:
                        img = cv2.imread(img_filename)
                        if img is not None:
                            img_rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
                            cv2.imwrite(img_filename, img_rgb)
                            saved_files.append(img_filename)
                            print(f"Сохранено высокоточное PNG через SDK: {img_filename}")
                        else:
                            print(f"Ошибка загрузки изображения для конвертации: {img_filename}")
                    else:
                        print(f"Ошибка сохранения высокоточного PNG через SDK: {ret}")
                
                else:
                    pixmap = self.image_label.pixmap()
                    if pixmap is not None:
                        pixmap.save(img_filename)
                        saved_files.append(img_filename)
                        print(f"Сохранено PNG через QPixmap: {img_filename}")
                    else:
                        print("Нет изображения для сохранения")
            
            if saved_files:
                files_str = "\n".join(saved_files)
                print(f"Сохраненные файлы:\n{files_str}")
            else:
                print("Не выбраны типы данных для сохранения")
            
        except Exception as e:
            print(f"Ошибка сохранения данных: {e}")

    def update_frame(self):
        try:
            # Получение изображения
            ret = self.camera_manager.libir.evo_irimager_get_thermal_palette_image_metadata(
                self.thermal_width, self.thermal_height, 
                self.np_thermal.ctypes.data_as(ct.POINTER(ct.c_ushort)), 
                self.palette_width, self.palette_height, 
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
            qimg = QImage(img_rgb.data, width, height, bytes_per_line, QImage.Format_RGB888)
            
            # Масштабирование с сохранением пропорций
            pixmap = QPixmap.fromImage(qimg)
            
            # Получаем размер доступной области для изображения
            label_size = self.image_label.size()
            
            # Масштабируем с сохранением пропорций
            scaled_pixmap = pixmap.scaled(
                label_size, 
                Qt.KeepAspectRatio, 
                Qt.SmoothTransformation
            )
            
            # Отображение в интерфейсе
            self.image_label.setPixmap(scaled_pixmap)
            
            # Запись видео
            if self.recording and self.video_writer is not None:
                frame_bgr = cv2.cvtColor(img_rgb, cv2.COLOR_RGB2BGR)
                self.video_writer.write(frame_bgr)
            
            # Расчет FPS
            self.frame_count += 1
            current_time = time.time()
            elapsed = current_time - self.last_update_time
            
            if elapsed > 0.5:
                self.fps = self.frame_count / elapsed
                self.fps_label.setText(f"FPS: {self.fps:.1f}")
                self.last_update_time = current_time
                self.frame_count = 0
            
            # Температура в центре кадра
            center_index = (self.thermal_height.value // 2) * self.thermal_width.value + (self.thermal_width.value // 2)
            raw_temp = self.np_thermal[center_index]
            temp_c = (raw_temp / 10.0) - 100.0
            self.temp_label.setText(f"Центральная точка: {temp_c:.2f} °C (RAW: {raw_temp})")
            
            # Средняя температура кадра
            temperatures = (self.np_thermal.astype(np.float32) / 10.0) - 100.0
            avg_temp = np.mean(temperatures)
            self.avg_temp_label.setText(f"Средняя температура: {avg_temp:.2f} °C")
            
            # Состояние флага - как число
            self.flag_label.setText(f"Состояние флага: {self.metadata.flagState}")
            
            # Температура чипа
            self.chip_temp_label.setText(f"Температура чипа: {self.metadata.tempChip:.2f} °C")
            
            # Температура флага
            self.flag_temp_label.setText(f"Температура флага: {self.metadata.tempFlag:.2f} °C")
            
            # Температура корпуса
            self.box_temp_label.setText(f"Температура корпуса: {self.metadata.tempBox:.2f} °C")
            
            # Счетчик кадров
            self.frame_counter_label.setText(f"Счетчик кадров: {self.metadata.counter}")
            
            # Временная метка
            self.timestamp_label.setText(f"Временная метка: {self.metadata.timestamp}")
            
            # Обновляем лейбл с разрешением
            self.resolution_label.setText(
                f"Разрешение: {self.thermal_width.value}x{self.thermal_height.value} (Thermal)\n"
                f"Палитра: {self.palette_width.value}x{self.palette_height.value} (RGB)"
            )
            
        except Exception as e:
            # Выводим более подробную информацию об ошибке
            import traceback
            print(f"Ошибка обновления кадра: {e}")
            print(traceback.format_exc())

    def closeEvent(self, event):
        """Очистка ресурсов при закрытии"""
        self.timer.stop()
        self.record_timer.stop()
        
        if self.recording:
            self.stop_video_recording()
            
        if hasattr(self, 'camera_manager'):
            self.camera_manager.deinit_camera()
        super().closeEvent(event)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = ThermalCameraApp()
    window.show()
    sys.exit(app.exec())