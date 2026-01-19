"""
Модуль диалогового окна для подтверждения повторного контроля зоны
Содержит класс RetestDialog для взаимодействия с пользователем
"""

from PySide6.QtCore import Qt as QtCore, Signal
from PySide6.QtWidgets import (
    QDialog, QFrame, QLabel, QPushButton,
    QVBoxLayout, QHBoxLayout, QSizePolicy
)


class RetestDialog(QDialog):
    """
    Диалоговое окно для подтверждения или отмены повторного контроля зоны
    
    Attributes:
        yes_clicked (Signal): Сигнал при выборе "Да"
        no_clicked (Signal): Сигнал при выборе "Нет"
    """
    
    # Сигналы для обработки ответов пользователя
    yes_clicked = Signal()
    no_clicked = Signal()
    
    def __init__(self, zone_number="1,1", parent=None):
        """
        Инициализация диалогового окна
        
        Args:
            zone_number (str): Координаты зоны в формате "x,y"
            parent (QWidget, optional): Родительский виджет
        """
        super().__init__(parent)
        self._zone_number = zone_number  # Строка формата "x,y"
        
        self._setup_window_properties()
        self._create_widgets()
        self._setup_layout()
        self._connect_signals()
        
    def _setup_window_properties(self):
        """Настройка основных параметров окна"""
        self.setWindowTitle("Повторный контроль зоны")
        self.setFixedSize(500, 300)
        self.setModal(True)
        self.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        
        # Центрирование окна относительно родителя
        if self.parent():
            parent_geometry = self.parent().geometry()
            self.move(parent_geometry.center() - self.rect().center())
    
    def _create_widgets(self):
        """Создание виджетов диалогового окна"""
        # Основной фрейм
        self._frame = QFrame()
        self._frame.setObjectName("RetestFrame")
        self._frame.setMinimumSize(400, 200)
        self._frame.setFrameStyle(QFrame.StyledPanel | QFrame.Raised)
        
        # Заголовок с координатами зоны
        self._title_label = QLabel()
        self._title_label.setObjectName("RetestTitle")
        self._title_label.setMinimumSize(336, 80)
        self._title_label.setAlignment(QtCore.AlignLeft | QtCore.AlignTop)
        self._title_label.setWordWrap(True)
        self._update_title_text()
        
        # Кнопки
        self._no_button = QPushButton("Нет")
        self._no_button.setObjectName("RetestNoButton")
        self._no_button.setMinimumSize(120, 40)
        self._no_button.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        
        self._yes_button = QPushButton("Да")
        self._yes_button.setObjectName("RetestYesButton")
        self._yes_button.setMinimumSize(120, 40)
        self._yes_button.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
    
    def _update_title_text(self):
        """Обновление текста заголовка с координатами зоны"""
        # Форматируем координаты в математическом формате (x, y)
        if ',' in self._zone_number:
            try:
                x, y = self._zone_number.split(',')
                x = x.strip()
                y = y.strip()
                coordinates = f"({x}, {y})"
            except ValueError:
                coordinates = self._zone_number
        else:
            coordinates = self._zone_number
            
        html_text = f"""
        <html>
        <head/>
        <body>
            <p>
                <span style="font-size:24px; font-weight:600; color:#252525;">
                    Зона {coordinates}<br/>
                </span>
                <br/>
                <span style="font-size:14px; color:#252525;">
                    Вы хотите повторить контроль этой зоны? Старые данные текущей зоны будут удалены<br/>
                </span>
            </p>
        </body>
        </html>
        """
        self._title_label.setText(html_text)
    
    def _setup_layout(self):
        """Настройка компоновки элементов интерфейса"""
        # Основной layout окна
        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(25, 25, 25, 25)
        main_layout.setSpacing(0)
        
        # Layout фрейма
        frame_layout = QVBoxLayout(self._frame)
        frame_layout.setContentsMargins(32, 40, 32, 40)
        frame_layout.setSpacing(30)
        
        # Добавление заголовка
        frame_layout.addWidget(self._title_label)
        frame_layout.addStretch()
        
        # Layout для кнопок
        buttons_layout = QHBoxLayout()
        buttons_layout.setSpacing(32)
        
        buttons_layout.addWidget(self._no_button)
        buttons_layout.addStretch()
        buttons_layout.addWidget(self._yes_button)
        
        frame_layout.addLayout(buttons_layout)
        main_layout.addWidget(self._frame)
    
    def _connect_signals(self):
        """Подключение сигналов к слотам"""
        self._no_button.clicked.connect(self._on_no_clicked)
        self._yes_button.clicked.connect(self._on_yes_clicked)
    
    def _on_no_clicked(self):
        """Обработчик нажатия кнопки 'Нет'"""
        self.no_clicked.emit()
        self.accept()
    
    def _on_yes_clicked(self):
        """Обработчик нажатия кнопки 'Да'"""
        self.yes_clicked.emit()
        self.accept()
    
    def set_zone_number(self, zone_number):
        """
        Установка координат зоны для отображения
        
        Args:
            zone_number (str): Координаты зоны в формате "x,y"
        """
        self._zone_number = str(zone_number)
        self._update_title_text()
    
    def get_zone_number(self):
        """
        Получение текущих координат зоны
        
        Returns:
            str: Координаты зоны в формате "x,y"
        """
        return self._zone_number
    
    def keyPressEvent(self, event):
        """
        Обработка нажатий клавиш
        
        Args:
            event (QKeyEvent): Событие нажатия клавиши
        """
        # Закрытие окна по Escape
        if event.key() == QtCore.Key_Escape:
            self.reject()
        # Обработка Enter/Return как "Да"
        elif event.key() in (QtCore.Key_Return, QtCore.Key_Enter):
            self._on_yes_clicked()
        else:
            super().keyPressEvent(event)


if __name__ == "__main__":
    """Тестирование диалогового окна"""
    from PySide6.QtWidgets import QApplication
    import sys
    
    app = QApplication(sys.argv)
    
    # Тестовый вызов
    dialog = RetestDialog(zone_number="0,4")
    
    # Подключение сигналов для тестирования
    dialog.yes_clicked.connect(lambda: print("Выбрано: Да"))
    dialog.no_clicked.connect(lambda: print("Выбрано: Нет"))
    
    # Показ диалога
    result = dialog.exec()
    print(f"Диалог закрыт с кодом: {result}")
    
    sys.exit(app.exec())