"""
Модуль окна настроек приложения для теплового неразрушающего контроля
"""
from PySide6.QtCore import QSize
from PySide6.QtWidgets import (
    QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
    QLabel, QPushButton, QFrame, QTabWidget,
    QScrollArea, QComboBox, QGroupBox,
    QSpinBox, QCheckBox, QMessageBox
)
from PySide6.QtGui import QFont
from settings import Settings


class SettingsWindow(QMainWindow):
    """Окно настроек приложения"""
    WIDGET_SPACING = 20
    FIELD_WIDTH = 250
    FIELD_HEIGHT = 32
    BUTTON_HEIGHT = FIELD_HEIGHT + 3
    BUTTON_SIZE = QSize(120, BUTTON_HEIGHT)
    WINDOW_MIN_SIZE = (850, 425)
    CONTENT_MIN_WIDTH = 800
    CONTENT_MAX_WIDTH = 1200

    INDICATOR_BORDER_RADIUS = 6
    INDICATOR_BORDER_DIAMETER = INDICATOR_BORDER_RADIUS * 2
    INDICATOR_SIZE = QSize(INDICATOR_BORDER_DIAMETER, INDICATOR_BORDER_DIAMETER)

    HEATER_BUTTON_SIZE = QSize(FIELD_WIDTH, 55)

    LAYOUT_SPACING = 12
    LAYOUT_SPACING_SMALL = 10
    LAYOUT_SPACING_LARGE = 15
    CONTENT_WRAPPER_MARGINS = (0, 5, 0, 25)
    FOOTER_SPACING = 20

    COMBOBOX_PADDING = 10
    SPINBOX_PADDING = COMBOBOX_PADDING - 5
    INFO_LABEL_PADDING = COMBOBOX_PADDING - 1

    INDICATOR_CONNECTED = "connected"
    INDICATOR_DISCONNECTED = "disconnected"
    INDICATOR_CONNECTING = "connecting"
    INDICATOR_ERROR = "error"
    INDICATOR_OFF = "off"
    INDICATOR_HEATING = "heating"

    INDICATOR_COLORS = {
        INDICATOR_CONNECTED: "#27ae60",
        INDICATOR_DISCONNECTED: "#7f8c8d",
        INDICATOR_CONNECTING: "#f39c12",
        INDICATOR_ERROR: "#e74c3c",
        INDICATOR_OFF: "#7f8c8d",
        INDICATOR_HEATING: "#e74c3c",
    }

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

    def __init__(self, settings: Settings, parent=None):
        super().__init__(parent)
        self._settings = settings
        self._setup_window_properties()
        self._create_widgets()
        self._setup_layout()
        self._connect_signals()
        self._load_settings()
        self.showMaximized()

    def _setup_window_properties(self):
        self.setWindowTitle("Настройки")
        self.setMinimumSize(*self.WINDOW_MIN_SIZE)

    def _create_widgets(self):
        tab_font = QFont("Segoe UI", 11, QFont.Medium)
        form_label_font = QFont("Segoe UI", 9, QFont.Normal)

        self._central_widget = QWidget()
        self.setCentralWidget(self._central_widget)

        self._tab_widget = QTabWidget()
        self._tab_widget.setDocumentMode(True)
        self._tab_widget.setMovable(False)
        self._tab_widget.setFont(tab_font)
        self._tab_widget.setStyleSheet(self.TAB_BAR_STYLE)

        self._create_testing_tab(form_label_font)
        self._create_cameras_tab(form_label_font)
        self._create_heater_tab(form_label_font)
        self._create_interface_tab(form_label_font)

        self._save_button = QPushButton("Применить")
        self._save_button.setMinimumSize(self.BUTTON_SIZE)
        self._save_button.setDefault(True)

        self._cancel_button = QPushButton("Отмена")
        self._cancel_button.setMinimumSize(self.BUTTON_SIZE)

        self._reset_button = QPushButton("Сбросить")
        self._reset_button.setMinimumSize(self.BUTTON_SIZE)
        self._reset_button.setEnabled(False)

    def _setup_layout(self):
        self._main_layout = QVBoxLayout(self._central_widget)

        center_container = QWidget()
        center_layout = QHBoxLayout(center_container)
        center_layout.addStretch(1)

        content_wrapper = QWidget()
        content_wrapper_layout = QVBoxLayout(content_wrapper)
        content_wrapper_layout.setContentsMargins(*self.CONTENT_WRAPPER_MARGINS)
        content_wrapper_layout.setSpacing(self.WIDGET_SPACING)
        content_wrapper_layout.addWidget(self._tab_widget)

        footer_layout = QHBoxLayout()
        footer_layout.setSpacing(self.FOOTER_SPACING)
        footer_layout.addStretch()
        footer_layout.addWidget(self._reset_button)
        footer_layout.addWidget(self._cancel_button)
        footer_layout.addWidget(self._save_button)
        content_wrapper_layout.addLayout(footer_layout)

        content_wrapper.setMinimumWidth(self.CONTENT_MIN_WIDTH)
        content_wrapper.setMaximumWidth(self.CONTENT_MAX_WIDTH)

        center_layout.addWidget(content_wrapper)
        center_layout.addStretch(1)

        self._main_layout.addWidget(center_container)

    def _connect_signals(self):
        self._save_button.clicked.connect(self._save_settings)
        self._cancel_button.clicked.connect(self.close)
        self._reset_button.clicked.connect(self._reset_settings)

    def _get_indicator_style(self, status: str) -> str:
        color = self.INDICATOR_COLORS.get(status, self.INDICATOR_COLORS[self.INDICATOR_OFF])
        return f"""
            QFrame {{
                background-color: {color};
                border-radius: {self.INDICATOR_BORDER_RADIUS}px;
            }}
        """

    def _set_indicator_status(self, indicator: QFrame, status: str):
        indicator.setStyleSheet(self._get_indicator_style(status))
        indicator.setProperty("status", status)

    def _create_indicator(self) -> QFrame:
        indicator = QFrame()
        indicator.setFixedSize(self.INDICATOR_SIZE)
        indicator.setStyleSheet(self._get_indicator_style(self.INDICATOR_DISCONNECTED))
        return indicator

    def _create_spinbox_row(self, label_text, default_value, min_val, max_val, font):
        """Создаёт горизонтальный layout с меткой и спинбоксом, возвращает layout и спинбокс."""
        layout = QHBoxLayout()
        layout.setSpacing(self.LAYOUT_SPACING)

        label = QLabel(label_text)
        label.setFont(font)
        layout.addWidget(label)
        layout.addStretch()

        spinbox = QSpinBox()
        spinbox.setFixedHeight(self.FIELD_HEIGHT)
        spinbox.setFixedWidth(self.FIELD_WIDTH)
        spinbox.setRange(min_val, max_val)
        spinbox.setValue(default_value)
        spinbox.setStyleSheet(f"QSpinBox {{ padding-left: {self.SPINBOX_PADDING}px; }}")
        layout.addWidget(spinbox)

        return layout, spinbox

    def _create_combo_row(self, label_text, items, default_text, font):
        """Создаёт горизонтальный layout с меткой и комбобоксом, возвращает layout и комбобокс."""
        layout = QHBoxLayout()
        layout.setSpacing(self.LAYOUT_SPACING)

        label = QLabel(label_text)
        label.setFont(font)
        layout.addWidget(label)
        layout.addStretch()

        combo = QComboBox()
        combo.setFixedHeight(self.FIELD_HEIGHT)
        combo.setFixedWidth(self.FIELD_WIDTH)
        combo.setStyleSheet(f"QComboBox {{ padding-left: {self.COMBOBOX_PADDING}px; }}")
        combo.addItems(items)

        if default_text in items:
            combo.setCurrentText(default_text)

        layout.addWidget(combo)

        return layout, combo

    def _create_info_row(self, label_text, value_text, font):
        """
        Создаёт горизонтальный layout с меткой и информационным полем (только для чтения).
        Возвращает layout и label значения для последующего обновления.
        """
        layout = QHBoxLayout()
        layout.setSpacing(self.LAYOUT_SPACING)

        label = QLabel(label_text)
        label.setFont(font)
        layout.addWidget(label)
        layout.addStretch()

        value_label = QLabel(value_text)
        value_label.setFont(font)
        value_label.setStyleSheet(f"QLabel {{ padding-left: {self.INFO_LABEL_PADDING}px; }}")
        value_label.setFixedWidth(self.FIELD_WIDTH)
        layout.addWidget(value_label)
        
        return layout, value_label

    def _create_testing_tab(self, font):
        tab = QWidget()
        layout = QVBoxLayout(tab)

        container = QWidget()
        container_layout = QVBoxLayout(container)
        container_layout.setSpacing(self.WIDGET_SPACING)

        main_group = self._create_group_box("Параметры теплового контроля", font)
        main_layout = QVBoxLayout(main_group)
        main_layout.setSpacing(self.LAYOUT_SPACING_LARGE)

        total_layout, self._total_duration_spin = self._create_spinbox_row(
            "Полная длительность контроля зоны, с",
            getattr(self._settings, 'duration_of_testing', 120),
            1, 300, font
        )
        main_layout.addLayout(total_layout)
        
        heating_layout, self._heating_duration_spin = self._create_spinbox_row(
            "Длительность импульса нагрева, с:",
            getattr(self._settings, 'heating_duration', 6),
            1, 12, font
        )
        main_layout.addLayout(heating_layout)

        cooling_duration = (
            getattr(self._settings, 'duration_of_testing', 120) -
            getattr(self._settings, 'heating_duration', 60)
        )
        
        cooling_layout, self._cooling_duration_info = self._create_info_row(
            "Длительность естественного охлаждения, с:",
            str(cooling_duration),
            font
        )
        main_layout.addLayout(cooling_layout)

        container_layout.addWidget(main_group)

        # Параметры записи с камеры видимого спектра
        record_group = self._create_group_box("Параметры записи с камеры видимого спектра", font)
        record_layout = QVBoxLayout(record_group)
        record_layout.setSpacing(self.LAYOUT_SPACING_LARGE)

        recording_fps = getattr(self._settings, 'recording_fps', 30)

        format_layout, self._visible_record_format_combo = self._create_combo_row(
            "Формат записи видео:",
            ["AVI", "MP4", "MKV"],
            "AVI",
            font
        )
        record_layout.addLayout(format_layout)

        fps_layout, self._visible_record_fps_combo = self._create_combo_row(
            "Частота записи видео:",
            ["30 FPS", "25 FPS", "15 FPS", "10 FPS"],
            f"{recording_fps} FPS",
            font
        )
        record_layout.addLayout(fps_layout)

        container_layout.addWidget(record_group)

        # Параметры записи с тепловизора
        record2_group = self._create_group_box("Параметры записи с тепловизора", font)
        record2_layout = QVBoxLayout(record2_group)
        record2_layout.setSpacing(self.LAYOUT_SPACING_LARGE)

        format2_layout, self._thermal_record_format_combo = self._create_combo_row(
            "Формат записи видео:",
            ["AVI", "MP4", "MKV"],
            "AVI",
            font
        )
        record2_layout.addLayout(format2_layout)

        fps2_layout, self._thermal_record_fps_combo = self._create_combo_row(
            "Частота записи видео:",
            ["30 FPS", "25 FPS", "15 FPS", "10 FPS"],
            f"{recording_fps} FPS",
            font
        )
        record2_layout.addLayout(fps2_layout)

        container_layout.addWidget(record2_group)
        container_layout.addStretch()

        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll.setFrameShape(QFrame.NoFrame)
        scroll.setWidget(container)

        layout.addWidget(scroll)
        self._tab_widget.addTab(tab, "Контроль")

    def _create_cameras_tab(self, font):
        tab = QWidget()
        layout = QVBoxLayout(tab)

        container = QWidget()
        container_layout = QVBoxLayout(container)
        container_layout.setSpacing(self.WIDGET_SPACING)

        # Камера видимого спектра
        visible_group = self._create_group_box("Настройка камеры видимого спектра", font)
        visible_layout = QVBoxLayout(visible_group)
        visible_layout.setSpacing(self.LAYOUT_SPACING_LARGE)

        dev_layout, self._visible_device_combo = self._create_combo_row(
            "Устройство:",
            ["FLIR BFS-PGE-27S5C", "Камера 2", "Камера 3"],
            "Камера 1",
            font
        )
        visible_layout.addLayout(dev_layout)

        res_layout, self._visible_resolution_combo = self._create_combo_row(
            "Разрешение:",
            ["1936×1464", "1280×720", "640×480"],
            "1936×1464",
            font
        )
        visible_layout.addLayout(res_layout)

        fps_layout, self._visible_preview_fps_combo = self._create_combo_row(
            "Частота предварительного просмотра видео:",
            ["60 FPS", "30 FPS", "15 FPS"],
            "30 FPS",
            font
        )
        visible_layout.addLayout(fps_layout)

        container_layout.addWidget(visible_group)

        # Тепловизор
        thermal_group = self._create_group_box("Настройка тепловизора", font)
        thermal_layout = QVBoxLayout(thermal_group)
        thermal_layout.setSpacing(self.LAYOUT_SPACING_LARGE)

        dev_th_layout, self._thermal_device_combo = self._create_combo_row(
            "Устройство:",
            ["Optris PI 640", "Камера 2", "Камера 3"],
            "Камера 1",
            font
        )
        thermal_layout.addLayout(dev_th_layout)

        res_th_layout, self._thermal_resolution_combo = self._create_combo_row(
            "Разрешение:",
            ["640×480", "320×240", "160×120"],
            "640×480",
            font
        )
        thermal_layout.addLayout(res_th_layout)

        fps_th_layout, self._thermal_preview_fps_combo = self._create_combo_row(
            "Частота предварительного просмотра видео:",
            ["32 FPS", "30 FPS", "15 FPS", "9 FPS"],
            "32 FPS",
            font
        )
        thermal_layout.addLayout(fps_th_layout)

        palette_layout, self._thermal_palette_combo = self._create_combo_row(
            "Цветовая палитра:",
            ["Iron", "Rainbow", "Gray", "Arctic", "Lava",
             "Rain HC", "White Hot", "Black Hot"],
            "Iron",
            font
        )
        thermal_layout.addLayout(palette_layout)

        thermal_btn_layout = QHBoxLayout()

        self._thermal_auto_calibration_checkbox = QCheckBox("Разрешить автоматическую калибровку")
        self._thermal_auto_calibration_checkbox.setChecked(True)

        thermal_btn_layout.addWidget(self._thermal_auto_calibration_checkbox)
        thermal_btn_layout.addStretch()

        calib_button = QPushButton("Ручная калибровка")
        calib_button.setFixedWidth(self.FIELD_WIDTH)
        calib_button.setFixedHeight(self.FIELD_HEIGHT)

        thermal_btn_layout.addWidget(calib_button)
        thermal_layout.addLayout(thermal_btn_layout)

        container_layout.addWidget(thermal_group)
        container_layout.addStretch()

        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll.setFrameShape(QFrame.NoFrame)
        scroll.setWidget(container)

        layout.addWidget(scroll)
        self._tab_widget.addTab(tab, "Камеры")

    def _create_heater_tab(self, font):
        tab = QWidget()
        layout = QVBoxLayout(tab)

        container = QWidget()
        container_layout = QVBoxLayout(container)
        container_layout.setSpacing(self.WIDGET_SPACING)

        connect_group = self._create_group_box(
            "Параметры подключения к контроллеру нагревателя", font
        )
        connect_layout = QVBoxLayout(connect_group)
        connect_layout.setSpacing(self.LAYOUT_SPACING_LARGE)

        self._heater_auto_connect_checkbox = QCheckBox(
            "Автопоиск и подключение (рекомендуется)"
        )
        self._heater_auto_connect_checkbox.setFont(font)
        self._heater_auto_connect_checkbox.setChecked(True)
        connect_layout.addWidget(self._heater_auto_connect_checkbox)

        com_layout, self._heater_com_combo = self._create_combo_row(
            "COM-порт:",
            ["COM1", "COM2", "COM3", "COM4", "COM5", "COM6"],
            "COM1",
            font
        )
        self._heater_com_combo.setEnabled(False)
        connect_layout.addLayout(com_layout)

        baud_layout, self._heater_baud_combo = self._create_combo_row(
            "Скорость соединения, бод/с:",
            ["9600", "19200", "38400", "57600", "115200"],
            "115200",
            font
        )
        self._heater_baud_combo.setEnabled(False)
        connect_layout.addLayout(baud_layout)

        status_row_layout = QHBoxLayout()
        status_row_layout.setSpacing(self.LAYOUT_SPACING_SMALL)

        self._heater_connect_indicator = self._create_indicator()
        self._set_indicator_status(
            self._heater_connect_indicator,
            self.INDICATOR_DISCONNECTED
        )
        status_row_layout.addWidget(self._heater_connect_indicator)

        self._heater_connect_status = QLabel("Контроллер не найден")
        self._heater_connect_status.setFont(font)
        status_row_layout.addWidget(self._heater_connect_status)

        status_row_layout.addStretch()

        self._heater_connect_button = QPushButton("Подключить")
        self._heater_connect_button.setFixedHeight(self.FIELD_HEIGHT)
        self._heater_connect_button.setFixedWidth(self.FIELD_WIDTH)
        self._heater_connect_button.setEnabled(False)
        status_row_layout.addWidget(self._heater_connect_button)

        connect_layout.addLayout(status_row_layout)

        container_layout.addWidget(connect_group)

        info_group = self._create_group_box("Информация о нагревателе", font)
        info_layout = QVBoxLayout(info_group)
        info_layout.setSpacing(self.LAYOUT_SPACING_SMALL)

        rev_layout, self._heater_revision_info = self._create_info_row(
            "Ревизия нагревательного узла:", "Rev. 2", font
        )
        info_layout.addLayout(rev_layout)

        lamps_layout, self._heater_lamps_info = self._create_info_row(
            "Количество нагревательных элементов (ламп):", "4", font
        )
        info_layout.addLayout(lamps_layout)

        power_layout, self._heater_power_info = self._create_info_row(
            "Общая мощность нагревателя:", "2000 Вт", font
        )
        info_layout.addLayout(power_layout)

        firmware_layout, self._heater_firmware_info = self._create_info_row(
            "Версия прошивки контроллера нагревателя:", "0.1.0", font
        )
        info_layout.addLayout(firmware_layout)

        container_layout.addWidget(info_group)

        warning_group = self._create_group_box("Внимание", font)
        warning_layout = QVBoxLayout(warning_group)
        warning_layout.setSpacing(self.LAYOUT_SPACING_SMALL)

        warning_label = QLabel(
            "⚠️ Не направляйте прибор на людей и легковоспламеняющиеся предметы.\n\n"
            "Нагревательные лампы работают только когда оба предохранительных выключателя нажаты."
        )
        warning_label.setFont(font)
        warning_label.setWordWrap(True)
        warning_label.setStyleSheet("color: palette(text);")
        warning_layout.addWidget(warning_label)

        container_layout.addWidget(warning_group)

        test_group = self._create_group_box("Тестирование нагревателя", font)
        test_layout = QVBoxLayout(test_group)
        test_layout.setSpacing(self.LAYOUT_SPACING_LARGE)

        test_status_row_layout = QHBoxLayout()
        test_status_row_layout.setSpacing(self.LAYOUT_SPACING_SMALL)
        test_status_row_layout.addStretch()

        test_status_label = QLabel("Состояние нагревателя: ")
        test_status_label.setFont(font)
        test_status_row_layout.addWidget(test_status_label)

        self._heater_test_indicator = self._create_indicator()
        self._set_indicator_status(
            self._heater_test_indicator,
            self.INDICATOR_OFF
        )

        test_status_row_layout.addWidget(self._heater_test_indicator)

        self._heater_test_status = QLabel("Выключен")
        self._heater_test_status.setFont(font)

        test_status_row_layout.addWidget(self._heater_test_status)
        test_status_row_layout.addStretch()

        test_layout.addLayout(test_status_row_layout)

        buttons_layout = QHBoxLayout()
        buttons_layout.setSpacing(self.WIDGET_SPACING)

        buttons_layout.addStretch()

        self._heater_power_off_button = QPushButton("Выключить нагрев")
        self._heater_power_off_button.setMinimumSize(self.HEATER_BUTTON_SIZE)
        buttons_layout.addWidget(self._heater_power_off_button)

        self._heater_power_on_button = QPushButton("Включить нагрев")
        self._heater_power_on_button.setMinimumSize(self.HEATER_BUTTON_SIZE)
        buttons_layout.addWidget(self._heater_power_on_button)

        buttons_layout.addStretch()

        test_layout.addLayout(buttons_layout)

        container_layout.addWidget(test_group)
        container_layout.addStretch()

        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll.setFrameShape(QFrame.NoFrame)
        scroll.setWidget(container)

        layout.addWidget(scroll)
        self._tab_widget.addTab(tab, "Нагреватель")

    def _create_interface_tab(self, font):
        tab = QWidget()
        layout = QVBoxLayout(tab)

        container = QWidget()
        container_layout = QVBoxLayout(container)
        container_layout.setSpacing(self.WIDGET_SPACING)

        lang_group = self._create_group_box("Язык", font)
        lang_layout = QVBoxLayout(lang_group)
        lang_layout.setSpacing(self.LAYOUT_SPACING_LARGE)

        lang_row_layout, self._language_combo = self._create_combo_row(
            "Язык интерфейса:",
            ["Русский"],
            "Русский",
            font
        )
        lang_layout.addLayout(lang_row_layout)

        container_layout.addWidget(lang_group)

        other_group = self._create_group_box("Прочие настройки", font)
        other_layout = QVBoxLayout(other_group)
        other_layout.setSpacing(self.LAYOUT_SPACING_LARGE)

        self._auto_fill_checkbox = QCheckBox("Автозаполнение стартовой формы")
        self._auto_fill_checkbox.setFont(font)
        self._auto_fill_checkbox.setChecked(
            getattr(self._settings, 'auto_fill_forms', False)
        )
        other_layout.addWidget(self._auto_fill_checkbox)

        self._osk_checkbox = QCheckBox("Автоматическое открытие экранной клавиатуры")
        self._osk_checkbox.setFont(font)
        self._osk_checkbox.setChecked(True)
        other_layout.addWidget(self._osk_checkbox)

        self._confirm_checkbox = QCheckBox(
            "Запрашивать подтверждение перед завершением контроля"
        )
        self._confirm_checkbox.setFont(font)
        self._confirm_checkbox.setChecked(True)
        other_layout.addWidget(self._confirm_checkbox)

        container_layout.addWidget(other_group)
        container_layout.addStretch()

        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll.setFrameShape(QFrame.NoFrame)
        scroll.setWidget(container)

        layout.addWidget(scroll)
        self._tab_widget.addTab(tab, "Интерфейс")

    def _create_group_box(self, title, font):
        group = QGroupBox(title)
        group.setFont(font)
        group.setStyleSheet(self.GROUP_BOX_STYLE)
        return group

    def _load_settings(self):
        # TODO: загрузить настройки в UI элементы
        pass

    def _save_settings(self):
        if not self._validate_settings():
            return

        try:
            # TODO: сохранить настройки из UI элементов
            self._settings.save_to_file()

            QMessageBox.information(
                self,
                "Настройки сохранены",
                "Все настройки успешно сохранены.\n"
                "Некоторые изменения могут вступить в силу после перезапуска приложения."
            )
            self.close()
        except Exception as e:
            QMessageBox.critical(
                self,
                "Ошибка сохранения",
                f"Не удалось сохранить настройки:\n{e}"
            )

    def _validate_settings(self):
        # TODO: валидация
        return True

    def _reset_settings(self):
        reply = QMessageBox.question(
            self,
            "Сброс настроек",
            "Вы уверены, что хотите сбросить все настройки к значениям по умолчанию?",
            QMessageBox.Yes | QMessageBox.No,
            QMessageBox.No
        )

        if reply == QMessageBox.Yes:
            # TODO: сброс настроек
            QMessageBox.information(
                self,
                "Настройки сброшены",
                "Все настройки сброшены к значениям по умолчанию."
            )
            self._load_settings()


if __name__ == "__main__":
    from PySide6.QtWidgets import QApplication
    import sys
    app = QApplication(sys.argv)
    window = SettingsWindow(Settings.load_from_file())
    window.show()
    sys.exit(app.exec())