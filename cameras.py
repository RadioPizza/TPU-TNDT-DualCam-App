import cv2
import PySpin

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
