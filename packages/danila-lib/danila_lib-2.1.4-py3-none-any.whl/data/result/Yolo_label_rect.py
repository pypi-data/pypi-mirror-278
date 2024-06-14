from data.result.Rect import Rect


class Yolo_label_Rect:

    @staticmethod
    def build_from_2D_array(data, h, w):
        Yolo_label_Rect(data[0][1], data[0][3], data[0][2], data[0][4], h, w)

    def __init__(self, xc=0.0, ow=0.0, yc=0.0, oh=0.0, h=0.0, w=0.0):
        self.xc = xc
        self.ow = ow
        self.yc = yc
        self.oh = oh
        self.w = w
        self.h = h


    def build_rect(self):
        xmin_t = int((self.xc - self.ow / 2) * self.w)
        xmax_t = int((self.xc + self.ow / 2) * self.w)
        ymin_t = int((self.yc - self.oh / 2) * self.h)
        ymax_t = int((self.yc + self.oh / 2) * self.h)
        return Rect(xmin_t, xmax_t, ymin_t, ymax_t)

