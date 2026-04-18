from PySide6.QtCore import Qt, QSize, QObject, Signal, Slot, QTimer, QEvent
from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout,
    QLabel, QToolButton, QFileDialog, QMessageBox, QDialog, QVBoxLayout, QComboBox, QDialogButtonBox, QApplication, QToolTip,
)
from PySide6.QtGui import QFont, QImage, QPixmap
# Tseries, Timage - model
from thermograms.thermograms import loadfile, Tseries, WB_PALETTE, IRON_PALETTE
import numpy as np
from typing import Dict
from scipy.io import savemat
from pickle import dump as pickle_dump, load as pickle_load
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure


from Processing import ParameterDialog, ProcessingWindow, PipelineManager

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



#presenter
class ProcessingPresenter(QObject):
    """
    Презентер для окна обработки термограмм.
    Управляет взаимодействием между View (ProcessingWindow) и Model (термограммы, пайплайн).
    """

    # Сигналы, которые может эмитировать презентер для уведомления view
    frame_updated = Signal(np.ndarray)           # новый кадр для отображения
    current_frame_changed = Signal(int)          # текущий кадр
    pipeline_changed = Signal(list)              # список этапов для отображения
    status_message = Signal(str)                 # сообщение в строку состояния
    processing_finished = Signal()
    palette = WB_PALETTE
    default_fps = 30
    fps = default_fps

    #figsize_scale = 4
    initial_data = None
    _data = Tseries(array=np.zeros((1, 1, 1), dtype=np.float32))
    _path = ''
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
        self._playback_timer.setInterval(1000 // self.fps)
        self._playback_timer.timeout.connect(self._on_playback_timer)

        # Инициализация соединений и начального состояния
        self._connect_signals()
        self._view.fps_spinbox.blockSignals(True)
        self._view.fps_spinbox.setValue(self.default_fps)
        self._view.fps_spinbox.blockSignals(False)
        self._update_ui_from_model()

    # ---------- Инициализация соединений ----------
    def _connect_signals(self):
        """Подключает сигналы из view к слотам презентера."""
        # Сигналы
        self.frame_updated.connect(self.on_frame_updated)
        self.status_message.connect(self.status_label_set_text)
        self.current_frame_changed.connect(self.on_current_frame_changed)

        # Кнопки управления
        self._view._play_button.clicked.connect(self.on_play_clicked)
        self._view._pause_button.clicked.connect(self.on_pause_clicked)
        self._view._stop_button.clicked.connect(self.on_stop_clicked)
        self._view._step_forward_button.clicked.connect(self.on_step_forward)
        self._view._step_backward_button.clicked.connect(self.on_step_backward)
        self._view.fps_spinbox.valueChanged.connect(self.on_fps_changed)
        self._view._add_stage_button.clicked.connect(self.on_add_stage_clicked)

        # Ползунок времени
        self._view._time_slider.valueChanged.connect(self.on_slider_value_changed)

        # Кнопки управления
        self._view._apply_button.clicked.connect(self.on_apply_pipeline)

        self._view.open_action.triggered.connect(self.on_open_file)
        self._view.toggle_colorbar_action.toggled.connect(self.on_toggle_colorbar)
        self._view.toggle_on_mouse_value_action.toggled.connect(self.on_toggle_on_mouse_value_action)
        self._view.keep_initial_data_action.toggled.connect(self.on_keep_initial_data_action)
        self._view.export_npy_action.triggered.connect(self.on_export_npy_action)
        self._view.export_mat_action.triggered.connect(self.on_export_mat_action)
        self._view.export_pipeline_action.triggered.connect(self.on_export_pipeline_action)
        self._view.import_pipeline_action.triggered.connect(self.on_import_pipeline_action)
        self._view.palette_default.triggered.connect(self.on_palette_default)
        self._view.palette_gray.triggered.connect(self.on_palette_gray)
        self._view.palette_iron.triggered.connect(self.on_palette_iron)

        self._view._monitor_label.setMouseTracking(False)
        self._view._monitor_label.installEventFilter(self)

    def eventFilter(self, obj: QObject, event: QEvent):
        if obj == self._view._monitor_label:
            if event.type() == QEvent.Type.MouseMove:
                self._show_pixel_value(event.pos())
            elif event.type() == QEvent.Type.MouseButtonPress:
                self._on_image_clicked(event.pos())
        return super().eventFilter(obj, event)

    # ---------- Слоты для пользовательских действий ----------
    @Slot(str)
    def status_label_set_text(self, text: str):
        self._view.status_label.setText(text)
    
    @Slot(int)
    def on_current_frame_changed(self, frame_index: int):
        self._view.frame_index_label.setText(str(frame_index))

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

            # Применить ко всем кадрам
            self._data = self._pipeline.apply_to_series(self._data)
            self._update_ui_from_model()
            self.status_message.emit("Пайплайн применён ко всей серии")

    @Slot()
    def on_open_file(self):
        """Открыть файл с термограммами."""
        # Открываем диалог выбора файла
        file_path, _ = QFileDialog.getOpenFileName(
            self._view,
            "Открыть файл термограмм",
            "",
            "Все поддерживаемые файлы (*.npy *.mat *.ravi);;NumPy файлы (*.npy);;MATLAB файлы (*.mat);;RAVI файлы (*.ravi);;Все файлы (*)"
        )
        if not file_path:
            return  # Пользователь отменил выбор
        
        try:
            self.status_message.emit('Загрузка серии...')
            QApplication.processEvents() # чтобы успела появиться надпись 'Загрузка серии...' 
            frames = loadfile(file_path)
            self.fps = None

            if isinstance(frames, dict):
                if 'frequency' in frames:
                    self.fps = frames['frequency']
                for possible_key in frames.keys():
                    if isinstance(frames[possible_key], np.ndarray):
                        frames = frames[possible_key].astype('float64')
                        break
            
            if isinstance(frames, dict):
                raise ValueError('This dict has no array to be series')
            
            if frames is None or frames.size == 0:
                QMessageBox.warning(self._view, "Ошибка загрузки", "Файл не содержит данных")
                return
            
            if self.initial_data is not None:
                self.initial_data = frames
            self._data = Tseries(array=frames)
            self._path = file_path
            if self.fps is None:
                self.fps = self._view.fps_spinbox.value()
            else:
                self.on_fps_changed(self.fps)
            self._pipeline.not_applied()

            self._update_ui_from_model()

            self.status_message.emit('Готов к обработке')

        except Exception as e:
            QMessageBox.critical(self._view, "Ошибка загрузки", f"Не удалось загрузить файл:\n{str(e)}")
            self.status_message.emit("Ошибка загрузки файла")
    
    @Slot(float)
    def on_fps_changed(self, value: int):
        self.fps = value
        self._playback_timer.setInterval(1000 // self.fps)
        
        self.set_current_frame(self._current_frame_index)

    @Slot(bool)
    def on_toggle_timeline(self, checked: bool):
        """Показать/скрыть панель таймлайна."""
        self._view._timeline_frame.setVisible(checked)

    @Slot(bool)
    def on_toggle_colorbar(self, checked: bool):
        """Показать/скрыть колорбар."""
        self.colorbar = checked
        
        self.set_current_frame(self._current_frame_index)

    @Slot(bool)
    def on_toggle_on_mouse_value_action(self, checked: bool):
        """Показать/скрыть значение термограммы при наведении мыши."""
        self._view._monitor_label.setMouseTracking(checked)

    @Slot(bool)
    def on_keep_initial_data_action(self, checked: bool):
        """Показать/скрыть значение термограммы при наведении мыши."""
        if checked:
            if self._path == '':
                self.initial_data = np.zeros((1, 1, 1), dtype=np.float32)
                return
            try:
                self.status_message.emit('Загрузка серии...')
                QApplication.processEvents() # чтобы успела появиться надпись 'Загрузка серии...' 
                frames = loadfile(self._path)

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

                self.initial_data = frames

                self._update_ui_from_model()

                self.status_message.emit('Готов к обработке')

            except Exception as e:
                QMessageBox.critical(self._view, "Ошибка загрузки", f"Не удалось загрузить файл:\n{str(e)}")
                self.status_message.emit("Ошибка загрузки файла")
        else:
            self.initial_data = None

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
        self._update_ui_from_model()
        self.status_message.emit(f"Добавлен этап: {method['name']}")
    
    @Slot()
    def on_export_npy_action(self):
        """Экспорт данных в формате .npy."""
        file_path, _ = QFileDialog.getSaveFileName(
            self._view,
            "Сохранить как .npy",
            "",
            "NumPy files (*.npy)"
        )
        if not file_path:
            return

        try:
            self.status_message.emit(f"Экспорт данных в {file_path}")
            QApplication.processEvents()
            np.save(file_path, self._data.array)
            self.status_message.emit(f"Данные экспортированы в {file_path}")
        except Exception as e:
            QMessageBox.critical(self._view, "Ошибка экспорта", f"Не удалось экспортировать данные:\n{str(e)}")
            self.status_message.emit("Ошибка экспорта")
    
    @Slot()
    def on_export_mat_action(self):
        """Экспорт данных в формате .mat."""
        file_path, _ = QFileDialog.getSaveFileName(
            self._view,
            "Сохранить как .mat",
            "",
            "MatLab files (*.mat)"
        )
        if not file_path:
            return

        try:
            self.status_message.emit(f"Экспорт данных в {file_path}")
            QApplication.processEvents()
            savemat(file_path, {'data': self._data.array})
            self.status_message.emit(f"Данные экспортированы в {file_path}")
        except Exception as e:
            QMessageBox.critical(self._view, "Ошибка экспорта", f"Не удалось экспортировать данные:\n{str(e)}")
            self.status_message.emit("Ошибка экспорта")
    
    @Slot()
    def on_export_pipeline_action(self):
        """Экспорт пайплайна"""
        file_path, _ = QFileDialog.getSaveFileName(
            self._view,
            "Сохранить как .pickle",
            "",
            "Pickle files (*.pickle)"
        )
        if not file_path:
            return

        try:
            self.status_message.emit(f"Экспорт данных в {file_path}")
            QApplication.processEvents()
            with open(file_path, 'wb') as file:
                pickle_dump([[method_idx, params, False] for method_idx, params, applied in self._pipeline.stages], file)
            self.status_message.emit(f"Данные экспортированы в {file_path}")
        except Exception as e:
            QMessageBox.critical(self._view, "Ошибка экспорта", f"Не удалось экспортировать данные:\n{str(e)}")
            self.status_message.emit("Ошибка экспорта")
    
    @Slot()
    def on_import_pipeline_action(self):
        """Экспорт пайплайна"""
        file_path, _ = QFileDialog.getOpenFileName(
            self._view,
            "Открыть файл пайплайна",
            "",
            "Pickle files (*.pickle)"
        )
        if not file_path:
            return

        try:
            self.status_message.emit(f"Импорт пайплайна из {file_path}")
            QApplication.processEvents()
            with open(file_path, 'rb') as file:
                self._pipeline.stages = pickle_load(file)
                self._pipeline.not_applied()
            self._update_ui_from_model()
            self.status_message.emit(f"Пайплайн импортирован")
        except Exception as e:
            QMessageBox.critical(self._view, "Ошибка импорта", f"Не удалось импортировать пайплайн:\n{str(e)}")
            self.status_message.emit("Ошибка импорта")
    
    @Slot()
    def on_palette_default(self):
        """Установка палитры по умолчанию"""
        self.palette = WB_PALETTE
        self._update_ui_from_model()
    
    @Slot()
    def on_palette_gray(self):
        """Установка палитры градации серого"""
        self.palette = WB_PALETTE
        self._update_ui_from_model()
    
    @Slot()
    def on_palette_iron(self):
        """Установка палитры каления железа"""
        self.palette = IRON_PALETTE
        self._update_ui_from_model()
        

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
        self._current_frame = self._pipeline.apply_to_frame(self._data[index])
        self.frame_updated.emit(
            #self._pipeline.apply_to_frame(self._current_frame).imshow(figsize=(self.figsize_scale, self.figsize_scale*self._data.shape[0]/self._data.shape[1]), return_=True, colorbar=self.colorbar)
            self._current_frame.show(palette=self.palette)
        )

        # Обновить ползунок без генерации сигнала
        self._view._time_slider.blockSignals(True)
        self._view._time_slider.setValue(index)
        self._view._time_slider.blockSignals(False)

        self.current_frame_changed.emit(self._current_frame_index)

    def _update_ui_from_model(self):
        """Обновить интерфейс в соответствии с текущим состоянием модели."""
        # Установить диапазон слайдера
        frame_count = self._data.shape[2]
        self._view._time_slider.setRange(0, frame_count - 1 if frame_count > 0 else 0)

        # Установить метки времени
        self._view._end_time_label.setText(str(frame_count))
        QApplication.processEvents()

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
        for idx, (method_idx, params, applied) in enumerate(self._pipeline.stages):
            stage_widget = self._create_stage_widget(
                idx,
                self._pipeline.methods[method_idx]['name'],
                [(param_name, param_value) for (param_value, (param_name, _)) in zip(params, self._pipeline.methods[method_idx]['params'])],
                applied
            )
            layout.insertWidget(layout.count() - 1, stage_widget)

    def _create_stage_widget(self, index: int, stage_type: str, params: Dict, applied: bool) -> QWidget:
        """Создаёт виджет для отображения одного этапа обработки."""

        widget = QWidget()
        layout = QHBoxLayout(widget)
        layout.setContentsMargins(0, 0, 0, 0)

        # Метка с номером и названием
        label = f"{index+1}. {stage_type}"

        for param_name, param_value in params:
            label += f'\n{param_name}={param_value}'

        label = QLabel(label)
        layout.addWidget(label)

        # Кнопка изменения
        change_btn = QToolButton()
        change_btn.setText("change")
        change_btn.clicked.connect(lambda: self._change_stage(index))
        layout.addWidget(change_btn)

        # Кнопка удаления
        delete_btn = QToolButton()
        delete_btn.setText("✕")
        delete_btn.clicked.connect(lambda: self._remove_stage(index))
        layout.addWidget(delete_btn)

        if applied: widget.setStyleSheet("background-color: #e0e0ff;")

        return widget

    def _change_stage(self, index: int):
        """Изменить этап обработки по индексу."""
        stage_name = self._pipeline.methods[self._pipeline.stages[index][0]]['name']
        self.status_message.emit(f'Изменение этапа обработки: {index+1}. {stage_name}')
        QApplication.processEvents()

        param_dialog = ParameterDialog(
            [(param_name, param_value) for (param_name, param_default), param_value in zip(self._pipeline.methods[self._pipeline.stages[index][0]]['params'], self._pipeline.stages[index][1])],
            self._view)
        if param_dialog.exec() != QDialog.Accepted:
            return
        param_values = param_dialog.get_values()

        if self._pipeline.stages[index][2]:
            if self.initial_data is not None:
                self._data = Tseries(array=self.initial_data)
            else:
                frames = loadfile(self._path)
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

        self._pipeline.change_stage(index, param_values)
        
        self._update_ui_from_model()
        self.status_message.emit(f"Этап {index+1}. {stage_name} изменен")

    def _remove_stage(self, index: int):
        """Удалить этап обработки по индексу."""
        stage_name = self._pipeline.methods[self._pipeline.stages[index][0]]['name']
        self.status_message.emit(f'Удаление этапа обработки: {index+1}. {stage_name}')
        QApplication.processEvents()

        if self._pipeline.stages[index][2]:
            if self.initial_data is not None:
                self._data = Tseries(array=self.initial_data)
            else:
                frames = loadfile(self._path)
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

        self._pipeline.remove_stage(index)
        
        self._update_ui_from_model()
        self.status_message.emit(f"Этап {index+1}. {stage_name} удалён")

    # ---------- Вспомогательные методы для интеграции с view ----------
    def show(self):
        """Показать окно."""
        self._view.show()

    # ---------- Методы для обновления отображения кадра ----------
    @Slot(np.ndarray)
    def on_frame_updated(self, img: np.ndarray):
        """Слот для отображения кадра. Вызывается по сигналу frame_updated."""

        h, w, _ = img.shape
        qimage = QImage(img.astype('uint8'), w, h, w*3, QImage.Format.Format_RGB888)

        pixmap = QPixmap.fromImage(qimage)
        # Масштабировать под размер метки
        pixmap = pixmap.scaled(self._view._monitor_frame.size() * 0.9, Qt.KeepAspectRatio, Qt.SmoothTransformation)

        self._view._monitor_label.setPixmap(pixmap)
        self.update_colorbar()
    
    def update_colorbar(self):
        colorbar = np.repeat(self.palette[255::-1].reshape(-1, 1, 3), 32, axis=1)

        h, w, _ = colorbar.shape
        qimage = QImage(colorbar.astype('uint8'), w, h, w*3, QImage.Format.Format_RGB888)
        
        pixmap = QPixmap.fromImage(qimage)
        height = self._view._monitor_label.pixmap().size().height()
        width = w * height // h
        pixmap = pixmap.scaled(QSize(width, height), Qt.AspectRatioMode.IgnoreAspectRatio, Qt.SmoothTransformation)
        
        self._view._colorbar_label.setPixmap(pixmap)

        max_value = str(  self._current_frame.array.max()  ) + '0'*3
        min_value = str(  self._current_frame.array.min()  ) + '0'*3

        self._view._colorbar_max_label.setText(max_value[:5])
        self._view._colorbar_min_label.setText(min_value[:5])

    def _show_pixel_value(self, pos):
        label = self._view._monitor_label
        pixmap = label.pixmap()
        if not pixmap or pixmap.isNull() or not self._pipeline.applied:
            return

        # Размеры отображаемого pixmap
        pw, ph = pixmap.width(), pixmap.height()

        x = pos.x()
        y = pos.y()

        if 0 <= x < pw and 0 <= y < ph:
            # Масштабирование: координаты в исходном изображении
            orig_h, orig_w = self._data.shape[:2]
            ix = x * orig_w // pw
            iy = y * orig_h // ph

            # Значение температуры (или интенсивности)
            value = self._data[iy, ix, self._current_frame_index]
            tooltip_text = f"x={ix}, y={iy}\nvalue={value:.2f}"
            QToolTip.showText(label.mapToGlobal(pos), tooltip_text, label)
        else:
            QToolTip.hideText()
    
    def _on_image_clicked(self, pos):
        """Обработка клика по изображению: показать график температуры в точке."""
        label = self._view._monitor_label
        pixmap = label.pixmap()
        if not pixmap or pixmap.isNull() or not self._pipeline.applied:
            return
        
        # Размеры отображаемого pixmap
        pw, ph = pixmap.width(), pixmap.height()
        # Размеры метки
        lw, lh = label.width(), label.height()
        
        # Смещение из-за выравнивания по центру
        offset_x = max(0, (lw - pw) // 2)
        offset_y = max(0, (lh - ph) // 2)
        
        # Координаты внутри области изображения
        x = pos.x() - offset_x
        y = pos.y() - offset_y
        
        if 0 <= x < pw and 0 <= y < ph:
            # Масштабирование к исходному разрешению
            orig_h, orig_w = self._data.shape[:2]
            scale_x = orig_w / pw
            scale_y = orig_h / ph
            ix = int(x * scale_x)
            iy = int(y * scale_y)

            # Значение температуры (или интенсивности)
            self._show_plot(ix, iy)
        else:
            return
    
    def _show_plot(self, ix, iy):
        dialog = QDialog(self._view)
        dialog.setWindowTitle(f"График значений в точке ({ix}, {iy})")
        dialog.resize(800, 500)

        layout = QVBoxLayout(dialog)

        # Создание фигуры и canvas
        fig = Figure(figsize=(6, 4))
        canvas = FigureCanvas(fig)
        layout.addWidget(canvas)

        # Построение графика
        ax = fig.add_subplot(111)
        ax.plot(self._data.array[iy, ix], color='red', linewidth=1.5)
        ax.set_xlabel("Кадр", fontsize=10)
        ax.set_ylabel("Значение", fontsize=10)
        ax.set_title(f"Изменение значений в пикселе ({ix}, {iy})", fontsize=12)
        ax.grid(True, linestyle='--', alpha=0.6)

        # Автоматическое масштабирование осей
        ax.relim()
        ax.autoscale_view()

        canvas.draw()

        # Кнопка закрытия
        button_box = QDialogButtonBox(QDialogButtonBox.Close)
        button_box.rejected.connect(dialog.reject)
        layout.addWidget(button_box)

        dialog.exec()