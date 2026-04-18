from PySide6.QtCore import QSize
from PySide6.QtGui import QFont
# Tseries, Timage - model
from thermograms.thermograms import Timage, Tseries, CAM_K
import numpy as np
import cv2
from typing import Dict, Any

# Импорт единых шрифтов и констант (предполагается наличие модулей)
try:
    from ui_fonts import fonts  # словарь с QFont, например fonts['regular'], fonts['small']
    from ui_constants import (
        LAYOUT_SPACING, WIDGET_SPACING, FIELD_HEIGHT,
        BUTTON_SIZE, GROUP_BOX_STYLE
    )
except ImportError:
    # Заглушки на случай отсутствия модулей (для автономной работы примера)
    fonts = {
        'regular': QFont('Segoe UI', 9),
        'small': QFont('Segoe UI', 8),
        'medium': QFont('Segoe UI', 10, QFont.Medium),
        'large': QFont('Segoe UI', 12, QFont.Medium)
    }
    LAYOUT_SPACING = 10
    WIDGET_SPACING = 15
    FIELD_HEIGHT = 32
    BUTTON_SIZE = QSize(120, FIELD_HEIGHT)
    GROUP_BOX_STYLE = """
        QGroupBox {
            font-weight: 600;
            margin-top: 9px;
            padding: 12px;
        }
        QGroupBox::title {
            subcontrol-origin: margin;
            left: 15px;
            padding: 0 5px;
        }
    """

need_to_apply = np.zeros((1080, 1920, 3), dtype=np.uint8)
# Параметры текста
text = """You need to apply methods to series first"""
font = cv2.FONT_HERSHEY_SIMPLEX
font_scale = 2.5
color = (255, 255, 255)  # белый
thickness = 3
# Размеры текста для центрирования
(text_w, text_h), baseline = cv2.getTextSize(text, font, font_scale, thickness)
# Координаты центра
x = (need_to_apply.shape[1] - text_w) // 2
y = (need_to_apply.shape[0] + text_h) // 2
# Наносим текст
cv2.putText(need_to_apply, text, (x, y), font, font_scale, color, thickness)
need_to_apply = need_to_apply[..., 0].astype('float64')



class PipelineManager:
    def __init__(self):
        self.applied = True
        self.stages = []  # [[method_idx, params, applied]]
        self.methods = [ # self.methods[method_idx] = {'name', 'params': [(name, variable name, default value)], 'req_series', 'Timage', 'Tseries'}
            {
                'name': 'Медианное размытие',
                'params': [('Радиус', 3)],
                'req_series': False,
                'Timage': lambda t, radius: t.median_blur(radius),
                'Tseries': lambda t, radius: t.median_blur(radius),
            },
            {
                'name': 'Размытие по Гауссу',
                'params': [('Радиус', 3), ('Ст. отклонение', 1.0)],
                'req_series': False,
                'Timage': lambda t, radius, stddev: t.gaussian_blur(stddev, radius),
                'Tseries': lambda t, radius, stddev: t.gaussian_blur(stddev, radius),
            },
            {
                'name': 'Увеличение резкости',
                'params': [('Радиус', 3), ('Ст. отклонение', 1.0)],
                'req_series': False,
                'Timage': lambda t, radius, stddev: t.sharpness(radius, stddev),
                'Tseries': lambda t, radius, stddev: t.sharpness(radius, stddev),
            },
            {
                'name': 'Исправление искажений',
                'params': [],
                'req_series': False,
                'Timage': lambda t: t.distorted(CAM_K, scale=1.15)[17:-17, 6:-6],
                'Tseries': lambda t: t.distorted(CAM_K, scale=1.15)[17:-17, 6:-6],
            },
            #{
            #    'name': 'Аффинные преобразования',
            #    'params': [],
            #    'req_series': False,
            #    'Timage': lambda t: t.median_blur(radius),
            #    'Tseries': lambda t: t.median_blur(radius),
            #},
            {
                'name': 'Обрезка',
                'params': [('Строка начала', 0), ('Строка конца (не включ.)', -1), ('Столбец начала', 0), ('Столбец конца (не включ.)', -1)],
                'req_series': False,
                'Timage': lambda t, i0, i1, j0, j1: t[i0:i1, j0:j1],
                'Tseries': lambda t, i0, i1, j0, j1: t[i0:i1, j0:j1],
            },
            {
                'name': 'Обрезка по времени',
                'params': [('Кадр начала', 0), ('Кадр конца (не включ.)', -1)],
                'req_series': True,
                'Tseries': lambda t, frame0, frame1: t[..., frame0: frame1],
            },
            {
                'name': 'Карта отклонений',
                'params': [('Бинаризация', 0)],
                'req_series': True,
                'Tseries': lambda t, binarization: Tseries(array=t.std_map(binarization=binarization if binarization!=0 else 'otsu')[..., np.newaxis]),
            },
            {
                'name': 'Усреднение по времени',
                'params': [('Кадры', 3)],
                'req_series': True,
                'Tseries': lambda t, frames: t.avg_time(frames),
            },
            {
                'name': 'Быстрое преобразование Фурье: вещественная часть',
                'params': [],
                'req_series': True,
                'Tseries': lambda t: Tseries(array=t.fft().real),
            },
            {
                'name': 'Быстрое преобразование Фурье: мнимая часть',
                'params': [],
                'req_series': True,
                'Tseries': lambda t: Tseries(array=t.fft().imag),
            },
            {
                'name': 'Метод главных компонент',
                'params': [('Количество компонент', 4)],
                'req_series': True,
                'Tseries': lambda t, n_components: Tseries(array=t.pca(n_components)),
            }
        ]

    def add_stage(self, method_idx: str, params: Dict[str, Any]):
        self.stages.append([method_idx, params, False])
        self.applied = False

    def remove_stage(self, index: int):
        if self.stages[index][2]:
            for i in range(len(self.stages)):
                self.stages[i][2] = False
        del self.stages[index]
        if len(self.stages)==0: self.applied = True
        else: self.applied = False

    def clear(self):
        self.stages.clear()
        self.applied = True

    def apply_to_frame(self, frame: Timage) -> Timage:
        """Применить все этапы к одному кадру (пример)."""
        result = frame
        
        for method_idx, params, applied in self.stages:
            if not applied:
                if self.methods[method_idx]['req_series']: return Timage(array=need_to_apply)
                result = self.methods[method_idx]['Timage'](result, *params)
        
        return result

    def apply_to_series(self, frames: Tseries) -> Tseries:
        """Применить пайплайн ко всем кадрам."""
        result = frames

        for i, (method_idx, params, applied) in enumerate(self.stages):
            if not applied:
                result = self.methods[method_idx]['Tseries'](result, *params)
            self.stages[i][2] = True
        self.applied = True

        return result
    
    def not_applied(self):
        for i in range(len(self.stages)):
            self.stages[i][2] = False # not applied
        if len(self.stages): self.applied = False

    def change_stage(self, index, params):
        self.stages[index][1] = params
        if not self.stages[index][2]: return
        self.not_applied()