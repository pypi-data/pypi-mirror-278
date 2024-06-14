from data.result.Class_text import Class_text
from data.result.Rect import Rect


class Text_area:

    def __init__(self, dict_text_area):
        self.class_im = Class_text(dict_text_area['class'])
        self.rect = Rect(
                            xmin = int(float(dict_text_area['xmin'])),
                            xmax = int(float(dict_text_area['xmax'])),
                            ymin = int(float(dict_text_area['ymin'])),
                            ymax = int(float(dict_text_area['ymax']))
        )



