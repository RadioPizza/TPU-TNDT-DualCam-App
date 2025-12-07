# -*- coding: utf-8 -*-

from PySide6.QtCore import Signal, QSize
from PySide6.QtWidgets import (
    QDialog, QFrame, QLabel, QPushButton, 
    QVBoxLayout, QHBoxLayout, QSizePolicy
)
from PySide6.QtCore import Qt
from PySide6.QtGui import QFont


class RetestDialog(QDialog):
    """
    Диалоговое окно для подтверждения повторного тестирования зоны.
    Наследуется от QDialog и использует ручную разметку.
    
    Args:
        zone_number (int): Номер текущей зоны для отображения в заголовке
        parent (QWidget): Родительский виджет
    """
    
    # Сигналы для обработки ответов пользователя
    yes_clicked = Signal()
    no_clicked = Signal()
    
    def __init__(self, zone_number=1, parent=None):
        super().__init__(parent)
        
        self._zone_number = zone_number
        self._setup_window()
        self._create_widgets()
        self._setup_layout()
        self._connect_signals()
    
    def _setup_window(self):
        """Настройка основных параметров окна."""
        self.setWindowTitle("Retesting the zone")
        self.setFixedSize(450, 250)
        self.setModal(True)
        self.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        
        # Центрируем окно относительно родителя
        if self.parent():
            parent_geometry = self.parent().geometry()
            self.move(
                parent_geometry.center() - self.rect().center()
            )
    
    def _create_widgets(self):
        """Создание виджетов."""
        # Основной фрейм
        self.frame = QFrame()
        self.frame.setObjectName("RetestFrame")
        self.frame.setMinimumSize(400, 200)
        self.frame.setFrameStyle(QFrame.StyledPanel | QFrame.Raised)
        
        # Заголовок с номером зоны
        self.title_label = QLabel()
        self.title_label.setObjectName("RetestTitle")
        self.title_label.setMinimumSize(336, 80)
        self.title_label.setAlignment(Qt.AlignLeft | Qt.AlignTop)
        self.title_label.setWordWrap(True)
        self._update_title_text()
        
        # Кнопки
        self.no_button = QPushButton("No")
        self.no_button.setObjectName("RetestNoButton")
        self.no_button.setMinimumSize(120, 40)
        self.no_button.setSizePolicy(
            QSizePolicy.Fixed, QSizePolicy.Fixed
        )
        
        self.yes_button = QPushButton("Yes")
        self.yes_button.setObjectName("RetestYesButton")
        self.yes_button.setMinimumSize(120, 40)
        self.yes_button.setSizePolicy(
            QSizePolicy.Fixed, QSizePolicy.Fixed
        )
    
    def _update_title_text(self):
        """Обновление текста заголовка с номером зоны."""
        html_text = f"""
        <html>
        <head/>
        <body>
            <p>
                <span style="font-size:24px; font-weight:600; color:#252525;">
                    Zone № {self._zone_number}<br/>
                </span>
                <br/>
                <span style="font-size:14px; color:#252525;">
                    Would you like to repeat testing of this zone?<br/>
                </span>
            </p>
        </body>
        </html>
        """
        self.title_label.setText(html_text)
    
    def _setup_layout(self):
        """Настройка компоновки."""
        # Основной layout окна
        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(25, 25, 25, 25)
        main_layout.setSpacing(0)
        
        # Layout фрейма
        frame_layout = QVBoxLayout(self.frame)
        frame_layout.setContentsMargins(32, 40, 32, 40)
        frame_layout.setSpacing(30)
        
        # Добавляем заголовок
        frame_layout.addWidget(self.title_label)
        
        # Добавляем отступ
        frame_layout.addStretch()
        
        # Layout для кнопок
        buttons_layout = QHBoxLayout()
        buttons_layout.setSpacing(32)
        
        # Добавляем кнопки с отступами
        buttons_layout.addWidget(self.no_button)
        buttons_layout.addStretch()
        buttons_layout.addWidget(self.yes_button)
        
        # Добавляем layout кнопок в frame
        frame_layout.addLayout(buttons_layout)
        
        # Добавляем frame в основной layout
        main_layout.addWidget(self.frame)
    
    def _connect_signals(self):
        """Подключение обработчиков сигналов."""
        self.no_button.clicked.connect(self._on_no_clicked)
        self.yes_button.clicked.connect(self._on_yes_clicked)
    
    def _on_no_clicked(self):
        """Обработчик нажатия кнопки 'Нет'."""
        self.no_clicked.emit()
        self.accept()
    
    def _on_yes_clicked(self):
        """Обработчик нажатия кнопки 'Да'."""
        self.yes_clicked.emit()
        self.accept()
    
    def set_zone_number(self, zone_number):
        """
        Установка номера зоны для отображения.
        
        Args:
            zone_number (int): Номер зоны
        """
        self._zone_number = zone_number
        self._update_title_text()
    
    def get_zone_number(self):
        """
        Получение текущего номера зоны.
        
        Returns:
            int: Номер зоны
        """
        return self._zone_number
    
    def keyPressEvent(self, event):
        """
        Обработка нажатий клавиш.
        
        Args:
            event (QKeyEvent): Событие нажатия клавиши
        """
        # Закрытие окна по Escape
        if event.key() == Qt.Key_Escape:
            self.reject()
        # Обработка Enter/Return как "Да"
        elif event.key() in (Qt.Key_Return, Qt.Key_Enter):
            self._on_yes_clicked()
        else:
            super().keyPressEvent(event)


# Для обратной совместимости можно оставить алиас
Ui_RetestDialog = RetestDialog


if __name__ == "__main__":
    """Тестирование диалога."""
    from PySide6.QtWidgets import QApplication
    import sys
    
    app = QApplication(sys.argv)
    
    # Тестовый вызов
    dialog = RetestDialog(zone_number=5)
    
    # Подключаем сигналы для тестирования
    dialog.yes_clicked.connect(lambda: print("Yes"))
    dialog.no_clicked.connect(lambda: print("No"))
    
    # Показываем диалог
    result = dialog.exec()
    print(f"Диалог закрыт с кодом: {result}")
    
    sys.exit(app.exec())