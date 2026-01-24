"""
Модуль диалогового окна выбора траектории для теплового контроля
Содержит класс TrajectoryDialog для выбора направления следующей зоны контроля
"""

from PySide6.QtCore import Qt, Signal, QSize
from PySide6.QtWidgets import (
    QDialog, QFrame, QLabel, QPushButton,
    QVBoxLayout, QHBoxLayout, QSizePolicy
)
from PySide6.QtGui import QFont, QIcon
import res_rs  # Импортируем ресурсы для иконок


class TrajectoryDialog(QDialog):
    """
    Диалоговое окно для выбора направления следующей зоны контроля
    
    Attributes:
        direction_selected (Signal[str]):   Сигнал с выбранным направлением
        retest_requested (Signal):          Сигнал запроса повторного контроля
        preview_requested (Signal):         Сигнал запроса предпросмотра
        finish_requested (Signal):          Сигнал запроса завершения
    """
    
    # Сигналы
    direction_selected = Signal(str)
    retest_requested = Signal()
    preview_requested = Signal()
    finish_requested = Signal()
    
    def __init__(self, parent=None):
        """
        Инициализация диалогового окна
        
        Args:
            parent (QWidget, optional): Родительский виджет
        """
        super().__init__(parent)
        
        # Флаг разрешения на закрытие
        self.allow_close = False
        
        self._setup_window_properties()
        self._create_widgets()
        self._setup_layout()
        self._connect_signals()
    
    def _setup_window_properties(self):
        """Настройка основных параметров окна"""
        self.setWindowTitle("Выбор траектории")
        self.setFixedSize(450, 450)
        self.setModal(True)
        self.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
    
    def _create_widgets(self):
        """Создание всех виджетов"""
        # Основной фрейм
        self._frame = QFrame()
        self._frame.setObjectName("TrajectoryFrame")
        self._frame.setMinimumSize(400, 400)
        self._frame.setFrameStyle(QFrame.StyledPanel | QFrame.Raised)
        
        # Основной заголовок (статус)
        self._title_label = QLabel("Контроль зоны завершён!")
        self._title_label.setObjectName("TrajectoryTitle")
        
        # Настройка шрифта для заголовка
        title_font = QFont()
        title_font.setPointSize(14)
        title_font.setWeight(QFont.Bold)
        self._title_label.setFont(title_font)
        self._title_label.setAlignment(Qt.AlignCenter)
        
        # Подзаголовок
        self._subtitle_label = QLabel("Выберите расположение следующей зоны контроля")
        self._subtitle_label.setObjectName("TrajectorySubtitle")
        
        # Настройка шрифта для подзаголовка
        subtitle_font = QFont()
        subtitle_font.setPointSize(10)
        self._subtitle_label.setFont(subtitle_font)
        self._subtitle_label.setAlignment(Qt.AlignCenter)
        
        # Кнопки направления
        self._left_button = QPushButton()
        self._left_button.setObjectName("TrajectoryLeftButton")
        self._left_button.setIcon(QIcon(":/icons/icons/arrow_left.svg"))
        self._left_button.setIconSize(QSize(50, 50))
        self._left_button.setFixedSize(80, 60)
        
        self._up_button = QPushButton()
        self._up_button.setObjectName("TrajectoryUpButton")
        self._up_button.setIcon(QIcon(":/icons/icons/arrow_up.svg"))
        self._up_button.setIconSize(QSize(50, 50))
        self._up_button.setFixedSize(80, 60)
        
        self._down_button = QPushButton()
        self._down_button.setObjectName("TrajectoryDownButton")
        self._down_button.setIcon(QIcon(":/icons/icons/arrow_down.svg"))
        self._down_button.setIconSize(QSize(50, 50))
        self._down_button.setFixedSize(80, 60)
        
        self._right_button = QPushButton()
        self._right_button.setObjectName("TrajectoryRightButton")
        self._right_button.setIcon(QIcon(":/icons/icons/arrow_right.svg"))
        self._right_button.setIconSize(QSize(50, 50))
        self._right_button.setFixedSize(80, 60)
        
        # Надпись
        self._action_label = QLabel("Либо выберите другое действие")
        self._action_label.setObjectName("TrajectoryActionLabel")
        
        # Настройка шрифта для надписи действия
        action_font = QFont()
        action_font.setPointSize(10)
        action_font.setWeight(QFont.Medium)
        self._action_label.setFont(action_font)
        self._action_label.setAlignment(Qt.AlignCenter)
        
        # Кнопка предпросмотра
        self._preview_button = QPushButton("Предпросмотр результата")
        self._preview_button.setObjectName("TrajectoryPreviewButton")
        self._preview_button.setFixedSize(336, 40)
        
        # Кнопка повторения
        self._repeat_button = QPushButton("Повторить последнюю зону")
        self._repeat_button.setObjectName("TrajectoryRepeatButton")
        self._repeat_button.setFixedSize(336, 40)
        
        # Кнопка завершения
        self._finish_button = QPushButton("Завершить контроль")
        self._finish_button.setObjectName("TrajectoryFinishButton")
        self._finish_button.setFixedSize(336, 40)
    
    def _setup_layout(self):
        """Настройка компоновки элементов интерфейса"""
        # Основной layout окна
        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(25, 25, 25, 25)
        main_layout.setSpacing(0)
        
        # Layout фрейма
        frame_layout = QVBoxLayout(self._frame)
        frame_layout.setContentsMargins(32, 30, 32, 30)
        frame_layout.setSpacing(10)
        
        # Добавляем заголовки
        frame_layout.addWidget(self._title_label)
        frame_layout.addSpacing(20)  # Отступ после заголовка
        
        # Добавляем подзаголовок
        frame_layout.addWidget(self._subtitle_label)
        frame_layout.addSpacing(0)
        
        
        # Layout для кнопок направления
        direction_layout = QHBoxLayout()
        direction_layout.setSpacing(8)
        direction_layout.setAlignment(Qt.AlignCenter)
        
        direction_layout.addWidget(self._left_button)
        direction_layout.addWidget(self._up_button)
        direction_layout.addWidget(self._down_button)
        direction_layout.addWidget(self._right_button)
        
        frame_layout.addLayout(direction_layout)
        frame_layout.addSpacing(20)  # Отступ после кнопок направления
        
        # Добавляем надпись "Либо выберите другое действие"
        frame_layout.addWidget(self._action_label)
        frame_layout.addSpacing(0)
        
        # Группируем основные кнопки в отдельный контейнер
        buttons_container = QVBoxLayout()
        buttons_container.setSpacing(8)
        buttons_container.setAlignment(Qt.AlignCenter)
        
        buttons_container.addWidget(self._preview_button)
        buttons_container.addWidget(self._repeat_button)
        buttons_container.addWidget(self._finish_button)
        
        frame_layout.addLayout(buttons_container)
        
        # Добавляем растягивающий элемент
        frame_layout.addStretch()
        
        main_layout.addWidget(self._frame)
    
    def _connect_signals(self):
        """Подключение сигналов к слотам"""
        # Подключаем кнопки направления
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
        
        # Подключаем остальные кнопки
        self._preview_button.clicked.connect(self.preview_requested.emit)
        self._repeat_button.clicked.connect(self.retest_requested.emit)
        self._finish_button.clicked.connect(self.finish_requested.emit)
    
    def closeEvent(self, event):
        """
        Переопределяем событие закрытия окна
        
        Args:
            event: Событие закрытия
        """
        if self.allow_close:
            event.accept()
        else:
            event.ignore()


if __name__ == "__main__":
    """Тестирование диалогового окна"""
    from PySide6.QtWidgets import QApplication
    import sys
    
    app = QApplication(sys.argv)
    
    # Тестовый вызов
    dialog = TrajectoryDialog()
    
    # Подключение сигналов для тестирования
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
    
    # Разрешаем закрытие для тестирования
    dialog.allow_close = True
    
    # Показ диалога
    result = dialog.exec()
    print(f"Диалог закрыт с кодом: {result}")
    
    sys.exit(app.exec())