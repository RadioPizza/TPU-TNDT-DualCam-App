import json
import os
from dataclasses import asdict, dataclass, field
from typing import List, Optional

from PySide6.QtCore import QObject, Signal


@dataclass
class UserData(QObject):
    user_name:          Optional[str] = None
    user_surname:       Optional[str] = None
    object_of_testing:  Optional[str] = None
    save_path:          Optional[str] = None

    _instance = None

    data_changed = Signal()

    def __post_init__(self):
        super().__init__()

    @staticmethod
    def get_instance():
        if UserData._instance is None:
            UserData._instance = UserData()
        return UserData._instance

    def set_user_name(self, user_name: str):
        self.user_name = user_name
        self.data_changed.emit()

    def set_user_surname(self, user_surname: str):
        self.user_surname = user_surname
        self.data_changed.emit()

    def set_object_of_testing(self, object_of_testing: str):
        self.object_of_testing = object_of_testing
        self.data_changed.emit()

    def set_save_path(self, save_path: str):
        self.save_path = save_path
        self.data_changed.emit()


@dataclass
class Settings(QObject):
    duration_of_testing: int = 30
    heating_duration: int = 10
    language: str = 'EN'
    theme: str = 'Light'
    camera_index: int = 0
    camera_resolution: List[int] = field(default_factory=lambda: [640, 480])
    camera_previewFPS: int = 30
    camera_recordFPS: int = 5
    thermal_camera_index: int = 1
    thermal_camera_resolution: List[int] = field(default_factory=lambda: [640, 480])
    thermal_camera_previewFPS: int = 20
    thermal_camera_recordFPS: int = 5
    heater_COM_port_number: int = 0
    heater_baud_rate: int = 9600

    _instance = None

    data_changed = Signal()

    def __post_init__(self):
        super().__init__()

    @staticmethod
    def get_instance():
        if Settings._instance is None:
            Settings._instance = Settings.load_from_file()
        return Settings._instance

    def set_duration_of_testing(self, duration: int):
        self.duration_of_testing = duration
        self.data_changed.emit()

    def set_heating_duration(self, duration: int):
        self.heating_duration = duration
        self.data_changed.emit()

    def set_language(self, language: str):
        self.language = language
        self.data_changed.emit()

    def set_theme(self, theme: str):
        self.theme = theme
        self.data_changed.emit()

    def set_thermal_camera_index(self, index: int):
        self.thermal_camera_index = index
        self.data_changed.emit()

    def set_thermal_camera_resolution(self, resolution: List[int]):
        self.thermal_camera_resolution = resolution
        self.data_changed.emit()

    def set_thermal_camera_previewFPS(self, fps: int):
        self.thermal_camera_previewFPS = fps
        self.data_changed.emit()

    def set_thermal_camera_recordFPS(self, fps: int):
        self.thermal_camera_recordFPS = fps
        self.data_changed.emit()

    def set_camera_index(self, index: int):
        self.camera_index = index
        self.data_changed.emit()

    def set_camera_resolution(self, resolution: List[int]):
        self.camera_resolution = resolution
        self.data_changed.emit()

    def set_camera_previewFPS(self, fps: int):
        self.camera_previewFPS = fps
        self.data_changed.emit()

    def set_camera_recordFPS(self, fps: int):
        self.camera_recordFPS = fps
        self.data_changed.emit()

    def set_heater_COM_port_number(self, number: int):
        self.heater_COM_port_number = number
        self.data_changed.emit()

    def set_heater_baud_rate(self, rate: int):
        self.heater_baud_rate = rate
        self.data_changed.emit()

    def save_to_file(self):
        settings_file = 'settings.json'
        with open(settings_file, 'w') as f:
            json.dump(asdict(self), f, indent=4)

    @staticmethod
    def load_from_file():
        settings_file = 'settings.json'
        if os.path.exists(settings_file):
            with open(settings_file, 'r') as f:
                data = json.load(f)
                return Settings(**data)
        else:
            return Settings()  # Возвращаем экземпляр с значениями по умолчанию


@dataclass
class PreviewSettings(QObject):
    # выбранная для просмотра зона контроля
    number_of_zone: List[int] = field(default_factory=lambda: [0, 0])  
    map_flag:      int = 1  # показывает, активен ли режим карты
    current_frame: int = 0  # текущий просматриваемый кадр видео
    type_of_graph: int = 0  # 0 - 2D, 1 - 3D

    # Алгоритмы постобработки изображений: 0 - off, 1 - on
    bs_alg:  int = 0    # Background Subtraction
    fft_alg: int = 0    # Fast Fourier Transform
    pca_alg: int = 0    # Principal Component Analysis

    _instance = None

    data_changed = Signal()

    def __post_init__(self):
        super().__init__()

    @staticmethod
    def get_instance():
        if PreviewSettings._instance is None:
            PreviewSettings._instance = PreviewSettings()
        return PreviewSettings._instance

    def set_number_of_zone(self, zone: List[int]):
        self.number_of_zone = zone
        self.data_changed.emit()

    def set_map_flag(self, flag: int):
        self.map_flag = flag
        self.data_changed.emit()

    def set_current_frame(self, frame: int):
        self.current_frame = frame
        self.data_changed.emit()

    def set_type_of_graph(self, graph_type: int):
        self.type_of_graph = graph_type
        self.data_changed.emit()

    def set_bs_alg(self, alg: int):
        self.bs_alg = alg
        self.data_changed.emit()

    def set_fft_alg(self, alg: int):
        self.fft_alg = alg
        self.data_changed.emit()

    def set_pca_alg(self, alg: int):
        self.pca_alg = alg
        self.data_changed.emit()
