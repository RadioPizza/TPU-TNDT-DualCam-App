import logging
import PySpin
from typing import Tuple, Optional

logger = logging.getLogger(__name__)



def run_flir_diagnostics():
    try:
        logger.info("PySpin успешно импортирован")
        # Быстрая проверка камер без длительного удержания ресурсов
        system = PySpin.System.GetInstance()
        cam_list = system.GetCameras()
        num_cameras = cam_list.GetSize()
        logger.info(f"Количество обнаруженных камер FLIR: {num_cameras}")
        if num_cameras > 0:
            # Получаем информацию о первой камере
            camera = cam_list.GetByIndex(0)
            camera.Init()
            try:
                nodemap = camera.GetNodeMap()
                node_model = PySpin.CStringPtr(nodemap.GetNode("DeviceModelName"))
                if PySpin.IsAvailable(node_model):
                    logger.info(f"Модель камеры: {node_model.GetValue()}")
            finally:
                camera.DeInit()
                del camera

        cam_list.Clear()

        system.ReleaseInstance()

    except Exception as e:
        logger.error(f"Диагностика PySpin не удалась: {e}")

if __name__ == '__main__':
    # Для отладки при прямом запуске diagnostics.py
    logging.basicConfig(level=logging.INFO)
    run_flir_diagnostics()