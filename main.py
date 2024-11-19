# PTT v0.6.0

# Стандартные библиотеки
import json
import sys
from dataclasses import asdict, dataclass, field
from pathlib import Path
from typing import List, Optional

# Библиотеки третьих сторон
import cv2
import numpy as np
import PySpin
from PySide6.QtCore import QEvent, QObject, Qt, QTimer, Signal
from PySide6.QtGui import QImage, QPixmap
from PySide6.QtWidgets import (QApplication, QDialog, QFileDialog,
                               QGraphicsPixmapItem, QGraphicsScene, QLineEdit,
                               QMainWindow, QMessageBox)
from serial_communicator import SerialCommunicator as com

# Локальные модули
from FinishDialog import Ui_FinishDialog
from heater_interface import Heater
from MainWindow import Ui_MainWindow
from osk import OnScreenKeyboard as osk
from PreviewWindow import Ui_PreviewWindow
from RetestDialog import Ui_RetestDialog
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

class CameraWidget:
    """Базовый класс для виджета камеры."""

    def __init__(self, camera_index, preview_fps, graphics_view):
        """
        Инициализация камеры и связанных компонентов.

        :param camera_index: Индекс устройства камеры для cv2.VideoCapture.
        :param preview_fps: Частота обновления кадров.
        :param graphics_view: QGraphicsView для отображения видео.
        """
        self.camera = cv2.VideoCapture(camera_index)
        if not self.camera.isOpened():
            print(f"Ошибка: Не удалось открыть камеру с индексом {camera_index}")
            # Можно вызвать исключение или обработать ошибку соответствующим образом.

        self.timer = QTimer()
        self.timer.timeout.connect(self.update_frame)
        self.timer.start(1000 // preview_fps)

        self.scene = QGraphicsScene()
        graphics_view.setScene(self.scene)
        self.pixmap_item = QGraphicsPixmapItem()
        self.scene.addItem(self.pixmap_item)
        self.graphics_view = graphics_view

    def update_frame(self):
        """Захватывает и обновляет кадры с камеры."""
        ret, frame = self.camera.read()
        if ret:
            frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            h, w, ch = frame.shape
            bytes_per_line = ch * w
            q_image = QImage(frame.data, w, h, bytes_per_line, QImage.Format_RGB888)
            pixmap = QPixmap.fromImage(q_image)
            self.pixmap_item.setPixmap(pixmap)
            self.graphics_view.fitInView(self.pixmap_item, Qt.KeepAspectRatio)
        else:
            print("Ошибка: Не удалось получить кадр с камеры")

    def release(self):
        """Освобождает ресурсы камеры."""
        if self.camera.isOpened():
            self.camera.release()
        self.timer.stop()

class MainCameraWidget(CameraWidget):
    """Класс для основной камеры."""
    def __init__(self, graphics_view):
        super().__init__(settings.camera_index, settings.camera_previewFPS, graphics_view)

class ThermalCameraWidget(CameraWidget):
    """Класс для ИК камеры."""
    def __init__(self, graphics_view):
        super().__init__(settings.thermal_camera_index, settings.thermal_camera_previewFPS, graphics_view)

    def update_frame(self):
        """Переопределяем метод для обработки кадров с ИК камеры."""
        ret, frame = self.camera.read()
        if ret:
            # Предположим, что ИК камера выдает одноканальное изображение
            # Дополнительная обработка для ИК камеры
            frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            # Например, применим цветовую карту к ИК изображению
            # frame = cv2.applyColorMap(frame, cv2.COLORMAP_JET)
            h, w, ch = frame.shape
            bytes_per_line = ch * w
            q_image = QImage(frame.data, w, h, bytes_per_line, QImage.Format_RGB888)
            pixmap = QPixmap.fromImage(q_image)
            self.pixmap_item.setPixmap(pixmap)
            self.graphics_view.fitInView(self.pixmap_item, Qt.KeepAspectRatio)
        else:
            print("Ошибка: Не удалось получить кадр с ИК камеры")

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)

        # Поля
        self.current_position = np.zeros(2) # вектор, хранящий координаты текущей зоны [x, y]
        self.last_moving = np.zeros(2)      # вектор, хранящий последнее перемещение [dx, dy]
        self.progress = 0
        
        # Выставляем 0 на полосе прогресса
        self.ui.MainProgressBar.setValue(0)
        
        # Подключаем сигналы кнопок
        self.ui.MainPlayButton.clicked.connect(self.start_testing)
        self.ui.MainStopButton.clicked.connect(self.stop_testing)
        self.ui.MainSettingsButton.clicked.connect(self.open_settings_window)

        # Инициализируем основную камеру
        self.camera_widget = CameraWidget(self.ui.MainCameraView)

        # Инициализируем ИК камеру
        self.thermal_camera_widget = ThermalCameraWidget(self.ui.MainTCameraView)
        
    def keyPressEvent(self, event) -> None:
        """Обрабатывает нажатия клавиш, игнорируя Esc."""
        if event.key() != Qt.Key_Escape:
            super().keyPressEvent(event)

    def start_testing(self) -> None:
        """Запускает/продолжает контроль."""
        heater.turn_on()
        # здесь будет код самой логики контроля

    def stop_testing(self) -> None:
        """Останавливает контроль."""
        heater.turn_off()
        # здесь будет код остановки самой логики контроля
        self.delete_current_zone_data()

    def open_settings_window(self) -> None:
        """Открывает окно настроек."""
        self.settingsWindow = SettingsWindow()
        self.settingsWindow.show()
    
    def open_trajectory_dialog(self) -> None:
        """Открывает диалоговое окно выбора следующего положения."""
        self.TrajectoryDialog = TrajectoryDialog()
        self.TrajectoryDialog.show()

    def delete_current_zone_data(self) -> None:
        """Удаляет данные о текущей зоне контроля и последнем перемещении."""
        # здесь будет delete last video
        self.current_position -= self.last_moving
    
    def update_frame(self):
        """Захватывает и обновляет кадры с камеры."""
        ret, frame = self.camera.read()  # Читаем кадр с камеры
        if ret:
            # Преобразуем изображение из формата BGR (OpenCV) в RGB (для отображения в PySide6)
            frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            h, w, ch = frame.shape
            bytes_per_line = ch * w
            q_image = QImage(frame.data, w, h, bytes_per_line, QImage.Format_RGB888)

            # Преобразуем QImage в QPixmap и обновляем QGraphicsPixmapItem
            pixmap = QPixmap.fromImage(q_image)
            self.pixmap_item.setPixmap(pixmap)

    def closeEvent(self, event):
        """Закрывает камеры и таймеры при закрытии окна."""
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

@dataclass
class UserData:
    user_name: Optional[str] = None
    user_surname: Optional[str] = None
    object_of_testing: Optional[str] = None
    save_path: Optional[str] = None

@dataclass
class Settings:
    duration_of_testing: int = 30
    heating_duration: int = 10
    language: str = 'EN'
    theme: str = 'Light'
    thermal_camera_index: int = 0
    thermal_camera_resolution: List[int] = field(default_factory=lambda: [640, 480])
    thermal_camera_previewFPS: int = 20
    thermal_camera_recordFPS: int = 5
    camera_index: int = 0
    camera_resolution: List[int] = field(default_factory=lambda: [640, 480])
    camera_previewFPS: int = 30
    camera_recordFPS: int = 5
    heater_COM_port_number: int = 0
    heater_baud_rate: int = 9600

    def save_settings(self, filename: str = 'settings.json') -> None:
        """Сохраняет настройки в файл"""
        settings_dict = asdict(self)
        with open(filename, 'w') as f:
            json.dump(settings_dict, f, indent=4)
        print(f"Настройки сохранены в файл {filename}.")

    def load_settings(self, path: str) -> None:
        """Устанавливает настройки из файла"""
        with open(path, 'r') as f:
            settings_dict = json.load(f)
        for key, value in settings_dict.items():
            setattr(self, key, value)
        print(f"Настройки загружены из файла {path}.")

@dataclass
class PreviewSettings:
    number_of_zone: List[int] = field(default_factory=lambda: [0, 0])  # выбранная для просмотра зона контроля
    map_flag: int = 1       # показывает, активен ли режим карты
    current_frame: int = 0  # текущий просматриваемый кадр видео
    type_of_graph: int = 0  # 0 - 2D, 1 - 3D

    # Алгоритмы постобработки изображений: 0 - off, 1 - on
    bs_alg: int = 0     # Background Subtraction
    fft_alg: int = 0    # Fast Fourier Transform
    pca_alg: int = 0    # Principal Component Analysis

if __name__ == '__main__':
    app = QApplication(sys.argv)
    stylesheet_path = "LightStyle.qss"
    app.setStyleSheet(Path(stylesheet_path).read_text())
    StartWindow = StartWindow()
    StartWindow.show()
    user_data = UserData()
    settings = Settings()
    preview_settings = PreviewSettings()
    heater = Heater(settings.heater_COM_port_number, settings.heater_baud_rate)
    sys.exit(app.exec())
