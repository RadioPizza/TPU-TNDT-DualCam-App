import sys
from PySide6.QtWidgets import QApplication, QMainWindow, QDialog

# Импортируем сгенерированные классы UI
from MainWindow import Ui_MainWindow
from StartDialog import Ui_StartDialog

class StartApp(QDialog):
    def __init__(self):
        super(StartApp, self).__init__()
        self.ui = Ui_StartDialog()
        self.ui.setupUi(self)

        # При нажатии на кнопку, будет осуществлен переход к главному окну
        self.ui.StartStartButton.clicked.connect(self.openMainWindow)

    def openMainWindow(self):
        self.mainWindow = MainApp()  # Используем класс главного окна
        self.mainWindow.show()
        self.close()  # Закрываем стартовое окно при переходе

class MainApp(QMainWindow):
    def __init__(self):
        super(MainApp, self).__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)

        # Здесь код для инициализации элементов главного окна, включая обработчики событий

if __name__ == '__main__':
    app = QApplication(sys.argv)

    # Показываем сначала стартовое окно
    startApp = StartApp()
    startApp.show()

    sys.exit(app.exec())
