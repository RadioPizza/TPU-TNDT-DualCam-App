"""
Модуль диалогового окна для выбора направления следующей зоны теплового контроля
"""

from PySide6.QtCore import Qt, Signal, QSize
from PySide6.QtWidgets import (
    QDialog, QFrame, QLabel, QPushButton,
    QVBoxLayout, QHBoxLayout, QSizePolicy,
    QApplication
)
from PySide6.QtGui import QIcon, QPalette
from ui_fonts import TITLE_FONT, SUBTITLE_FONT, FORM_LABEL_FONT
import res_rs
from ui_constants import WINDOW_MARGINS, BUTTON_SIZE, DIALOG_MEDIUM


def is_dark_theme():
    """Проверяет, используется ли тёмная тема"""
    app = QApplication.instance()
    if not app:
        return False
    
    bg_color = app.palette().color(QPalette.Window)
    
    # Определяем яркость цвета (0-255)
    # Формула для воспринимаемой яркости
    brightness = 0.299 * bg_color.red() + 0.587 * bg_color.green() + 0.114 * bg_color.blue()
    
    # Если фон темный (яркость < 128) - это тёмная тема
    return brightness < 128


class TrajectoryDialog(QDialog): 
    direction_selected = Signal(str)    # Сигнал с выбранным направлением
    retest_requested = Signal()         # Сигнал запроса повторного контроля
    preview_requested = Signal()        # Сигнал запроса предпросмотра
    finish_requested = Signal()         # Сигнал запроса завершения
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self._setup_window_properties()
        self._create_widgets()
        self._setup_layout()
        self._connect_signals()
    
    def _setup_window_properties(self):
        self.setModal(True)
        self.setWindowTitle("Выбор траектории")
        self.setFixedSize(DIALOG_MEDIUM)
        self.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        
        # Центрирование относительно родительского окна
        if self.parent():
            parent_geometry = self.parent().geometry()
            self.move(parent_geometry.center() - self.rect().center())
    
    def _create_widgets(self):
        self._frame = QFrame()
        self._frame.setMinimumSize(400, 400)
        self._frame.setFrameShape(QFrame.StyledPanel)
        
        self._title_label = QLabel("Контроль зоны завершён!")
        self._title_label.setFont(TITLE_FONT)
        self._title_label.setAlignment(Qt.AlignCenter)
        
        self._subtitle_label = QLabel("Выберите расположение следующей зоны контроля")
        self._subtitle_label.setFont(SUBTITLE_FONT)
        self._subtitle_label.setAlignment(Qt.AlignCenter)
        
        self._icon_suffix = "_black" if not is_dark_theme() else "_white"
        
        self._left_button = self._create_arrow_button('left')
        self._up_button = self._create_arrow_button('up')
        self._down_button = self._create_arrow_button('down')
        self._right_button = self._create_arrow_button('right')
        
        self._action_label = QLabel("Либо выберите другое действие")
        self._action_label.setFont(SUBTITLE_FONT)
        self._action_label.setAlignment(Qt.AlignCenter)
        
        self._preview_button = QPushButton("Предпросмотр результата")
        self._preview_button.setFixedSize(BUTTON_SIZE)
        
        self._repeat_button = QPushButton("Повторить последнюю зону")
        self._repeat_button.setFixedSize(BUTTON_SIZE)
        
        self._finish_button = QPushButton("Завершить контроль")
        self._finish_button.setFixedSize(BUTTON_SIZE)
    
    def _create_arrow_button(self, direction):
        button = QPushButton()
        # Используем соответствующий суффикс для иконки
        icon_path = f":/icons/icons/arrow_{direction}{self._icon_suffix}.svg"
        button.setIcon(QIcon(icon_path))
        button.setIconSize(QSize(50, 50))
        button.setFixedSize(80, 60)
        return button
    
    def _setup_layout(self):
        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(*WINDOW_MARGINS)
        
        frame_layout = QVBoxLayout(self._frame)
        frame_layout.setContentsMargins(*WINDOW_MARGINS)
        frame_layout.addWidget(self._title_label)
        frame_layout.addSpacing(20)
        frame_layout.addWidget(self._subtitle_label)
        frame_layout.addSpacing(0)
        
        direction_layout = QHBoxLayout()
        direction_layout.setSpacing(8)
        direction_layout.setAlignment(Qt.AlignCenter)
        
        direction_layout.addWidget(self._left_button)
        direction_layout.addWidget(self._up_button)
        direction_layout.addWidget(self._down_button)
        direction_layout.addWidget(self._right_button)
        
        frame_layout.addLayout(direction_layout)
        frame_layout.addSpacing(20)
        frame_layout.addWidget(self._action_label)
        frame_layout.addSpacing(0)
        
        buttons_container = QVBoxLayout()
        buttons_container.setSpacing(8)
        buttons_container.setAlignment(Qt.AlignCenter)
        buttons_container.addWidget(self._preview_button)
        buttons_container.addWidget(self._repeat_button)
        buttons_container.addWidget(self._finish_button)
        
        frame_layout.addLayout(buttons_container)
        frame_layout.addStretch()
        
        main_layout.addWidget(self._frame)
    
    def _connect_signals(self):
        self._left_button.clicked.connect(lambda: self._on_action_selected(self.direction_selected, 'left'))
        self._up_button.clicked.connect(lambda: self._on_action_selected(self.direction_selected, 'up'))
        self._down_button.clicked.connect(lambda: self._on_action_selected(self.direction_selected, 'down'))
        self._right_button.clicked.connect(lambda: self._on_action_selected(self.direction_selected, 'right'))

        self._preview_button.clicked.connect(lambda: self._on_action_selected(self.preview_requested))
        self._repeat_button.clicked.connect(lambda: self._on_action_selected(self.retest_requested))
        self._finish_button.clicked.connect(lambda: self._on_action_selected(self.finish_requested))
    
    def _on_action_selected(self, signal, payload=None):
        """Вспомогательный метод для отправки сигнала и немедленного закрытия окна"""
        if payload is not None:
            signal.emit(payload)
        else:
            signal.emit()
        self.accept()