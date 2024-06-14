"""module for rectangle operations"""

class Rect:
    """rectangle class contains xmin, ymin - upperleft and xmax ymax - downright corners of rectangle"""
    # прочитать из json результата йоло
    @staticmethod
    def get_rect_from_yolo_json(yolo_json):
        """from yolo JSON answer reads Rect object"""
        if len(yolo_json) > 0:
            xmin = int(float(yolo_json[0]['xmin']))
            xmax = int(float(yolo_json[0]['xmax']))
            ymin = int(float(yolo_json[0]['ymin']))
            ymax = int(float(yolo_json[0]['ymax']))
            rect = Rect(xmin, xmax, ymin, ymax)
            return rect
        else:
            return None

    def __init__(self, xmin=0, xmax=0, ymin=0, ymax=0):
        """makes Rect object from xmin, xmax, ymin, ymax"""
        self.xmin = xmin
        self.xmax = xmax
        self.ymin = ymin
        self.ymax = ymax

    # Найти IOU между этим прямоугольником и другим, данным в объекте
    def IoU(self, rect):
        """find intersection over union between object and other rectangle"""
        def IOU(xmin, xmax, ymin, ymax, xmin_t, xmax_t, ymin_t, ymax_t,h,w):
            I = 0
            U = 0
            for i in range(0, w):
                for j in range(0, h):
                    flag = ((i <= xmax) and (i >= xmin) and (j <= ymax) and (j >= ymin))
                    flag_t = ((i <= xmax_t) and (i >= xmin_t) and (j <= ymax_t) and (j >= ymin_t))
                    if (flag and flag_t):
                        I += 1
                    if (flag or flag_t):
                        U += 1
            resultat = I / float(U)
            return resultat
        h = max(self.ymax, rect.ymax) - min(self.ymin, rect.ymin)
        w = max(self.xmax, rect.xmax) - min(self.xmin, rect.xmin)
        return IOU(self.xmin, self.xmax, self.ymin, self.ymax,
                   rect.xmin, rect.xmax, rect.ymin, rect.ymax)

    def __str__(self):
        """makes string from object"""
        res = ('xmin = ' + str(self.xmin) + ', xmax = ' + str(self.xmax) + ', ymin = ' + str(self.ymin) +
               ', ymax = ' + str(self.ymax))
        return res

    def intersection(self, rect):
        """find intersection square between object and other rectangle"""
        h = max(self.ymax, rect.ymax) - min(self.ymin, rect.ymin)
        w = max(self.xmax, rect.xmax) - min(self.xmin, rect.xmin)
        I = 0
        U = 0
        for i in range(0, w):
            for j in range(0, h):
                flag = ((i <= self.xmax) and (i >= self.xmin) and (j <= self.ymax) and (j >= self.ymin))
                flag_t = ((i <= rect.xmax) and (i >= rect.xmin) and (j <= rect.ymax) and (j >= rect.ymin))
                if (flag and flag_t):
                    I += 1
        return I

    def union(self, rect):
        """find union RECT between object and other rectangle"""
        new_xmin = min(self.xmin, rect.xmin)
        new_ymin = min(self.ymin, rect.ymin)
        new_xmax = max(self.xmax, rect.xmax)
        new_ymax = max(self.ymax, rect.ymax)
        return Rect(new_xmin, new_xmax, new_ymin, new_ymax)
