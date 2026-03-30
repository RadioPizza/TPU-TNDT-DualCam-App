"""
Единый модуль констант GUI
"""

from PySide6.QtCore import QSize

# Размеры полей ввода
LINE_HEIGHT = 32

# Размер кнопок
BUTTON_SIZE = QSize(120, 45)
BUTTON_HEIGHT = LINE_HEIGHT + 3

# Отступы и интервалы 
LABEL_MARGINS = (5, 0, 0, 0)
CONTENT_MARGINS = (30, 30, 30, 30)
LAYOUT_SPACING = 3
CONTENT_MIN_WIDTH = 800
CONTENT_MAX_WIDTH = 1200

# Рахмеры окон
WINDOW_FIXED_SIZE = QSize(1280, 720)
WINDOW_MIN_SIZE = QSize(850, 425)

# Размер индикаторов
INDICATOR_SIZE = QSize(120, 30)

# Размеры вспомогательных окон
RETEST_DIALOG_SIZE = QSize(450, 300)
SETTINGS_WINDOW_SIZE = QSize(600, 500)