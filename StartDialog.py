import os
from pathlib import Path
from PySide6.QtCore import QEvent, QObject, Qt, QTimer, Signal
from PySide6.QtGui import QFont
from PySide6.QtWidgets import (
    QApplication, QDialog, QFileDialog, QFrame,
    QHBoxLayout, QLabel, QLineEdit, QMessageBox,
    QPushButton, QScrollArea, QVBoxLayout, QWidget
)

from settings import Settings, UserData
from osk import OnScreenKeyboard as osk


class FocusWatcher(QObject):
    """Наблюдатель за фокусом для управления экранной клавиатурой"""
    focus_in = Signal()
    focus_out = Signal()

    def eventFilter(self, obj, event: QEvent) -> bool:
        if event.type() == QEvent.FocusIn:
            self.focus_in.emit()
        elif event.type() == QEvent.FocusOut:
            QTimer.singleShot(0, self.emit_focus_out)
        return super().eventFilter(obj, event)

    def emit_focus_out(self):
        self.focus_out.emit()


class StartWindow(QDialog):
    """Стартовое окно приложения с авторизацией оператора"""
    
    DEFAULT_STYLE = """
        QLineEdit {
            padding-left: 8px;
            padding-right: 8px;
        }
    """
    
    ERROR_STYLE = """
        QLineEdit {
            border: 1px solid #e74c3c;
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
        self._init_focus_watcher()
        self._auto_fill_form()
        
        QTimer.singleShot(0, self._adjust_scroll_height)
    
    def _setup_window_properties(self):
        self.setWindowTitle("TPU-TNDT-DualCam-App")
        self.setWindowModality(Qt.ApplicationModal)
        self.resize(800, 600)
        self.setMinimumSize(600, 400)
        self.setSizeGripEnabled(False)
    
    def _create_widgets(self):
        self.scroll_area = QScrollArea()
        self.scroll_area.setWidgetResizable(True)
        self.scroll_area.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOn)
        self.scroll_area.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        
        self.scroll_content = QWidget()
        self.scroll_area.setWidget(self.scroll_content)
        
        self._main_frame = QFrame()
        self._main_frame.setFrameShape(QFrame.StyledPanel)
        self._main_frame.setFrameShadow(QFrame.Raised)
        
        self._auth_title_label = QLabel("Авторизация оператора")
        title_font = QFont()
        title_font.setPointSize(16)
        title_font.setWeight(QFont.DemiBold)
        self._auth_title_label.setFont(title_font)
        
        self._auth_subtitle_label = QLabel("Введите ваше имя, фамилию и название объекта контроля")
        subtitle_font = QFont()
        subtitle_font.setPointSize(11)
        subtitle_font.setWeight(QFont.Normal)
        self._auth_subtitle_label.setFont(subtitle_font)
        
        form_label_font = QFont()
        form_label_font.setPointSize(9)
        form_label_font.setWeight(QFont.Normal)
        
        self._name_label = QLabel("Имя")
        self._name_label.setFont(form_label_font)
        self._name_label.setContentsMargins(5, 0, 0, 0)
        
        self._name_edit = QLineEdit()
        self._name_edit.setMinimumHeight(35)
        
        self._surname_label = QLabel("Фамилия")
        self._surname_label.setFont(form_label_font)
        self._surname_label.setContentsMargins(5, 0, 0, 0)
        
        self._surname_edit = QLineEdit()
        self._surname_edit.setMinimumHeight(35)
        
        self._object_label = QLabel("Объект контроля")
        self._object_label.setFont(form_label_font)
        self._object_label.setContentsMargins(5, 0, 0, 0)
        
        self._object_edit = QLineEdit()
        self._object_edit.setMinimumHeight(35)
        
        self._path_label = QLabel("Путь сохранения файлов")
        self._path_label.setFont(form_label_font)
        self._path_label.setContentsMargins(5, 0, 0, 0)
        
        self._path_edit = QLineEdit()
        self._path_edit.setReadOnly(True)
        self._path_edit.setMinimumHeight(35)
        self._path_edit.setText("...")
        
        self._change_path_button = QPushButton("Обзор...")
        self._change_path_button.setMinimumHeight(37)
        
        self._start_button = QPushButton("Начать")
        self._start_button.setMinimumHeight(37)
        self._start_button.setMinimumWidth(120)
        self._start_button.setDefault(True)
        
        self._exit_button = QPushButton("Выход")
        self._exit_button.setMinimumHeight(37)
        self._exit_button.setMinimumWidth(120)
        
        self._input_fields = [self._name_edit, self._surname_edit, self._object_edit]
        
        self._apply_default_style()
    
    def _apply_default_style(self):
        for field in [self._name_edit, self._surname_edit, 
                     self._object_edit, self._path_edit]:
            field.setStyleSheet(self.DEFAULT_STYLE)
    
    def _setup_layout(self):
        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.addWidget(self.scroll_area)
        
        scroll_layout = QVBoxLayout(self.scroll_content)
        scroll_layout.setContentsMargins(0, 0, 0, 0)
        scroll_layout.addSpacing(20)
        
        center_widget = QWidget()
        center_layout = QHBoxLayout(center_widget)
        center_layout.setContentsMargins(0, 0, 0, 0)
        center_layout.addStretch()
        
        form_container = QWidget()
        form_container.setMaximumWidth(600)
        form_layout = QVBoxLayout(form_container)
        form_layout.setContentsMargins(0, 0, 0, 0)
        form_layout.addWidget(self._main_frame)
        
        center_layout.addWidget(form_container)
        center_layout.addStretch()
        
        scroll_layout.addWidget(center_widget)
        scroll_layout.addSpacing(50)
        scroll_layout.addStretch(1)
        
        frame_layout = QVBoxLayout(self._main_frame)
        frame_layout.setContentsMargins(30, 30, 30, 30)
        frame_layout.setSpacing(3)
        
        frame_layout.addWidget(self._auth_title_label)
        frame_layout.addSpacing(10)
        frame_layout.addWidget(self._auth_subtitle_label)
        frame_layout.addSpacing(20)
        
        frame_layout.addWidget(self._name_label)
        frame_layout.addWidget(self._name_edit)
        frame_layout.addSpacing(10)
        
        frame_layout.addWidget(self._surname_label)
        frame_layout.addWidget(self._surname_edit)
        frame_layout.addSpacing(10)
        
        frame_layout.addWidget(self._object_label)
        frame_layout.addWidget(self._object_edit)
        frame_layout.addSpacing(10)
        
        frame_layout.addWidget(self._path_label)
        path_layout = QHBoxLayout()
        path_layout.addWidget(self._path_edit)
        path_layout.addWidget(self._change_path_button)
        frame_layout.addLayout(path_layout)
        frame_layout.addSpacing(30)
        
        buttons_layout = QHBoxLayout()
        buttons_layout.addStretch()
        buttons_layout.addWidget(self._exit_button)
        buttons_layout.addWidget(self._start_button)
        frame_layout.addLayout(buttons_layout)
        
        self._adjust_scroll_height()
    
    def _adjust_scroll_height(self):
        if hasattr(self, 'scroll_content'):
            window_height = self.height()
            form_height = self._main_frame.minimumSizeHint().height()
            scroll_height = form_height + int(window_height * 0.7)
            self.scroll_content.setMinimumHeight(scroll_height)
    
    def resizeEvent(self, event):
        super().resizeEvent(event)
        self._adjust_scroll_height()
    
    def _connect_signals(self):
        self._start_button.clicked.connect(self.open_main_window)
        self._exit_button.clicked.connect(self.close)
        self._change_path_button.clicked.connect(self.change_save_path)
    
    def _init_focus_watcher(self):
        self._focus_watcher = FocusWatcher()
        for field in self._input_fields:
            field.installEventFilter(self._focus_watcher)
        
        self._focus_watcher.focus_in.connect(osk.open)
        self._focus_watcher.focus_out.connect(self._hide_osk)
    
    def _auto_fill_form(self):
        settings = Settings.load_from_file()
        if settings.auto_fill_forms:
            self._name_edit.setText("Олег")
            self._surname_edit.setText("Кравцов")
            self._object_edit.setText("Тестовый объект")
            self._path_edit.setText(os.getcwd())
    
    def showMaximized(self):
        super().showMaximized()
        QTimer.singleShot(100, self._adjust_scroll_height)
    
    def keyPressEvent(self, event):
        if event.key() not in (Qt.Key_Return, Qt.Key_Enter):
            super().keyPressEvent(event)
    
    def _hide_osk(self):
        QTimer.singleShot(250, self._conditional_close_osk)
    
    def _conditional_close_osk(self):
        focused_widget = QApplication.focusWidget()
        if focused_widget not in self._input_fields:
            osk.close()
    
    def change_save_path(self):
        try:
            path = QFileDialog.getExistingDirectory(self, "Выберите папку")
            if path:
                self._path_edit.setText(path)
        except Exception as e:
            QMessageBox.critical(self, "Ошибка", 
                               f"Произошла ошибка при выборе пути сохранения: {e}.")
    
    def open_main_window(self):
        if self._validate_form():
            user_data = UserData.get_instance()
            user_data.user_name = self._name_edit.text().strip()
            user_data.user_surname = self._surname_edit.text().strip()
            user_data.object_of_testing = self._object_edit.text().strip()
            user_data.save_path = self._path_edit.text().strip()
            
            from main import MainWindow
            self.main_window = MainWindow()
            self.main_window.show()
            self.close()
    
    def _validate_form(self) -> bool:
        errors = []
        
        user_name = self._name_edit.text().strip()
        user_surname = self._surname_edit.text().strip()
        object_of_testing = self._object_edit.text().strip()
        save_path = self._path_edit.text().strip()
        
        self._apply_default_style()
        
        if not user_name:
            errors.append("Имя не может быть пустым.")
            self._name_edit.setStyleSheet(self.ERROR_STYLE)
        elif not user_name.isalpha():
            errors.append("Имя должно содержать только буквы.")
            self._name_edit.setStyleSheet(self.ERROR_STYLE)
        elif len(user_name) == 1:
            errors.append("Имя не может состоять из одной буквы.")
            self._name_edit.setStyleSheet(self.ERROR_STYLE)
        
        if not user_surname:
            errors.append("Фамилия не может быть пустой.")
            self._surname_edit.setStyleSheet(self.ERROR_STYLE)
        elif not user_surname.isalpha():
            errors.append("Фамилия должна содержать только буквы.")
            self._surname_edit.setStyleSheet(self.ERROR_STYLE)
        elif len(user_surname) == 1:
            errors.append("Фамилия не может состоять из одной буквы.")
            self._surname_edit.setStyleSheet(self.ERROR_STYLE)
        
        if not object_of_testing:
            errors.append("Объект контроля не может быть пустым.")
            self._object_edit.setStyleSheet(self.ERROR_STYLE)
        
        if not save_path or save_path == '...':
            errors.append("Необходимо выбрать путь сохранения.")
            self._path_edit.setStyleSheet(self.ERROR_STYLE)
        else:
            try:
                if not Path(save_path).exists():
                    errors.append("Указанный путь сохранения недействителен.")
                    self._path_edit.setStyleSheet(self.ERROR_STYLE)
            except (OSError, ValueError):
                errors.append("Указанный путь сохранения недействителен.")
                self._path_edit.setStyleSheet(self.ERROR_STYLE)
        
        if errors:
            QMessageBox.critical(self, "Ошибка заполнения формы", "\n".join(errors))
            return False
        
        return True


if __name__ == "__main__":
    import sys
    
    class TestSettings:
        auto_fill_forms = True
    
    Settings.load_from_file = lambda: TestSettings()
    
    app = QApplication(sys.argv)
    window = StartWindow()
    window.showMaximized()
    sys.exit(app.exec())