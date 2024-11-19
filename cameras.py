import logging
from typing import List

import cv2
from PySide6.QtCore import QObject, Qt, QTimer, Signal
from PySide6.QtGui import QImage, QPixmap
from PySide6.QtWidgets import (QGraphicsPixmapItem, QGraphicsScene,
                               QGraphicsView)

from settings import Settings

logger = logging.getLogger(__name__)

class CameraWidget:
    """Базовый класс для виджета камеры."""

    def __init__(self, settings: Settings, graphics_view: QGraphicsView):
        """
        Инициализация камеры и связанных компонентов.

        :param settings: Объект настроек.
        :param graphics_view: QGraphicsView для отображения видео.
        """
        self.settings = settings
        self.graphics_view = graphics_view

        # Инициализируем камеру
        self.camera = None  # Инициализируем как None
        self.camera = cv2.VideoCapture(self.get_camera_index())
        self.setup_camera()
        if self.camera:
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

    def setup_camera(self):
        """Попытка инициализировать камеру."""
        camera_index = self.get_camera_index()
        logger.info(f"Попытка открыть камеру с индексом {camera_index}")
        self.camera = cv2.VideoCapture(camera_index)
        if not self.camera.isOpened():
            logger.error(f"Не удалось открыть камеру с индексом {camera_index}")
            self.camera = None  # Устанавливаем в None для явного указания отсутствия камеры
    
    def get_camera_index(self) -> int:
        """Получение индекса камеры. Переопределяется в подклассах."""
        return self.settings.camera_index

    def get_preview_fps(self) -> int:
        """Получение FPS для предпросмотра. Переопределяется в подклассах."""
        return self.settings.camera_previewFPS
    
    def get_record_fps(self) -> int:
        """Получение FPS для записи. Переопределяется в подклассах."""
        return self.settings.camera_recordFPS

    def get_resolution(self) -> List[int]:
        """Получение разрешения камеры. Переопределяется в подклассах."""
        return self.settings.camera_resolution

    def apply_camera_settings(self):
        """Применение настроек к камере."""
        width, height = self.get_resolution()
        self.camera.set(cv2.CAP_PROP_FRAME_WIDTH, width)
        self.camera.set(cv2.CAP_PROP_FRAME_HEIGHT, height)
        self.camera.set(cv2.CAP_PROP_FPS, self.get_preview_fps())
        logger.info(f"Настройки камеры применены: Разрешение={width}x{height}, preFPS={self.get_preview_fps()}, recFPS={self.get_record_fps}")
        
    def update_frame(self):
        """Захватывает и обновляет кадры с камеры."""
        if not self.camera:
            logger.debug("Камера не инициализирована. Пропуск обновления кадра.")
            return

        ret, frame = self.camera.read()
        if not ret:
            logger.error("Не удалось получить кадр с камеры.")
            return
        
        # Конвертируем цветовую схему для отображения
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
            logger.info("Камера освобождена.")
        if hasattr(self, 'timer'):
            self.timer.stop()
            logger.info("Таймер обновления кадров остановлен.")

class VisibleCameraWidget(CameraWidget):
    """Класс для основной (видимой) камеры."""
    pass

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
