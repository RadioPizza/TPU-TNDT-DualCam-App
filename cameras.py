import cv2
import logging
from abc import ABC, abstractmethod
from typing import List, Tuple, Optional
from PySide6.QtCore import QTimer, Qt, Slot
from PySide6.QtWidgets import QGraphicsView, QGraphicsScene, QGraphicsPixmapItem, QMessageBox
from PySide6.QtGui import QImage, QPixmap
import numpy as np

try:
    import PySpin
    PYSPIN_AVAILABLE = True
except ImportError:
    PYSPIN_AVAILABLE = False
    logging.warning("PySpin not available. FLIR cameras will not work.")

from settings import Settings

logger = logging.getLogger(__name__)


# ==================== EXCEPTIONS ====================
class CameraError(Exception):
    """Базовое исключение для ошибок камер"""
    pass

class CameraNotInitializedError(CameraError):
    """Исключение при использовании неинициализированной камеры"""
    pass

class CameraNotFoundError(CameraError):
    """Исключение при отсутствии камеры"""
    pass

class CameraConnectionError(CameraError):
    """Исключение при проблемах с подключением к камере"""
    pass


# ==================== BASE CLASS ====================
class BaseCamera(ABC):
    """Абстрактный базовый класс для всех камер"""
    
    def __init__(self, settings: Settings, graphics_view: QGraphicsView):
        self.settings = settings
        self.graphics_view = graphics_view
        self.is_recording = False
        self.video_writer = None
        self._initialized = False
        self.is_disconnected = False
        
        # Параметры повторного подключения
        self.reconnect_interval = 5000  # миллисекунды между попытками
        self.reconnect_timer = QTimer()
        self.reconnect_timer.setInterval(self.reconnect_interval)
        self.reconnect_timer.timeout.connect(self.attempt_reconnect)
        
        # Настройка сцены для отображения
        self.scene = QGraphicsScene()
        self.graphics_view.setScene(self.scene)
        self.pixmap_item = QGraphicsPixmapItem()
        self.scene.addItem(self.pixmap_item)
        
        # Таймер для обновления кадров
        self.timer = QTimer()
        self.timer.timeout.connect(self.update_frame)
    
    @abstractmethod
    def initialize(self) -> bool:
        """Инициализирует камеру и возвращает статус успеха"""
        pass
    
    @abstractmethod
    def capture_frame(self):
        """Захватывает кадр с камеры"""
        pass
    
    @abstractmethod
    def release_resources(self):
        """Освобождает ресурсы камеры"""
        pass
    
    @abstractmethod
    def get_camera_name(self) -> str:
        """Возвращает название камеры"""
        pass
    
    @abstractmethod
    def get_resolution(self) -> List[int]:
        """Возвращает разрешение камеры"""
        pass
    
    @abstractmethod
    def get_preview_fps(self) -> int:
        """Возвращает FPS для предпросмотра"""
        pass
    
    @abstractmethod
    def get_record_fps(self) -> int:
        """Возвращает FPS для записи"""
        pass
    
    def is_initialized(self) -> bool:
        """Проверяет, инициализирована ли камера"""
        return self._initialized
    
    def start_recording(self, file_path: str):
        """Начинает запись видео"""
        if not self.is_initialized():
            raise CameraNotInitializedError(f"Камера {self.get_camera_name()} не инициализирована")
        
        width, height = self.get_resolution()
        fps = self.get_record_fps()
        fourcc = cv2.VideoWriter_fourcc(*'XVID')
        self.video_writer = cv2.VideoWriter(file_path, fourcc, fps, (width, height))
        self.is_recording = True
        logger.info(f"Начата запись видео: {file_path}")
    
    def stop_recording(self):
        """Останавливает запись видео"""
        if self.is_recording and self.video_writer:
            self.video_writer.release()
            self.video_writer = None
            self.is_recording = False
            logger.info("Запись видео остановлена.")
    
    def update_frame(self):
        """Обновляет кадр с камеры и отображает его"""
        try:
            frame = self.capture_frame()
            if frame is None:
                if not self.is_disconnected:
                    self.is_disconnected = True
                    self.notify_camera_error(f"Камера {self.get_camera_name()} была отключена.")
                    self.stop_recording_if_needed()
                    self.timer.stop()
                    self.start_reconnect_timer()
                return
            
            # Если ранее была отключена, но теперь удалось получить кадр
            if self.is_disconnected:
                self.is_disconnected = False
                self.notify_camera_reconnected(f"Камера {self.get_camera_name()} восстановлена.")
                self.stop_reconnect_timer()
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
            
        except Exception as e:
            logger.error(f"Ошибка при обновлении кадра: {e}")
            if not self.is_disconnected:
                self.is_disconnected = True
                self.notify_camera_error(f"Ошибка камеры {self.get_camera_name()}: {e}")
                self.stop_recording_if_needed()
                self.timer.stop()
                self.start_reconnect_timer()
    
    def release(self):
        """Освобождает все ресурсы камеры"""
        self.stop_recording()
        if self.timer.isActive():
            self.timer.stop()
        if self.reconnect_timer.isActive():
            self.reconnect_timer.stop()
        self.release_resources()
    
    def start_reconnect_timer(self):
        """Запускает таймер повторного подключения."""
        if not self.reconnect_timer.isActive():
            logger.info(f"Запуск таймера повторного подключения для камеры {self.get_camera_name()}.")
            self.reconnect_timer.start()
    
    def stop_reconnect_timer(self):
        """Останавливает таймер повторного подключения."""
        if self.reconnect_timer.isActive():
            logger.info(f"Остановка таймера повторного подключения для камеры {self.get_camera_name()}.")
            self.reconnect_timer.stop()
    
    @Slot()
    def attempt_reconnect(self):
        """Пытается повторно подключиться к камере."""
        logger.info(f"Попытка повторного подключения к камере {self.get_camera_name()}...")
        if self.initialize():
            logger.info(f"Повторное подключение к камере {self.get_camera_name()} успешно.")
            self.timer.start(1000 // self.get_preview_fps())
            self.stop_reconnect_timer()
        else:
            logger.warning(f"Повторное подключение к камере {self.get_camera_name()} неудачно.")
    
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


# ==================== OPENCV CAMERA ====================
class OpenCVCamera(BaseCamera):
    """Реализация для обычных камер через OpenCV"""
    
    def __init__(self, settings: Settings, graphics_view: QGraphicsView, camera_index: int):
        super().__init__(settings, graphics_view)
        self.camera_index = camera_index
        self.camera = None
    
    def initialize(self) -> bool:
        try:
            self.camera = cv2.VideoCapture(self.camera_index)
            if self.camera and self.camera.isOpened():
                self._apply_opencv_settings()
                self._initialized = True
                self.timer.start(1000 // self.get_preview_fps())
                return True
            else:
                logger.warning(f"Камера {self.get_camera_name()} не инициализирована.")
                self.notify_camera_error(f"Камера {self.get_camera_name()} не обнаружена.")
                self.start_reconnect_timer()
                return False
        except Exception as e:
            logger.error(f"Ошибка инициализации OpenCV камеры: {e}")
            self.notify_camera_error(f"Ошибка инициализации камеры {self.get_camera_name()}: {e}")
            self.start_reconnect_timer()
            return False
    
    def _apply_opencv_settings(self):
        """Применяет настройки для OpenCV камеры"""
        width, height = self.get_resolution()
        self.camera.set(cv2.CAP_PROP_FRAME_WIDTH, width)
        self.camera.set(cv2.CAP_PROP_FRAME_HEIGHT, height)
        self.camera.set(cv2.CAP_PROP_FPS, self.get_preview_fps())
    
    def capture_frame(self):
        """Захватывает кадр с OpenCV камеры"""
        if not self.is_initialized():
            return None
        
        ret, frame = self.camera.read()
        if not ret:
            logger.error(f"Не удалось получить кадр с камеры {self.get_camera_name()}.")
            return None
        
        return frame
    
    def release_resources(self):
        """Освобождает ресурсы OpenCV камеры"""
        if self.camera and self.camera.isOpened():
            self.camera.release()
        self.camera = None
        self._initialized = False
    
    def get_camera_name(self) -> str:
        return f"OpenCV Camera {self.camera_index}"
    
    def get_resolution(self) -> List[int]:
        return self.settings.visible_camera_resolution
    
    def get_preview_fps(self) -> int:
        return self.settings.visible_camera_previewFPS
    
    def get_record_fps(self) -> int:
        return self.settings.visible_camera_recordFPS


# ==================== FLIR CAMERA ====================
class FLIRCamera(BaseCamera):
    """Реализация для камер FLIR через PySpin"""
    
    def __init__(self, settings: Settings, graphics_view: QGraphicsView):
        if not PYSPIN_AVAILABLE:
            raise ImportError("PySpin is not available. Cannot create FLIR camera.")
        
        super().__init__(settings, graphics_view)
        self.system = None
        self.cam_list = None
        self.camera = None
        self.pixel_format_logged = False
    
    def initialize(self) -> bool:
        try:
            self.system = PySpin.System.GetInstance()
            self.cam_list = self.system.GetCameras()
            num_cameras = self.cam_list.GetSize()
            
            if num_cameras == 0:
                logger.error("No FLIR cameras found.")
                self.notify_camera_error("Не найдено камер FLIR.")
                self.start_reconnect_timer()
                return False
            
            self.camera = self.cam_list.GetByIndex(0)
            self.camera.Init()
            self._apply_flir_settings()
            self.camera.BeginAcquisition()
            
            self._initialized = True
            self.timer.start(1000 // self.get_preview_fps())
            logger.info("FLIR camera initialized successfully")
            return True
            
        except PySpin.SpinnakerException as ex:
            logger.error(f"FLIR camera initialization failed: {ex}")
            self.notify_camera_error(f"Ошибка инициализации FLIR камеры: {ex}")
            self.release_resources()
            self.start_reconnect_timer()
            return False
        except Exception as e:
            logger.error(f"Unexpected error during FLIR camera initialization: {e}")
            self.notify_camera_error(f"Неожиданная ошибка при инициализации FLIR камеры: {e}")
            self.release_resources()
            self.start_reconnect_timer()
            return False
    
    def _apply_flir_settings(self):
        """Применяет настройки для FLIR камеры"""
        nodemap = self.camera.GetNodeMap()
        
        # Отключаем биннинг и декimation
        for node_name in ['BinningHorizontal', 'BinningVertical', 
                         'DecimationHorizontal', 'DecimationVertical']:
            node = PySpin.CIntegerPtr(nodemap.GetNode(node_name))
            if PySpin.IsAvailable(node) and PySpin.IsWritable(node):
                node.SetValue(1)
                logger.info(f"Set {node_name} to 1")
        
        # Устанавливаем смещение в 0
        node_offset_x = PySpin.CIntegerPtr(nodemap.GetNode("OffsetX"))
        if PySpin.IsAvailable(node_offset_x) and PySpin.IsWritable(node_offset_x):
            node_offset_x.SetValue(0)
            logger.info("Set OffsetX to 0")
        
        node_offset_y = PySpin.CIntegerPtr(nodemap.GetNode("OffsetY"))
        if PySpin.IsAvailable(node_offset_y) and PySpin.IsWritable(node_offset_y):
            node_offset_y.SetValue(0)
            logger.info("Set OffsetY to 0")
        
        # Устанавливаем максимальное разрешение
        node_width_max = PySpin.CIntegerPtr(nodemap.GetNode("WidthMax"))
        node_height_max = PySpin.CIntegerPtr(nodemap.GetNode("HeightMax"))
        
        if PySpin.IsAvailable(node_width_max) and PySpin.IsAvailable(node_height_max):
            width_max = node_width_max.GetValue()
            height_max = node_height_max.GetValue()
            
            node_width = PySpin.CIntegerPtr(nodemap.GetNode("Width"))
            node_height = PySpin.CIntegerPtr(nodemap.GetNode("Height"))
            
            if (PySpin.IsAvailable(node_width) and PySpin.IsWritable(node_width) and
                PySpin.IsAvailable(node_height) and PySpin.IsWritable(node_height)):
                
                node_width.SetValue(width_max)
                node_height.SetValue(height_max)
                logger.info(f"Set resolution to maximum: {width_max}x{height_max}")
        
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
        
        # Установка FPS
        node_fps = PySpin.CFloatPtr(nodemap.GetNode("AcquisitionFrameRate"))
        if PySpin.IsAvailable(node_fps) and PySpin.IsWritable(node_fps):
            node_fps.SetValue(self.get_preview_fps())
    
    def capture_frame(self):
        """Захватывает кадр с FLIR камеры"""
        if not self.is_initialized():
            return None
        
        try:
            image_result = self.camera.GetNextImage(1000)
            if image_result.IsIncomplete():
                logger.warning("FLIR image incomplete with status: %d", image_result.GetImageStatus())
                image_result.Release()
                return None
            
            # Получаем изображение в виде numpy массива
            image_data = image_result.GetNDArray()
            
            # Получаем формат пикселя для правильной конвертации
            pixel_format = image_result.GetPixelFormat()
            
            # Логируем формат для отладки
            if not self.pixel_format_logged:
                logger.info(f"FLIR Pixel Format: {pixel_format}")
                logger.info(f"FLIR Image shape: {image_data.shape}")
                self.pixel_format_logged = True
            
            # Конвертируем в BGR в зависимости от формата
            if pixel_format == PySpin.PixelFormat_Mono8:
                # Монохромное изображение - конвертируем в псевдоцвет
                bgr_image = cv2.applyColorMap(image_data, cv2.COLORMAP_JET)
            elif pixel_format == PySpin.PixelFormat_BayerBG8:
                bgr_image = cv2.cvtColor(image_data, cv2.COLOR_BAYER_BG2BGR)
            elif pixel_format == PySpin.PixelFormat_BayerGB8:
                bgr_image = cv2.cvtColor(image_data, cv2.COLOR_BAYER_GB2BGR)
            elif pixel_format == PySpin.PixelFormat_BayerGR8:
                bgr_image = cv2.cvtColor(image_data, cv2.COLOR_BAYER_GR2BGR)
            elif pixel_format == PySpin.PixelFormat_BayerRG8:
                bgr_image = cv2.cvtColor(image_data, cv2.COLOR_BAYER_RG2BGR)
            elif pixel_format == PySpin.PixelFormat_BGR8:
                bgr_image = image_data  # Уже в BGR
            elif pixel_format == PySpin.PixelFormat_RGB8:
                bgr_image = cv2.cvtColor(image_data, cv2.COLOR_RGB2BGR)
            else:
                # Для неизвестного формата попробуем конвертировать как есть
                logger.warning(f"Unsupported pixel format: {pixel_format}. Using raw image.")
                bgr_image = image_data
            
            image_result.Release()
            return bgr_image
            
        except PySpin.SpinnakerException as ex:
            logger.error("FLIR camera error: %s", ex)
            return None
    
    def release_resources(self):
        """Освобождает ресурсы FLIR камеры"""
        try:
            if self.camera and hasattr(self.camera, 'IsInitialized') and self.camera.IsInitialized():
                if self.camera.IsStreaming():
                    self.camera.EndAcquisition()
                self.camera.DeInit()
                del self.camera
                self.camera = None
            
            if self.cam_list:
                self.cam_list.Clear()
                del self.cam_list
                self.cam_list = None
            
            if self.system:
                self.system.ReleaseInstance()
                del self.system
                self.system = None
                
        except Exception as e:
            logger.error(f"Error releasing FLIR resources: {e}")
        
        self._initialized = False
    
    def get_camera_name(self) -> str:
        return "FLIR Camera"
    
    def get_resolution(self) -> List[int]:
        return self.settings.visible_camera_resolution
    
    def get_preview_fps(self) -> int:
        return self.settings.visible_camera_previewFPS
    
    def get_record_fps(self) -> int:
        return self.settings.visible_camera_recordFPS


# ==================== THERMAL CAMERA ====================
class ThermalCamera(BaseCamera):
    """Реализация для тепловизоров (заглушка для будущей реализации)"""
    
    def __init__(self, settings: Settings, graphics_view: QGraphicsView):
        super().__init__(settings, graphics_view)
        self.camera = None
    
    def initialize(self) -> bool:
        try:
            # Заглушка для будущей реализации тепловизора
            # В реальной реализации здесь будет код инициализации тепловизора
            logger.warning("Thermal camera implementation is not yet complete")
            
            # Для тестирования создаем заглушку с черным изображением
            self._initialized = True
            self.timer.start(1000 // self.get_preview_fps())
            return True
            
        except Exception as e:
            logger.error(f"Thermal camera initialization failed: {e}")
            self.notify_camera_error(f"Ошибка инициализации тепловизора: {e}")
            self.start_reconnect_timer()
            return False
    
    def capture_frame(self):
        """Захватывает кадр с тепловизора (заглушка)"""
        if not self.is_initialized():
            return None
        
        # Заглушка: создаем черное изображение с текстом
        width, height = self.get_resolution()
        frame = np.zeros((height, width, 3), dtype=np.uint8)
        cv2.putText(frame, "Thermal Camera Not Implemented", (10, height//2), 
                   cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 255, 255), 2)
        
        return frame
    
    def release_resources(self):
        """Освобождает ресурсы тепловизора"""
        self.camera = None
        self._initialized = False
    
    def get_camera_name(self) -> str:
        return "Thermal Camera"
    
    def get_resolution(self) -> List[int]:
        return self.settings.thermal_camera_resolution
    
    def get_preview_fps(self) -> int:
        return self.settings.thermal_camera_previewFPS
    
    def get_record_fps(self) -> int:
        return self.settings.thermal_camera_recordFPS


# ==================== CAMERA FACTORY ====================
class CameraFactory:
    """Фабрика для создания экземпляров камер"""
    
    @staticmethod
    def create_camera(camera_type: str, settings: Settings, graphics_view: QGraphicsView):
        """
        Создает экземпляр камеры указанного типа
        
        Args:
            camera_type: Тип камеры ("visible" или "thermal")
            settings: Экземпляр настроек
            graphics_view: Виджет для отображения видео
            
        Returns:
            Экземпляр камеры указанного типа
            
        Raises:
            ValueError: Если передан неизвестный тип камеры
            ImportError: Если запрошена FLIR камера, но PySpin недоступен
        """
        if camera_type == "visible":
            if getattr(settings, 'use_flir_camera', True) and PYSPIN_AVAILABLE:
                return FLIRCamera(settings, graphics_view)
            else:
                camera_index = getattr(settings, 'visible_camera_index', 0)
                return OpenCVCamera(settings, graphics_view, camera_index)
        elif camera_type == "thermal":
            return ThermalCamera(settings, graphics_view)
        else:
            raise ValueError(f"Неизвестный тип камеры: {camera_type}")


# ==================== CAMERA MANAGER ====================
class CameraManager:
    """Управляет несколькими камерами и их синхронизацией"""
    
    def __init__(self):
        self.cameras = {}
    
    def add_camera(self, name: str, camera: BaseCamera):
        """Добавляет камеру в менеджер"""
        self.cameras[name] = camera
    
    def initialize_all(self):
        """Инициализирует все камеры"""
        results = {}
        for name, camera in self.cameras.items():
            results[name] = camera.initialize()
        return results
    
    def start_recording_all(self, base_path: str):
        """Начинает запись на всех камерах"""
        for name, camera in self.cameras.items():
            if camera.is_initialized():
                camera.start_recording(f"{base_path}_{name}.avi")
    
    def stop_recording_all(self):
        """Останавливает запись на всех камерах"""
        for camera in self.cameras.values():
            camera.stop_recording()
    
    def release_all(self):
        """Освобождает ресурсы всех камер"""
        for camera in self.cameras.values():
            camera.release()
    
    def get_camera(self, name: str) -> Optional[BaseCamera]:
        """Возвращает камеру по имени"""
        return self.cameras.get(name)


# ==================== UTILITY FUNCTIONS ====================
def get_available_cameras() -> List[Tuple[int, str]]:
    """
    Определяет доступные камеры и возвращает их индексы и имена.
    
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