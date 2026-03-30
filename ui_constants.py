"""
Единый модуль констант GUI
"""

from PySide6.QtCore import QSize

# Размеры полей ввода
LINE_HEIGHT = 32

# Размер кнопок
BUTTON_SIZE = QSize(200, 45)
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

"""
Отдельно для модуля MainWindow
"""
VIDEO_STYLE = """
        QGraphicsView {
            background-color: #333333;
            border: 2px solid #3c3c3c;
            border-radius: 8px;
        }
    """

"""
Отдельно для модуля SettingsWindow
"""

GROUP_BOX_STYLE = """
        QGroupBox {
            font-weight: 600;
            margin-top: 9px;
            padding: 16px;
        }
        QGroupBox::title {
            subcontrol-origin: margin;
            left: 20px;
            padding: 0 5px;
        }
    """

TAB_BAR_STYLE = """
        QTabBar::tab {
            padding: 16px 46px;
            margin-right: 4px;
            border-top-left-radius: 4px;
            border-top-right-radius: 4px;
            min-width: 100px;
            border-bottom: 1px solid palette(button);
        }
        QTabBar::tab:selected {
            border-bottom: 3px solid palette(highlight);
            background-color: palette(base);
        }
        QTabBar::tab:hover {
            background-color: palette(button);
        }
    """


CHECKBOX_STYLE = """
        QCheckBox {
            spacing: 10px;
        }
    """

"""
Отдельно для модуля StartDialog
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

"""
Отдельно для модуля FinishDialog
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

LINE_WARNING_STYLE = """
    QLineEdit {
        border: 1px solid #f39c12;
        border-radius: 4px;
        padding-left: 8px;
        padding-right: 8px;
    }
"""