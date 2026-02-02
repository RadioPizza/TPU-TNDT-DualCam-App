"""
Модуль стартового окна с формой авторизации оператора
"""

import os
from pathlib import Path
from PySide6.QtCore import Qt, Signal, QEvent, QObject, QTimer
from PySide6.QtGui import QFont
from PySide6.QtWidgets import (
    QDialog, QFrame, QLabel, QPushButton,
    QVBoxLayout, QHBoxLayout, QScrollArea,
    QWidget, QLineEdit, QFileDialog, QMessageBox, QApplication
)
from settings import Settings, UserData
from osk import OnScreenKeyboard as osk


class FocusWatcher(QObject):
    """Отслеживает фокус для показа/скрытия экранной клавиатуры"""
    focus_gained = Signal()
    focus_lost = Signal()

    def eventFilter(self, watched_widget: QObject, event: QEvent) -> bool:
        """Обрабатывает события фокуса виджета"""
        if event.type() == QEvent.FocusIn:
            self.focus_gained.emit()
        elif event.type() == QEvent.FocusOut:
            # Ждем завершения всех событий перед проверкой фокуса
            QTimer.singleShot(0, self.focus_lost.emit)
        
        # Передаем событие дальше по цепочке обработчиков
        return super().eventFilter(watched_widget, event)


class StartDialog(QDialog):
    LABEL_MARGINS = (5, 0, 0, 0)  # left, top, right, bottom
    
    LINE_HEIGHT = 32
    
    BUTTON_HEIGHT = LINE_HEIGHT + 3
    
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
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self._setup_window_properties()
        self._create_widgets()
        self._setup_layout()
        self._connect_signals()
        self._init_focus_watcher()
        self._auto_fill_form()
    
    def _setup_window_properties(self):
        self.setModal(True)
        self.setWindowTitle("TPU-TNDT-DualCam-App")
        self.resize(800, 600)
        self.setMinimumSize(600, 400)
    
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
        
        self.scroll_area = QScrollArea()
        self.scroll_area.setWidgetResizable(True)
        self.scroll_area.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOn)
        self.scroll_area.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        
        self.scroll_content = QWidget()
        self.scroll_area.setWidget(self.scroll_content)
        
        self._main_frame = QFrame()
        self._main_frame.setFrameShape(QFrame.StyledPanel)
        
        self._auth_title_label = QLabel("Авторизация оператора")
        self._auth_title_label.setFont(title_font)
        
        self._auth_subtitle_label = QLabel("Введите ваше имя, фамилию и название объекта контроля")
        self._auth_subtitle_label.setFont(subtitle_font)
        
        self._name_label = QLabel("Имя")
        self._name_label.setFont(form_label_font)
        self._name_label.setContentsMargins(*self.LABEL_MARGINS)
        
        self._name_edit = QLineEdit()
        self._name_edit.setMinimumHeight(self.LINE_HEIGHT)
        
        self._surname_label = QLabel("Фамилия")
        self._surname_label.setFont(form_label_font)
        self._surname_label.setContentsMargins(*self.LABEL_MARGINS)
        
        self._surname_edit = QLineEdit()
        self._surname_edit.setMinimumHeight(self.LINE_HEIGHT)
        
        self._object_label = QLabel("Объект контроля")
        self._object_label.setFont(form_label_font)
        self._object_label.setContentsMargins(*self.LABEL_MARGINS)
        
        self._object_edit = QLineEdit()
        self._object_edit.setMinimumHeight(self.LINE_HEIGHT)
        
        self._path_label = QLabel("Путь сохранения файлов")
        self._path_label.setFont(form_label_font)
        self._path_label.setContentsMargins(*self.LABEL_MARGINS)
        
        self._path_edit = QLineEdit()
        self._path_edit.setReadOnly(True)
        self._path_edit.setMinimumHeight(self.LINE_HEIGHT)
        self._path_edit.setText("...")
        
        self._change_path_button = QPushButton("Обзор...")
        self._change_path_button.setMinimumHeight(self.BUTTON_HEIGHT)
        
        self._start_button = QPushButton("Начать")
        self._start_button.setMinimumHeight(self.BUTTON_HEIGHT)
        self._start_button.setMinimumWidth(120)
        self._start_button.setDefault(True)

        self._exit_button = QPushButton("Выход")
        self._exit_button.setMinimumHeight(self.BUTTON_HEIGHT)
        self._exit_button.setMinimumWidth(120)
        
        self._input_fields = [self._name_edit, self._surname_edit, self._object_edit]
        
        self._apply_default_style()
    
    def _apply_default_style(self):
        for field in [self._name_edit, self._surname_edit, 
                     self._object_edit, self._path_edit]:
            field.setStyleSheet(self.LINE_DEFAULT_STYLE)
    
    def _setup_layout(self):
        main_layout = QVBoxLayout(self)
        main_layout.addWidget(self.scroll_area)
        
        scroll_layout = QVBoxLayout(self.scroll_content)
        scroll_layout.addSpacing(20)
        
        center_widget = QWidget()
        center_layout = QHBoxLayout(center_widget)
        center_layout.addStretch()
        
        form_container = QWidget()
        form_container.setMaximumWidth(600)
        form_layout = QVBoxLayout(form_container)
        form_layout.addWidget(self._main_frame)
        
        center_layout.addWidget(form_container)
        center_layout.addStretch()
        
        scroll_layout.addWidget(center_widget)
        scroll_layout.addSpacing(50)
        scroll_layout.addStretch()
        
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
        
        self._focus_watcher.focus_gained.connect(osk.open)
        self._focus_watcher.focus_lost.connect(self._hide_osk)
        
    def _hide_osk(self):
        QTimer.singleShot(250, self._conditional_close_osk)
    
    def _conditional_close_osk(self):
        focused_widget = QApplication.focusWidget()
        if focused_widget not in self._input_fields:
            osk.close()    
    
    def _auto_fill_form(self):
        settings = Settings.load_from_file()
        if settings.auto_fill_forms:
            self._name_edit.setText("Олег")
            self._surname_edit.setText("Кравцов")
            self._object_edit.setText("Тестовый объект")
            self._path_edit.setText(os.getcwd())
    
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
            self.accept()
    
    def _validate_form(self) -> bool:
        errors = []
        
        user_name = self._name_edit.text().strip()
        user_surname = self._surname_edit.text().strip()
        object_of_testing = self._object_edit.text().strip()
        save_path = self._path_edit.text().strip()
        
        self._apply_default_style()
        
        if not user_name:
            errors.append("Имя не может быть пустым.")
            self._name_edit.setStyleSheet(self.LINE_ERROR_STYLE)
        elif not user_name.isalpha():
            errors.append("Имя должно содержать только буквы.")
            self._name_edit.setStyleSheet(self.LINE_ERROR_STYLE)
        elif len(user_name) == 1:
            errors.append("Имя не может состоять из одной буквы.")
            self._name_edit.setStyleSheet(self.LINE_ERROR_STYLE)
        
        if not user_surname:
            errors.append("Фамилия не может быть пустой.")
            self._surname_edit.setStyleSheet(self.LINE_ERROR_STYLE)
        elif not user_surname.isalpha():
            errors.append("Фамилия должна содержать только буквы.")
            self._surname_edit.setStyleSheet(self.LINE_ERROR_STYLE)
        elif len(user_surname) == 1:
            errors.append("Фамилия не может состоять из одной буквы.")
            self._surname_edit.setStyleSheet(self.LINE_ERROR_STYLE)
        
        if not object_of_testing:
            errors.append("Объект контроля не может быть пустым.")
            self._object_edit.setStyleSheet(self.LINE_ERROR_STYLE)
        
        if not save_path or save_path == '...':
            errors.append("Необходимо выбрать путь сохранения.")
            self._path_edit.setStyleSheet(self.LINE_ERROR_STYLE)
        else:
            try:
                if not Path(save_path).exists():
                    errors.append("Указанный путь сохранения недействителен.")
                    self._path_edit.setStyleSheet(self.LINE_ERROR_STYLE)
            except (OSError, ValueError):
                errors.append("Указанный путь сохранения недействителен.")
                self._path_edit.setStyleSheet(self.LINE_ERROR_STYLE)
        
        if errors:
            QMessageBox.critical(self, "Ошибка заполнения формы", "\n".join(errors))
            return False
        
        return True