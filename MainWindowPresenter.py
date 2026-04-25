"""
Presenter главного окна.
Управляет процессом контроля, таймерами, камерами, нагревателем и навигацией.
"""
import os
import logging
import shutil
import numpy as np
from PySide6.QtCore import QTimer, QPropertyAnimation, QEasingCurve, Qt
from PySide6.QtWidgets import QDialog

from settings import Settings, UserData
from heater import Heater
from cameras import CameraManager, CameraFactory
from TrajectoryDialog import TrajectoryDialog
from RetestDialog import RetestDialog
from FinishDialog import FinishDialog
from SettingsWindow import SettingsWindow

logger = logging.getLogger(__name__)

class MainWindowPresenter:
    def __init__(self, view, heater: Heater, camera_manager: CameraManager, settings: Settings, user_data: UserData):
        self.view = view
        self.heater = heater
        self.camera_manager = camera_manager
        self.settings = settings
        self.user_data = user_data

        # Состояние процесса
        self.current_position = np.zeros(2, dtype=int)
        self.last_moving = np.zeros(2, dtype=int)
        self.current_base_path = None
        self.is_testing = False

        # Таймеры и анимации
        self._heating_timer = QTimer()
        self._heating_timer.setSingleShot(True)
        self._heating_timer.timeout.connect(self._start_cooling)

        self._cooling_timer = QTimer()
        self._cooling_timer.setSingleShot(True)
        self._cooling_timer.timeout.connect(self._finish_testing)

        self._status_update_timer = QTimer()
        self._status_update_timer.setInterval(1000)
        self._status_update_timer.timeout.connect(self._update_status_text)

        self._telemetry_timer = QTimer()
        self._telemetry_timer.setInterval(500)
        self._telemetry_timer.timeout.connect(self._update_telemetry)

        self._progress_animation = QPropertyAnimation(self.view.progress_bar, b"value")
        self._progress_animation.setEasingCurve(QEasingCurve.Linear)

        # Инициализация
        self._initialize_cameras()
        self._connect_view_signals()
        self._telemetry_timer.start()
        self.view.update_position_status(*self.current_position)
        self.view.set_status("Готов к началу")

    def _connect_view_signals(self):
        self.view.start_requested.connect(self.start_testing_process)
        self.view.stop_requested.connect(self.stop_testing)
        self.view.settings_requested.connect(self._open_settings)

    def _initialize_cameras(self):
        try:
            vis_cam = CameraFactory.create_camera("visible", self.settings, self.view.visible_video)
            therm_cam = CameraFactory.create_camera("thermal", self.settings, self.view.thermal_video)
            
            if not vis_cam.initialize():
                logger.warning("Не удалось инициализировать камеру видимого спектра")
            if not therm_cam.initialize():
                logger.warning("Не удалось инициализировать тепловизор")
                
            self.camera_manager.add_camera("visible", vis_cam)
            self.camera_manager.add_camera("thermal", therm_cam)
        except Exception as e:
            logger.error(f"Ошибка инициализации камер: {e}")
            self.view.show_error("Ошибка камеры", f"Не удалось инициализировать камеры: {e}")

    def start_testing_process(self):
        if self.is_testing: return
        self.is_testing = True
        logger.info(f"Начало контроля зоны {tuple(self.current_position)}")
        
        object_name = self.user_data.object_of_testing.replace(" ", "_")
        
        if getattr(self.user_data, 'use_autoincrement', False):
            object_name = f"{object_name}_{self.user_data.current_number:02d}"

        position = f"zone({self.current_position[0]},{self.current_position[1]})"
        self.current_base_path = f"{self.user_data.save_path}/{object_name}_{position}"

        self.view.enable_start(False)
        self.view.enable_stop(True)

        try:
            self.camera_manager.start_recording_all(self.current_base_path)
            self.view.update_recording_status(True)
        except Exception as e:
            logger.error(f"Не удалось начать запись видео: {e}")
            self.view.show_error("Ошибка камер", f"Не удалось запустить запись: {e}")
            self.stop_testing()
            return

        try:
            self.heater.turn_on()
            self.view.update_heater_status(True)
        except Exception as e:
            logger.error(f"Не удалось включить нагреватель: {e}")
            self.view.update_heater_status(False, has_error=True)
            self.view.show_error("Нагреватель: ошибка", f"Не удалось запустить нагреватель: {e}")
            self.stop_testing()
            return

        self.view.set_status(f"Нагрев... (осталось {self.settings.heating_duration} с)")
        self._status_update_timer.start()

        total_time_ms = self.settings.duration_of_testing * 1000
        self._progress_animation.setDuration(total_time_ms)
        self._progress_animation.setStartValue(0)
        self._progress_animation.setEndValue(100)
        self._progress_animation.start()

        self._heating_timer.start(self.settings.heating_duration * 1000)

    def _start_cooling(self):
        try:
            self.heater.turn_off()
            self.view.update_heater_status(False)
        except Exception as e:
            logger.error(f"Ошибка выключения нагревателя: {e}")
            self.view.update_heater_status(True, has_error=True)

        cooling_duration = self.settings.duration_of_testing - self.settings.heating_duration
        self.view.set_status(f"Охлаждение... (осталось {cooling_duration} с)")
        self._cooling_timer.start(cooling_duration * 1000)

    def _finish_testing(self):
        self._stop_all_timers()
        self.camera_manager.stop_recording_all()
        self.view.update_recording_status(False)
        self.view.enable_stop(False)
        self._progress_animation.stop()
        self.view.set_progress(100)
        self.view.set_status("Контроль зоны успешно завершён!")
        self.is_testing = False
        logger.info(f"Контроль зоны {tuple(self.current_position)} завершён.")
        self._open_trajectory_dialog()

    def stop_testing(self):
        if not self.is_testing: return
        self._stop_all_timers()
        try: 
            self.heater.turn_off()
            self.view.update_heater_status(False)
        except Exception as e:
            logger.error(f"Ошибка выключения нагревателя при прерывании: {e}")
            self.view.update_heater_status(False, has_error=True)

        self.camera_manager.stop_recording_all()
        self.view.update_recording_status(False)
        self._progress_animation.stop()
        self.view.set_status("Контроль прерван")
        self.is_testing = False
        logger.warning("Контроль был прерван пользователем")
        self._delete_current_zone_files()
        self._reset_state()

    def _stop_all_timers(self):
        self._heating_timer.stop()
        self._cooling_timer.stop()
        self._status_update_timer.stop()

    def _update_status_text(self):
        elapsed = self._progress_animation.currentTime() / 1000
        remaining = self.settings.duration_of_testing - elapsed
        if elapsed < self.settings.heating_duration:
            phase = "Нагрев"
            phase_remaining = self.settings.heating_duration - elapsed
        else:
            phase = "Охлаждение"
            phase_remaining = remaining
        self.view.set_status(f"{phase}... (осталось {phase_remaining:.0f} с)")

    def _delete_current_zone_files(self):
        try:
            if self.current_base_path:
                for cam_name in self.camera_manager.cameras.keys():
                    fp = f"{self.current_base_path}_{cam_name}.avi"
                    if os.path.exists(fp): 
                        os.remove(fp)
                        logger.info(f"Удален файл: {fp}")
        except Exception as e: 
            logger.error(f"Ошибка удаления файлов: {e}")

    def _reset_state(self):
        self.view.set_progress(0)
        self.view.enable_stop(False)
        self.view.enable_start(True)
        self.view.set_status("Готов к началу")
        try:
            self.heater.turn_off()
            self.view.update_heater_status(False)
        except Exception:
            pass

    def _open_trajectory_dialog(self):
        dialog = TrajectoryDialog(parent=self.view)
        dialog.direction_selected.connect(self._handle_direction)
        dialog.retest_requested.connect(self._open_retest_dialog)
        dialog.preview_requested.connect(self._handle_preview)
        dialog.finish_requested.connect(self._open_finish_dialog)
        dialog.exec()

    def _handle_direction(self, direction: str):
        direction_map = {'right': [1, 0], 'left': [-1, 0], 'up': [0, 1], 'down': [0, -1]}
        translation = {'right': 'вправо', 'left': 'влево', 'up': 'вверх', 'down': 'вниз'}
        move_vector = np.array(direction_map[direction])
        self.last_moving = move_vector
        self.current_position += move_vector
        self.view.update_position_status(*self.current_position)
        self.view.show_info("Перемещение дефектоскопа", f"Пожалуйста, переместите дефектоскоп в направлении {translation[direction]}.\nПосле перемещения нажмите ОК, чтобы начать контроль новой зоны.")
        self.view.enable_start(True)

    def _open_retest_dialog(self):
        dialog = RetestDialog(x=int(self.current_position[0]), y=int(self.current_position[1]), parent=self.view)
        if dialog.exec() == QDialog.Accepted:
            self._delete_current_zone_files()
            self._reset_state()
            self.view.set_status("Готов к повторному контролю текущей зоны")
            logger.info(f"Подготовка к повторному контролю зоны {tuple(self.current_position)}")
        else: 
            self._open_trajectory_dialog()

    def _handle_preview(self):
        self.view.show_info("Предпросмотр", "Функция предпросмотра ещё в разработке")
        self._open_trajectory_dialog()

    def _open_finish_dialog(self):
        dialog = FinishDialog(parent=self.view)
        dialog.set_save_path(self.user_data.save_path)
        if dialog.exec() == QDialog.Accepted: 
            if getattr(self.user_data, 'use_autoincrement', False):
                self.settings.current_number = self.user_data.current_number + 1
                self.settings.use_autoincrement = True
                try:
                    self.settings.save_to_file()
                    logger.info(f"Счетчик автоинкремента обновлен: {self.settings.current_number}")
                except Exception as e:
                    logger.error(f"Ошибка сохранения счетчика: {e}")
            logger.info("Контроль успешно завершён")
            self.view.close()
        else: 
            logger.info("Завершение контроля отменено")
            self._open_trajectory_dialog()

    def _open_settings(self):
        SettingsWindow(settings=self.settings, parent=self.view).exec()

    def _update_telemetry(self):
        try:
            path = self.user_data.save_path if self.user_data.save_path else "/"
            _, _, free = shutil.disk_usage(path)
            self.view.update_disk_space(free / (1024 ** 3))
        except Exception: 
            self.view.update_disk_space(None)