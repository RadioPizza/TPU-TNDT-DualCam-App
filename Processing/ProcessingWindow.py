from PySide6.QtCore import Qt, QSize, QObject, Signal, Slot, QTimer, QEvent
from PySide6.QtWidgets import (
    QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
    QLabel, QPushButton, QFrame, QSplitter, QSlider,
    QListWidget, QListWidgetItem, QCheckBox, QMenuBar,
    QMenu, QStatusBar, QScrollArea, QGroupBox, QSpacerItem,
    QSizePolicy, QToolButton, QButtonGroup, QFileDialog, QMessageBox, QDoubleSpinBox,
    QDialog, QVBoxLayout, QComboBox, QDialogButtonBox, QSpinBox, QApplication, QToolTip,
)
from PySide6.QtGui import QAction, QFont, QImage, QPixmap
import numpy as np
import cv2
from typing import List, Optional, Tuple, Dict, Any
from scipy.io import savemat
from pickle import dump as pickle_dump, load as pickle_load
import matplotlib.pyplot as plt
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure

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



# view
class ProcessingWindow(QMainWindow):
    """Окно постобработки термограмм (только интерфейс)."""

    # Константы размеров (можно дополнить из ui_constants)
    MIN_WIDTH = 1024
    MIN_HEIGHT = 600
    LEFT_PANEL_DEFAULT_RATIO = 65  # %
    RIGHT_PANEL_DEFAULT_RATIO = 35  # %

    def __init__(self, pipeline, parent=None):
        super().__init__(parent)
        self.pipeline = pipeline
        self._setup_window_properties()
        self._create_widgets()
        self._setup_layout()
        self._setup_menu_bar()
        self._setup_status_bar()

    def _setup_window_properties(self):
        """Настройка свойств окна."""
        self.setWindowTitle("TPU-TNDT-DualCam-App - Обработка")
        self.setMinimumSize(self.MIN_WIDTH, self.MIN_HEIGHT)

    def _create_widgets(self):
        """Создание всех виджетов интерфейса."""
        # Центральный виджет
        self._central_widget = QWidget()
        self.setCentralWidget(self._central_widget)

        # Главный сплиттер (левая/правая панели)
        self._main_splitter = QSplitter(Qt.Horizontal)
        self._main_splitter.setHandleWidth(2)
        self._main_splitter.setChildrenCollapsible(False)

        # Левая панель (визуализация + таймлайн)
        self._left_panel = self._create_left_panel()

        # Правая панель (боковая панель с пайплайном и управлением)
        self._right_panel = self._create_right_panel()

        # Добавляем панели в сплиттер
        self._main_splitter.addWidget(self._left_panel)
        self._main_splitter.addWidget(self._right_panel)

        # Устанавливаем начальные размеры (проценты)
        total_width = self.width()
        left_width = int(total_width * self.LEFT_PANEL_DEFAULT_RATIO / 100)
        right_width = total_width - left_width
        self._main_splitter.setSizes([left_width, right_width])

    def _create_left_panel(self) -> QWidget:
        """Создаёт левую панель (монитор, кнопки, таймлайн)."""
        panel = QWidget()
        layout = QVBoxLayout(panel)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(WIDGET_SPACING)

        # ----- Область предпросмотра (Monitor panel) -----
        self._monitor_frame = QFrame()
        self._monitor_frame.setFrameShape(QFrame.Box)
        self._monitor_frame.setLineWidth(1)
        self._monitor_frame.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)

        # Горизонтальный макет внутри фрейма
        monitor_hbox = QHBoxLayout(self._monitor_frame)
        monitor_hbox.setContentsMargins(2, 0.3, 2, 0.3)
        monitor_hbox.setSpacing(2)

        # Растяжка слева (чтобы блок изображение+шкала центрировался по горизонтали)
        monitor_hbox.addStretch()

        # ----- Изображение -----
        self._monitor_label = QLabel("Область предпросмотра")
        self._monitor_label.setAlignment(Qt.AlignCenter)
        self._monitor_label.setFont(fonts['large'])
        self._monitor_label.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        monitor_hbox.addWidget(self._monitor_label)

        monitor_hbox.setSpacing(70)

        # ----- Контейнер для колорбара и подписей -----
        colorbar_container = QWidget()
        colorbar_layout = QHBoxLayout(colorbar_container)
        colorbar_layout.setContentsMargins(0, 0, 0, 0)
        colorbar_layout.setSpacing(2)

        # Колорбар (вертикальный)
        self._colorbar_label = QLabel()
        self._colorbar_label.setAlignment(Qt.AlignLeft)
        self._colorbar_label.setFixedWidth(25)
        self._colorbar_label.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        colorbar_layout.addWidget(self._colorbar_label)

        # Вертикальные подписи справа от колорбара
        self._colorbar_marks = QWidget()
        marks_layout = QVBoxLayout(self._colorbar_marks)
        marks_layout.setContentsMargins(0, 0, 0, 0)
        marks_layout.setSpacing(0)
        self._colorbar_max_label = QLabel("0")
        self._colorbar_max_label.setAlignment(Qt.AlignCenter)
        self._colorbar_max_label.setFont(fonts['small'])
        self._colorbar_min_label = QLabel("0")
        self._colorbar_min_label.setAlignment(Qt.AlignCenter)
        self._colorbar_min_label.setFont(fonts['small'])
        marks_layout.addWidget(self._colorbar_max_label)
        marks_layout.addStretch()
        marks_layout.addWidget(self._colorbar_min_label)
        colorbar_layout.addWidget(self._colorbar_marks)

        monitor_hbox.addWidget(colorbar_container)

        # Растяжка справа
        monitor_hbox.addStretch()

        layout.addWidget(self._monitor_frame, stretch=3)

        # ----- Середина: панель инструментов (Buttons panel) -----
        self._toolbar_frame = QFrame()
        self._toolbar_frame.setFrameShape(QFrame.NoFrame)
        toolbar_layout = QHBoxLayout(self._toolbar_frame)
        toolbar_layout.setContentsMargins(5, 5, 5, 5)
        toolbar_layout.setSpacing(LAYOUT_SPACING)

        # Кнопки управления воспроизведением (пример)
        self._play_button = QToolButton()
        self._play_button.setText("▶")
        self._play_button.setFixedSize(BUTTON_SIZE)

        self._pause_button = QToolButton()
        self._pause_button.setText("⏸")
        self._pause_button.setFixedSize(BUTTON_SIZE)

        self._stop_button = QToolButton()
        self._stop_button.setText("⏹")
        self._stop_button.setFixedSize(BUTTON_SIZE)

        self._step_forward_button = QToolButton()
        self._step_forward_button.setText("⏩")
        self._step_forward_button.setFixedSize(BUTTON_SIZE)

        self._step_backward_button = QToolButton()
        self._step_backward_button.setText("⏪")
        self._step_backward_button.setFixedSize(BUTTON_SIZE)

        # Группируем для удобства
        toolbar_layout.addWidget(self._play_button)
        toolbar_layout.addWidget(self._pause_button)
        toolbar_layout.addWidget(self._stop_button)
        toolbar_layout.addWidget(self._step_backward_button)
        toolbar_layout.addWidget(self._step_forward_button)

        toolbar_layout.addStretch()

        self.fps_label = QLabel("Кадров в секунду:")
        self.fps_label.setFont(fonts['small'])
        self.fps_spinbox = QDoubleSpinBox()
        self.fps_spinbox.setRange(1.0, 120.0)
        self.fps_spinbox.setSingleStep(1.0)
        self.fps_spinbox.setValue(10.0) # начальное значение, синхронизируется с presenter
        self.fps_spinbox.setFixedWidth(80)
        self.fps_spinbox.setFont(fonts['small'])
        toolbar_layout.addStretch()
        toolbar_layout.addWidget(self.fps_label)
        toolbar_layout.addWidget(self.fps_spinbox)

        layout.addWidget(self._toolbar_frame, stretch=0)

        # ----- Низ: панель таймлайна (Timeline panel) -----
        self._timeline_frame = QFrame()
        self._timeline_frame.setFrameShape(QFrame.NoFrame)
        timeline_layout = QVBoxLayout(self._timeline_frame)
        timeline_layout.setContentsMargins(5, 5, 5, 5)
        timeline_layout.setSpacing(LAYOUT_SPACING)

        # Ползунок времени
        self._time_slider = QSlider(Qt.Horizontal)
        self._time_slider.setRange(0, 0)
        self._time_slider.setValue(0)
        self._time_slider.setTickPosition(QSlider.TicksBelow)
        self._time_slider.setTickInterval(1)

        # Метки времени (начало/конец)
        time_labels_layout = QHBoxLayout()
        self._start_time_label = QLabel("0")
        self._start_time_label.setFont(fonts['small'])
        self._start_time_label.setAlignment(Qt.AlignLeft)
        self._end_time_label = QLabel("1")
        self._end_time_label.setFont(fonts['small'])
        self._end_time_label.setAlignment(Qt.AlignRight)
        self.frame_index_label = QLabel("0")
        self.frame_index_label.setFont(fonts['small'])
        self.frame_index_label.setAlignment(Qt.AlignmentFlag.AlignHCenter)

        time_labels_layout.addWidget(self._start_time_label)
        time_labels_layout.addStretch()
        time_labels_layout.addWidget(self.frame_index_label)
        time_labels_layout.addStretch()
        time_labels_layout.addWidget(self._end_time_label)

        timeline_layout.addWidget(self._time_slider)
        timeline_layout.addLayout(time_labels_layout)

        layout.addWidget(self._timeline_frame, stretch=1)

        return panel

    def _create_right_panel(self) -> QWidget:
        """Создаёт правую боковую панель (Pipeline + Control)."""
        panel = QWidget()
        layout = QVBoxLayout(panel)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(WIDGET_SPACING)

        # ----- Верх: панель пайплайна (Pipeline panel) -----
        self._pipeline_group = QGroupBox("Пайплайн обработки")
        self._pipeline_group.setFont(fonts['medium'])
        self._pipeline_group.setStyleSheet(GROUP_BOX_STYLE)

        pipeline_layout = QVBoxLayout(self._pipeline_group)
        pipeline_layout.setSpacing(LAYOUT_SPACING)

        # Кнопка добавления нового этапа
        self._add_stage_button = QPushButton()
        self._add_stage_button.setText("+ Добавить этап")
        self._add_stage_button.setFixedSize(QSize(150, FIELD_HEIGHT))
        self._add_stage_button.setFont(fonts['regular'])
        pipeline_layout.addWidget(self._add_stage_button)


        # Контейнер для списка этапов (скроллируемый)
        self._stages_scroll = QScrollArea()
        self._stages_scroll.setWidgetResizable(True)
        self._stages_scroll.setFrameShape(QFrame.NoFrame)

        self._stages_container = QWidget()
        self._stages_layout = QVBoxLayout(self._stages_container)
        self._stages_layout.setContentsMargins(0, 0, 0, 0)
        self._stages_layout.setSpacing(LAYOUT_SPACING)
        self._stages_layout.addStretch()  # чтобы элементы прижимались к верху

        self._stages_scroll.setWidget(self._stages_container)
        pipeline_layout.addWidget(self._stages_scroll)

        layout.addWidget(self._pipeline_group, stretch=1)

        # ----- Низ: панель управления (Control panel) -----
        self._control_group = QGroupBox("Управление")
        self._control_group.setFont(fonts['medium'])
        self._control_group.setStyleSheet(GROUP_BOX_STYLE)

        control_layout = QVBoxLayout(self._control_group)
        control_layout.setSpacing(LAYOUT_SPACING)

        # Кнопка "Применить ко всей серии" (default)
        self._apply_button = QPushButton("Применить ко всей серии")
        self._apply_button.setDefault(True)
        self._apply_button.setFixedHeight(FIELD_HEIGHT)
        self._apply_button.setFont(fonts['regular'])
        control_layout.addWidget(self._apply_button)

        # Добавим растяжку сверху, чтобы кнопки были снизу (если группа маленькая)
        control_layout.addStretch()

        layout.addWidget(self._control_group, stretch=0)

        return panel

    def _setup_layout(self):
        """Размещение главного сплиттера в центральном виджете."""
        main_layout = QVBoxLayout(self._central_widget)
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.setSpacing(0)
        main_layout.addWidget(self._main_splitter)

    def _setup_menu_bar(self):
        """Создание строки меню."""
        menubar = self.menuBar()

        # ----- Меню "Файл" -----
        file_menu = menubar.addMenu("Файл")

        self.open_action = QAction("Открыть", self)
        self.open_action.setShortcut("Ctrl+O")
        file_menu.addAction(self.open_action)

        self.import_pipeline_action = QAction("Импортировать пайплайн обработки", self)
        file_menu.addAction(self.import_pipeline_action)

        file_menu.addSeparator()

        self.export_npy_action = QAction("Экспорт в .npy", self)
        file_menu.addAction(self.export_npy_action)

        self.export_mat_action = QAction("Экспорт в .mat", self)
        file_menu.addAction(self.export_mat_action)

        self.export_pipeline_action = QAction("Экспортировать пайплайн обработки", self)
        file_menu.addAction(self.export_pipeline_action)

        self.keep_initial_data_action = QAction("Хранение исходных данных в оперативной памяти", self)
        self.keep_initial_data_action.setCheckable(True)
        self.keep_initial_data_action.setChecked(False)
        file_menu.addAction(self.keep_initial_data_action)

        # ----- Меню "Изменить" -----
        edit_menu = menubar.addMenu("Изменить")

        self.undo_action = QAction("Отменить", self)
        self.undo_action.setShortcut("Ctrl+Z")
        edit_menu.addAction(self.undo_action)

        self.redo_action = QAction("Повторить", self)
        edit_menu.addAction(self.redo_action)

        # ----- Меню "Просмотр" -----
        view_menu = menubar.addMenu("Просмотр")

        palette_menu = view_menu.addMenu("Палитра")
        self.palette_default = QAction("По умолчанию", self)
        self.palette_gray = QAction("Градации серого", self)
        self.palette_iron = QAction("Каление железа", self)

        palette_menu.addAction(self.palette_default)
        palette_menu.addAction(self.palette_gray)
        palette_menu.addAction(self.palette_iron)

        self.toggle_on_mouse_value_action = QAction("Показывать значение при наведении курсора", self)
        self.toggle_on_mouse_value_action.setCheckable(True)
        self.toggle_on_mouse_value_action.setChecked(False)
        view_menu.addAction(self.toggle_on_mouse_value_action)

        # ----- Меню "Окно" -----
        window_menu = menubar.addMenu("Окно")

        self.toggle_colorbar_action = QAction("Колорбар", self)
        self.toggle_colorbar_action.setCheckable(True)
        self.toggle_colorbar_action.setChecked(False)
        window_menu.addAction(self.toggle_colorbar_action)

        # ----- Меню "Справка" -----
        help_menu = menubar.addMenu("Справка")

        self.about_action = QAction("О программе...", self)
        help_menu.addAction(self.about_action)

    def _setup_status_bar(self):
        """Создание строки состояния."""
        status_bar = QStatusBar()
        self.setStatusBar(status_bar)

        # Информационная метка
        self.status_label = QLabel("Готов к обработке")
        self.status_label.setFont(fonts['small'])
        status_bar.addWidget(self.status_label, stretch=1)

        #self._resources_label = QLabel("CPU: 12% | RAM: 4.2 ГБ")
        #self._resources_label.setFont(fonts['small'])
        #status_bar.addWidget(self._resources_label)