"""
Модуль диалогового окна для выбора направления следующей зоны теплового контроля
"""

from PySide6.QtCore import Qt, Signal, QSize
from PySide6.QtWidgets import (
    QDialog, QFrame, QLabel, QPushButton,
    QVBoxLayout, QHBoxLayout, QSizePolicy
)
from PySide6.QtGui import QFont, QIcon
import res_rs


class TrajectoryDialog(QDialog): 
    direction_selected = Signal(str)    # Сигнал с выбранным направлением
    retest_requested = Signal()         # Сигнал запроса повторного контроля
    preview_requested = Signal()        # Сигнал запроса предпросмотра
    finish_requested = Signal()         # Сигнал запроса завершения
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.allow_close_flag = False
        self._setup_window_properties()
        self._create_widgets()
        self._setup_layout()
        self._connect_signals()
    
    def _setup_window_properties(self):
        self.setModal(True)
        self.setWindowTitle("Выбор траектории")
        self.setFixedSize(450, 450)
        self.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
    
    def _create_widgets(self):
        title_font = QFont("Segoe UI")
        title_font.setPointSize(16)
        title_font.setWeight(QFont.DemiBold)
        
        subtitle_font = QFont("Segoe UI")
        subtitle_font.setPointSize(10)
        subtitle_font.setWeight(QFont.Normal)
        
        self._frame = QFrame()
        self._frame.setMinimumSize(400, 400)
        self._frame.setFrameShape(QFrame.StyledPanel)
        
        self._title_label = QLabel("Контроль зоны завершён!")
        self._title_label.setFont(title_font)
        self._title_label.setAlignment(Qt.AlignCenter)
        
        self._subtitle_label = QLabel("Выберите расположение следующей зоны контроля")
        self._subtitle_label.setFont(subtitle_font)
        self._subtitle_label.setAlignment(Qt.AlignCenter)
        
        self._left_button = self._create_arrow_button('left')
        self._up_button = self._create_arrow_button('up')
        self._down_button = self._create_arrow_button('down')
        self._right_button = self._create_arrow_button('right')
        
        self._action_label = QLabel("Либо выберите другое действие")
        self._action_label.setFont(subtitle_font)
        self._action_label.setAlignment(Qt.AlignCenter)
        
        BUTTON_SIZE = QSize(336, 45)
        
        self._preview_button = QPushButton("Предпросмотр результата")
        self._preview_button.setFixedSize(BUTTON_SIZE)
        
        self._repeat_button = QPushButton("Повторить последнюю зону")
        self._repeat_button.setFixedSize(BUTTON_SIZE)
        
        self._finish_button = QPushButton("Завершить контроль")
        self._finish_button.setFixedSize(BUTTON_SIZE)
    
    def _create_arrow_button(self, direction):
        button = QPushButton()
        button.setIcon(QIcon(f":/icons/icons/arrow_{direction}.svg"))
        button.setIconSize(QSize(50, 50))
        button.setFixedSize(80, 60)
        return button
    
    def _setup_layout(self):
        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(30, 30, 30, 30)
        
        frame_layout = QVBoxLayout(self._frame)
        frame_layout.setContentsMargins(30, 30, 30, 30)
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
        self._left_button.clicked.connect(
            lambda: self.direction_selected.emit('left')
        )
        self._up_button.clicked.connect(
            lambda: self.direction_selected.emit('up')
        )
        self._down_button.clicked.connect(
            lambda: self.direction_selected.emit('down')
        )
        self._right_button.clicked.connect(
            lambda: self.direction_selected.emit('right')
        )

        self._preview_button.clicked.connect(self.preview_requested.emit)
        self._repeat_button.clicked.connect(self.retest_requested.emit)
        self._finish_button.clicked.connect(self.finish_requested.emit)
    
    def closeEvent(self, event):
        if self.allow_close_flag:
            event.accept()
        else:
            event.ignore()


if __name__ == "__main__":
    """Тестирование диалогового окна"""
    from PySide6.QtWidgets import QApplication
    import sys
    
    app = QApplication(sys.argv)
    
    dialog = TrajectoryDialog()
    
    dialog.direction_selected.connect(
        lambda direction: print(f"Выбрано направление: {direction}")
    )
    dialog.retest_requested.connect(
        lambda: print("Запрошен повторный контроль")
    )
    dialog.preview_requested.connect(
        lambda: print("Запрошен предпросмотр")
    )
    dialog.finish_requested.connect(
        lambda: print("Запрошено завершение")
    )
    
    dialog.allow_close_flag = True
    
    result = dialog.exec()
    print(f"Диалог закрыт с кодом: {result}")