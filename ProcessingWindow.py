"""
Модуль окна обработки термограмм (View).
Содержит только интерфейс, без логики.
"""

from PySide6.QtCore import Qt, QSize, QObject, Signal, Slot, QTimer
from PySide6.QtWidgets import (
    QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
    QLabel, QPushButton, QFrame, QSplitter, QSlider,
    QListWidget, QListWidgetItem, QCheckBox, QMenuBar,
    QMenu, QStatusBar, QScrollArea, QGroupBox, QSpacerItem,
    QSizePolicy, QToolButton, QButtonGroup, QFileDialog, QMessageBox, QDoubleSpinBox,
    QDialog, QVBoxLayout, QComboBox, QDialogButtonBox, QSpinBox
)
from PySide6.QtGui import QAction, QFont, QImage, QPixmap
from thermograms.thermograms import loadfile, Timage, Tseries, CAM_K
import numpy as np
import cv2
from typing import List, Optional, Tuple, Dict, Any

# Импорт единых шрифтов и констант (предполагается наличие модулей)
try:
    from ui_fonts import fonts  # словарь с QFont, например fonts['regular'], fonts['small']
    from ui_constants import (
        LAYOUT_SPACING, WIDGET_SPACING, FIELD_HEIGHT,
        BUTTON_SIZE, GROUP_BOX_STYLE, TAB_BAR_STYLE
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
    TAB_BAR_STYLE = ""


need_to_apply = np.zeros((1080, 1920, 3), dtype=np.uint8)
# Параметры текста
text = """You need to apply methods to series first"""
font = cv2.FONT_HERSHEY_SIMPLEX
font_scale = 2.5
color = (255, 255, 255)  # белый
thickness = 3
# Размеры текста для центрирования
(text_w, text_h), baseline = cv2.getTextSize(text, font, font_scale, thickness)
# Координаты центра
x = (need_to_apply.shape[1] - text_w) // 2
y = (need_to_apply.shape[0] + text_h) // 2
# Наносим текст
cv2.putText(need_to_apply, text, (x, y), font, font_scale, color, thickness)
need_to_apply = need_to_apply[..., 0]

FPS = 30 # TODO

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

        # ----- Верх: область предпросмотра (Monitor panel) -----
        self._monitor_frame = QFrame()
        self._monitor_frame.setFrameShape(QFrame.Box)
        self._monitor_frame.setLineWidth(1)
        self._monitor_frame.setMinimumHeight(300)
        self._monitor_frame.setSizePolicy(
            QSizePolicy.Expanding, QSizePolicy.Expanding
        )

        # Внутри можно разместить заглушку
        monitor_layout = QVBoxLayout(self._monitor_frame)
        self._monitor_label = QLabel("Область предпросмотра")
        self._monitor_label.setAlignment(Qt.AlignCenter)
        self._monitor_label.setFont(fonts['large'])
        monitor_layout.addWidget(self._monitor_label)

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

        self.scale_label = QLabel("Масштаб:")
        self.scale_label.setFont(fonts['small'])
        self.scale_spinbox = QDoubleSpinBox()
        self.scale_spinbox.setRange(0.5, 10.0)
        self.scale_spinbox.setSingleStep(0.5)
        self.scale_spinbox.setValue(4.0) # начальное значение, синхронизируется с presenter
        self.scale_spinbox.setFixedWidth(80)
        self.scale_spinbox.setFont(fonts['small'])
        toolbar_layout.addStretch()
        toolbar_layout.addWidget(self.scale_label)
        toolbar_layout.addWidget(self.scale_spinbox)

        layout.addWidget(self._toolbar_frame, stretch=0)

        # ----- Низ: панель таймлайна (Timeline panel) -----
        self._timeline_frame = QFrame()
        self._timeline_frame.setFrameShape(QFrame.NoFrame)
        timeline_layout = QVBoxLayout(self._timeline_frame)
        timeline_layout.setContentsMargins(5, 5, 5, 5)
        timeline_layout.setSpacing(LAYOUT_SPACING)

        # Ползунок времени
        self._time_slider = QSlider(Qt.Horizontal)
        self._time_slider.setRange(0, 100)
        self._time_slider.setValue(0)
        self._time_slider.setTickPosition(QSlider.TicksBelow)
        self._time_slider.setTickInterval(1)

        # Метки времени (начало/конец)
        time_labels_layout = QHBoxLayout()
        self._start_time_label = QLabel("0 %")
        self._start_time_label.setFont(fonts['small'])
        self._end_time_label = QLabel("100 %")
        self._end_time_label.setFont(fonts['small'])
        self._end_time_label.setAlignment(Qt.AlignRight)

        time_labels_layout.addWidget(self._start_time_label)
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

        # Кнопка "Экспорт" (изначально неактивна)
        self._export_button = QPushButton("Экспорт")
        self._export_button.setEnabled(False)
        self._export_button.setFixedHeight(FIELD_HEIGHT)
        self._export_button.setFont(fonts['regular'])
        control_layout.addWidget(self._export_button)

        # Добавим растяжку сверху, чтобы кнопки были снизу (если группа маленькая)
        control_layout.addStretch()

        layout.addWidget(self._control_group, stretch=0)

        return panel

    def _add_demo_stage(self, number: int, name: str, checked: bool):
        """Вспомогательный метод для добавления демо-этапа пайплайна."""
        stage_widget = QWidget()
        stage_layout = QHBoxLayout(stage_widget)
        stage_layout.setContentsMargins(0, 0, 0, 0)
        stage_layout.setSpacing(5)

        # Порядковый номер
        number_label = QLabel(f"{number}. {name}")
        number_label.setAlignment(Qt.AlignLeft)
        number_label.setFont(fonts['regular'])
        stage_layout.addWidget(number_label)

        # Кнопка удаления
        delete_button = QToolButton()
        delete_button.setText("✕")
        stage_layout.addWidget(delete_button)

        self._stages_layout.insertWidget(self._stages_layout.count() - 1, stage_widget)

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

        self.preprocess_action = QAction("Предзагрузка изображений", self)
        view_menu.addAction(self.preprocess_action)

        # ----- Меню "Окно" -----
        window_menu = menubar.addMenu("Окно")

        self.toggle_timeline_action = QAction("Таймлайн", self)
        self.toggle_timeline_action.setCheckable(True)
        self.toggle_timeline_action.setChecked(True)
        window_menu.addAction(self.toggle_timeline_action)

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

        # Дополнительная информация о ресурсах (заглушка)
        self._resources_label = QLabel("CPU: 12% | RAM: 4.2 ГБ")
        self._resources_label.setFont(fonts['small'])
        status_bar.addWidget(self._resources_label)



class PipelineManager:
    def __init__(self):
        self.stages = []  # [(method_idx, params)]
        self.methods = [ # self.methods[method_idx] = {'name', 'params': [(name, variable name, default value)], 'req_series', 'Timage', 'Tseries'}
            {
                'name': 'Медианное размытие',
                'params': [('Радиус', 3)],
                'req_series': False,
                'Timage': lambda t, radius: t.median_blur(radius),
                'Tseries': lambda t, radius: t.median_blur(radius),
            },
            {
                'name': 'Размытие по Гауссу',
                'params': [('Радиус', 3), ('Ст. отклонение', 1)],
                'req_series': False,
                'Timage': lambda t, radius, stddev: t.gaussian_blur(stddev, radius),
                'Tseries': lambda t, radius, stddev: t.gaussian_blur(stddev, radius),
            },
            {
                'name': 'Увеличение резкости',
                'params': [('Радиус', 3), ('Ст. отклонение', 1)],
                'req_series': False,
                'Timage': lambda t, radius, stddev: t.sharpness(radius, stddev),
                'Tseries': lambda t, radius, stddev: t.sharpness(radius, stddev),
            },
            {
                'name': 'Исправление искажений',
                'params': [],
                'req_series': False,
                'Timage': lambda t, radius: t.distorted(self, CAM_K, scale=1.15),
                'Tseries': lambda t, radius: t.distorted(self, CAM_K, scale=1.15),
            },
            #{
            #    'name': 'Аффинные преобразования',
            #    'params': [],
            #    'req_series': False,
            #    'Timage': lambda t, radius: t.median_blur(radius),
            #    'Tseries': lambda t, radius: t.median_blur(radius),
            #},
            {
                'name': 'Обрезка',
                'params': [('Строка начала', 0), ('Строка конца (не включ.)', -1), ('Столбец начала', 0), ('Столбец конца (не включ.)', -1)],
                'req_series': False,
                'Timage': lambda t, i0, i1, j0, j1: t[i0:i1, j0:j1],
                'Tseries': lambda t, i0, i1, j0, j1: t[i0:i1, j0:j1],
            },
            {
                'name': 'Обрезка по времени',
                'params': [('Кадр начала', 0), ('Кадр конца (не включ.)', -1)],
                'req_series': True,
                'Tseries': lambda t, frame0, frame1: t[..., frame0: frame1],
            },
            {
                'name': 'Карта отклонений',
                'params': [],
                'req_series': True,
                'Tseries': lambda t: t.std_map(),
            },
            {
                'name': 'Усреднение по времени',
                'params': [('Кадры', 3)],
                'req_series': True,
                'Tseries': lambda t, frames: t.avg_time(frames),
            },
            {
                'name': 'Быстрое преобразование Фурье: вещественная часть',
                'params': [],
                'req_series': True,
                'Tseries': lambda t: Tseries(array=t.fft().real),
            },
            {
                'name': 'Быстрое преобразование Фурье: мнимая часть',
                'params': [],
                'req_series': True,
                'Tseries': lambda t: Tseries(array=t.fft().imag),
            },
            {
                'name': 'Метод главных компонент',
                'params': [('Количество компонент', 4)],
                'req_series': True,
                'Tseries': lambda t, n_components: Tseries(array=t.pca(n_components)),
            }
        ]

    def add_stage(self, method_idx: str, params: Dict[str, Any]):
        self.stages.append((method_idx, params))

    def remove_stage(self, index: int):
        if 0 <= index < len(self.stages):
            del self.stages[index]

    def clear(self):
        self.stages.clear()

    def apply_to_frame(self, frame: Timage) -> Timage:
        """Применить все этапы к одному кадру (пример)."""
        result = frame
        
        for method_idx, params in self.stages:
            if self.methods[method_idx]['req_series']: return Timage(array=need_to_apply)
            result = self.methods[method_idx]['Timage'](result, *params)
        
        return result

    def apply_to_series(self, frames: Tseries) -> Tseries:
        """Применить пайплайн ко всем кадрам."""
        result = frames

        for method_idx, params in self.stages:
            result = self.methods[method_idx]['Tseries'](result, *params)

        return result


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
    

class ProcessingPresenter(QObject):
    """
    Презентер для окна обработки термограмм.
    Управляет взаимодействием между View (ProcessingWindow) и Model (термограммы, пайплайн).
    """

    # Сигналы, которые может эмитировать презентер для уведомления view
    frame_updated = Signal(np.ndarray)           # новый кадр для отображения
    time_range_changed = Signal(float, float)    # начало/конец времени (в секундах)
    current_time_changed = Signal(float)         # текущее время
    pipeline_changed = Signal(list)              # список этапов для отображения
    status_message = Signal(str)                 # сообщение в строку состояния
    processing_finished = Signal()

    figsize_scale = 4
    _preprocessed_output = None
    _data = Tseries(array=np.zeros((1, 1, 1), dtype=np.float32))
    colorbar = False

    _is_playing = False
    _current_frame_index = 0
    _current_frame = None

    def __init__(self, view: ProcessingWindow):
        """
        :param view: экземпляр ProcessingWindow
        :param data_model: модель данных термограмм (если None, будет создана пустая)
        :param pipeline_model: менеджер пайплайна (если None, будет создан новый)
        """
        super().__init__()
        self._view = view
        self._pipeline: PipelineManager = self._view.pipeline

        # Таймер для воспроизведения
        self._playback_timer = QTimer()
        self._playback_timer.setInterval(1000 // FPS)
        self._playback_timer.timeout.connect(self._on_playback_timer)

        # Инициализация соединений и начального состояния
        self._connect_signals()
        self._view.scale_spinbox.blockSignals(True)
        self._view.scale_spinbox.setValue(self.figsize_scale)
        self._view.scale_spinbox.blockSignals(False)
        self._update_ui_from_model()

    # ---------- Инициализация соединений ----------
    def _connect_signals(self):
        """Подключает сигналы из view к слотам презентера."""
        # Сигналы
        self.frame_updated.connect(self.on_frame_updated)
        self.status_message.connect(self.status_label_set_text)

        # Кнопки управления
        self._view._play_button.clicked.connect(self.on_play_clicked)
        self._view._pause_button.clicked.connect(self.on_pause_clicked)
        self._view._stop_button.clicked.connect(self.on_stop_clicked)
        self._view._step_forward_button.clicked.connect(self.on_step_forward)
        self._view._step_backward_button.clicked.connect(self.on_step_backward)
        self._view.scale_spinbox.valueChanged.connect(self.on_scale_changed)
        self._view._add_stage_button.clicked.connect(self.on_add_stage_clicked)

        # Ползунок времени
        self._view._time_slider.valueChanged.connect(self.on_slider_value_changed)

        # Кнопки управления
        self._view._apply_button.clicked.connect(self.on_apply_pipeline)
        self._view._export_button.clicked.connect(self.on_export_clicked)

        self._view.open_action.triggered.connect(self.on_open_file)
        self._view.preprocess_action.triggered.connect(self.on_preprocess)
        self._view.toggle_colorbar_action.toggled.connect(self.on_toggle_colorbar)

    # ---------- Слоты для пользовательских действий ----------
    @Slot(str)
    def status_label_set_text(self, text: str):
        self._view.status_label.setText(text)

    @Slot()
    def on_play_clicked(self):
        """Запуск воспроизведения."""
        if self._data.shape[2] <= 1:
            return
        self._is_playing = True
        self._playback_timer.start()

    @Slot()
    def on_pause_clicked(self):
        """Пауза."""
        self._is_playing = False
        self._playback_timer.stop()

    @Slot()
    def on_stop_clicked(self):
        """Остановка (сброс на первый кадр)."""
        self._is_playing = False
        self._playback_timer.stop()
        self.set_current_frame(0)

    @Slot()
    def on_step_forward(self):
        """Перейти к следующему кадру."""
        if self._data.shape[2] == 0:
            return
        new_index = self._current_frame_index + 1
        if new_index >= self._data.shape[2]:
            new_index = self._data.shape[2] - 1
        self.set_current_frame(new_index)

    @Slot()
    def on_step_backward(self):
        """Перейти к предыдущему кадру."""
        if self._data.shape[2] == 0:
            return
        new_index = self._current_frame_index - 1
        if new_index < 0:
            new_index = 0
        self.set_current_frame(new_index)

    @Slot(int)
    def on_slider_value_changed(self, value: int):
        """Обработка изменения ползунка времени."""
        if not self._is_playing:
            self.set_current_frame(value)

    @Slot()
    def on_apply_pipeline(self):
        """Применить текущий пайплайн к данным."""
        if self._pipeline.stages:
            self.status_message.emit("Применение пайплайна...")
            QApplication.processEvents()
            try:
                # Применить ко всем кадрам
                self._data = self._pipeline.apply_to_series(self._data)
                self._update_ui_from_model()
                self.status_message.emit("Пайплайн применён ко всей серии")
            except Exception as e:
                self.status_message.emit(f"Ошибка применения пайплайна: {e}")
            finally:
                self.processing_finished.emit()

    @Slot()
    def on_export_clicked(self):
        """Экспорт данных."""
        # Открыть диалог сохранения, выбрать формат, сохранить
        self.status_message.emit("Экспорт выполнен (заглушка)")

    @Slot()
    def on_open_file(self):
        """Открыть файл с термограммами."""
        # Открываем диалог выбора файла
        file_path, _ = QFileDialog.getOpenFileName(
            self._view,
            "Открыть файл термограмм",
            "",
            "Все поддерживаемые файлы (*.npy *.mat);;NumPy файлы (*.npy);;MATLAB файлы (*.mat);;Все файлы (*)"
        )
        if not file_path:
            return  # Пользователь отменил выбор
        
        self._preprocessed_output = None
        try:
            self.status_message.emit('Загрузка серии...')
            QApplication.processEvents() # чтобы успела появиться надпись 'Загрузка серии...' 
            frames = loadfile(file_path)

            if isinstance(frames, dict):
                for possible_key in frames.keys():
                    if isinstance(frames[possible_key], np.ndarray):
                        frames = frames[possible_key]
                        break
            
            if isinstance(frames, dict):
                raise ValueError('This dict has no array to be series')
            
            if frames is None or frames.size == 0:
                QMessageBox.warning(self._view, "Ошибка загрузки", "Файл не содержит данных")
                return
            
            self._data = Tseries(array=frames)

            self._update_ui_from_model()

            self.status_message.emit('Готов к обработке')

        except Exception as e:
            QMessageBox.critical(self._view, "Ошибка загрузки", f"Не удалось загрузить файл:\n{str(e)}")
            self.status_message.emit("Ошибка загрузки файла")
        
    @Slot()
    def on_preprocess(self):
        img = self._data[0].imshow(figsize=(self.figsize_scale, self.figsize_scale*self._data.shape[0]/self._data.shape[1]), return_=True, colorbar=self.colorbar)
        self._preprocessed_output = np.zeros(shape=(self._data.shape[2], *img.shape), dtype=img.dtype)

        for i in range(self._data.shape[2]):
            self._preprocessed_output[i] = self._data[i].imshow(figsize=(self.figsize_scale, self.figsize_scale*self._data.shape[0]/self._data.shape[1]), return_=True, colorbar=self.colorbar)
            self.status_message.emit(f'Предзагрузка изображения {i}/{self._data.shape[2]-1}...')
            QApplication.processEvents() # чтобы успела появиться надпись 'Предзагрузка изображений...' 

        self.status_message.emit('Готов к обработке')
    
    @Slot(float)
    def on_scale_changed(self, value: float):
        self.figsize_scale = value
        self._preprocessed_output = None
        
        self.set_current_frame(self._current_frame_index)

    @Slot(bool)
    def on_toggle_timeline(self, checked: bool):
        """Показать/скрыть панель таймлайна."""
        self._view._timeline_frame.setVisible(checked)

    @Slot(bool)
    def on_toggle_colorbar(self, checked: bool):
        """Показать/скрыть колорбар (если есть)."""
        self.colorbar = checked
        self._preprocessed_output = None
        
        self.set_current_frame(self._current_frame_index)

    @Slot()
    def on_about(self):
        """Показать информацию о программе."""
        self.status_message.emit("TPU-TNDT-DualCam-App v1.0")

    @Slot()
    def on_add_stage_clicked(self):
        # Диалог выбора метода
        dialog = QDialog(self._view)
        dialog.setWindowTitle("Добавить этап обработки")
        layout = QVBoxLayout(dialog)

        layout.addWidget(QLabel("Выберите метод:"))
        combo = QComboBox()
        combo.addItems([method['name'] for method in self._pipeline.methods])
        layout.addWidget(combo)

        buttons = QDialogButtonBox(QDialogButtonBox.Ok | QDialogButtonBox.Cancel)
        buttons.accepted.connect(dialog.accept)
        buttons.rejected.connect(dialog.reject)
        layout.addWidget(buttons)

        if dialog.exec() != QDialog.Accepted:
            return

        method_idx = combo.currentIndex()
        method = self._pipeline.methods[method_idx]

        # Если у метода есть параметры, запрашиваем их
        if method['params']:
            param_dialog = ParameterDialog(method['params'], self._view)
            if param_dialog.exec() != QDialog.Accepted:
                return
            param_values = param_dialog.get_values()
        else:
            param_values = []

        # Добавляем этап в пайплайн
        self._pipeline.add_stage(method_idx, param_values)

        # Обновляем UI
        self._update_pipeline_ui()
        self.status_message.emit(f"Добавлен этап: {method['name']}")

    # ---------- Внутренние методы ----------
    def _on_playback_timer(self):
        """Обновление кадра при воспроизведении."""
        if not self._is_playing:
            return
        new_index = self._current_frame_index + 1
        if new_index >= self._data.shape[2]:
            new_index = 0  # зацикливание
        self.set_current_frame(new_index)

    def set_current_frame(self, index: int):
        """Установить текущий кадр и обновить интерфейс."""
        if not 0 <= index < self._data.shape[2]:
            return
        self._current_frame_index = index
        self._current_frame = self._data[index]
        if self._preprocessed_output is None or self._pipeline.stages:
            self.frame_updated.emit(
                self._pipeline.apply_to_frame(self._current_frame).imshow(figsize=(self.figsize_scale, self.figsize_scale*self._data.shape[0]/self._data.shape[1]), return_=True, colorbar=self.colorbar)
            )
        else:
            self.frame_updated.emit(self._preprocessed_output[index])

        # Обновить ползунок без генерации сигнала
        self._view._time_slider.blockSignals(True)
        self._view._time_slider.setValue(index)
        self._view._time_slider.blockSignals(False)

        # Обновить метки времени
        time_sec = index / FPS
        self.current_time_changed.emit(time_sec)

    def _update_ui_from_model(self):
        """Обновить интерфейс в соответствии с текущим состоянием модели."""
        # Установить диапазон слайдера
        frame_count = self._data.shape[2]
        self._view._time_slider.setRange(0, frame_count - 1 if frame_count > 0 else 0)

        # Установить метки времени
        duration = frame_count / FPS if frame_count > 0 else 0.0
        self.time_range_changed.emit(0.0, duration)

        # Отобразить первый кадр
        if frame_count > 0:
            self.set_current_frame(0)

        # Заполнить список этапов
        self._update_pipeline_ui()

    def _update_pipeline_ui(self):
        """Обновить отображение списка этапов в пайплайне."""
        # Очистить контейнер этапов
        layout = self._view._stages_layout
        while layout.count() > 1:  # оставить stretch
            item = layout.takeAt(0)
            widget = item.widget()
            if widget:
                widget.deleteLater()

        # Добавить этапы из модели
        for idx, (method_idx, params) in enumerate(self._pipeline.stages):
            stage_widget = self._create_stage_widget(idx, self._pipeline.methods[method_idx]['name'], self._pipeline.methods[method_idx]['params'])
            layout.insertWidget(layout.count() - 1, stage_widget)

    def _create_stage_widget(self, index: int, stage_type: str, params: Dict) -> QWidget:
        """Создаёт виджет для отображения одного этапа обработки."""
        from PySide6.QtWidgets import QWidget, QHBoxLayout, QLabel, QToolButton

        widget = QWidget()
        layout = QHBoxLayout(widget)
        layout.setContentsMargins(0, 0, 0, 0)

        # Метка с номером и названием
        label = QLabel(f"{index+1}. {stage_type}")
        layout.addWidget(label)

        # Кнопка удаления
        delete_btn = QToolButton()
        delete_btn.setText("✕")
        delete_btn.clicked.connect(lambda: self._remove_stage(index))
        layout.addWidget(delete_btn)

        return widget

    def _remove_stage(self, index: int):
        """Удалить этап обработки по индексу."""
        self._pipeline.remove_stage(index)
        self._update_pipeline_ui()
        self.status_message.emit(f"Этап {index+1} удалён")

    # ---------- Вспомогательные методы для интеграции с view ----------
    def show(self):
        """Показать окно."""
        self._view.show()

    # ---------- Методы для обновления отображения кадра ----------
    # В реальном приложении нужно конвертировать numpy в QPixmap и обновлять _monitor_label
    @Slot(np.ndarray)
    def on_frame_updated(self, img: np.ndarray):
        """Слот для отображения кадра. Вызывается по сигналу frame_updated."""

        h, w, _ = img.shape
        qimage = QImage(img, w, h, w*4, QImage.Format.Format_RGBA8888)

        pixmap = QPixmap.fromImage(qimage)
        # Масштабировать под размер метки
        pixmap = pixmap.scaled(self._view._monitor_frame.size(), Qt.KeepAspectRatio, Qt.SmoothTransformation)

        self._view._monitor_label.setPixmap(pixmap)

if __name__ == '__main__':
    from PySide6.QtWidgets import QApplication
    import sys

    app = QApplication(sys.argv)
    window = ProcessingWindow(pipeline=PipelineManager())
    presenter = ProcessingPresenter(window)   # контроллер подключает сигналы
    window.show()
    sys.exit(app.exec())