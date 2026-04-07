"""
Единый модуль шрифтов для всего приложения.
Все шрифты используют семейство "Segoe UI" для визуальной согласованности.
"""

from PySide6.QtGui import QFont


FONT_FAMILY = "Segoe UI"


TITLE_FONT = QFont(FONT_FAMILY)
TITLE_FONT.setPointSize(16)
TITLE_FONT.setWeight(QFont.DemiBold)


SUBTITLE_FONT = QFont(FONT_FAMILY)
SUBTITLE_FONT.setPointSize(10)
SUBTITLE_FONT.setWeight(QFont.Normal)


FORM_LABEL_FONT = QFont(FONT_FAMILY)
FORM_LABEL_FONT.setPointSize(9)
FORM_LABEL_FONT.setWeight(QFont.Normal)


TAB_FONT = QFont(FONT_FAMILY)
TAB_FONT.setPointSize(11)
TAB_FONT.setWeight(QFont.Medium)