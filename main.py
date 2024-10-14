# PTT v0.3.0

import sys
import os
from pathlib import Path
import psutil

from PySide6.QtWidgets import QApplication, QMainWindow, QDialog, QFileDialog, QMessageBox
from PySide6.QtCore import Qt, QObject, Signal, QEvent, QTimer

from StartDialog import Ui_StartDialog
from MainWindow import Ui_MainWindow
from SettingsWindow import Ui_SettingsWindow
from TrajectoryDialog import Ui_TrajectoryDialog
from RetestDialog import Ui_RetestDialog
from PreviewWindow import Ui_PreviewWindow
from FinishDialog import Ui_FinishDialog

class FocusWatcher(QObject):
    focus_in = Signal()
    focus_out = Signal()

    def eventFilter(self, obj, event: QEvent) -> bool:
        if event.type() == QEvent.FocusIn:
            self.focus_in.emit()
        elif event.type() == QEvent.FocusOut:
            # Используем QTimer.singleShot, чтобы убедиться, что фокус уже обновился
            QTimer.singleShot(0, self.emit_focus_out)
        return super(FocusWatcher, self).eventFilter(obj, event)

    def emit_focus_out(self):
        self.focus_out.emit()

class StartWindow(QDialog):
    def __init__(self):
        super(StartWindow, self).__init__()
        self.ui = Ui_StartDialog()
        self.ui.setupUi(self)

        # Создаем экземпляр наблюдателя за фокусом
        self.focus_watcher = FocusWatcher()

        # Устанавливаем фильтр событий на поля ввода
        self.ui.StartNameLineEdit.installEventFilter(self.focus_watcher)
        self.ui.StartSurnameLineEdit.installEventFilter(self.focus_watcher)
        self.ui.StartObjectLineEdit.installEventFilter(self.focus_watcher)

        # Подключаем сигналы
        self.ui.StartStartButton.clicked.connect(self.open_MainWindow)
        self.ui.StartExitButton.clicked.connect(self.close)
        self.ui.StartChangePathButton.clicked.connect(self.change_save_path)
        self.focus_watcher.focus_in.connect(self.open_osk)
        self.focus_watcher.focus_out.connect(self.close_osk)
    
    def is_osk_running(self) -> bool:
        """Проверяет, запущена ли экранная клавиатура."""
        for proc in psutil.process_iter(['name']):
            if proc.info['name'] == 'osk.exe':
                return True
        return False
     
    def open_osk(self) -> None:
        """Запускает экранную клавиатуру."""
        if not self.is_osk_running():
            try:
                os.startfile("osk")
            except Exception as e:
                print(f"Не удалось запустить экранную клавиатуру: {e}")

    def close_osk(self) -> None:
        """Закрывает экранную клавиатуру, если фокус ушел не на другое текстовое поле."""
        QTimer.singleShot(250, self._conditional_close_osk)

    def _conditional_close_osk(self):
        focused_widget = QApplication.focusWidget()
        # Список текстовых полей
        text_fields = [
            self.ui.StartNameLineEdit,
            self.ui.StartSurnameLineEdit,
            self.ui.StartObjectLineEdit
        ]
        if focused_widget not in text_fields:
            # Если фокус не на текстовом поле, закрываем osk
            try:
                for proc in psutil.process_iter(['pid', 'name']):
                    if proc.info['name'] == 'osk.exe':
                        proc.kill()  # Принудительно завершает процесс
                        break
            except (psutil.NoSuchProcess, Exception) as e:
                print(f"Не удалось закрыть экранную клавиатуру: {e}")
        # Иначе не делаем ничего, osk остается открытой

    def keyPressEvent(self, event) -> None:
        if event.key() not in (Qt.Key_Return, Qt.Key_Enter):
            super().keyPressEvent(event)

    def change_save_path(self) -> None:
        """Открывает диалоговое окно выбора каталога и устанавливает путь в поле StartPathLineEdit."""
        try:
            path = QFileDialog.getExistingDirectory(self, "Select Directory")
            if path:
                self.ui.StartPathLineEdit.setText(path)
        except Exception as e:
             self.show_error(f"Произошла ошибка при выборе пути сохранения: {e}")

    def open_MainWindow(self) -> None:
        '''Открывает основное окно, закрывая стартовое'''
        if self._validate_form():
            user_data = {
                "name": self.ui.StartNameLineEdit.text().strip(),
                "surname": self.ui.StartSurnameLineEdit.text().strip(),
                "object_of_testing": self.ui.StartObjectLineEdit.text().strip(),
                "save_path": self.ui.StartPathLineEdit.text().strip(),
            }
            self.mainWindow = MainWindow(user_data)
            self.mainWindow.show()
            self.close()
    
    def _validate_form(self) -> bool:
        '''Проверяет заполнены ли все поля'''
        name = self.ui.StartNameLineEdit.text().strip()
        surname = self.ui.StartSurnameLineEdit.text().strip()
        object_of_testing = self.ui.StartObjectLineEdit.text().strip()
        save_path = self.ui.StartPathLineEdit.text().strip()

        if not all([name, surname, object_of_testing]) or save_path == '...':
            QMessageBox.warning(self, "Incomplete Form", "Please fill in all fields and select a save path.")
            return False
        elif not self.is_valid_path(save_path):
            self.show_error("The specified save path is invalid. Please select an existing folder.")
            return False
        return True
        
    def is_valid_path(self, path: str) -> bool:
        '''Проверяет путь'''
        return Path(path).exists() and Path(path).is_dir()
    
    def show_error(self, message: str) -> None:
        """Показывает сообщение об ошибке."""
        QMessageBox.critical(self, message)

class MainWindow(QMainWindow):
    def __init__(self, user_data):
        super(MainWindow, self).__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)

        self.ui.MainSettingsButton.clicked.connect(self.openSettingsWindow)
        self.ui.MainPlayButton.clicked.connect(self.startTesting)
        
        print(user_data)

    def openSettingsWindow(self):
        self.settingsWindow = SettingsWindow()
        self.settingsWindow.show()
    
    def openTrajectoryDialog(self):
        self.TrajectoryDialog = TrajectoryDialog()
        self.TrajectoryDialog.show()

    def startTesting(self):
        self.openTrajectoryDialog()

    def stopTesting(self):
        pass

    def saveData(self):
        pass

class SettingsWindow(QDialog):
    def __init__(self):
        super(SettingsWindow, self).__init__()
        self.ui = Ui_SettingsWindow()
        self.ui.setupUi(self)
        
        self.ui.SettingsHomeButton.clicked.connect(self.close)

class TrajectoryDialog(QDialog):
    def __init__(self):
        super(TrajectoryDialog, self).__init__()
        self.ui = Ui_TrajectoryDialog()
        self.ui.setupUi(self)

        self.ui.TrajectoryRepeatButton.clicked.connect(self.openRetestDialog)
        self.ui.TrajectoryPreviewButton.clicked.connect(self.openPreviewWindow)
        self.ui.TrajectoryFinishButton.clicked.connect(self.openFinishDialog)

    def openRetestDialog(self):
        self.RetestDialog = RetestDialog()
        self.RetestDialog.show()
        self.close()
    
    def openPreviewWindow(self):
        self.PreviewWindow = PreviewWindow()
        self.PreviewWindow.show()
        self.close()
    
    def openFinishDialog(self):
        self.FinishDialog = FinishDialog()
        self.FinishDialog.show()
        self.close()

class RetestDialog(QDialog):
    def __init__(self):
        super(RetestDialog, self).__init__()
        self.ui = Ui_RetestDialog()
        self.ui.setupUi(self)

        self.ui.RetestYesButton.clicked.connect(self.openMainWindow)
        self.ui.RetestNoButton.clicked.connect(self.openTrajectoryDialog)

    def openMainWindow(self):
        self.close()
    
    def openTrajectoryDialog(self):
        self.openTrajectoryDialog = TrajectoryDialog()
        self.openTrajectoryDialog.show()
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
    app = QApplication(sys.argv)
    stylesheet_path = "LightStyle.qss"
    app.setStyleSheet(Path(stylesheet_path).read_text())
    StartWindow = StartWindow()
    StartWindow.show()
    sys.exit(app.exec())
