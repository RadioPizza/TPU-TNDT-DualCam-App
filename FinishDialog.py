"""
Модуль финального диалогового окна для завершения теплового контроля
Содержит класс FinishDialog для подтверждения завершения сеанса контроля
"""

from PySide6.QtCore import Qt, Signal
from PySide6.QtWidgets import (
    QDialog, QFrame, QLabel, QPushButton, QLineEdit,
    QVBoxLayout, QHBoxLayout, QSizePolicy, QFileDialog, QMessageBox
)
from PySide6.QtGui import QFont


class FinishDialog(QDialog):
    """
    Диалоговое окно для подтверждения завершения теплового контроля
    
    Attributes:
        accepted (Signal): Сигнал при подтверждении завершения
        rejected (Signal): Сигнал при отмене завершения
    """
    
    # Сигналы для обработки ответов пользователя
    accepted = Signal()
    rejected = Signal()
    
    def __init__(self, parent=None):
        """
        Инициализация диалогового окна
        
        Args:
            parent (QWidget, optional): Родительский виджет
        """
        super().__init__(parent)
        
        self._setup_window_properties()
        self._create_widgets()
        self._setup_layout()
        self._connect_signals()
    
    def _setup_window_properties(self):
        """Настройка основных параметров окна"""
        self.setWindowTitle("Завершение теплового контроля")
        self.setFixedSize(450, 375)
        self.setModal(True)
        self.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
    
    def _create_widgets(self):
        """Создание виджетов диалогового окна"""
        # Основной фрейм
        self._frame = QFrame()
        self._frame.setObjectName("FinishFrame")
        self._frame.setMinimumSize(400, 325)
        self._frame.setFrameStyle(QFrame.StyledPanel | QFrame.Raised)
        
        # Основной заголовок
        self._title_label = QLabel("Завершить тепловой контроль?")
        self._title_label.setObjectName("FinishTitle")
        
        # Настройка шрифта для заголовка
        title_font = QFont()
        title_font.setPointSize(16)
        title_font.setWeight(QFont.Bold)
        self._title_label.setFont(title_font)
        self._title_label.setAlignment(Qt.AlignCenter)
        
        # Подзаголовок
        self._subtitle_label = QLabel("Проверьте путь сохранения")
        self._subtitle_label.setObjectName("FinishSubtitle")
        subtitle_font = QFont()
        subtitle_font.setPointSize(11)
        self._subtitle_label.setFont(subtitle_font)
        self._subtitle_label.setAlignment(Qt.AlignCenter)
        
        # Метка пути сохранения
        self._path_label = QLabel("Путь сохранения файлов")
        self._path_label.setObjectName("FinishPathLabel")
        self._path_label.setStyleSheet("font-weight: 500;")  # Полужирный
        
        # Поле пути сохранения (только для чтения)
        self._path_line_edit = QLineEdit()
        self._path_line_edit.setObjectName("FinishPathLineEdit")
        self._path_line_edit.setReadOnly(True)
        self._path_line_edit.setPlaceholderText("...")
        self._path_line_edit.setMinimumHeight(32)
        
        # Кнопка изменения пути
        self._change_path_button = QPushButton("Изменить путь")
        self._change_path_button.setObjectName("FinishChangePathButton")
        self._change_path_button.setFixedSize(96, 32)
        
        # Кнопки подтверждения/отмены
        self._yes_button = QPushButton("Да")
        self._yes_button.setObjectName("FinishYesButton")
        self._yes_button.setFixedSize(120, 40)
        
        self._no_button = QPushButton("Нет")
        self._no_button.setObjectName("FinishNoButton")
        self._no_button.setFixedSize(120, 40)
    
    def _setup_layout(self):
        """Настройка компоновки элементов интерфейса"""
        # Основной layout окна
        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(25, 25, 25, 25)
        main_layout.setSpacing(0)
        
        # Layout фрейма
        frame_layout = QVBoxLayout(self._frame)
        frame_layout.setContentsMargins(32, 30, 32, 30)
        frame_layout.setSpacing(25)
        
        # Добавление заголовков с отступами
        frame_layout.addWidget(self._title_label)
        frame_layout.addWidget(self._subtitle_label)
        frame_layout.addSpacing(10)
        
        # Группируем метку пути и поле ввода в один контейнер
        path_container = QVBoxLayout()
        path_container.setSpacing(4)
        path_container.addWidget(self._path_label)
        
        # Layout для поля ввода и кнопки изменения пути
        input_layout = QHBoxLayout()
        input_layout.setSpacing(8)
        
        # Добавляем поле ввода (растягиваемое)
        input_layout.addWidget(self._path_line_edit)
        
        # Добавляем кнопку изменения пути
        input_layout.addWidget(self._change_path_button)
        
        path_container.addLayout(input_layout)
        
        frame_layout.addLayout(path_container)
        
        # Добавляем растягивающий элемент
        frame_layout.addStretch()
        
        # Layout для кнопок подтверждения/отмены
        buttons_layout = QHBoxLayout()
        buttons_layout.setContentsMargins(0, 15, 0, 0)  # Отступ сверху
        
        # Кнопки в том же порядке, что и в старой версии: "Да" слева, "Нет" справа
        buttons_layout.addWidget(self._yes_button)
        buttons_layout.addStretch()
        buttons_layout.addWidget(self._no_button)
        
        frame_layout.addLayout(buttons_layout)
        main_layout.addWidget(self._frame)
    
    def _connect_signals(self):
        """Подключение сигналов к слотам"""
        self._change_path_button.clicked.connect(self._change_save_path)
        self._yes_button.clicked.connect(self._on_yes_clicked)
        self._no_button.clicked.connect(self._on_no_clicked)
    
    def set_save_path(self, path):
        """
        Установка пути сохранения в поле ввода
        
        Args:
            path (str): Путь для сохранения файлов
        """
        self._path_line_edit.setText(path)
    
    def get_save_path(self):
        """
        Получение текущего пути сохранения
        
        Returns:
            str: Текущий путь сохранения
        """
        return self._path_line_edit.text()
    
    def _change_save_path(self):
        """Открывает диалоговое окно выбора каталога и устанавливает путь"""
        try:
            path = QFileDialog.getExistingDirectory(self, "Выберите папку")
            
            if path:
                self._path_line_edit.setText(path)
                
        except Exception as e:
            QMessageBox.critical(
                self,
                "Ошибка",
                f"Произошла ошибка при выборе пути сохранения: {e}."
            )
    
    def _on_yes_clicked(self):
        """Обработчик нажатия кнопки 'Да'"""
        self.accepted.emit()
    
    def _on_no_clicked(self):
        """Обработчик нажатия кнопки 'Нет'"""
        self.rejected.emit()
        

if __name__ == "__main__":
    """Тестирование диалогового окна"""
    from PySide6.QtWidgets import QApplication
    import sys
    
    app = QApplication(sys.argv)
    
    # Тестовый вызов
    dialog = FinishDialog()
    
    # Устанавливаем тестовый путь
    dialog.set_save_path("/tmp/test_path")
    
    # Подключение сигналов для тестирования
    dialog.accepted.connect(lambda: print("Выбрано: Да (завершить)"))
    dialog.rejected.connect(lambda: print("Выбрано: Нет (вернуться)"))
    
    # Показ диалога
    result = dialog.exec()
    print(f"Диалог закрыт с кодом: {result}")
    
    sys.exit(app.exec())