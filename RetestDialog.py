"""
Модуль диалогового окна для подтверждения повторного контроля последней зоны
"""

from PySide6.QtCore import QSize
from PySide6.QtWidgets import (
    QDialog, QFrame, QLabel, QDialogButtonBox,
    QVBoxLayout
)
from PySide6.QtGui import QFont


class RetestDialog(QDialog):
    BUTTON_SIZE = QSize(120, 45)
    
    def __init__(self, x: int, y: int, parent=None):
        super().__init__(parent)
        self.x = x
        self.y = y
        self._setup_window_properties()
        self._create_widgets()
        self._setup_layout()
        
    def _setup_window_properties(self):
        self.setModal(True)
        self.setWindowTitle("Повторный контроль зоны")
        self.setFixedSize(450, 300)
        
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
        
        self._frame = QFrame()
        self._frame.setFrameShape(QFrame.StyledPanel)
        
        self._title_label = QLabel(f"Зона ({self.x}, {self.y})")
        self._title_label.setFont(title_font)
        
        self._subtitle_label = QLabel(
            "Вы хотите повторить контроль этой зоны? Старые данные текущей зоны будут удалены")
        self._subtitle_label.setFont(subtitle_font)
        self._subtitle_label.setWordWrap(True)
        
        self._button_box = QDialogButtonBox(
            QDialogButtonBox.Yes | QDialogButtonBox.No, self)
        self._button_box.button(QDialogButtonBox.Yes).setText("Да")
        self._button_box.button(QDialogButtonBox.No).setText("Нет")
        self._button_box.button(QDialogButtonBox.Yes).setMinimumSize(self.BUTTON_SIZE)
        self._button_box.button(QDialogButtonBox.No).setMinimumSize(self.BUTTON_SIZE)
        self._button_box.button(QDialogButtonBox.No).setDefault(True)
        self._button_box.accepted.connect(self.accept)
        self._button_box.rejected.connect(self.reject)
    
    def _setup_layout(self):
        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(30, 30, 30, 30)

        frame_layout = QVBoxLayout(self._frame)
        frame_layout.setContentsMargins(30, 30, 30, 30)
        frame_layout.setSpacing(3)

        frame_layout.addWidget(self._title_label)
        frame_layout.addSpacing(10)
        frame_layout.addWidget(self._subtitle_label)
        frame_layout.addStretch()
        frame_layout.addWidget(self._button_box)
        
        main_layout.addWidget(self._frame)


if __name__ == "__main__":
    """Тестирование диалогового окна"""
    from PySide6.QtWidgets import QApplication
    import sys
    
    app = QApplication(sys.argv)
    
    dialog = RetestDialog(0, 2)
    
    # Просто проверяем результат
    result = dialog.exec()
    
    if result == QDialog.Accepted:
        print("Пользователь выбрал: Да")
    else:
        print("Пользователь выбрал: Нет")
    
    sys.exit(app.exec())