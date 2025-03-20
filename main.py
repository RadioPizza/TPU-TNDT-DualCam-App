# PTT v0.6.0

# Стандартные библиотеки
import logging
import sys
from pathlib import Path

# Библиотеки третьих сторон
import numpy as np
from PySide6.QtCore import QEvent, QObject, Qt, QTimer, Signal
from PySide6.QtGui import QImage, QPixmap
from PySide6.QtWidgets import (QApplication, QDialog, QFileDialog,
                               QGraphicsPixmapItem, QGraphicsScene, QLineEdit,
                               QMainWindow, QMessageBox)
from serial_communicator import SerialCommunicator as com

# Локальные модули
from cameras import get_available_cameras, VisibleCameraWidget, ThermalCameraWidget
from FinishDialog import Ui_FinishDialog
from heater_interface import Heater
from MainWindow import Ui_MainWindow
from osk import OnScreenKeyboard as osk
from PreviewWindow import Ui_PreviewWindow
from RetestDialog import Ui_RetestDialog
from settings import PreviewSettings, Settings, UserData
from SettingsWindow import Ui_SettingsWindow
from StartDialog import Ui_StartDialog
from TrajectoryDialog import Ui_TrajectoryDialog
from utils import Utilities as utils


class FocusWatcher(QObject):
    # Определяем сигналы, которые будем испускать при получении и потере фокуса
    focus_in = Signal()
    focus_out = Signal()

    # Переопределяем метод eventFilter для фильтрации событий
    def eventFilter(self, obj, event: QEvent) -> bool:
        # Проверяем тип события
        if event.type() == QEvent.FocusIn:
            # Если объект получил фокус, испускаем сигнал focus_in
            self.focus_in.emit()
        elif event.type() == QEvent.FocusOut:
            # Если объект потерял фокус
            # Используем QTimer.singleShot, чтобы убедиться, что фокус уже обновился
            # Это откладывает вызов emit_focus_out до следующего цикла обработки событий
            QTimer.singleShot(0, self.emit_focus_out)
        # Вызываем базовый метод для продолжения стандартной обработки события
        return super(FocusWatcher, self).eventFilter(obj, event)

    # Метод для испускания сигнала focus_out
    def emit_focus_out(self):
        self.focus_out.emit()

class StartWindow(QDialog):
    def __init__(self):
        super().__init__()
        self.ui = Ui_StartDialog()
        self.ui.setupUi(self)

        # Список полей ввода, за которыми будем отслеживать фокус
        self.input_fields = [
            self.ui.StartNameLineEdit,
            self.ui.StartSurnameLineEdit,
            self.ui.StartObjectLineEdit
        ]

        # Создаем экземпляр наблюдателя за фокусом и устанавливаем на поля
        self.focus_watcher = FocusWatcher()
        for field in self.input_fields:
            field.installEventFilter(self.focus_watcher)

        # Подключаем сигналы фокусировки
        self.focus_watcher.focus_in.connect(osk.open)
        self.focus_watcher.focus_out.connect(self.hide_osk)

        # Подключаем сигналы кнопок
        self.ui.StartStartButton.clicked.connect(self.open_main_window)
        self.ui.StartExitButton.clicked.connect(self.close)
        self.ui.StartChangePathButton.clicked.connect(self.change_save_path)
    
    def keyPressEvent(self, event) -> None:
        """Обрабатывает нажатия клавиш, игнорируя Enter и Return."""
        if event.key() not in (Qt.Key_Return, Qt.Key_Enter):
            super().keyPressEvent(event)

    def hide_osk(self) -> None:
        """Закрывает экранную клавиатуру, если фокус ушел не на другое текстовое поле."""
        QTimer.singleShot(250, self._conditional_close_osk)

    def _conditional_close_osk(self) -> None:
        focused_widget = QApplication.focusWidget()
        if focused_widget not in self.input_fields:
            osk.close()
        # Если фокус на одном из текстовых полей, ничего не делаем

    def change_save_path(self) -> None:
        """Открывает диалоговое окно выбора каталога и устанавливает путь в поле StartPathLineEdit."""
        try:
            path = QFileDialog.getExistingDirectory(self, "Select Directory")
            if path:
                self.ui.StartPathLineEdit.setText(path)
        except Exception as e:
            QMessageBox.critical(self, "Error", f"An error occurred while selecting the save path: {e}.")

    def open_main_window(self) -> None:
        """Открывает основное окно, закрывая стартовое."""
        if self._validate_form():
            user_data.user_name = self.ui.StartNameLineEdit.text().strip()
            user_data.user_surname = self.ui.StartSurnameLineEdit.text().strip()
            user_data.object_of_testing = self.ui.StartObjectLineEdit.text().strip()
            user_data.save_path = self.ui.StartPathLineEdit.text().strip()

            self.main_window = MainWindow()
            self.main_window.show()
            self.close()
    
    def _validate_form(self) -> bool:
        """Проверяет заполнены ли все необходимые поля и корректны ли введенные данные."""
        errors = []

        user_name = self.ui.StartNameLineEdit.text().strip()
        user_surname = self.ui.StartSurnameLineEdit.text().strip()
        object_of_testing = self.ui.StartObjectLineEdit.text().strip()
        save_path = self.ui.StartPathLineEdit.text().strip()

        # Сброс ранее установленных стилей
        self._reset_field_styles()

        # Проверка имени
        if not user_name:
            errors.append("Name cannot be empty.")
            self._highlight_field(self.ui.StartNameLineEdit)
        elif not user_name.isalpha():
            errors.append("The name must contain only letters.")
            self._highlight_field(self.ui.StartNameLineEdit)
        elif len(user_name) == 1:
            errors.append("The name cannot consist of one letter.")
            self._highlight_field(self.ui.StartNameLineEdit)

        # Проверка фамилии
        if not user_surname:
            errors.append("The last name cannot be empty.")
            self._highlight_field(self.ui.StartSurnameLineEdit)
        elif not user_surname.isalpha():
            errors.append("The last name must contain only letters.")
            self._highlight_field(self.ui.StartSurnameLineEdit)
        elif len(user_surname) == 1:
            errors.append("The surname cannot consist of one letter.")
            self._highlight_field(self.ui.StartSurnameLineEdit)

        # Проверка объекта тестирования
        if not object_of_testing:
            errors.append("The test object cannot be empty.")
            self._highlight_field(self.ui.StartObjectLineEdit)

        # Проверка пути сохранения
        if not save_path or save_path == '...':
            errors.append("You must select a path to save.")
            self._highlight_field(self.ui.StartPathLineEdit)
        elif not utils.is_valid_path(save_path):
            errors.append("The specified save path is invalid. Please select an existing folder..")
            self._highlight_field(self.ui.StartPathLineEdit)

        if errors:
            error_message = "\n".join(errors)
            QMessageBox.critical(self, "Error filling out the form", error_message)
            return False

        return True
    
    def _highlight_field(self, field: QLineEdit) -> None:
        """Выделяет поле, в котором обнаружена ошибка."""
        field.setStyleSheet("border: 1px solid red;")

    def _reset_field_styles(self) -> None:
        """Сбрасывает стили всех полей ввода."""
        fields = [
            self.ui.StartNameLineEdit,
            self.ui.StartSurnameLineEdit,
            self.ui.StartObjectLineEdit,
            self.ui.StartPathLineEdit
        ]
        for field in fields:
            field.setStyleSheet("")

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)

        # Поля
        self.current_position = np.zeros(2, dtype=int)  # Текущая зона контроля [x, y]
        self.last_moving = np.zeros(2, dtype=int)       # Последнее перемещение [dx, dy]
        self.progress = 0

        # Камеры
        self.camera_widget = VisibleCameraWidget(settings, self.ui.MainCameraView)
        self.thermal_camera_widget = ThermalCameraWidget(settings, self.ui.MainTCameraView)

        # Таймеры
        self.heating_timer = QTimer()
        self.heating_timer.timeout.connect(self.start_cooling)

        self.cooling_timer = QTimer()
        self.cooling_timer.timeout.connect(self.finish_recording)

        # Подключение кнопок
        self.ui.MainPlayButton.clicked.connect(self.start_testing)
        self.ui.MainStopButton.clicked.connect(self.stop_testing)
        self.ui.MainSettingsButton.clicked.connect(self.open_settings_window)

        # Путь для сохранения файлов
        self.save_path = user_data.save_path

    def start_testing(self):
        """Начинает процесс контроля: нагрев + охлаждение."""
        logger.info(f"Начало тестирования зоны {tuple(self.current_position)}")

        # Формируем имена файлов
        object_name = user_data.object_of_testing.replace(" ", "_")
        position = f"zone({self.current_position[0]},{self.current_position[1]})"
        visible_file = f"{self.save_path}/{object_name}_{position}_visible.avi"
        thermal_file = f"{self.save_path}/{object_name}_{position}_thermal.avi"

        # Начинаем запись видео
        self.camera_widget.start_recording(visible_file)
        self.thermal_camera_widget.start_recording(thermal_file)

        # Включаем нагрев
        heater.turn_on()
        self.ui.MainProcessLabel.setText("Heating...")

        # Запускаем таймер нагрева
        heating_duration = settings.heating_duration * 1000  # В миллисекундах
        self.heating_timer.start(heating_duration)

    def start_cooling(self):
        """Переходит к процессу охлаждения."""
        heater.turn_off()
        self.ui.MainProcessLabel.setText("Cooling...")

        # Запускаем таймер охлаждения
        cooling_duration = (settings.duration_of_testing - settings.heating_duration) * 1000  # В миллисекундах
        self.cooling_timer.start(cooling_duration)

    def finish_recording(self):
        """Завершает процесс контроля и запись видео."""
        self.heating_timer.stop()
        self.cooling_timer.stop()

        # Останавливаем запись
        self.camera_widget.stop_recording()
        self.thermal_camera_widget.stop_recording()

        self.ui.MainProcessLabel.setText("Zone completed.")
        logger.info(f"Тестирование зоны {tuple(self.current_position)} завершено.")

        # Переход к следующему действию
        self.open_trajectory_dialog()

    def stop_testing(self):
        """Прерывает процесс контроля."""
        self.heating_timer.stop()
        self.cooling_timer.stop()
        heater.turn_off()

        # Останавливаем запись
        self.camera_widget.stop_recording()
        self.thermal_camera_widget.stop_recording()

        self.ui.MainProcessLabel.setText("Testing stopped.")
        logger.warning("Тестирование было прервано пользователем.")

    def open_trajectory_dialog(self):
        """Открывает диалог выбора следующей зоны."""
        self.trajectory_dialog = TrajectoryDialog()
        self.trajectory_dialog.show()

    def open_settings_window(self):
        """Открывает окно настроек."""
        self.settingsWindow = SettingsWindow()
        self.settingsWindow.show()

    def closeEvent(self, event):
        """Закрывает камеры при завершении работы приложения."""
        self.camera_widget.release()
        self.thermal_camera_widget.release()
        event.accept()
    
class SettingsWindow(QDialog):
    def __init__(self):
        super(SettingsWindow, self).__init__()
        self.ui = Ui_SettingsWindow()
        self.ui.setupUi(self)
        
        self.ui.SettingsHomeButton.clicked.connect(self.close)

class TrajectoryDialog(QDialog):
    def __init__(self):
        super().__init__()
        self.ui = Ui_TrajectoryDialog()
        self.ui.setupUi(self)

        # Подключаем сигналы кнопок
        self.ui.TrajectoryRightButton.clicked.connect(lambda: self.trajectory_handler('right'))
        self.ui.TrajectoryLeftButton.clicked.connect(lambda: self.trajectory_handler('left'))
        self.ui.TrajectoryUpButton.clicked.connect(lambda: self.trajectory_handler('up'))
        self.ui.TrajectoryDownButton.clicked.connect(lambda: self.trajectory_handler('down'))
        self.ui.TrajectoryRepeatButton.clicked.connect(self.open_retest_dialog)
        self.ui.TrajectoryPreviewButton.clicked.connect(self.open_preview_window)
        self.ui.TrajectoryFinishButton.clicked.connect(self.open_finish_dialog)

    def trajectory_handler(self, direction: str) -> None:
        """Здесь нужно написать описание."""
        match direction:
            case 'right':   MainWindow.last_moving = np.array([ 1,  0])
            case 'left':    MainWindow.last_moving = np.array([-1,  0])
            case 'up':      MainWindow.last_moving = np.array([ 0,  1])
            case 'down':    MainWindow.last_moving = np.array([ 0, -1])
        MainWindow.current_position += MainWindow.last_moving
        self.close()

    def open_retest_dialog(self) -> None:
        """Открывает диалоговое окно Retest, закрывая себя."""
        self.RetestDialog = RetestDialog()
        self.RetestDialog.show()
        self.close()
    
    def open_preview_window(self) -> None:
        """Открывает окно предпросмотра, закрывая себя."""
        self.PreviewWindow = PreviewWindow()
        self.PreviewWindow.show()
        self.close()
    
    def open_finish_dialog(self) -> None:
        """Открывает финальное окно, закрывая себя."""
        self.FinishDialog = FinishDialog()
        self.FinishDialog.show()
        self.close()

class RetestDialog(QDialog):
    def __init__(self):
        super().__init__()
        self.ui = Ui_RetestDialog()
        self.ui.setupUi(self)
        
        # Подключаем сигналы кнопок
        self.ui.RetestNoButton.clicked.connect(self.openTrajectoryDialog)
        self.ui.RetestYesButton.clicked.connect(self.close())

    def open_trajectory_dialog(self) -> None:
        """Открывает диалоговое окно выбора следующего положения."""
        self.TrajectoryDialog = TrajectoryDialog()
        self.TrajectoryDialog.show()
        self.close()

    def retest(self):
        """Здесь нужно написать описание."""
        self.main_window.delete_current_zone_data()
        self.close()

class PreviewWindow(QDialog):
    def __init__(self):
        super(PreviewWindow, self).__init__()
        self.ui = Ui_PreviewWindow()
        self.ui.setupUi(self)

        self.ui.PreviewHomeButton.clicked.connect(self.openTrajectoryDialog)
        self.ui.PreviewFinishButton.clicked.connect(self.openFinishDialog)

    def openTrajectoryDialog(self):
        self.openTrajectoryDialog = TrajectoryDialog()
        self.openTrajectoryDialog.show()
        self.close()
    
    def openFinishDialog(self):
        self.FinishDialog = FinishDialog()
        self.FinishDialog.show()
        self.close()

class FinishDialog(QDialog):
    def __init__(self):
        super(FinishDialog, self).__init__()
        self.ui = Ui_FinishDialog()
        self.ui.setupUi(self)

if __name__ == '__main__':
    # Настройка базового конфигуратора логирования
    logging.basicConfig(
        level=logging.INFO,  # Уровень логирования можно изменить при необходимости
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        handlers=[
            #FileHandler("app.log"),    # Запись логов в файл
            logging.StreamHandler()     # Также вывод логов в консоль
        ]
    )

    logger = logging.getLogger(__name__)
    
    # Инициализация приложения Qt
    app = QApplication(sys.argv)
    
    # Установка пути к файлу стилей
    stylesheet_path = "LightStyle.qss"
    
    # Установка стиля приложения из файла QSS
    app.setStyleSheet(Path(stylesheet_path).read_text())
    
    # Создание и отображение главного окна приложения
    StartWindow = StartWindow()
    StartWindow.show()
    
    # Получение экземпляра объекта UserData
    user_data = UserData.get_instance()
    
    # Загрузка настроек из файла
    settings = Settings.load_from_file()
    
    # Получение экземпляра объекта PreviewSettings
    preview_settings = PreviewSettings.get_instance()
    
    # Инициализация обогревателя с параметрами из настроек
    heater = Heater(settings.heater_COM_port_number, settings.heater_baud_rate)
    
    # Запуск главного цикла приложения и выход при завершении
    sys.exit(app.exec())