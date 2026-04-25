"""
Модуль основного окна приложения для теплового неразрушающего контроля (View Layer)
"""
from PySide6.QtCore import Qt, QSize, Signal
from PySide6.QtWidgets import (
    QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
    QLabel, QPushButton, QProgressBar, QSizePolicy,
    QGraphicsView, QMessageBox, QStatusBar
)
from ui_fonts import TITLE_FONT, SUBTITLE_FONT
from ui_constants import BUTTON_SIZE, WINDOW_MARGINS, WINDOW_MAIN_MIN, STATUS_BAR_LABEL_SIZE

class MainWindow(QMainWindow):
    # Сигналы для Presenter
    start_requested = Signal()
    stop_requested = Signal()
    settings_requested = Signal()

    VIDEO_STYLE = """
        QGraphicsView {
            background-color: palette(base);
            border: 2px solid palette(dark);
            border-radius: 8px;
        }
    """

    def __init__(self, parent=None):
        super().__init__(parent)
        self._setup_window_properties()
        self._create_widgets()
        self._setup_layout()
        self._create_status_bar()
        self._connect_signals()

    def _setup_window_properties(self):
        self.setWindowTitle("TPU-TNDT-DualCam-App")
        self.setMinimumSize(WINDOW_MAIN_MIN)
        self.showMaximized()

    def _create_widgets(self):
        self._central_widget = QWidget()
        self.setCentralWidget(self._central_widget)
        
        self._main_layout = QVBoxLayout(self._central_widget)
        self._main_layout.setContentsMargins(*WINDOW_MARGINS)
        
        self._visible_label = QLabel("Камера видимого спектра")
        self._visible_label.setFont(TITLE_FONT)
        
        self.visible_video = QGraphicsView()
        self.visible_video.setMinimumSize(QSize(400, 300))
        self.visible_video.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        self.visible_video.setStyleSheet(self.VIDEO_STYLE)
        
        self._thermal_label = QLabel("Тепловизор")
        self._thermal_label.setFont(TITLE_FONT)
        
        self.thermal_video = QGraphicsView()
        self.thermal_video.setMinimumSize(QSize(400, 300))
        self.thermal_video.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        self.thermal_video.setStyleSheet(self.VIDEO_STYLE)
        
        self._process_status_label = QLabel("Готов к началу")
        self._process_status_label.setFont(SUBTITLE_FONT)
        self._process_status_label.setAlignment(Qt.AlignLeft)
        
        self.progress_bar = QProgressBar()
        self.progress_bar.setRange(0, 100)
        self.progress_bar.setValue(0)
        self.progress_bar.setTextVisible(False)
        self.progress_bar.setMinimumHeight(20)
        
        self._play_button = QPushButton("Старт")
        self._play_button.setMinimumSize(BUTTON_SIZE)
        self._play_button.setDefault(True)
        
        self._stop_button = QPushButton("Стоп")
        self._stop_button.setMinimumSize(BUTTON_SIZE)
        self._stop_button.setEnabled(False)
        
        self._settings_button = QPushButton("Настройки")
        self._settings_button.setMinimumSize(BUTTON_SIZE)

    def _setup_layout(self):
        visible_layout = QVBoxLayout()
        visible_layout.addWidget(self._visible_label)
        visible_layout.addWidget(self.visible_video)
        
        thermal_layout = QVBoxLayout()
        thermal_layout.addWidget(self._thermal_label)
        thermal_layout.addWidget(self.thermal_video)
        
        cameras_layout = QHBoxLayout()
        cameras_layout.setSpacing(10)
        cameras_layout.addLayout(visible_layout)
        cameras_layout.addLayout(thermal_layout)
        
        buttons_layout = QHBoxLayout()
        buttons_layout.setSpacing(20)
        buttons_layout.addStretch()
        buttons_layout.addWidget(self._stop_button)
        buttons_layout.addWidget(self._play_button)
        buttons_layout.addStretch()
        
        settings_layout = QHBoxLayout()
        settings_layout.addStretch()
        settings_layout.addWidget(self._settings_button)
        
        self._main_layout.addLayout(cameras_layout)
        self._main_layout.addSpacing(60)
        self._main_layout.addWidget(self._process_status_label)
        self._main_layout.addWidget(self.progress_bar)
        self._main_layout.addLayout(buttons_layout)
        self._main_layout.addLayout(settings_layout)

    def _connect_signals(self):
        self._play_button.clicked.connect(self.start_requested.emit)
        self._stop_button.clicked.connect(self.stop_requested.emit)
        self._settings_button.clicked.connect(self.settings_requested.emit)

    def _create_status_bar(self):
        self.status_bar = QStatusBar()
        self.setStatusBar(self.status_bar)
        self.status_bar.setStyleSheet("QLabel { padding: 0 5px; }")
        
        self.lbl_position = QLabel("Координаты: (0, 0)")
        self.lbl_heater = QLabel("Нагреватель: выкл")
        self.lbl_cam_vis = QLabel("Камера: ожидание")
        self.lbl_fps_vis = QLabel("FPS: 0")
        self.lbl_cam_therm = QLabel("Тепл.: ожидание")
        self.lbl_fps_therm = QLabel("FPS: 0")
        self.lbl_recording = QLabel("Запись: выкл")
        self.lbl_disk = QLabel("Диск: вычисление...")

        for label in [self.lbl_position, self.lbl_heater, self.lbl_cam_vis, self.lbl_fps_vis, self.lbl_cam_therm, self.lbl_fps_therm, self.lbl_recording]:
            label.setFixedSize(STATUS_BAR_LABEL_SIZE)

        self.status_bar.addWidget(self.lbl_position)
        self.status_bar.addWidget(self.lbl_heater)
        self.status_bar.addWidget(self.lbl_cam_vis)
        self.status_bar.addWidget(self.lbl_fps_vis)
        self.status_bar.addWidget(self.lbl_cam_therm)
        self.status_bar.addWidget(self.lbl_fps_therm)

        self.status_bar.addPermanentWidget(self.lbl_recording)
        self.status_bar.addPermanentWidget(self.lbl_disk)

    def set_status(self, text: str):
        self._process_status_label.setText(text)

    def set_progress(self, value: int):
        self.progress_bar.setValue(value)

    def enable_start(self, enabled: bool):
        self._play_button.setEnabled(enabled)

    def enable_stop(self, enabled: bool):
        self._stop_button.setEnabled(enabled)

    def update_position_status(self, x: int, y: int):
        self.lbl_position.setText(f"Зона: ({x}, {y})")

    def update_heater_status(self, is_on: bool, has_error: bool = False):
        if has_error:
            self.lbl_heater.setText("Нагреватель: ошибка")
            self.lbl_heater.setStyleSheet("color: #e74c3c;")
        else:
            state = "вкл" if is_on else "выкл"
            color = "green" if is_on else "palette(window-text)"
            self.lbl_heater.setText(f"Нагреватель: {state}")
            self.lbl_heater.setStyleSheet(f"color: {color};")

    def update_recording_status(self, is_recording: bool):
        if is_recording:
            self.lbl_recording.setText("Запись: идет")
            self.lbl_recording.setStyleSheet("color: #e74c3c; font-weight: bold;")
        else:
            self.lbl_recording.setText("Запись: выкл")
            self.lbl_recording.setStyleSheet("color: palette(window-text);")

    def update_camera_telemetry(self, cam_type: str, status: str, fps: int = 0):
        if cam_type == 'visible':
            self.lbl_cam_vis.setText(f"Камера: {status}")
            self.lbl_fps_vis.setText(f"FPS: {fps}")
            if status != "ОК":
                self.lbl_cam_vis.setStyleSheet("color: #e74c3c;")
            else:
                self.lbl_cam_vis.setStyleSheet("color: palette(window-text);") 

        elif cam_type == 'thermal':
            self.lbl_cam_therm.setText(f"Тепл.: {status}")
            self.lbl_fps_therm.setText(f"FPS: {fps}")
            if status != "ОК":
                self.lbl_cam_therm.setStyleSheet("color: #e74c3c;")
            else:
                self.lbl_cam_therm.setStyleSheet("color: palette(window-text);")

    def update_disk_space(self, free_gb: float | None):
        if free_gb is None:
            self.lbl_disk.setText("Свободно: ошибка")
            return
        self.lbl_disk.setText(f"Свободно: {free_gb:.1f} ГБ")
        if free_gb < 5.0:
            self.lbl_disk.setStyleSheet("color: #e74c3c; font-weight: bold;")
        else:
            self.lbl_disk.setStyleSheet("color: palette(window-text);")

    def show_info(self, title: str, message: str):
        QMessageBox.information(self, title, message, QMessageBox.Ok)

    def show_error(self, title: str, message: str):
        QMessageBox.critical(self, title, message, QMessageBox.Ok)

    def closeEvent(self, event):
        event.accept()