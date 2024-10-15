from PySide6.QtWidgets import (
    QApplication, QWidget, QPushButton, QLabel, QVBoxLayout,
    QMessageBox, QComboBox, QHBoxLayout
)
from PySide6.QtCore import Qt
from heater_interface import Heater
import sys
import serial.tools.list_ports

class HeaterApp(QWidget):
    def __init__(self):
        super().__init__()

        # Инициализация нагревателя будет после выбора настроек
        self.heater = None

        # Инициализация пользовательского интерфейса
        self.init_ui()

    def init_ui(self):
        self.setWindowTitle("Управление Нагревателем")
        self.setFixedSize(400, 300)

        # Выпадающий список для выбора COM порта
        self.com_port_label = QLabel("Выберите COM порт:", self)
        self.com_port_combo = QComboBox(self)
        self.refresh_com_ports()

        # Выпадающий список для выбора скорости передачи данных
        self.baud_rate_label = QLabel("Выберите скорость (бод):", self)
        self.baud_rate_combo = QComboBox(self)
        self.baud_rate_combo.addItems([
            '1200', '2400', '4800', '9600', '19200', '38400',
            '57600', '115200', '230400', '460800', '921600'
        ])
        self.baud_rate_combo.setCurrentText('9600')  # Устанавливаем скорость по умолчанию

        # Кнопка подключения
        self.connect_button = QPushButton("Подключиться", self)
        self.connect_button.clicked.connect(self.connect_to_heater)
        
        # Кнопка разрыва соединения
        self.disconnect_button = QPushButton("Разорвать соединение", self)
        self.disconnect_button.clicked.connect(self.disconnect_from_heater)
        self.disconnect_button.setEnabled(False)

        # Метка состояния
        self.status_label = QLabel("Нагреватель не подключен", self)
        self.status_label.setAlignment(Qt.AlignCenter)
        self.status_label.setStyleSheet("font-size: 16px;")

        # Кнопка включения
        self.on_button = QPushButton("Включить", self)
        self.on_button.clicked.connect(self.turn_heater_on)
        self.on_button.setEnabled(False)

        # Кнопка выключения
        self.off_button = QPushButton("Выключить", self)
        self.off_button.clicked.connect(self.turn_heater_off)
        self.off_button.setEnabled(False)

        # Расположение виджетов
        settings_layout = QHBoxLayout()
        settings_layout.addWidget(self.com_port_label)
        settings_layout.addWidget(self.com_port_combo)

        baud_rate_layout = QHBoxLayout()
        baud_rate_layout.addWidget(self.baud_rate_label)
        baud_rate_layout.addWidget(self.baud_rate_combo)

        # Расположение кнопок подключения и разрыва соединения
        connect_layout = QHBoxLayout()
        connect_layout.addWidget(self.connect_button)
        connect_layout.addWidget(self.disconnect_button)

        buttons_layout = QHBoxLayout()
        buttons_layout.addWidget(self.on_button)
        buttons_layout.addWidget(self.off_button)

        layout = QVBoxLayout()
        layout.addLayout(settings_layout)
        layout.addLayout(baud_rate_layout)
        layout.addLayout(connect_layout)
        layout.addWidget(self.status_label)
        layout.addLayout(buttons_layout)

        self.setLayout(layout)

    def refresh_com_ports(self):
        """
        Обновляет список доступных COM портов.
        """
        ports = serial.tools.list_ports.comports()
        self.com_port_combo.clear()
        for port in ports:
            self.com_port_combo.addItem(port.device)

    def connect_to_heater(self):
        """
        Подключается к нагревателю с выбранными параметрами.
        """
        port = self.com_port_combo.currentText()
        baud_rate = int(self.baud_rate_combo.currentText())

        if not port:
            QMessageBox.warning(self, "Ошибка", "Выберите COM порт.")
            return
        # Если ранее было соединение, разрываем его
        if self.heater:
            self.heater.disconnect()

        # Создаём экземпляр Heater
        self.heater = Heater(port, baud_rate)

        # Устанавливаем соединение
        connected = self.heater.connect()

        if connected:
            self.status_label.setText(f"Подключено к {port} со скоростью {baud_rate} бод")
            self.connect_button.setEnabled(False)
            self.disconnect_button.setEnabled(True)
            self.on_button.setEnabled(True)
            self.off_button.setEnabled(True)
        else:
            QMessageBox.warning(self, "Ошибка", f"Не удалось подключиться к {port}.")
            self.heater = None

    def disconnect_from_heater(self):
        """
        Разрывает соединение с нагревателем.
        """
        if self.heater:
            self.heater.disconnect()
            self.heater = None
            self.status_label.setText("Соединение разорвано")
            self.connect_button.setEnabled(True)
            self.disconnect_button.setEnabled(False)
            self.on_button.setEnabled(False)
            self.off_button.setEnabled(False)
        else:
            QMessageBox.information(self, "Информация", "Нагреватель не подключен.")

    def turn_heater_on(self):
        self.heater.turn_on()
        if self.heater.state:
            self.status_label.setText("Нагреватель включен")
            self.on_button.setEnabled(False)
            self.off_button.setEnabled(True)
        else:
            QMessageBox.warning(self, "Ошибка", "Не удалось включить нагреватель.")

    def turn_heater_off(self):
        self.heater.turn_off()
        if not self.heater.state:
            self.status_label.setText("Нагреватель выключен")
            self.on_button.setEnabled(True)
            self.off_button.setEnabled(False)
        else:
            QMessageBox.warning(self, "Ошибка", "Не удалось выключить нагреватель.")

    def closeEvent(self, event):
        """
        Вызывается при закрытии приложения.
        Отключает нагреватель и закрывает соединение.
        """
        if self.heater:
            if self.heater.state:
                self.heater.turn_off()
            self.heater.disconnect()
        event.accept()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = HeaterApp()
    window.show()
    sys.exit(app.exec())
