"""
Модуль финального диалогового окна для завершения теплового контроля
"""

import os
from pathlib import Path
from PySide6.QtCore import Qt, QSize, QTimer
from PySide6.QtWidgets import (
    QDialog, QFrame, QLabel, QLineEdit, QPushButton,
    QVBoxLayout, QHBoxLayout, QSizePolicy, QFileDialog, 
    QMessageBox, QDialogButtonBox
)
from PySide6.QtGui import QFont


class FinishDialog(QDialog):
    LABEL_MARGINS = (5, 0, 0, 0)  # left, top, right, bottom
    
    LINE_HEIGHT = 32
    
    BUTTON_HEIGHT = LINE_HEIGHT + 3
    
    BUTTON_SIZE = QSize(120, 45)
    
    LINE_DEFAULT_STYLE = """
        QLineEdit {
            padding-left: 8px;
            padding-right: 8px;
        }
    """
    
    LINE_ERROR_STYLE = """
        QLineEdit {
            border: 1px solid #e74c3c;
            border-radius: 4px;
            padding-left: 8px;
            padding-right: 8px;
        }
    """
    
    LINE_WARNING_STYLE = """
        QLineEdit {
            border: 1px solid #f39c12;
            border-radius: 4px;
            padding-left: 8px;
            padding-right: 8px;
        }
    """
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self._setup_window_properties()
        self._create_widgets()
        self._setup_layout()
        self._connect_signals()
        self._initial_validation = True
    
    def _setup_window_properties(self):
        self.setModal(True)
        self.setWindowTitle("Завершение теплового контроля")
        self.setFixedSize(600, 400)
        self.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        
        # Центрирование окна относительно родителя
        if self.parent():
            parent_geometry = self.parent().geometry()
            self.move(parent_geometry.center() - self.rect().center())
    
    def _create_widgets(self):
        title_font = QFont("Segoe UI")
        title_font.setPointSize(16)
        title_font.setWeight(QFont.DemiBold)
        
        subtitle_font = QFont("Segoe UI")
        subtitle_font.setPointSize(10)
        subtitle_font.setWeight(QFont.Normal)
        
        form_label_font = QFont("Segoe UI")
        form_label_font.setPointSize(9)
        form_label_font.setWeight(QFont.Normal)
        
        self._frame = QFrame()
        self._frame.setFrameShape(QFrame.StyledPanel)
        
        self._title_label = QLabel("Завершить тепловой контроль?")
        self._title_label.setFont(title_font)
        self._title_label.setAlignment(Qt.AlignCenter)

        self._subtitle_label = QLabel("Проверьте путь сохранения")
        self._subtitle_label.setFont(subtitle_font)
        self._subtitle_label.setAlignment(Qt.AlignCenter)
        
        self._path_label = QLabel("Путь сохранения файлов")
        self._path_label.setFont(form_label_font)
        self._path_label.setContentsMargins(*self.LABEL_MARGINS)
        
        self._path_line_edit = QLineEdit()
        self._path_line_edit.setMinimumHeight(self.LINE_HEIGHT)
        self._path_line_edit.setPlaceholderText("Нажмите 'Обзор...' для выбора пути")
        self._path_line_edit.setStyleSheet(self.LINE_DEFAULT_STYLE)
        self._path_line_edit.setReadOnly(True)
        
        self._change_path_button = QPushButton("Обзор...")
        self._change_path_button.setFixedSize(80, self.BUTTON_HEIGHT)
        
        self._button_box = QDialogButtonBox(
            QDialogButtonBox.Yes | QDialogButtonBox.No,
            self
        )
        self._button_box.button(QDialogButtonBox.Yes).setText("Завершить")
        self._button_box.button(QDialogButtonBox.No).setText("Отмена")
        self._button_box.button(QDialogButtonBox.Yes).setMinimumSize(self.BUTTON_SIZE)
        self._button_box.button(QDialogButtonBox.No).setMinimumSize(self.BUTTON_SIZE)
        self._button_box.button(QDialogButtonBox.No).setDefault(True)
    
    def _setup_layout(self):
        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(30, 30, 30, 30)
        
        frame_layout = QVBoxLayout(self._frame)
        frame_layout.setContentsMargins(30, 30, 30, 30)
        frame_layout.setSpacing(3)
        frame_layout.addWidget(self._title_label)
        frame_layout.addSpacing(10)
        frame_layout.addWidget(self._subtitle_label)
        frame_layout.addSpacing(20)
        
        path_container = QVBoxLayout()
        path_container.setSpacing(4)
        path_container.addWidget(self._path_label)
        
        input_layout = QHBoxLayout()
        input_layout.setSpacing(8)
        input_layout.addWidget(self._path_line_edit)
        input_layout.addWidget(self._change_path_button)
        
        path_container.addLayout(input_layout)
        frame_layout.addLayout(path_container)
        frame_layout.addStretch()
        
        frame_layout.addWidget(self._button_box)
        
        main_layout.addWidget(self._frame)
    
    def _connect_signals(self):
        self._change_path_button.clicked.connect(self._browse_save_path)
        self._button_box.accepted.connect(self._on_accept)
        self._button_box.rejected.connect(self.reject)
        self._path_line_edit.textChanged.connect(self._validate_path)
    
    def set_save_path(self, path: str):
        """Устанавливает путь сохранения"""
        self._path_line_edit.setText(path)
        QTimer.singleShot(100, self._validate_path)
    
    def get_save_path(self) -> str:
        """Возвращает текущий путь сохранения"""
        return self._path_line_edit.text().strip()
    
    def _validate_path(self):
        """Проверяет валидность пути сохранения"""
        path = self.get_save_path()
        
        # Сбрасываем стиль
        self._path_line_edit.setStyleSheet(self.LINE_DEFAULT_STYLE)
        self._button_box.button(QDialogButtonBox.Yes).setEnabled(True)
        
        if not path:
            # Путь пустой
            self._show_path_error("Путь сохранения не может быть пустым")
            return False
        
        try:
            path_obj = Path(path)
            
            if not path_obj.exists():
                self._show_path_error("Указанный путь не существует")
                return False
            
            if not path_obj.is_dir():
                self._show_path_error("Указанный путь не является директорией")
                return False
            
            test_file = path_obj / "test_write_permission.tmp"
            try:
                test_file.touch()
                test_file.unlink()
            except (PermissionError, OSError):
                self._show_path_warning("Нет прав на запись в указанную директорию")
                return False
            
            # Проверяем достаточно ли свободного места
            try:
                free_space = path_obj.drive if os.name == 'nt' else path_obj
                free_bytes = os.path.getmount(str(free_space)).free
                if free_bytes < 100 * 1024 * 1024:  # 100 МБ
                    self._show_path_warning(f"Мало свободного места: {free_bytes // (1024*1024)} МБ")
                    # Не блокируем кнопку, только предупреждаем
                    return True
            except (AttributeError, OSError):
                # Не удалось проверить свободное место, но это не критично
                pass
            
            # Все проверки пройдены
            self._button_box.button(QDialogButtonBox.Yes).setEnabled(True)
            return True
            
        except Exception as e:
            # Любая другая ошибка
            self._show_path_error(f"Некорректный путь: {str(e)}")
            return False
    
    def _show_path_error(self, message: str):
        """Показывает ошибку пути"""
        self._path_line_edit.setStyleSheet(self.LINE_ERROR_STYLE)
        self._button_box.button(QDialogButtonBox.Yes).setEnabled(False)
        
        # Показываем всплывающую подсказку
        self._path_line_edit.setToolTip(message)
        
        # Показываем всплывающее сообщение только при первой валидации
        if not self._initial_validation:
            QMessageBox.warning(
                self,
                "Проблема с путем сохранения",
                f"{message}\n\nПожалуйста, выберите корректный путь для сохранения.",
                QMessageBox.Ok
            )
        self._initial_validation = False
    
    def _show_path_warning(self, message: str):
        """Показывает предупреждение о пути"""
        self._path_line_edit.setStyleSheet(self.LINE_WARNING_STYLE)
        self._path_line_edit.setToolTip(message)
        # Не блокируем кнопку при предупреждении
        self._button_box.button(QDialogButtonBox.Yes).setEnabled(True)
        
        if not self._initial_validation:
            result = QMessageBox.warning(
                self,
                "Предупреждение",
                f"{message}\n\nПродолжить с этим путем?",
                QMessageBox.Yes | QMessageBox.No,
                QMessageBox.No
            )
            if result == QMessageBox.No:
                self._path_line_edit.setFocus()
        self._initial_validation = False
    
    def _browse_save_path(self):
        """Открывает диалог выбора каталога"""
        try:
            current_path = self.get_save_path()
            if current_path and Path(current_path).exists():
                start_dir = current_path
            else:
                try:
                    start_dir = str(Path.home())
                except:
                    start_dir = "C:\\" if os.name == 'nt' else "/"
            
            path = QFileDialog.getExistingDirectory(
                self, 
                "Выберите папку для сохранения",
                start_dir,
                QFileDialog.ShowDirsOnly | QFileDialog.DontResolveSymlinks
            )
            
            if path:
                self.set_save_path(path)
                self._validate_path()
                
        except Exception as e:
            QMessageBox.critical(
                self,
                "Ошибка",
                f"Не удалось выбрать путь сохранения: {e}"
            )
    
    def _on_accept(self):
        if self._validate_path():
            super().accept()
        else:
            QMessageBox.critical(
                self,
                "Ошибка пути",
                "Невозможно завершить контроль с текущим путём сохранения.\n"
                "Пожалуйста, выберите корректный путь."
            )


if __name__ == "__main__":
    """Тестирование диалогового окна"""
    from PySide6.QtWidgets import QApplication
    import sys
    
    app = QApplication(sys.argv)
    
    dialog = FinishDialog()
    dialog.set_save_path("D:\\")
    
    result = dialog.exec()
    
    if result == QDialog.Accepted:
        print(f"Выбрано: Завершить (путь: {dialog.get_save_path()})")
    else:
        print("Выбрано: Отмена")
    
    sys.exit(app.exec())