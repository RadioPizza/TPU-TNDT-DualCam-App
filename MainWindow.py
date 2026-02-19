"""
Модуль основного окна приложения для теплового неразрушающего контроля
"""
import logging
import os
import numpy as np
from PySide6.QtCore import QTimer, QPropertyAnimation, QEasingCurve, Qt, QSize
from PySide6.QtWidgets import (
    QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
    QLabel, QPushButton, QProgressBar, QSizePolicy,
    QGraphicsView, QMessageBox, QDialog
)
from PySide6.QtGui import QFont
from cameras import CameraFactory, CameraManager
from FinishDialog import FinishDialog
from heater_interface import Heater
from RetestDialog import RetestDialog
from settings import Settings, UserData
from SettingsWindow import SettingsWindow
from TrajectoryDialog import TrajectoryDialog

logger = logging.getLogger(__name__)


class MainWindow(QMainWindow):
    BUTTON_SIZE = QSize(120, 40)
    
    VIDEO_STYLE = """
        QGraphicsView {
            background-color: #333333;
            border: 2px solid #3c3c3c;
            border-radius: 8px;
        }
    """

    def __init__(self, heater: Heater, settings: Settings, parent=None):
        super().__init__(parent)
        
        # Сохраняем глобальные объекты
        self.heater = heater
        self.settings = settings
        self.user_data = UserData.get_instance()
        
        # Поля состояния
        self.current_position = np.zeros(2, dtype=int)
        self.last_moving = np.zeros(2, dtype=int)
        self.progress = 0
        self.current_base_path = None
        
        # Инициализация UI
        self._setup_window_properties()
        self._create_widgets()
        self._setup_layout()
        self._connect_signals()
        
        # Инициализация
        self._initialize_cameras()
        self._initialize_timers()
        self._reset_main_window_state()

    def _setup_window_properties(self):
        self.setWindowTitle("TPU-TNDT-DualCam-App")
        self.setMinimumSize(1280, 720)
        self.showMaximized()

    def _create_widgets(self):
        title_font = QFont("Segoe UI")
        title_font.setPointSize(16)
        title_font.setWeight(QFont.DemiBold)
        
        process_status_font = QFont("Segoe UI")
        process_status_font.setPointSize(10)
        process_status_font.setWeight(QFont.Normal)
        
        self._central_widget = QWidget()
        self.setCentralWidget(self._central_widget)
        
        self._main_layout = QVBoxLayout(self._central_widget)
        self._main_layout.setContentsMargins(30, 60, 30, 60)
        
        self._visible_label = QLabel("Камера видимого спектра")
        self._visible_label.setFont(title_font)
        
        self._visible_video = QGraphicsView()
        self._visible_video.setMinimumSize(400, 200)
        self._visible_video.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        self._visible_video.setStyleSheet(self.VIDEO_STYLE)
        
        self._thermal_label = QLabel("Тепловизор")
        self._thermal_label.setFont(title_font)
        
        self._thermal_video = QGraphicsView()
        self._thermal_video.setMinimumSize(400, 200)
        self._thermal_video.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        self._thermal_video.setStyleSheet(self.VIDEO_STYLE)
        
        self._process_status_label = QLabel("Готов к началу")
        self._process_status_label.setFont(process_status_font)
        self._process_status_label.setAlignment(Qt.AlignLeft)
        
        self._progress_bar = QProgressBar()
        self._progress_bar.setRange(0, 100)
        self._progress_bar.setValue(0)
        self._progress_bar.setTextVisible(False)
        self._progress_bar.setMinimumHeight(20)
        
        self._play_button = QPushButton("Старт")
        self._play_button.setMinimumSize(self.BUTTON_SIZE)
        self._play_button.setDefault(True)
        
        self._stop_button = QPushButton("Стоп")
        self._stop_button.setMinimumSize(self.BUTTON_SIZE)
        self._stop_button.setEnabled(False)
        
        self._settings_button = QPushButton("Настройки")
        self._settings_button.setMinimumSize(self.BUTTON_SIZE)

    def _setup_layout(self):
        visible_layout = QVBoxLayout()
        visible_layout.addWidget(self._visible_label)
        visible_layout.addWidget(self._visible_video)
        
        thermal_layout = QVBoxLayout()
        thermal_layout.addWidget(self._thermal_label)
        thermal_layout.addWidget(self._thermal_video)
        
        cameras_layout = QHBoxLayout()
        cameras_layout.setSpacing(10)
        cameras_layout.addLayout(visible_layout)
        cameras_layout.addLayout(thermal_layout)
        
        buttons_layout = QHBoxLayout()
        buttons_layout.setSpacing(20)
        buttons_layout.addStretch()
        buttons_layout.addWidget(self._stop_button)
        buttons_layout.addWidget(self._play_button)
        buttons_layout.addStretch()
        
        settings_layout = QHBoxLayout()
        settings_layout.addStretch()
        settings_layout.addWidget(self._settings_button)
        
        self._main_layout.addLayout(cameras_layout)
        self._main_layout.addSpacing(60)
        self._main_layout.addWidget(self._process_status_label)
        self._main_layout.addWidget(self._progress_bar)
        self._main_layout.addLayout(buttons_layout)
        self._main_layout.addLayout(settings_layout)

    def _connect_signals(self):
        self._play_button.clicked.connect(self.start_testing_process)
        self._stop_button.clicked.connect(self.stop_testing)
        self._settings_button.clicked.connect(self.open_settings_window)

    def _initialize_cameras(self):
        self._camera_manager = CameraManager()
        
        try:
            self._visible_camera = CameraFactory.create_camera(
                "visible", 
                self.settings, 
                self._visible_video
            )
            self._thermal_camera = CameraFactory.create_camera(
                "thermal", 
                self.settings, 
                self._thermal_video
            )

            visible_init_success = self._visible_camera.initialize()
            thermal_init_success = self._thermal_camera.initialize()
            
            if not visible_init_success:
                logger.warning("Не удалось инициализировать камеру видимого спектра")
            if not thermal_init_success:
                logger.warning("Не удалось инициализировать тепловизор")
            
            self._camera_manager.add_camera("visible", self._visible_camera)
            self._camera_manager.add_camera("thermal", self._thermal_camera)
            
        except Exception as e:
            logger.error(f"Ошибка инициализации камер: {e}")
            QMessageBox.critical(
                self, 
                "Ошибка камеры", 
                f"Не удалось инициализировать камеры: {e}"
            )

    def _initialize_timers(self):
        self._heating_timer = QTimer()
        self._heating_timer.setSingleShot(True)
        self._heating_timer.timeout.connect(self.start_cooling)
        
        self._cooling_timer = QTimer()
        self._cooling_timer.setSingleShot(True)
        self._cooling_timer.timeout.connect(self.finish_testing)
        
        self._progress_bar_animation = QPropertyAnimation(self._progress_bar, b"value")
        self._progress_bar_animation.setEasingCurve(QEasingCurve.Linear)

    def start_testing_process(self):
        """Начинает процесс контроля: нагрев + охлаждение"""
        logger.info(f"Начало контроля зоны {tuple(self.current_position)}")
        
        # Формируем имена файлов
        object_name = self.user_data.object_of_testing.replace(" ", "_")
        position = f"zone({self.current_position[0]},{self.current_position[1]})"
        base_path = f"{self.user_data.save_path}/{object_name}_{position}"
        
        # Сохраняем путь для возможного удаления
        self.current_base_path = base_path
        
        # Активируем кнопку Stop
        self._stop_button.setEnabled(True)
        
        # Деактивируем кнопку Start
        self._play_button.setEnabled(False)
        
        # Начинаем запись видео на всех камерах
        try:
            self._camera_manager.start_recording_all(base_path)
        except Exception as e:
            logger.error(f"Не удалось начать запись: {e}")
            QMessageBox.critical(
                self, 
                "Ошибка записи", 
                f"Не удалось начать запись: {e}"
            )
            self.stop_testing()
            return
        
        # Включаем нагрев
        self.heater.turn_on()
        
        # Обновляем текст с оставшимся временем
        self._process_status_label.setText(
            f"Нагрев... (осталось {self.settings.heating_duration} с)"
        )
        
        # Запускаем таймер для обновления текста
        self._status_update_timer = QTimer()
        self._status_update_timer.setInterval(1000)
        self._status_update_timer.timeout.connect(self.update_status_text)
        self._status_update_timer.start()
        
        # Настраиваем и запускаем анимацию прогресс-бара
        total_time_ms = self.settings.duration_of_testing * 1000
        self._progress_bar_animation.setDuration(total_time_ms)
        self._progress_bar_animation.setStartValue(0)
        self._progress_bar_animation.setEndValue(100)
        self._progress_bar_animation.start()
        
        # Запускаем таймер нагрева
        heating_duration = self.settings.heating_duration * 1000
        self._heating_timer.start(heating_duration)

    def start_cooling(self):
        """Переходит к процессу охлаждения"""
        # Выключаем нагреватель
        self.heater.turn_off()
        
        # Обновляем текст процесса
        cooling_duration = (
            self.settings.duration_of_testing - self.settings.heating_duration
        )
        self._process_status_label.setText(
            f"Охлаждение... (осталось {cooling_duration} с)"
        )
        
        # Запускаем таймер охлаждения
        cooling_duration_ms = cooling_duration * 1000
        self._cooling_timer.start(cooling_duration_ms)

    def finish_testing(self):
        """Завершает процесс контроля и запись видео"""
        # Останавливаем таймеры
        self._heating_timer.stop()
        self._cooling_timer.stop()
        
        # Останавливаем запись на всех камерах
        self._camera_manager.stop_recording_all()
        
        # Деактивируем кнопку Stop после успешного завершения
        self._stop_button.setEnabled(False)
        
        # Останавливаем анимацию прогресс-бара
        self._progress_bar_animation.stop()
        
        # Останавливаем таймер обновления текста
        if hasattr(self, '_status_update_timer'):
            self._status_update_timer.stop()
        
        # Устанавливаем завершающие значения
        self._progress_bar.setValue(100)
        self._process_status_label.setText("Контроль зоны успешно завершён!")
        logger.info(f"Контроль зоны {tuple(self.current_position)} завершён.")
        
        # Переход к следующему действию
        self.open_trajectory_dialog()

    def stop_testing(self):
        """Прерывает процесс контроля"""
        # Останавливаем таймеры
        self._heating_timer.stop()
        self._cooling_timer.stop()
        
        # Выключаем нагреватель
        self.heater.turn_off()
        
        # Останавливаем запись на всех камерах
        self._camera_manager.stop_recording_all()
        
        # Останавливаем анимацию прогресс-бара
        self._progress_bar_animation.stop()
        
        # Останавливаем таймер обновления текста
        if hasattr(self, '_status_update_timer'):
            self._status_update_timer.stop()
        
        # Обновляем статус
        self._process_status_label.setText("Контроль прерван")
        logger.warning("Контроль был прерван пользователем")
        
        # Удаляем записанные файлы текущей зоны
        self.delete_current_zone_files()
        
        # Сбрасываем состояние окна
        self._reset_main_window_state()

    def delete_current_zone_files(self):
        """Удаляет файлы текущей зоны при прерывании контроля"""
        try:
            if hasattr(self, 'current_base_path') and self.current_base_path:
                # Удаляем файлы для всех камер
                for camera_name in self._camera_manager.cameras.keys():
                    file_path = f"{self.current_base_path}_{camera_name}.avi"
                    if os.path.exists(file_path):
                        os.remove(file_path)
                        logger.info(f"Удален файл: {file_path}")
        except Exception as e:
            logger.error(f"Ошибка при удалении файлов: {e}")

    def open_settings_window(self):
        """Открывает окно настроек"""
        self._settings_window = SettingsWindow(settings=self.settings, parent=self)
        self._settings_window.exec()

    def closeEvent(self, event):
        """Закрывает камеры при завершении работы приложения"""
        self._camera_manager.release_all()
        event.accept()

    def update_status_text(self):
        """Обновляет текст статуса с оставшимся временем"""
        elapsed = self._progress_bar_animation.currentTime() / 1000  # В секундах
        remaining = self.settings.duration_of_testing - elapsed
        
        if elapsed < self.settings.heating_duration:
            phase = "Нагрев"
            phase_remaining = self.settings.heating_duration - elapsed
        else:
            phase = "Охлаждение"
            phase_remaining = remaining
        
        self._process_status_label.setText(
            f"{phase}... (осталось {phase_remaining:.0f} с)"
        )

    def open_trajectory_dialog(self):
        """Открывает диалоговое окно выбора следующей зоны"""
        self._trajectory_dialog = TrajectoryDialog(parent=self)
        
        # Подключаем сигналы диалога к слотам главного окна
        self._trajectory_dialog.direction_selected.connect(
            self.handle_direction_selected
        )
        self._trajectory_dialog.retest_requested.connect(
            self.open_retest_dialog
        )
        self._trajectory_dialog.preview_requested.connect(
            self.handle_preview_request
        )
        self._trajectory_dialog.finish_requested.connect(
            self.open_finish_dialog
        )
        
        self._trajectory_dialog.exec()

    def handle_direction_selected(self, direction: str):
        """Обрабатывает выбор направления перемещения"""
        # Словарь соответствия направления вектору перемещения
        direction_map = {
            'right': np.array([1, 0]),
            'left': np.array([-1, 0]),
            'up': np.array([0, 1]),
            'down': np.array([0, -1])
        }
        
        # Словарь для перевода направлений на русский
        direction_translation = {
            'right': 'вправо',
            'left': 'влево',
            'up': 'вверх',
            'down': 'вниз'
        }
        
        # Обновляем позицию
        move_vector = direction_map[direction]
        self.last_moving = move_vector
        self.current_position += move_vector
        
        # Закрываем диалог
        self._trajectory_dialog.allow_close_flag = True
        self._trajectory_dialog.close()
        
        # Показываем сообщение о перемещении дефектоскопа
        QMessageBox.information(
            self,
            "Перемещение дефектоскопа",
            f"Пожалуйста, переместите дефектоскоп в направлении "
            f"{direction_translation[direction]}.\n"
            "После перемещения нажмите ОК, чтобы начать контроль новой зоны.",
            QMessageBox.Ok
        )
        
        # Активируем кнопку Start для новой зоны
        self._play_button.setEnabled(True)

    def open_retest_dialog(self):
        """Открывает диалоговое окно повторного контроля текущей зоны"""
        # Закрываем диалог выбора траектории СРАЗУ при переходе
        if hasattr(self, '_trajectory_dialog') and self._trajectory_dialog:
            self._trajectory_dialog.allow_close_flag = True
            self._trajectory_dialog.close()
        
        # Создаем диалог повторного контроля
        self._retest_dialog = RetestDialog(
            x=int(self.current_position[0]),
            y=int(self.current_position[1]),
            parent=self
        )
        
        # Просто проверяем результат диалога
        result = self._retest_dialog.exec()
        
        if result == QDialog.Accepted:
            self.handle_retest_confirm()
        else:
            self.handle_retest_cancel()

    def handle_retest_confirm(self):
        """Обрабатывает подтверждение повторного контроля текущей зоны"""
        # Удаляем записанные файлы текущей зоны
        self.delete_current_zone_files()
        
        # Восстанавливаем элементы главного окна в исходное состояние
        self._reset_main_window_state()
        
        # Обновляем статус
        self._process_status_label.setText(
            "Готов к повторному контролю текущей зоны"
        )
        logger.info(
            f"Подготовка к повторному контролю зоны {tuple(self.current_position)}"
        )

    def handle_retest_cancel(self):
        """Обрабатывает отмену повторного контроля текущей зоны"""
        # Открываем диалог выбора траектории
        self.open_trajectory_dialog()

    def handle_preview_request(self):
        """Обрабатывает запрос на предпросмотр результатов"""
        # Закрываем диалог выбора траектории СРАЗУ при переходе
        if hasattr(self, '_trajectory_dialog') and self._trajectory_dialog:
            self._trajectory_dialog.allow_close_flag = True
            self._trajectory_dialog.close()
        
        # Показываем сообщение о том, что функция в разработке
        QMessageBox.information(
            self,
            "Предпросмотр",
            "Функция предпросмотра ещё в разработке"
        )
        
        # После закрытия сообщения снова открываем диалог выбора траектории
        self.open_trajectory_dialog()

    def open_finish_dialog(self):
        """Открывает финальное диалоговое окно"""
        # Закрываем диалог выбора траектории
        if hasattr(self, '_trajectory_dialog') and self._trajectory_dialog:
            self._trajectory_dialog.allow_close_flag = True
            self._trajectory_dialog.close()
        
        # Создаем финальный диалог
        self._finish_dialog = FinishDialog(parent=self)
        self._finish_dialog.set_save_path(self.user_data.save_path)
        
        # Проверяем результат
        result = self._finish_dialog.exec()
        
        if result == QDialog.Accepted:
            self.handle_finish_accepted()
        else:
            self.handle_finish_rejected()

    def handle_finish_accepted(self):
        """Обрабатывает принятие финального диалога"""
        logger.info("Контроль успешно завершён")
        # Закрываем приложение
        self.close()

    def handle_finish_rejected(self):
        """Обрабатывает отклонение финального диалога"""
        logger.info("Завершение контроля отменено")
        # Возвращаемся к диалогу выбора траектории
        self.open_trajectory_dialog()

    def _reset_main_window_state(self):
        """Сбрасывает состояние главного окна в исходное состояние"""
        # Сбрасываем прогресс-бар
        self._progress_bar.setValue(0)
        
        # Деактивируем кнопку Stop
        self._stop_button.setEnabled(False)
        
        # Активируем кнопку Start
        self._play_button.setEnabled(True)
        
        # Сбрасываем анимацию прогресс-бара
        self._progress_bar_animation.stop()
        
        # Останавливаем все таймеры, если они запущены
        self._heating_timer.stop()
        self._cooling_timer.stop()
        if hasattr(self, '_status_update_timer'):
            self._status_update_timer.stop()
        
        # Выключаем нагреватель на всякий случай
        try:
            self.heater.turn_off()
        except:
            pass
        
        # Обновляем текст статуса
        self._process_status_label.setText("Готов к началу")