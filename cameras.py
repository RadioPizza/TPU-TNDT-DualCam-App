import cv2
from typing import List
from PySide6.QtCore import QTimer, Qt
from PySide6.QtWidgets import QGraphicsView, QGraphicsScene, QGraphicsPixmapItem
from PySide6.QtGui import QImage, QPixmap
import logging
from settings import Settings

logger = logging.getLogger(__name__)

class CameraWidget:
    """Базовый класс для виджета камеры."""

    def __init__(self, settings, graphics_view: QGraphicsView):
        self.settings = settings
        self.graphics_view = graphics_view
        self.camera = None
        self.video_writer = None
        self.is_recording = False

        # Инициализация камеры
        self.camera = cv2.VideoCapture(self.get_camera_index())
        self.setup_camera()
        if self.camera and self.camera.isOpened():
            self.apply_camera_settings()

            # Настраиваем таймер для обновления кадров
            self.timer = QTimer()
            self.timer.timeout.connect(self.update_frame)
            self.timer.start(1000 // self.get_preview_fps())

            # Настраиваем сцену для отображения видео
            self.scene = QGraphicsScene()
            self.graphics_view.setScene(self.scene)
            self.pixmap_item = QGraphicsPixmapItem()
            self.scene.addItem(self.pixmap_item)
        else:
            logger.warning("Камера не инициализирована. Видео не будет отображаться.")

    def start_recording(self, file_path: str):
        """Начинает запись видео."""
        if not self.camera or not self.camera.isOpened():
            logger.error("Запись видео невозможна: камера не инициализирована.")
            return

        width, height = self.get_resolution()
        fps = self.get_record_fps()
        fourcc = cv2.VideoWriter_fourcc(*'XVID')  # Формат кодека
        self.video_writer = cv2.VideoWriter(file_path, fourcc, fps, (width, height))
        self.is_recording = True
        logger.info(f"Начата запись видео: {file_path}")

    def stop_recording(self):
        """Останавливает запись видео."""
        if self.is_recording and self.video_writer:
            self.video_writer.release()
            self.video_writer = None
            self.is_recording = False
            logger.info("Запись видео остановлена.")

    def update_frame(self):
        """Захватывает и обновляет кадры с камеры."""
        if not self.camera:
            logger.debug("Камера не инициализирована. Пропуск обновления кадра.")
            return

        ret, frame = self.camera.read()
        if not ret:
            logger.error("Не удалось получить кадр с камеры.")
            return

        # Если запись активна, записываем кадр
        if self.is_recording and self.video_writer:
            self.video_writer.write(frame)

        # Отображение видео в графической области
        frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        h, w, ch = frame.shape
        bytes_per_line = ch * w
        q_image = QImage(frame.data, w, h, bytes_per_line, QImage.Format_RGB888)
        pixmap = QPixmap.fromImage(q_image)
        self.pixmap_item.setPixmap(pixmap)
        self.graphics_view.fitInView(self.pixmap_item, Qt.KeepAspectRatio)

    def release(self):
        """Освобождает ресурсы камеры."""
        if self.camera and self.camera.isOpened():
            self.camera.release()
        if self.video_writer:
            self.video_writer.release()
        if hasattr(self, 'timer'):
            self.timer.stop()

    def get_camera_index(self) -> int:
        raise NotImplementedError("Метод get_camera_index должен быть реализован в подклассе.")

    def get_preview_fps(self) -> int:
        raise NotImplementedError("Метод get_preview_fps должен быть реализован в подклассе.")

    def get_record_fps(self) -> int:
        raise NotImplementedError("Метод get_record_fps должен быть реализован в подклассе.")

    def get_resolution(self) -> List[int]:
        raise NotImplementedError("Метод get_resolution должен быть реализован в подклассе.")

    def setup_camera(self):
        """Настройка параметров камеры (разрешение, FPS и т.д.)."""
        # Разрешение
        width, height = self.get_resolution()
        self.camera.set(cv2.CAP_PROP_FRAME_WIDTH, width)
        self.camera.set(cv2.CAP_PROP_FRAME_HEIGHT, height)
        # FPS
        self.camera.set(cv2.CAP_PROP_FPS, self.get_preview_fps())

    def apply_camera_settings(self):
        """Применение настроек камеры (яркость, контрастность и т.д.)."""
        pass  # Здесь можно добавить настройки для конкретной камеры

class VisibleCameraWidget(CameraWidget):
    """Класс для основной (видимой) камеры."""

    def get_camera_index(self) -> int:
        return self.settings.visible_camera_index

    def get_preview_fps(self) -> int:
        return self.settings.visible_camera_previewFPS

    def get_record_fps(self) -> int:
        return self.settings.visible_camera_recordFPS

    def get_resolution(self) -> List[int]:
        return self.settings.visible_camera_resolution

class ThermalCameraWidget(CameraWidget):
    """Класс для ИК камеры."""

    def get_camera_index(self) -> int:
        return self.settings.thermal_camera_index

    def get_preview_fps(self) -> int:
        return self.settings.thermal_camera_previewFPS

    def get_record_fps(self) -> int:
        return self.settings.thermal_camera_recordFPS

    def get_resolution(self) -> List[int]:
        return self.settings.thermal_camera_resolution

    # Если необходимо, можно переопределить методы для других настроек ИК камеры