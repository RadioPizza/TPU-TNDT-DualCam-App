"""
Модуль окна настроек приложения
"""

from PySide6.QtCore import Qt as QtCore
from PySide6.QtWidgets import (
    QMainWindow, QVBoxLayout, QHBoxLayout, QLabel, QPushButton, QFrame,
    QScrollArea, QWidget, QLineEdit, QComboBox, QFormLayout, 
    QGraphicsView, QGraphicsScene, QGraphicsRectItem, QApplication
)
from PySide6.QtGui import QIntValidator, QBrush, QColor, QPainter


class CameraGraphicsView(QGraphicsView):
    """
    Кастомный вид для отображения видео с камеры с поддержкой соотношения сторон
    
    Attributes:
        aspect_ratio (float): Соотношение сторон (ширина/высота) для поддержки
    """
    
    def __init__(self, aspect_ratio, parent=None):
        """
        Инициализация вида камеры
        
        Args:
            aspect_ratio (float): Соотношение сторон для отображения
            parent (QWidget, optional): Родительский виджет. Defaults to None.
        """
        super().__init__(parent)
        self.aspect_ratio = aspect_ratio
        self._setup_view()
        
    def _setup_view(self):
        """Настройка параметров отображения вида"""
        self.setScene(QGraphicsScene(self))
        self.setRenderHint(QPainter.Antialiasing)
        self.setRenderHint(QPainter.SmoothPixmapTransform)
        self.setHorizontalScrollBarPolicy(QtCore.ScrollBarAlwaysOff)
        self.setVerticalScrollBarPolicy(QtCore.ScrollBarAlwaysOff)
        self.setFrameShape(QFrame.NoFrame)
        
    def resizeEvent(self, event):
        """
        Обработчик изменения размера вида для поддержки соотношения сторон
        
        Args:
            event (QResizeEvent): Событие изменения размера
        """
        super().resizeEvent(event)
        # Поддерживаем соотношение сторон при изменении размера
        if self.scene() and self.scene().items():
            self.fitInView(self.scene().itemsBoundingRect(), QtCore.KeepAspectRatio)


class SettingsWindow(QMainWindow):
    """
    Окно настроек приложения
    
    Предоставляет интерфейс для настройки параметров контроля, камер, 
    тепловизора, нагревателя и интерфейса
    """
    
    def __init__(self):
        """Инициализация окна настроек"""
        super().__init__()
        self._setup_window_properties()
        self._setup_ui()
        self.showMaximized()

        
    def _setup_window_properties(self):
        """Настройка основных параметров окна"""
        self.setWindowTitle("Настройки")
        self.setMinimumSize(1050, 600)

    def _setup_ui(self):
        """Основная настройка пользовательского интерфейса"""
        # Центральный виджет для QMainWindow
        central_widget = QWidget()
        self.setCentralWidget(central_widget)

        # Главный layout окна
        main_layout = QVBoxLayout(central_widget)
        main_layout.setContentsMargins(20, 20, 20, 20)
        main_layout.setSpacing(20)
        
        # Создание и добавление элементов интерфейса
        header_layout = self._create_header()
        main_layout.addLayout(header_layout)
        
        scroll_area = self._create_scroll_area()
        main_layout.addWidget(scroll_area)

        
    def _create_header(self):
        """
        Создание заголовка окна с кнопкой возврата
        
        Returns:
            QHBoxLayout: Layout заголовка
        """
        layout = QHBoxLayout()
        
        title = QLabel("Настройки")
        title.setObjectName("StartTitle")
        
        home_btn = QPushButton("На главную")
        home_btn.setObjectName("SettingsHomeButton")
        home_btn.setFixedSize(120, 40)
        home_btn.clicked.connect(self.close)
        
        layout.addWidget(title)
        layout.addStretch()
        layout.addWidget(home_btn)
        
        return layout
        
    def _create_scroll_area(self):
        """
        Создание области прокрутки для настроек
        
        Returns:
            QScrollArea: Область прокрутки с содержимым настроек
        """
        scroll_area = QScrollArea()
        scroll_area.setWidgetResizable(True)
        scroll_area.setFrameShape(QFrame.NoFrame)
        
        # Контейнер для центрирования содержимого
        center_widget = QWidget()
        center_layout = QHBoxLayout(center_widget)
        center_layout.setContentsMargins(0, 0, 0, 0)
        
        content_widget = QWidget()
        self.content_layout = QVBoxLayout(content_widget)
        self.content_layout.setAlignment(QtCore.AlignTop)
        self.content_layout.setSpacing(25)
        
        # Создание секций настроек
        self._create_testing_section()
        self._create_camera_section()
        self._create_thermal_camera_section()
        self._create_heater_section()
        self._create_interface_section()
        
        # Центрирование содержимого
        center_layout.addStretch()
        center_layout.addWidget(content_widget)
        center_layout.addStretch()
        
        scroll_area.setWidget(center_widget)
        return scroll_area
        
    def _create_testing_section(self):
        """Создание секции настроек контроля"""
        frame = QFrame()
        frame.setObjectName("SettingsTestingFrame")
        frame.setMaximumWidth(1000)
        layout = QVBoxLayout(frame)
        layout.setContentsMargins(15, 15, 15, 15)
        layout.setSpacing(10)
        
        title = QLabel("Настройки контроля")
        title.setObjectName("MainProcessLabel")
        layout.addWidget(title)
        
        content_widget = self._create_testing_content()
        layout.addWidget(content_widget)
        self.content_layout.addWidget(frame)
        
    def _create_testing_content(self):
        """
        Создание содержимого секции контроля
        
        Returns:
            QWidget: Виджет с настройками контроля
        """
        content_widget = QWidget()
        content_layout = QVBoxLayout(content_widget)
        content_layout.setSpacing(15)
        
        # Длительность нагрева
        heating_widget = self._create_heating_duration_widget()
        content_layout.addWidget(heating_widget)
        
        # Длительность контроля
        testing_widget = self._create_testing_duration_widget()
        content_layout.addWidget(testing_widget)
        
        # Частота записи
        fps_widget = self._create_recording_fps_widget()
        content_layout.addWidget(fps_widget)
        
        return content_widget
        
    def _create_heating_duration_widget(self):
        """
        Создание виджета для настройки длительности нагрева
        
        Returns:
            QWidget: Виджет настройки нагрева
        """
        widget = QWidget()
        layout = QHBoxLayout(widget)
        layout.setContentsMargins(0, 0, 0, 0)
        
        label = QLabel("Длительность нагрева:")
        label.setObjectName("SettingsHeatingDurationLabel")
        
        edit = QLineEdit()
        edit.setObjectName("SettingsHeatingDurationEdit")
        edit.setFixedWidth(80)
        edit.setText("60")
        edit.setValidator(QIntValidator(0, 300))
        
        unit = QLabel("секунд")
        unit.setObjectName("SettingsHeatingDurationUnit")
        
        layout.addWidget(label)
        layout.addWidget(edit)
        layout.addWidget(unit)
        layout.addStretch()
        
        return widget
        
    def _create_testing_duration_widget(self):
        """
        Создание виджета для настройки длительности контроля
        
        Returns:
            QWidget: Виджет настройки контроля
        """
        widget = QWidget()
        layout = QHBoxLayout(widget)
        layout.setContentsMargins(0, 0, 0, 0)
        
        label = QLabel("Длительность контроля:")
        label.setObjectName("SettingsTestingDurationLabel")
        
        edit = QLineEdit()
        edit.setObjectName("SettingsTestingDurationEdit")
        edit.setFixedWidth(80)
        edit.setText("120")
        edit.setValidator(QIntValidator(0, 600))
        
        unit = QLabel("секунд")
        unit.setObjectName("SettingsTestingDurationUnit")
        
        layout.addWidget(label)
        layout.addWidget(edit)
        layout.addWidget(unit)
        layout.addStretch()
        
        return widget
        
    def _create_recording_fps_widget(self):
        """
        Создание виджета для настройки частоты записи
        
        Returns:
            QWidget: Виджет настройки FPS
        """
        widget = QWidget()
        layout = QHBoxLayout(widget)
        layout.setContentsMargins(0, 0, 0, 0)
        
        label = QLabel("Частота записи:")
        label.setObjectName("SettingsRecordFPSLabel")
        
        combo = QComboBox()
        combo.setObjectName("SettingsRecordFPSComboBox")
        combo.addItems(["30 FPS", "25 FPS", "15 FPS", "10 FPS"])
        
        layout.addWidget(label)
        layout.addWidget(combo)
        layout.addStretch()
        
        return widget
        
    def _create_camera_section(self):
        """Создание секции настроек камеры"""
        frame = QFrame()
        frame.setObjectName("SettingsCamFrame")
        frame.setMaximumWidth(1000)
        layout = QVBoxLayout(frame)
        layout.setContentsMargins(15, 15, 15, 15)
        layout.setSpacing(10)
        
        title = QLabel("Настройки камеры")
        title.setObjectName("MainCameraTitle")
        layout.addWidget(title)
        
        content_widget = self._create_camera_content()
        layout.addWidget(content_widget)
        self.content_layout.addWidget(frame)
        
    def _create_camera_content(self):
        """
        Создание содержимого секции камеры
        
        Returns:
            QWidget: Виджет с настройками камеры
        """
        content_widget = QWidget()
        content_layout = QHBoxLayout(content_widget)
        content_layout.setContentsMargins(0, 0, 0, 0)
        
        # Левая часть - предпросмотр камеры
        view_widget = self._create_camera_preview()
        content_layout.addWidget(view_widget, 2)
        content_layout.addSpacing(20)
        
        # Правая часть - управление камерой
        control_widget = self._create_camera_controls()
        content_layout.addWidget(control_widget, 1)
        
        return content_widget
        
    def _create_camera_preview(self):
        """
        Создание виджета предпросмотра камеры
        
        Returns:
            QWidget: Виджет предпросмотра
        """
        widget = QWidget()
        layout = QVBoxLayout(widget)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setAlignment(QtCore.AlignCenter)
        
        # Видимая камера с соотношением сторон 1.33 (640/480)
        cam_view = CameraGraphicsView(640/480)
        cam_view.setObjectName("SettingsCamView")
        cam_view.setMinimumSize(320, 240)
        cam_view.setMaximumSize(640, 480)
        
        # Тестовый прямоугольник для демонстрации
        self._add_test_rectangle(cam_view, QColor(200, 200, 255))
        
        label = QLabel("Предпросмотр камеры (1936×1464)")
        label.setObjectName("SettingsCamLabel")
        label.setAlignment(QtCore.AlignCenter)
        
        layout.addWidget(cam_view)
        layout.addWidget(label)
        
        return widget
        
    def _create_camera_controls(self):
        """
        Создание элементов управления камерой
        
        Returns:
            QWidget: Виджет управления камерой
        """
        widget = QWidget()
        layout = QFormLayout(widget)
        layout.setContentsMargins(0, 40, 0, 0)
        layout.setVerticalSpacing(15)
        layout.setHorizontalSpacing(20)
        
        # Разрешение
        res_label = QLabel("Разрешение:")
        res_label.setObjectName("SettingsCamResLabel")
        res_combo = QComboBox()
        res_combo.setObjectName("SettingsCamResComboBox")
        res_combo.addItems(["1936x1464", "1280x720", "640x480"])
        
        # Частота кадров
        fps_label = QLabel("Частота кадров:")
        fps_label.setObjectName("SettingsCamFPSLabel")
        fps_combo = QComboBox()
        fps_combo.setObjectName("SettingsCamFPSComboBox")
        fps_combo.addItems(["30 FPS", "60 FPS", "120 FPS"])
        
        # Выбор камеры
        cam_combo = QComboBox()
        cam_combo.setObjectName("SettingsCamComboBox")
        cam_combo.addItems(["Камера 1", "Камера 2", "Камера 3"])
        
        # Кнопка подключения
        connect_btn = QPushButton("Подключить")
        connect_btn.setObjectName("SettingsCamConnectButton")
        connect_btn.setFixedSize(200*3+10, 35)
        
        layout.addRow(res_label, res_combo)
        layout.addRow(fps_label, fps_combo)
        layout.addRow(QLabel("Камера:"), cam_combo)
        layout.addRow(connect_btn)
        
        return widget
        
    def _create_thermal_camera_section(self):
        """Создание секции настроек тепловизора"""
        frame = QFrame()
        frame.setObjectName("SettingsTCamFrame")
        frame.setMaximumWidth(1000)
        layout = QVBoxLayout(frame)
        layout.setContentsMargins(15, 15, 15, 15)
        layout.setSpacing(10)
        
        title = QLabel("Настройки тепловизора")
        title.setObjectName("MainTCameraTitle")
        layout.addWidget(title)
        
        content_widget = self._create_thermal_camera_content()
        layout.addWidget(content_widget)
        self.content_layout.addWidget(frame)
        
    def _create_thermal_camera_content(self):
        """
        Создание содержимого секции тепловизора
        
        Returns:
            QWidget: Виджет с настройками тепловизора
        """
        content_widget = QWidget()
        content_layout = QHBoxLayout(content_widget)
        content_layout.setContentsMargins(0, 0, 0, 0)
        
        # Левая часть - предпросмотр тепловизора
        view_widget = self._create_thermal_camera_preview()
        content_layout.addWidget(view_widget, 2)
        content_layout.addSpacing(20)
        
        # Правая часть - управление тепловизором
        control_widget = self._create_thermal_camera_controls()
        content_layout.addWidget(control_widget, 1)
        
        return content_widget
        
    def _create_thermal_camera_preview(self):
        """
        Создание виджета предпросмотра тепловизора
        
        Returns:
            QWidget: Виджет предпросмотра тепловизора
        """
        widget = QWidget()
        layout = QVBoxLayout(widget)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setAlignment(QtCore.AlignCenter)
        
        # Тепловизор с соотношением сторон 1.33
        tcam_view = CameraGraphicsView(640/480)
        tcam_view.setObjectName("SettingsTCamView")
        tcam_view.setMinimumSize(320, 240)
        tcam_view.setMaximumSize(640, 480)
        
        # Тестовый прямоугольник для демонстрации
        self._add_test_rectangle(tcam_view, QColor(255, 200, 200))
        
        label = QLabel("Предпросмотр тепловизора (640×480)")
        label.setObjectName("SettingsTCamLabel")
        label.setAlignment(QtCore.AlignCenter)
        
        layout.addWidget(tcam_view)
        layout.addWidget(label)
        
        return widget
        
    def _create_thermal_camera_controls(self):
        """
        Создание элементов управления тепловизором
        
        Returns:
            QWidget: Виджет управления тепловизором
        """
        widget = QWidget()
        layout = QFormLayout(widget)
        layout.setContentsMargins(0, 40, 0, 0)
        layout.setVerticalSpacing(15)
        layout.setHorizontalSpacing(20)
        
        # Разрешение
        res_label = QLabel("Разрешение:")
        res_label.setObjectName("SettingsTCamResLabel")
        res_combo = QComboBox()
        res_combo.setObjectName("SettingsTCamResComboBox")
        res_combo.addItems(["640x480", "320x240", "160x120"])
        
        # Частота кадров
        fps_label = QLabel("Частота кадров:")
        fps_label.setObjectName("SettingsTCamFPSLabel")
        fps_combo = QComboBox()
        fps_combo.setObjectName("SettingsTCamFPSComboBox")
        fps_combo.addItems(["30 FPS", "15 FPS", "9 FPS"])
        
        # Выбор тепловизора
        tcam_combo = QComboBox()
        tcam_combo.setObjectName("SettingsTCamComboBox")
        tcam_combo.addItems(["Тепловизор 1", "Тепловизор 2"])
        
        # Кнопки управления
        buttons_widget = self._create_thermal_camera_buttons()
        layout.addRow(res_label, res_combo)
        layout.addRow(fps_label, fps_combo)
        layout.addRow(QLabel("Тепловизор:"), tcam_combo)
        layout.addRow(buttons_widget)
        
        return widget
        
    def _create_thermal_camera_buttons(self):
        """
        Создание кнопок управления тепловизором
        
        Returns:
            QWidget: Виджет с кнопками управления
        """
        widget = QWidget()
        layout = QHBoxLayout(widget)
        
        connect_btn = QPushButton("Подключить")
        connect_btn.setObjectName("SettingsTCamConnectButton")
        connect_btn.setFixedSize(200, 35)
        
        cal_btn = QPushButton("Калибровка")
        cal_btn.setObjectName("SettingsTCamCalibrationButton")
        cal_btn.setFixedSize(200, 35)
        
        focus_btn = QPushButton("Фокус")
        focus_btn.setObjectName("SettingsTCamFocusButton")
        focus_btn.setFixedSize(200, 35)
        
        layout.addWidget(connect_btn)
        layout.addWidget(cal_btn)
        layout.addWidget(focus_btn)
        
        return widget
        
    def _create_interface_section(self):
        """Создание секции настроек интерфейса"""
        frame = QFrame()
        frame.setObjectName("SettingsUIFrame")
        frame.setMaximumWidth(1000)
        layout = QVBoxLayout(frame)
        layout.setContentsMargins(15, 15, 15, 15)
        layout.setSpacing(10)

        title = QLabel("Настройки интерфейса")
        title.setObjectName("MainProcessLabel")
        layout.addWidget(title)
        
        content_widget = self._create_interface_content()
        layout.addWidget(content_widget)
        self.content_layout.addWidget(frame)
        
    def _create_interface_content(self):
        """
        Создание содержимого секции интерфейса
        
        Returns:
            QWidget: Виджет с настройками интерфейса
        """
        widget = QWidget()
        layout = QFormLayout(widget)
        layout.setVerticalSpacing(15)
        layout.setHorizontalSpacing(20)
        
        # Настройка темы
        theme_label = QLabel("Тема оформления:")
        theme_label.setObjectName("SettingsThemeLabel")
        theme_combo = QComboBox()
        theme_combo.setObjectName("SettingsThemeComboBox")
        theme_combo.addItems(["Светлая", "Темная", "Системная"])
        
        # Настройка языка
        lang_label = QLabel("Язык интерфейса:")
        lang_label.setObjectName("SettingsLangLabel")
        lang_combo = QComboBox()
        lang_combo.setObjectName("SettingsLangComboBox")
        lang_combo.addItems(["Русский", "English"])
        
        layout.addRow(theme_label, theme_combo)
        layout.addRow(lang_label, lang_combo)
        
        return widget
        
    def _create_heater_section(self):
        """Создание секции тестирования нагревателя"""
        frame = QFrame()
        frame.setObjectName("SettingsHeaterFrame")
        frame.setMaximumWidth(1000)
        layout = QVBoxLayout(frame)
        layout.setContentsMargins(15, 15, 15, 15)
        layout.setSpacing(10)
        
        title = QLabel("Тестирование нагревателя")
        title.setObjectName("SettingsHeaterLabel")
        layout.addWidget(title)
        
        content_widget = self._create_heater_controls()
        layout.addWidget(content_widget)
        self.content_layout.addWidget(frame)
    
    def _create_heater_controls(self):
        """
        Создание элементов управления нагревателем
        
        Returns:
            QWidget: Виджет с кнопками управления нагревателем
        """
        widget = QWidget()
        layout = QHBoxLayout(widget)
        layout.setAlignment(QtCore.AlignCenter)
        
        heat_btn = QPushButton("Нагрев")
        heat_btn.setObjectName("SettingsHeatButton")
        heat_btn.setFixedSize(200, 50)
        heat_btn.clicked.connect(self._on_heat_clicked)
        
        stop_btn = QPushButton("Стоп")
        stop_btn.setObjectName("SettingsStopButton")
        stop_btn.setFixedSize(200, 50)
        stop_btn.clicked.connect(self._on_stop_clicked)
        
        layout.addWidget(heat_btn)
        layout.addSpacing(20)
        layout.addWidget(stop_btn)
        
        return widget
        
    def _add_test_rectangle(self, view, color):
        """
        Добавление тестового прямоугольника в сцену вида
        
        Args:
            view (CameraGraphicsView): Вид для добавления прямоугольника
            color (QColor): Цвет прямоугольника
        """
        test_rect = QGraphicsRectItem(0, 0, 640, 480)
        test_rect.setBrush(QBrush(color))
        view.scene().addItem(test_rect)
    
    def _on_heat_clicked(self):
        """Обработчик нажатия кнопки включения нагревателя"""
        # TODO: Реализовать логику включения нагревателя
        print("Heater ON")

    def _on_stop_clicked(self):
        """Обработчик нажатия кнопки выключения нагревателя"""
        # TODO: Реализовать логику выключения нагревателя  
        print("Heater OFF")
    
    def closeEvent(self, event):
        """
        Обработчик события закрытия окна
        
        Args:
            event (QCloseEvent): Событие закрытия окна
        """
        # TODO: Добавить логику сохранения настроек перед закрытием
        event.accept()

    @staticmethod
    def load_stylesheet(filename):
        """
        Загрузка CSS стилей из файла
        
        Args:
            filename (str): Путь к файлу со стилями
            
        Returns:
            str: Содержимое CSS файла
        """
        with open(filename, 'r', encoding='utf-8') as f:
            return f.read()


if __name__ == "__main__":
    app = QApplication([])
    
    # Загрузка стиля (раскомментировать при наличии файла стилей)
    # style = SettingsWindow.load_stylesheet('LightStyle.qss')
    # app.setStyleSheet(style)
    
    window = SettingsWindow()
    window.show()
    
    app.exec()