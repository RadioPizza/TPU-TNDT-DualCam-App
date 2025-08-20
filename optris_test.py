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

class ThermalCameraApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Optris PI 640 Viewer")
        self.setGeometry(100, 100, 1200, 700)
        
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
        self.image_label.setScaledContents(True)
        left_layout.addWidget(self.image_label, 1)  # Растягиваем изображение
        
        # Правая панель: элементы управления и информация
        right_panel = QWidget()
        right_layout = QVBoxLayout(right_panel)
        right_layout.setAlignment(Qt.AlignTop)
        
        # Группа для управления камерой
        camera_group = QGroupBox("Управление камерой")
        camera_layout = QVBoxLayout()
        camera_group.setLayout(camera_layout)
        right_layout.addWidget(camera_group)
        
        # Добавляем выбор разрешения видеопотока
        camera_layout.addWidget(QLabel("Разрешение видеопотока:", self))
        self.resolution_combo = QComboBox(self)
        self.resolution_combo.addItems([
            "640x480 @ 32Hz (полный кадр)",
            "640x120 @ 125Hz (высокая частота)"
        ])
        self.resolution_combo.currentIndexChanged.connect(self.change_video_format)
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
        # Список доступных палитр
        self.palette_combo.addItems([
            "Alarm Blue",
            "Pinkblue",
            "Bone",
            "Grayblack",
            "Alarm Green",
            "Iron",
            "Orange", 
            "Medical",
            "Rain",
            "Rainbow",
            "Alarm Red"
        ])
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
        splitter.setSizes([800, 400])  # Начальное соотношение размеров
        
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
        self.timer.start(100)  # 10 FPS

    def load_xml_template(self):
        """Загружает шаблон XML-файла для камеры"""
        try:
            with open('generic.xml', 'r') as f:
                return f.read()
        except Exception as e:
            print(f"Ошибка загрузки generic.xml: {e}")
            # Возвращаем стандартный шаблон как fallback
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

    def change_video_format(self, index):
        """Изменяет формат видео потока"""
        # Останавливаем таймеры
        self.timer.stop()
        self.record_timer.stop()
        
        # Останавливаем запись видео, если она активна
        if self.recording:
            self.stop_video_recording()
        
        # Определяем параметры для выбранного формата
        if index == 0:  # 640x480 @ 32Hz
            videoformatindex = 0
            framerate = 32.0
        else:  # 640x120 @ 125Hz
            videoformatindex = 1
            framerate = 125.0
        
        # Создаем временный XML-файл с новыми параметрами
        new_xml = re.sub(
            r'<videoformatindex>\d+</videoformatindex>',
            f'<videoformatindex>{videoformatindex}</videoformatindex>',
            self.xml_template
        )
        new_xml = re.sub(
            r'<framerate>[\d.]+</framerate>',
            f'<framerate>{framerate}</framerate>',
            new_xml
        )
        
        # Сохраняем временный XML-файл
        temp_xml_path = 'temp_generic.xml'
        try:
            with open(temp_xml_path, 'w') as f:
                f.write(new_xml)
        except Exception as e:
            print(f"Ошибка создания временного XML-файла: {e}")
            return
        
        # Переинициализируем камеру с новыми параметрами
        self.deinit_camera()
        if not self.init_camera(xml_path=temp_xml_path):
            print("Ошибка переинициализации камеры")
            # Пытаемся вернуться к предыдущей конфигурации
            self.deinit_camera()
            self.init_camera()
        
        # Запускаем таймеры снова
        self.timer.start(100)
        self.record_timer.start()
        
        # Удаляем временный файл
        try:
            os.remove(temp_xml_path)
        except:
            pass

    def run_save_speed_test(self):
        """Запускает тест скорости сохранения разными методами"""
        if not hasattr(self, 'libir'):
            QMessageBox.warning(self, "Ошибка", "Камера не инициализирована")
            return
        
        # Получаем текущий кадр
        try:
            ret = self.libir.evo_irimager_get_thermal_palette_image_metadata(
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
        
        # Подготавливаем данные для теста
        thermal_data = self.np_thermal.copy()
        palette_name = self.palette_combo.currentText()
        palette_map = {
            "Alarm Blue": 1,
            "Pinkblue": 2,
            "Bone": 3,
            "Grayblack": 4,
            "Alarm Green": 5,
            "Iron": 6,
            "Orange": 7, 
            "Medical": 8,
            "Rain": 9,
            "Rainbow": 10,
            "Alarm Red": 11,
        }
        palette_id = palette_map.get(palette_name, 6)
        
        # Создаем временный файл
        test_filename = "speed_test_temp.png"
        
        # Тестируем три метода
        results = []
        
        # Метод 1: Оптимальный (через SDK)
        times = []
        for _ in range(10):
            try:
                start_time = time.time()
                filename_bytes = test_filename.encode('utf-8')
                ret = self.libir.evo_irimager_to_palette_save_png(
                    thermal_data.ctypes.data_as(ct.POINTER(ct.c_ushort)),
                    self.thermal_width.value,
                    self.thermal_height.value,
                    filename_bytes,
                    palette_id,
                    2  # MinMax scaling
                )
                
                if ret == 0:
                    # Исправление цветовых каналов
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
                ret = self.libir.evo_irimager_to_palette_save_png_high_precision(
                    thermal_data.ctypes.data_as(ct.POINTER(ct.c_ushort)),
                    self.thermal_width.value,
                    self.thermal_height.value,
                    filename_bytes,
                    palette_id,
                    2,  # MinMax scaling
                    1   # 1 decimal place
                )
                
                if ret == 0:
                    # Исправление цветовых каналов
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
                # Создаем изображение для отображения
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
        
        # Форматируем результаты
        if not results:
            result_text = "Все методы завершились с ошибкой"
        else:
            result_text = "Результаты теста скорости (среднее за 10 попыток):\n\n" + "\n".join(results)
        
        # Показываем результаты
        QMessageBox.information(self, "Результаты теста", result_text)

    def start_video_recording(self):
        """Начинает запись видео в формате AVI"""
        if self.recording:
            return
            
        # Генерируем имя файла с временной меткой
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"thermal_video_{timestamp}.avi"
        
        # Параметры видео
        fps = max(1, int(self.fps))
        frame_size = (self.palette_width.value, self.palette_height.value)
        
        # Создаем VideoWriter
        fourcc = cv2.VideoWriter_fourcc(*'MJPG')
        self.video_writer = cv2.VideoWriter(filename, fourcc, fps, frame_size)
        
        if not self.video_writer.isOpened():
            print("Ошибка создания видеофайла")
            self.video_writer = None
            return
        
        # Устанавливаем флаги и запускаем таймер
        self.recording = True
        self.record_start_time = time.time()
        self.record_duration = 0
        self.record_time_label.setText("Время записи: 0 сек")
        self.record_timer.start()
        
        # Обновляем состояние кнопок
        self.start_record_button.setEnabled(False)
        self.stop_record_button.setEnabled(True)
        print(f"Начата запись видео: {filename}")

    def stop_video_recording(self):
        """Останавливает запись видео и сохраняет файл"""
        if not self.recording:
            return
            
        # Останавливаем запись
        self.recording = False
        self.record_timer.stop()
        
        # Закрываем видеофайл
        if self.video_writer:
            self.video_writer.release()
            self.video_writer = None
            print(f"Видео сохранено, длительность: {self.record_duration} сек")
        
        # Обновляем состояние кнопок
        self.start_record_button.setEnabled(True)
        self.stop_record_button.setEnabled(False)

    def update_record_time(self):
        """Обновляет время записи видео"""
        if self.recording:
            self.record_duration = int(time.time() - self.record_start_time)
            self.record_time_label.setText(f"Время записи: {self.record_duration} сек")

    def toggle_auto_calib(self, state):
        """Включает/выключает автоматическую калибровку"""
        if not hasattr(self, 'libir'):
            return
            
        shutter_mode = 1 if state == 2 else 0  # Qt.Checked == 2
        
        ret = self.libir.evo_irimager_set_shutter_mode(shutter_mode)
        if ret != 0:
            print(f"Ошибка установки режима затвора: {ret}")
        else:
            mode = "Автоматический" if shutter_mode == 1 else "Ручной"
            print(f"Установлен режим затвора: {mode}")

    def trigger_calibration(self):
        """Ручной запуск калибровки"""
        ret = self.libir.evo_irimager_trigger_shutter_flag()
        if ret != 0:
            print(f"Ошибка запуска калибровки: {ret}")
        else:
            print("Запущена ручная калибровка")

    def save_snapshot(self):
        """Сохраняет выбранные типы данных по нажатию кнопки"""
        try:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            base_filename = f"thermal_{timestamp}"
            saved_files = []
            
            # Сохраняем метаданные
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
            
            # Сохраняем температурные данные
            if self.save_tempdata_checkbox.isChecked():
                temp_filename = f"{base_filename}_data.npy"
                data_2d = self.np_thermal.reshape(self.thermal_height.value, self.thermal_width.value)
                np.save(temp_filename, data_2d)
                saved_files.append(temp_filename)
            
            # Сохраняем изображение
            if self.save_image_checkbox.isChecked():
                img_filename = f"{base_filename}_image.png"
                
                method = self.png_method_combo.currentIndex()
                
                if method == 0:
                    """
                    Метод: Оптимальный (через SDK)
                    - Среднее время сохранения: ~1.4 сек
                    * Сохраняет изображение с точной температурной шкалой
                    * Медленнее других методов в 5-15 раз
                    * Нестабильная производительность (может занимать до 4 сек)
                    - Рекомендации:
                    * Использовать только когда критична точность температурной шкалы
                    * Не подходит для серийной съемки или работы в реальном времени
                    """
                    filename_bytes = img_filename.encode('utf-8')
                    
                    # Получаем текущую палитру
                    palette_name = self.palette_combo.currentText()
                    palette_map = {
                        "Alarm Blue": 1,
                        "Pinkblue": 2,
                        "Bone": 3,
                        "Grayblack": 4,
                        "Alarm Green": 5,
                        "Iron": 6,
                        "Orange": 7, 
                        "Medical": 8,
                        "Rain": 9,
                        "Rainbow": 10,
                        "Alarm Red": 11,
                    }
                    # Для неизвестных значений используем Iron (6)
                    palette_id = palette_map.get(palette_name, 6)
                    
                    # Вызываем функцию SDK
                    ret = self.libir.evo_irimager_to_palette_save_png(
                        self.np_thermal.ctypes.data_as(ct.POINTER(ct.c_ushort)),
                        self.thermal_width.value,
                        self.thermal_height.value,
                        filename_bytes,
                        palette_id,
                        2  # MinMax scaling
                    )
                    
                    if ret == 0:
                        # Исправление цветовых каналов
                        img = cv2.imread(img_filename)
                        if img is not None:
                            # Конвертируем BGR в RGB
                            img_rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
                            cv2.imwrite(img_filename, img_rgb)
                            saved_files.append(img_filename)
                            print(f"Сохранено PNG через SDK: {img_filename}")
                        else:
                            print(f"Ошибка загрузки изображения для конвертации: {img_filename}")
                    else:
                        print(f"Ошибка сохранения PNG через SDK: {ret}")
                
                elif method == 1:
                    """
                    Метод: Высокоточный (через SDK)
                    - Среднее время сохранения: ~2.5 сек
                    * Сохраняет изображение с максимальной температурной точностью
                    * Самый медленный метод (в 10-15 раз медленнее QPixmap)
                    * Наибольший разброс времени выполнения (от 1.3 до 4+ сек)
                    - Рекомендации:
                    * Использовать только там, где критична точность
                    * Не подходит для рабочих задач из-за низкой производительности
                    """
                    filename_bytes = img_filename.encode('utf-8')
                    
                    # Получаем текущую палитру
                    palette_name = self.palette_combo.currentText()
                    palette_map = {
                        "Alarm Blue": 1,
                        "Pinkblue": 2,
                        "Bone": 3,
                        "Grayblack": 4,
                        "Alarm Green": 5,
                        "Iron": 6,
                        "Orange": 7, 
                        "Medical": 8,
                        "Rain": 9,
                        "Rainbow": 10,
                        "Alarm Red": 11,
                    }
                    # Для неизвестных значений используем Iron (6)
                    palette_id = palette_map.get(palette_name, 6)
                    
                    # Вызываем функцию SDK
                    ret = self.libir.evo_irimager_to_palette_save_png_high_precision(
                        self.np_thermal.ctypes.data_as(ct.POINTER(ct.c_ushort)),
                        self.thermal_width.value,
                        self.thermal_height.value,
                        filename_bytes,
                        palette_id,
                        2,  # MinMax scaling
                        1   # 1 decimal place
                    )
                    
                    if ret == 0:
                        # Исправление цветовых каналов
                        img = cv2.imread(img_filename)
                        if img is not None:
                            # Конвертируем BGR в RGB
                            img_rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
                            cv2.imwrite(img_filename, img_rgb)
                            saved_files.append(img_filename)
                            print(f"Сохранено высокоточное PNG через SDK: {img_filename}")
                        else:
                            print(f"Ошибка загрузки изображения для конвертации: {img_filename}")
                    else:
                        print(f"Ошибка сохранения высокоточного PNG через SDK: {ret}")
                
                else:
                    """
                    Метод: Исходный (через QPixmap)
                    - Среднее время сохранения: ~0.2 сек
                    * Самый быстрый метод (в 5-15 раз быстрее SDK методов)
                    * Стабильная производительность (время всегда около 0.2 сек)
                    * Простая реализация
                    * Сохраняет только визуальное представление
                    * Точность ограничена разрешением экранного представления
                    - Рекомендации:
                    * Основной метод для продакшена
                    * Идеален для серийной съемки и работы в реальном времени
                    * Для точных температурных измерений дополнять сохранением .npy
                    """
                    pixmap = self.image_label.pixmap()
                    if pixmap is not None:
                        pixmap.save(img_filename)
                        saved_files.append(img_filename)
                        print(f"Сохранено PNG через QPixmap: {img_filename}")
                    else:
                        print("Нет изображения для сохранения")
            
            # Формируем сообщение о сохраненных файлах
            if saved_files:
                files_str = "\n".join(saved_files)
                print(f"Сохраненные файлы:\n{files_str}")
            else:
                print("Не выбраны типы данных для сохранения")
            
        except Exception as e:
            print(f"Ошибка сохранения данных: {e}")
    
    def init_camera(self, xml_path='generic.xml'):
        """Инициализирует камеру с указанным XML-файлом"""
        try:
            # Загрузка библиотеки
            self.libir = ct.CDLL('.\libirimager.dll')
            
            # Определение типов аргументов
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
            
            # Функции палитры и калибровки
            self.libir.evo_irimager_set_palette.argtypes = [ct.c_int]
            self.libir.evo_irimager_set_palette.restype = ct.c_int
            
            self.libir.evo_irimager_set_shutter_mode.argtypes = [ct.c_int]
            self.libir.evo_irimager_set_shutter_mode.restype = ct.c_int
            
            self.libir.evo_irimager_trigger_shutter_flag.argtypes = []
            self.libir.evo_irimager_trigger_shutter_flag.restype = ct.c_int
            
            # Функции сохранения PNG
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
            
            # Инициализация камеры
            pathXml = xml_path.encode('utf-8')
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
                f"Разрешение: {self.thermal_width.value}x{self.thermal_height.value} (Thermal)\n"
                f"Палитра: {self.palette_width.value}x{self.palette_height.value} (RGB)"
            )
            
            # Буферы для данных
            self.np_thermal = np.zeros([self.thermal_width.value * self.thermal_height.value], dtype=np.uint16)
            self.np_img = np.zeros([self.palette_width.value * self.palette_height.value * 3], dtype=np.uint8)
            self.metadata = EvoIRFrameMetadata()
            
            # Установка начальной палитры
            self.set_palette(self.palette_combo.currentText())
            
            # Установка начального режима затвора
            ret = self.libir.evo_irimager_set_shutter_mode(1)
            if ret != 0:
                print(f"Ошибка установки начального режима затвора: {ret}")
            
            return True
            
        except Exception as e:
            print(f"Ошибка инициализации: {e}")
            return False

    def deinit_camera(self):
        """Освобождает ресурсы камеры"""
        if hasattr(self, 'libir'):
            self.libir.evo_irimager_terminate()

    def set_palette(self, palette_name):
        """Устанавливает цветовую палитру для камеры"""
        if not hasattr(self, 'libir'):
            return
            
        # КОРРЕКТНАЯ КАРТА ПАЛИТР
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
        
        # Для неизвестных значений используем Iron (6)
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
            
            # Отображение в интерфейсе
            self.image_label.setPixmap(QPixmap.fromImage(qimg))
            
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
            
        if hasattr(self, 'libir'):
            self.libir.evo_irimager_terminate()
        super().closeEvent(event)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = ThermalCameraApp()
    window.show()
    sys.exit(app.exec())