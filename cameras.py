import cv2
from PyQt5.QtWidgets import QGraphicsView, QGraphicsScene, QGraphicsPixmapItem
from PyQt5.QtCore import QTimer
from PyQt5.QtGui import QImage, QPixmap
from PyQt5.Qt import Qt

class CameraWidget:
    """Базовый класс для виджета камеры."""

    def __init__(self, camera_index: int, preview_fps: int, graphics_view: QGraphicsView):
        """
        Инициализация камеры и связанных компонентов.

        :param camera_index: Индекс устройства камеры для cv2.VideoCapture.
        :param preview_fps: Частота обновления кадров.
        :param graphics_view: QGraphicsView для отображения видео.
        """
        self.camera = cv2.VideoCapture(camera_index)
        if not self.camera.isOpened():
            raise RuntimeError(f"Ошибка: Не удалось открыть камеру с индексом {camera_index}")

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
        if not ret:
            print("Ошибка: Не удалось получить кадр с камеры")
            return
        
        frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        h, w, ch = frame.shape
        bytes_per_line = ch * w
        q_image = QImage(frame.data, w, h, bytes_per_line, QImage.Format_RGB888)
        pixmap = QPixmap.fromImage(q_image)
        self.pixmap_item.setPixmap(pixmap)
        self.graphics_view.fitInView(self.pixmap_item, Qt.KeepAspectRatio)

    def release(self):
        """Освобождает ресурсы камеры."""
        if self.camera.isOpened():
            self.camera.release()
        self.timer.stop()


class MainCameraWidget(CameraWidget):
    """Класс для основной камеры."""
    def __init__(self, graphics_view: QGraphicsView):
        super().__init__(settings.camera_index, settings.camera_previewFPS, graphics_view)


class ThermalCameraWidget(CameraWidget):
    """Класс для ИК камеры."""
    def __init__(self, graphics_view: QGraphicsView):
        super().__init__(settings.thermal_camera_index, settings.thermal_camera_previewFPS, graphics_view)

    def update_frame(self):
        """Переопределяем метод для обработки кадров с ИК камеры."""
        ret, frame = self.camera.read()
        if not ret:
            print("Ошибка: Не удалось получить кадр с ИК камеры")
            return
        
        # Дополнительная обработка для ИК камер
        frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        # frame = cv2.applyColorMap(frame, cv2.COLORMAP_JET)  # Применение цветовой карты
        h, w, ch = frame.shape
        bytes_per_line = ch * w
        q_image = QImage(frame.data, w, h, bytes_per_line, QImage.Format_RGB888)
        pixmap = QPixmap.fromImage(q_image)
        self.pixmap_item.setPixmap(pixmap)
        self.graphics_view.fitInView(self.pixmap_item, Qt.KeepAspectRatio)
