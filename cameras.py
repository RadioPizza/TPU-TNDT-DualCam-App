import cv2
from typing import List, Tuple
from PySide6.QtCore import QTimer, Qt, Slot
from PySide6.QtWidgets import QGraphicsView, QGraphicsScene, QGraphicsPixmapItem, QMessageBox
from PySide6.QtGui import QImage, QPixmap
import logging
from settings import Settings
import PySpin

logger = logging.getLogger(__name__)


def get_available_cameras() -> List[Tuple[int, str]]:
    """
    Определяет доступные камеры и возвращает их индексы и имена.
    Имена камер получить, к сожалению, нельзя.
    Returns:
        List[Tuple[int, str]]: Список кортежей, где первый элемент - индекс камеры,
                              а второй - строка "Camera {index}".
    """
    available_cameras = []
    for index in range(10):  # Проверяем первые 10 камер
        cap = cv2.VideoCapture(index)
        if cap.isOpened():
            available_cameras.append((index, f"Camera {index}"))
            cap.release()  # Освобождаем ресурс камеры сразу после проверки
        else:
            cap.release()
    return available_cameras


class CameraWidget:
    """Базовый класс для виджета камеры."""

    def __init__(self, settings, graphics_view: QGraphicsView):
        self.settings = settings
        self.graphics_view = graphics_view
        self.camera = None
        self.video_writer = None
        self.is_recording = False

        # Флаги для управления попытками подключения
        self.is_disconnected = False

        # Параметры повторного подключения
        self.reconnect_interval = 5000  # миллисекунды между попытками
        self.reconnect_timer = QTimer()
        self.reconnect_timer.setInterval(self.reconnect_interval)
        self.reconnect_timer.timeout.connect(self.attempt_reconnect)

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
            logger.warning(f"Камера {self.get_camera_index()} не инициализирована. Видео не будет отображаться.")
            self.notify_camera_error(f"Камера {self.get_camera_index()} не обнаружена.")
            self.start_reconnect_timer()

    def start_recording(self, file_path: str):
        """Начинает запись видео."""
        if not self.camera or not self.camera.isOpened():
            logger.error("Запись видео невозможна: камера не инициализирована.")
            QMessageBox.critical(None, "Ошибка", "Камера не инициализирована. Запись видео невозможна.")
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
            logger.error(f"Не удалось получить кадр с камеры {self.get_camera_index()}.")
            if not self.is_disconnected:
                self.is_disconnected = True
                self.notify_camera_error(f"Камера {self.get_camera_index()} была отключена.")
                self.stop_recording_if_needed()
                self.timer.stop()
                self.camera.release()
                self.start_reconnect_timer()
            return

        # Если ранее была отключена, но теперь удалось получить кадр
        if self.is_disconnected:
            self.is_disconnected = False
            self.notify_camera_reconnected(f"Камера {self.get_camera_index()} восстановлена.")
            self.stop_reconnect_timer()
            self.setup_camera()
            self.timer.start(1000 // self.get_preview_fps())

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
        if self.reconnect_timer.isActive():
            self.reconnect_timer.stop()

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

    def start_reconnect_timer(self):
        """Запускает таймер повторного подключения."""
        if not self.reconnect_timer.isActive():
            logger.info(f"Запуск таймера повторного подключения для камеры {self.get_camera_index()}.")
            self.reconnect_timer.start()

    def stop_reconnect_timer(self):
        """Останавливает таймер повторного подключения."""
        if self.reconnect_timer.isActive():
            logger.info(f"Остановка таймера повторного подключения для камеры {self.get_camera_index()}.")
            self.reconnect_timer.stop()

    @Slot()
    def attempt_reconnect(self):
        """Пытается повторно подключиться к камере."""
        logger.info(f"Попытка повторного подключения к камере {self.get_camera_index()}...")
        self.camera = cv2.VideoCapture(self.get_camera_index())
        if self.camera and self.camera.isOpened():
            logger.info(f"Повторное подключение к камере {self.get_camera_index()} успешно.")
            self.setup_camera()
            self.apply_camera_settings()

            # Настраиваем таймер для обновления кадров
            self.timer.start(1000 // self.get_preview_fps())

            # Останавливаем таймер повторного подключения
            self.stop_reconnect_timer()
        else:
            logger.warning(f"Повторное подключение к камере {self.get_camera_index()} неудачно.")

    def notify_camera_error(self, message: str):
        """Уведомляет пользователя об ошибке камеры."""
        QMessageBox.critical(None, "Ошибка камеры", message)

    def notify_camera_reconnected(self, message: str):
        """Уведомляет пользователя о восстановлении камеры."""
        QMessageBox.information(None, "Камера восстановлена", message)

    def stop_recording_if_needed(self):
        """Останавливает запись видео, если она активна."""
        if self.is_recording:
            self.stop_recording()


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


class FLIRCameraWidget:
    def __init__(self, settings, graphics_view: QGraphicsView):
        self.settings = settings
        self.graphics_view = graphics_view
        self.is_recording = False
        self.video_writer = None
        
        self.system = PySpin.System.GetInstance()
        self.cam_list = self.system.GetCameras()
        num_cameras = self.cam_list.GetSize()
        
        if num_cameras == 0:
            raise Exception("No FLIR cameras found.")
        
        try:
            self.camera = self.cam_list.GetByIndex(0)
            self.camera.Init()
            self.set_camera_settings()
            self.camera.BeginAcquisition()
            
            self.timer = QTimer()
            self.timer.timeout.connect(self.update_frame)
            self.timer.start(1000 // settings.visible_camera_previewFPS)
            
            self.scene = QGraphicsScene()
            graphics_view.setScene(self.scene)
            self.pixmap_item = QGraphicsPixmapItem()
            self.scene.addItem(self.pixmap_item)
            
            logger.info("FLIR camera initialized successfully")
        except PySpin.SpinnakerException as ex:
            self.release_resources()
            logger.error(f"FLIR camera initialization failed: {ex}")
            raise Exception(f"FLIR camera error: {ex}")
    
    def set_camera_settings(self):
        """Настройка параметров камеры FLIR"""
        nodemap = self.camera.GetNodeMap()
        
        # Попробуем установить цветной формат, если доступен
        node_pixel_format = PySpin.CEnumerationPtr(nodemap.GetNode("PixelFormat"))
        if PySpin.IsAvailable(node_pixel_format) and PySpin.IsWritable(node_pixel_format):
            # Попробуем установить RGB8 формат сначала
            pixel_format_rgb8 = PySpin.CEnumEntryPtr(node_pixel_format.GetEntryByName("RGB8"))
            if PySpin.IsAvailable(pixel_format_rgb8) and PySpin.IsReadable(pixel_format_rgb8):
                node_pixel_format.SetIntValue(pixel_format_rgb8.GetValue())
                logger.info("Set pixel format to RGB8")
            else:
                # Если RGB8 недоступен, попробуем BGR8
                pixel_format_bgr8 = PySpin.CEnumEntryPtr(node_pixel_format.GetEntryByName("BGR8"))
                if PySpin.IsAvailable(pixel_format_bgr8) and PySpin.IsReadable(pixel_format_bgr8):
                    node_pixel_format.SetIntValue(pixel_format_bgr8.GetValue())
                    logger.info("Set pixel format to BGR8")
                else:
                    # Если цветные форматы недоступны, оставляем монохромный
                    logger.warning("Color formats not available, using monochrome")
        
        # Установка разрешения
        node_width = PySpin.CIntegerPtr(nodemap.GetNode("Width"))
        if PySpin.IsAvailable(node_width) and PySpin.IsWritable(node_width):
            node_width.SetValue(self.settings.visible_camera_resolution[0])
        
        node_height = PySpin.CIntegerPtr(nodemap.GetNode("Height"))
        if PySpin.IsAvailable(node_height) and PySpin.IsWritable(node_height):
            node_height.SetValue(self.settings.visible_camera_resolution[1])
        
        # Установка FPS
        node_fps = PySpin.CFloatPtr(nodemap.GetNode("AcquisitionFrameRate"))
        if PySpin.IsAvailable(node_fps) and PySpin.IsWritable(node_fps):
            node_fps.SetValue(self.settings.visible_camera_previewFPS)
    
    def start_recording(self, file_path: str):
        """Начинает запись видео."""
        width, height = self.settings.visible_camera_resolution
        fps = self.settings.visible_camera_recordFPS
        fourcc = cv2.VideoWriter_fourcc(*'XVID')
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
        try:
            image_result = self.camera.GetNextImage(1000)
            if image_result.IsIncomplete():
                logger.warning("FLIR image incomplete with status: %d", image_result.GetImageStatus())
            else:
                # Получаем изображение в виде numpy массива
                image_data = image_result.GetNDArray()
                
                # Получаем формат пикселя для правильной конвертации
                pixel_format = image_result.GetPixelFormat()
                
                # Логируем формат для отладки
                if not hasattr(self, 'pixel_format_logged'):
                    logger.info(f"FLIR Pixel Format: {pixel_format}")
                    self.pixel_format_logged = True
                
                # Конвертируем в RGB в зависимости от формата
                if pixel_format == PySpin.PixelFormat_Mono8:
                    # Монохромное изображение - конвертируем в псевдоцвет
                    rgb_image = cv2.applyColorMap(image_data, cv2.COLORMAP_JET)
                elif pixel_format == PySpin.PixelFormat_BayerBG8:
                    rgb_image = cv2.cvtColor(image_data, cv2.COLOR_BAYER_BG2RGB)
                elif pixel_format == PySpin.PixelFormat_BayerGB8:
                    rgb_image = cv2.cvtColor(image_data, cv2.COLOR_BAYER_GB2RGB)
                elif pixel_format == PySpin.PixelFormat_BayerGR8:
                    rgb_image = cv2.cvtColor(image_data, cv2.COLOR_BAYER_GR2RGB)
                elif pixel_format == PySpin.PixelFormat_BayerRG8:
                    rgb_image = cv2.cvtColor(image_data, cv2.COLOR_BAYER_RG2RGB)
                elif pixel_format == PySpin.PixelFormat_BGR8:
                    rgb_image = cv2.cvtColor(image_data, cv2.COLOR_BGR2RGB)
                elif pixel_format == PySpin.PixelFormat_RGB8:
                    rgb_image = image_data  # Уже в RGB
                else:
                    # Для неизвестного формата попробуем конвертировать как BGR
                    logger.warning(f"Unsupported pixel format: {pixel_format}. Trying BGR to RGB conversion.")
                    rgb_image = cv2.cvtColor(image_data, cv2.COLOR_BGR2RGB)
                
                # Запись видео
                if self.is_recording and self.video_writer:
                    bgr_image = cv2.cvtColor(rgb_image, cv2.COLOR_RGB2BGR)
                    self.video_writer.write(bgr_image)
                
                # Отображение в интерфейсе
                height, width, _ = rgb_image.shape
                bytes_per_line = 3 * width
                q_image = QImage(rgb_image.data, width, height, bytes_per_line, QImage.Format_RGB888)
                pixmap = QPixmap.fromImage(q_image)
                self.pixmap_item.setPixmap(pixmap)
                self.graphics_view.fitInView(self.pixmap_item, Qt.KeepAspectRatio)
            
            image_result.Release()
        except PySpin.SpinnakerException as ex:
            logger.error("FLIR camera error: %s", ex)
    
    def release_resources(self):
        """Освобождает ресурсы камеры."""
        if hasattr(self, 'camera') and self.camera.IsInitialized():
            if self.camera.IsStreaming():
                self.camera.EndAcquisition()
            self.camera.DeInit()
            del self.camera
        
        if hasattr(self, 'cam_list'):
            self.cam_list.Clear()
            del self.cam_list
        
        if hasattr(self, 'system'):
            self.system.ReleaseInstance()
            del self.system
    
    def release(self):
        """Публичный метод для освобождения ресурсов."""
        if hasattr(self, 'timer') and self.timer.isActive():
            self.timer.stop()
        self.stop_recording()
        self.release_resources()


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