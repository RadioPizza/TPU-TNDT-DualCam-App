"""
Единый модуль констант GUI
"""

from PySide6.QtCore import QSize

"""
БАЗОВАЯ СЕТКА И ОТСТУПЫ (GRID & SPACING)
"""

SPACING_SMALL = 8
SPACING_MEDIUM = 16
SPACING_LARGE = 24

LAYOUT_SPACING = SPACING_SMALL
WINDOW_MARGINS = (SPACING_LARGE, SPACING_LARGE, SPACING_LARGE, SPACING_LARGE)

LABEL_MARGINS = (SPACING_SMALL, 0, 0, 0)
"""
БАЗОВЫЕ КОМПОНЕНТЫ (CONTROLS)
"""

CONTROL_HEIGHT = 32
CONTROL_WIDTH = 250
CONTENT_WIDTH_MIN = 800
CONTENT_WIDTH_MAX = 1200

BUTTON_SIZE = QSize(200, CONTROL_HEIGHT + 8)

STATUS_BAR_LABEL_SIZE = QSize(120, 30)
ROUND_INDICATOR_SIZE = QSize(12, 12)

INDICATOR_RADIUS = 6
ROUND_INDICATOR_SIZE = QSize(INDICATOR_RADIUS * 2, INDICATOR_RADIUS * 2)

"""
СТАНДАРТЫ ОКОН (WINDOW SIZES)
"""

WINDOW_MAIN = QSize(1280, 720)
WINDOW_MAIN_MIN = QSize(848, 424)


DIALOG_SMALL = QSize(400, 300)   #  (RetestDialog, TrajectoryDialog)
DIALOG_MEDIUM = QSize(600, 450)  #  (SettingsWindow, FinishDialog)
DIALOG_LARGE = QSize(800, 600)   #  (StartDialog)

"""
Общие стили
"""
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