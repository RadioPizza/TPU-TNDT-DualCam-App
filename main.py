# PTT v0.3.1

import sys
from pathlib import Path
from PySide6.QtWidgets import QApplication, QMainWindow, QDialog, QFileDialog, QMessageBox, QLineEdit
from PySide6.QtCore import Qt, QObject, Signal, QEvent, QTimer
from utils import Utilities as utils
from osk import OnScreenKeyboard as osk
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
    
    def hide_osk(self) -> None:
        """Закрывает экранную клавиатуру, если фокус ушел не на другое текстовое поле."""
        QTimer.singleShot(250, self._conditional_close_osk)

    def _conditional_close_osk(self) -> None:
        focused_widget = QApplication.focusWidget()
        if focused_widget not in self.input_fields:
            osk.close()
        # Если фокус на одном из текстовых полей, ничего не делаем

    def keyPressEvent(self, event) -> None:
        """Обрабатывает нажатия клавиш, игнорируя Enter и Return."""
        if event.key() not in (Qt.Key_Return, Qt.Key_Enter):
            super().keyPressEvent(event)

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
            user_data = {
                "name": self.ui.StartNameLineEdit.text().strip(),
                "surname": self.ui.StartSurnameLineEdit.text().strip(),
                "object_of_testing": self.ui.StartObjectLineEdit.text().strip(),
                "save_path": self.ui.StartPathLineEdit.text().strip(),
            }
            self.main_window = MainWindow(user_data)
            self.main_window.show()
            self.close()
    
    def _validate_form(self) -> bool:
        """Проверяет заполнены ли все необходимые поля и корректны ли введенные данные."""
        errors = []

        name = self.ui.StartNameLineEdit.text().strip()
        surname = self.ui.StartSurnameLineEdit.text().strip()
        object_of_testing = self.ui.StartObjectLineEdit.text().strip()
        save_path = self.ui.StartPathLineEdit.text().strip()

        # Сброс ранее установленных стилей
        self._reset_field_styles()

        # Проверка имени
        if not name:
            errors.append("Name cannot be empty.")
            self._highlight_field(self.ui.StartNameLineEdit)
        elif not name.isalpha():
            errors.append("The name must contain only letters.")
            self._highlight_field(self.ui.StartNameLineEdit)
        elif len(name) == 1:
            errors.append("The name cannot consist of one letter.")
            self._highlight_field(self.ui.StartNameLineEdit)

        # Проверка фамилии
        if not surname:
            errors.append("The last name cannot be empty.")
            self._highlight_field(self.ui.StartSurnameLineEdit)
        elif not surname.isalpha():
            errors.append("The last name must contain only letters.")
            self._highlight_field(self.ui.StartSurnameLineEdit)
        elif len(surname) == 1:
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
