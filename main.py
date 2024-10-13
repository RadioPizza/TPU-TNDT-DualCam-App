# PTT v0.2.2

from PySide6.QtWidgets import QApplication, QMainWindow, QDialog, QFileDialog, QMessageBox
from PySide6.QtCore import Qt, QObject, Signal, QEvent
from StartDialog import Ui_StartDialog
from MainWindow import Ui_MainWindow
from SettingsWindow import Ui_SettingsWindow
from TrajectoryDialog import Ui_TrajectoryDialog
from RetestDialog import Ui_RetestDialog
from PreviewWindow import Ui_PreviewWindow
from FinishDialog import Ui_FinishDialog

import sys
from pathlib import Path
import subprocess

class FocusWatcher(QObject):
    focus_in = Signal()
    focus_out = Signal()

    def eventFilter(self, obj, event):
        if event.type() == QEvent.FocusIn:
            self.focus_in.emit()
        elif event.type() == QEvent.FocusOut:
            self.focus_out.emit()
        return super(FocusWatcher, self).eventFilter(obj, event)
    
class StartWindow(QDialog):
    def __init__(self):
        super(StartWindow, self).__init__()
        self.ui = Ui_StartDialog()
        self.ui.setupUi(self)

        self.ui.StartStartButton.clicked.connect(self.openMainWindow)
        self.ui.StartExitButton.clicked.connect(self.close)
        self.ui.StartChangePathButton.clicked.connect(self.changePath)

        # Создаем экземпляр наблюдателя за фокусом
        self.focus_watcher = FocusWatcher()

        # Устанавливаем фильтр событий на поля ввода
        self.ui.StartNameLineEdit.installEventFilter(self.focus_watcher)
        self.ui.StartSurnameLineEdit.installEventFilter(self.focus_watcher)

        # Подключаем сигналы
        self.focus_watcher.focus_in.connect(self.open_osk)
        self.focus_watcher.focus_out.connect(self.close_osk)
        
        # Инициализация переменной для процесса экранной клавиатуры
        self.osk_process = None 
        
    def open_osk(self):
        if not self.osk_process:
            try:
                self.osk_process = subprocess.Popen('osk.exe')
                print("Экранная клавиатура запущена.")
            except Exception as e:
                print(f"Не удалось запустить экранную клавиатуру: {e}")

    def close_osk(self):
        if self.osk_process:
            try:
                self.osk_process.terminate()
                self.osk_process = None
                print("Экранная клавиатура закрыта.")
            except Exception as e:
                print(f"Не удалось закрыть экранную клавиатуру: {e}")


    def keyPressEvent(self, event):
        if event.key() == Qt.Key_Return or event.key() == Qt.Key_Enter:
            pass
        else:
            super().keyPressEvent(event)

    def changePath(self):
        # Открытие диалога выбора папки
        path = QFileDialog.getExistingDirectory(self, "Select Directory")
        if path:
            # Записывание выбранного пути в поле ввода пути
            self.ui.StartPathLineEdit.setText(path)

    def openMainWindow(self):
        # Считывание значений из полей ввода
        name = self.ui.StartNameLineEdit.text().strip()
        surname = self.ui.StartSurnameLineEdit.text().strip()
        object_of_testing = self.ui.StartObjectLineEdit.text().strip()
        files_saving_path = self.ui.StartPathLineEdit.text().strip()

        # Проверка, что все текстовые поля заполнены и выбран путь сохранения
        if not name or not surname or not object_of_testing or files_saving_path == '...':
            QMessageBox.warning(self, "Incomplete Form", "Please fill in all fields and select a save path.")
        else:
            # Все данные заполнены, открываем главное окно
            user_data = {
                "name": name,
                "surname": surname,
                "object_of_testing": object_of_testing,
                "files_saving_path": files_saving_path,
            }
            self.mainWindow = MainWindow(user_data)  # Передача данных пользователя в главное окно
            self.mainWindow.show()
            self.close()

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

    # Путь к файлу стилей
    stylesheet_path = "LightStyle.qss"
    app.setStyleSheet(Path(stylesheet_path).read_text())
    
    StartWindow = StartWindow()
    StartWindow.show()

    sys.exit(app.exec())
