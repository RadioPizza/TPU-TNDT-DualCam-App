from PySide6.QtCore import QSize
from PySide6.QtWidgets import (
    QVBoxLayout,
    QLabel,
    QDoubleSpinBox,
    QDialog, QVBoxLayout, QDialogButtonBox, QSpinBox
)
from PySide6.QtGui import QFont
from typing import List, Any

# Импорт единых шрифтов и констант (предполагается наличие модулей)
try:
    from ui_fonts import fonts  # словарь с QFont, например fonts['regular'], fonts['small']
    from ui_constants import (
        LAYOUT_SPACING, WIDGET_SPACING, FIELD_HEIGHT,
        BUTTON_SIZE, GROUP_BOX_STYLE
    )
except ImportError:
    # Заглушки на случай отсутствия модулей (для автономной работы примера)
    fonts = {
        'regular': QFont('Segoe UI', 9),
        'small': QFont('Segoe UI', 8),
        'medium': QFont('Segoe UI', 10, QFont.Medium),
        'large': QFont('Segoe UI', 12, QFont.Medium)
    }
    LAYOUT_SPACING = 10
    WIDGET_SPACING = 15
    FIELD_HEIGHT = 32
    BUTTON_SIZE = QSize(120, FIELD_HEIGHT)
    GROUP_BOX_STYLE = """
        QGroupBox {
            font-weight: 600;
            margin-top: 9px;
            padding: 12px;
        }
        QGroupBox::title {
            subcontrol-origin: margin;
            left: 15px;
            padding: 0 5px;
        }
    """

# TODO установить шрифты

class ParameterDialog(QDialog):
    def __init__(self, method_params: List[tuple], parent=None):
        """
        method_params: список кортежей (имя_параметра, значение_по_умолчанию)
        """
        super().__init__(parent)
        self.setWindowTitle("Параметры этапа")
        layout = QVBoxLayout(self)

        self.inputs = []
        for param_name, default in method_params:
            label = QLabel(param_name)
            layout.addWidget(label)

            # Определяем тип поля ввода
            if isinstance(default, int):
                spin = QSpinBox()
                spin.setRange(-1000000, 1000000)  # широкий диапазон
                spin.setValue(default)
            else:
                spin = QDoubleSpinBox()
                spin.setRange(-1e6, 1e6)
                spin.setValue(default)

            layout.addWidget(spin)
            self.inputs.append(spin)

        buttons = QDialogButtonBox(QDialogButtonBox.Ok | QDialogButtonBox.Cancel)
        buttons.accepted.connect(self.accept)
        buttons.rejected.connect(self.reject)
        layout.addWidget(buttons)

    def get_values(self) -> List[Any]:
        """Возвращает список введённых значений"""
        return [spin.value() for spin in self.inputs]