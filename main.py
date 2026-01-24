# Стандартные библиотеки
import logging
import sys, os
from pathlib import Path

# Сторонние библиотеки
import numpy as np
from PySide6.QtCore import QEvent, QObject, Qt, QTimer, Signal, QPropertyAnimation, QEasingCurve
from PySide6.QtGui import QImage, QPixmap
from PySide6.QtWidgets import (QApplication, QDialog, QFileDialog,
                               QGraphicsPixmapItem, QGraphicsScene, QLineEdit,
                               QMainWindow, QMessageBox)
from serial_communicator import SerialCommunicator as com

# Локальные модули
from cameras import CameraFactory, CameraManager, get_available_cameras
from FinishDialog import FinishDialog
from heater_interface import Heater
from MainWindow import Ui_MainWindow
from osk import OnScreenKeyboard as osk
from RetestDialog import RetestDialog
from settings import PreviewSettings, Settings, UserData
from SettingsWindow import SettingsWindow
from StartDialog import StartWindow
from TrajectoryDialog import TrajectoryDialog
from utils import Utilities as utils

# Настройка базового конфигуратора логирования
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.StreamHandler()
    ]
)

logger = logging.getLogger(__name__)

# Загрузка настроек из файла (глобальная переменная)
settings = Settings.load_from_file()

# Глобальные объекты, которые будут использоваться в MainWindow
user_data = UserData.get_instance()
preview_settings = PreviewSettings.get_instance()

# Инициализация нагревателя
if settings.mock_heater:
    class MockHeater:
        def turn_on(self):
            logger.info("СИМУЛЯЦИЯ: Нагреватель включен")
        
        def turn_off(self):
            logger.info("СИМУЛЯЦИЯ: Нагреватель выключен")
    
    heater = MockHeater()
else:
    heater = Heater(settings.heater_COM_port_number, settings.heater_baud_rate)

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.showMaximized()

        # Поля
        self.current_position = np.zeros(2, dtype=int)
        self.last_moving = np.zeros(2, dtype=int)
        self.progress = 0

        # Создаем менеджер камер
        self.camera_manager = CameraManager()
        
        try:
            # Создаем камеры через фабрику
            visible_camera = CameraFactory.create_camera("visible", settings, self.ui.MainCameraView)
            thermal_camera = CameraFactory.create_camera("thermal", settings, self.ui.MainTCameraView)
            
            # Инициализируем камеры
            visible_init_success = visible_camera.initialize()
            thermal_init_success = thermal_camera.initialize()
            
            if not visible_init_success:
                logger.warning("Не удалось инициализировать камеру видимого спектра")
            if not thermal_init_success:
                logger.warning("Не удалось инициализировать тепловизор")
            
            # Добавляем камеры в менеджер
            self.camera_manager.add_camera("visible", visible_camera)
            self.camera_manager.add_camera("thermal", thermal_camera)
            
        except Exception as e:
            logger.error(f"Ошибка инициализации камер: {e}")
            QMessageBox.critical(self, "Ошибка камеры", f"Не удалось инициализировать камеры: {e}")

        # Таймеры
        self.heating_timer = QTimer()
        self.heating_timer.setSingleShot(True)
        self.heating_timer.timeout.connect(self.start_cooling)
        
        self.cooling_timer = QTimer()
        self.cooling_timer.setSingleShot(True)
        self.cooling_timer.timeout.connect(self.finish_testing)
        
        # Установка начального текста статуса
        self.ui.MainProcessLabel.setText("Готов к началу")
        
        # Инициализация прогресс-бара
        self.ui.MainProgressBar.setValue(0)
        self.progress_animation = QPropertyAnimation(self.ui.MainProgressBar, b"value")
        self.progress_animation.setEasingCurve(QEasingCurve.Linear)

        # Подключение кнопок
        self.ui.MainPlayButton.clicked.connect(self.start_testing)
        self.ui.MainStopButton.setEnabled(False)  # Изначально неактивна
        self.ui.MainStopButton.clicked.connect(self.stop_testing)
        self.ui.MainSettingsButton.clicked.connect(self.open_settings_window)

        # Путь для сохранения файлов
        self.save_path = user_data.save_path

    def start_testing(self):
        """Начинает процесс контроля: нагрев + охлаждение."""
        logger.info(f"Начало контроля зоны {tuple(self.current_position)}")

        # Формируем имена файлов
        object_name = user_data.object_of_testing.replace(" ", "_")
        position = f"zone({self.current_position[0]},{self.current_position[1]})"
        base_path = f"{self.save_path}/{object_name}_{position}"
        
        # Сохраняем путь для возможного удаления
        self.current_base_path = base_path
        
        # Активируем кнопку Stop
        self.ui.MainStopButton.setEnabled(True)
        
        # Деактивируем кнопку Start
        self.ui.MainPlayButton.setEnabled(False)

        # Начинаем запись видео на всех камерах
        try:
            self.camera_manager.start_recording_all(base_path)
        except Exception as e:
            logger.error(f"Не удалось начать запись: {e}")
            QMessageBox.critical(self, "Ошибка записи", f"Не удалось начать запись: {e}")
            self.stop_testing()
            return

        # Включаем нагрев
        heater.turn_on()
        
        # Обновляем текст с оставшимся временем
        self.ui.MainProcessLabel.setText(f"Нагрев... (осталось {settings.heating_duration} с)")
        
        # Запускаем таймер для обновления текста
        self.status_update_timer = QTimer()
        self.status_update_timer.setInterval(1000)  # Обновляем каждую секунду
        self.status_update_timer.timeout.connect(self.update_status_text)
        self.status_update_timer.start()
        
        # Настраиваем и запускаем анимацию прогресс-бара
        total_time_ms = settings.duration_of_testing * 1000
        self.progress_animation.setDuration(total_time_ms)
        self.progress_animation.setStartValue(0)
        self.progress_animation.setEndValue(100)
        self.progress_animation.start()

        # Запускаем таймер нагрева
        heating_duration = settings.heating_duration * 1000  # В миллисекундах
        self.heating_timer.start(heating_duration)

    def start_cooling(self):
        """Переходит к процессу охлаждения."""
        # Выключаем нагреватель
        heater.turn_off()
        
        # Обновляем текст процесса
        cooling_duration = (settings.duration_of_testing - settings.heating_duration)
        self.ui.MainProcessLabel.setText(f"Охлаждение... (осталось {cooling_duration} с)")

        # Запускаем таймер охлаждения
        cooling_duration = (settings.duration_of_testing - settings.heating_duration) * 1000  # В миллисекундах
        self.cooling_timer.start(cooling_duration)

    def finish_testing(self):
        """Завершает процесс контроля и запись видео."""
        # Останавливаем таймеры
        self.heating_timer.stop()
        self.cooling_timer.stop()

        # Останавливаем запись на всех камерах
        self.camera_manager.stop_recording_all()
        
        # Деактивируем кнопку Stop после успешного завершения
        self.ui.MainStopButton.setEnabled(False)
        
        # Останавливаем анимацию прогресс-бара
        self.progress_animation.stop()
        
        # Останавливаем таймер обновления текста
        if hasattr(self, 'status_update_timer'):
            self.status_update_timer.stop()

        # Устанавливаем завершающие значения
        self.ui.MainProgressBar.setValue(100)
        self.ui.MainProcessLabel.setText("Контроль зоны успешно завершён!")
        logger.info(f"Контроль зоны {tuple(self.current_position)} завершён.")

        # Переход к следующему действию
        self.open_trajectory_dialog()

    def stop_testing(self):
        """Прерывает процесс контроля."""
        # Останавливаем таймеры
        self.heating_timer.stop()
        self.cooling_timer.stop()
        
        # Выключаем нагреватель
        heater.turn_off()

        # Останавливаем запись на всех камерах
        self.camera_manager.stop_recording_all()
        
        # Останавливаем анимацию прогресс-бара
        self.progress_animation.stop()
        
        # Останавливаем таймер обновления текста
        if hasattr(self, 'status_update_timer'):
            self.status_update_timer.stop()
        
        # Обновляем статус
        self.ui.MainProcessLabel.setText("Контроль прерван")
        logger.warning("Контроль был прерван пользователем")
        
        # Удаляем записанные файлы текущей зоны
        self.delete_current_zone_files()
        
        # Деактивируем кнопку Stop
        self.ui.MainStopButton.setEnabled(False)
        
        # Активируем кнопку Start
        self.ui.MainPlayButton.setEnabled(True)
    
    def delete_current_zone_files(self):
        """Удаляет файлы текущей зоны при прерывании контроля."""
        try:
            if hasattr(self, 'current_base_path'):
                # Удаляем файлы для всех камер
                for camera_name in self.camera_manager.cameras.keys():
                    file_path = f"{self.current_base_path}_{camera_name}.avi"
                    if os.path.exists(file_path):
                        os.remove(file_path)
                        logger.info(f"Удален файл: {file_path}")
        except Exception as e:
            logger.error(f"Ошибка при удалении файлов: {e}")
    
    def open_settings_window(self):
        """Открывает окно настроек."""
        self.settingsWindow = SettingsWindow()
        self.settingsWindow.exec()
    
    def closeEvent(self, event):
        """Закрывает камеры при завершении работы приложения."""
        self.camera_manager.release_all()
        event.accept()
    
    def update_status_text(self):
        """Обновляет текст статуса с оставшимся временем."""
        elapsed = self.progress_animation.currentTime() / 1000  # В секундах
        remaining = settings.duration_of_testing - elapsed
        
        if elapsed < settings.heating_duration:
            phase = "Нагрев"
            phase_remaining = settings.heating_duration - elapsed
        else:
            phase = "Охлаждение"
            phase_remaining = remaining
        
        self.ui.MainProcessLabel.setText(
            f"{phase}... (осталось {phase_remaining:.0f} с)"
        )
    
    def open_trajectory_dialog(self):
        """Открывает диалоговое окно выбора следующей зоны."""
        self.trajectory_dialog = TrajectoryDialog()
        
        # Подключаем сигналы диалога к слотам главного окна
        self.trajectory_dialog.direction_selected.connect(self.handle_direction_selected)
        self.trajectory_dialog.retest_requested.connect(self.open_retest_dialog)
        self.trajectory_dialog.preview_requested.connect(self.handle_preview_request)
        self.trajectory_dialog.finish_requested.connect(self.open_finish_dialog)
        
        self.trajectory_dialog.exec()
    
    def handle_direction_selected(self, direction: str):
        """Обрабатывает выбор направления перемещения."""
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
        self.trajectory_dialog.allow_close = True
        self.trajectory_dialog.close()
        
        # Показываем сообщение о перемещении дефектоскопа
        QMessageBox.information(
            self,
            "Перемещение дефектоскопа",
            f"Пожалуйста, переместите дефектоскоп в направлении {direction_translation[direction]}.\n"
            "После перемещения нажмите ОК, чтобы начать контроль новой зоны.",
            QMessageBox.Ok
        )
        
        # Активируем кнопку Start для новой зоны
        self.ui.MainPlayButton.setEnabled(True)
    
    def open_retest_dialog(self):
        """Открывает диалоговое окно повторного контроля текущей зоны."""
        # Закрываем диалог выбора траектории СРАЗУ при переходе
        if hasattr(self, 'trajectory_dialog') and self.trajectory_dialog:
            self.trajectory_dialog.allow_close = True
            self.trajectory_dialog.close()
        
        # Создаем диалог повторного контроля
        zone_num = f"{self.current_position[0]},{self.current_position[1]}"
        self.retest_dialog = RetestDialog(zone_number=zone_num, parent=self)
        
        # Подключаем сигналы с новыми именами (по вашей рекомендации)
        self.retest_dialog.yes_clicked.connect(self.handle_retest_confirm)
        self.retest_dialog.no_clicked.connect(self.handle_retest_cancel)
        
        self.retest_dialog.exec()

    def handle_retest_confirm(self):
        """Обрабатывает подтверждение повторного контроля текущей зоны."""
        # Закрываем диалог повторного контроля
        if hasattr(self, 'retest_dialog') and self.retest_dialog:
            self.retest_dialog.close()
        
        # Удаляем записанные файлы текущей зоны
        self.delete_current_zone_files()
        
        # Восстанавливаем элементы главного окна в исходное состояние
        self.reset_main_window_state()
        
        # Обновляем статус
        self.ui.MainProcessLabel.setText("Готов к повторному контролю текущей зоны")
        logger.info(f"Подготовка к повторному контролю зоны {tuple(self.current_position)}")
        
        # НЕ запускаем контроль автоматически!
        # Контроль должно начинаться ТОЛЬКО по нажатию оператором на кнопку старт

    def handle_retest_cancel(self):
        """Обрабатывает отмену повторного контроля текущей зоны."""
        # Закрываем диалог повторного контроля
        if hasattr(self, 'retest_dialog') and self.retest_dialog:
            self.retest_dialog.close()
        
        # Открываем диалог выбора траектории (trajectory_dialog НЕ должен существовать сейчас)
        self.open_trajectory_dialog()
    
    def handle_preview_request(self):
        """Обрабатывает запрос на предпросмотр результатов."""
        # Закрываем диалог выбора траектории СРАЗУ при переходе
        if hasattr(self, 'trajectory_dialog') and self.trajectory_dialog:
            self.trajectory_dialog.allow_close = True
            self.trajectory_dialog.close()
        
        # Показываем сообщение о том, что функция в разработке
        QMessageBox.information(
            self,
            "Предпросмотр",
            "Функция предпросмотра ещё в разработке"
        )
        
        # После закрытия сообщения снова открываем диалог выбора траектории
        self.open_trajectory_dialog()
    
    def open_finish_dialog(self):
        """Открывает финальное диалоговое окно."""
        # Закрываем диалог выбора траектории СРАЗУ при переходе
        if hasattr(self, 'trajectory_dialog') and self.trajectory_dialog:
            self.trajectory_dialog.allow_close = True
            self.trajectory_dialog.close()
        
        # Создаем финальный диалог
        self.finish_dialog = FinishDialog(parent=self)
        self.finish_dialog.accepted.connect(self.handle_finish_accepted)
        self.finish_dialog.rejected.connect(self.handle_finish_rejected)
        self.finish_dialog.exec()

    def handle_finish_accepted(self):
        """Обрабатывает принятие финального диалога."""
        logger.info("Контроль успешно завершён")
        # Закрываем приложение
        self.close()

    def handle_finish_rejected(self):
        """Обрабатывает отклонение финального диалога."""
        logger.info("Завершение контроля отменено")
        # Закрываем финальный диалог
        if hasattr(self, 'finish_dialog') and self.finish_dialog:
            self.finish_dialog.close()
        
        # Возвращаемся к диалогу выбора траектории
        self.open_trajectory_dialog()
    
    def reset_main_window_state(self):
        """Сбрасывает состояние главного окна в исходное состояние."""
        # Сбрасываем прогресс-бар
        self.ui.MainProgressBar.setValue(0)
        
        # Деактивируем кнопку Stop
        self.ui.MainStopButton.setEnabled(False)
        
        # Активируем кнопку Start
        self.ui.MainPlayButton.setEnabled(True)
        
        # Сбрасываем анимацию прогресс-бара
        self.progress_animation.stop()
        
        # Останавливаем все таймеры, если они запущены
        self.heating_timer.stop()
        self.cooling_timer.stop()
        if hasattr(self, 'status_update_timer'):
            self.status_update_timer.stop()
        
        # Выключаем нагреватель на всякий случай
        try:
            heater.turn_off()
        except:
            pass


if __name__ == '__main__':
    # Диагностика PySpin и камер FLIR
    try:
        import PySpin
        logger.info("PySpin успешно импортирован")
        
        # Быстрая проверка камер без длительного удержания ресурсов
        system = PySpin.System.GetInstance()
        cam_list = system.GetCameras()
        num_cameras = cam_list.GetSize()
        logger.info(f"Количество обнаруженных камер FLIR: {num_cameras}")
        
        if num_cameras > 0:
            # Получаем информацию о первой камере
            camera = cam_list.GetByIndex(0)
            camera.Init()
            
            try:
                nodemap = camera.GetNodeMap()
                node_model = PySpin.CStringPtr(nodemap.GetNode("DeviceModelName"))
                if PySpin.IsAvailable(node_model):
                    logger.info(f"Модель камеры: {node_model.GetValue()}")
            finally:
                camera.DeInit()
                del camera
        
        cam_list.Clear()
        system.ReleaseInstance()
        
    except Exception as e:
        logger.error(f"Диагностика PySpin не удалась: {e}")
    
    # Инициализация приложения Qt
    app = QApplication(sys.argv)
    
    # Создание и отображение главного окна приложения
    start_window = StartWindow()
    start_window.showMaximized()
      
    # Запуск главного цикла приложения и выход при завершении
    sys.exit(app.exec())