# import os
#
# import cv2
#
# from danila.danila_v1 import Danila_v1
# from danila.danila_v2 import Danila_v2
# from danila.danila_v3 import Danila_v3
from danila.danila_v4 import Danila_v4

"""main module for user"""


class Danila:
    """main class for user"""
    def __init__(self, version, yolov5_dir):
        if (version == 4):
            self.danila = Danila_v4(yolov5_dir)
        else:
            self.danila = Danila_v4(yolov5_dir)
    # returns string - class of rama using CNN network
    # img - openCV frame

    def detail_classify(self, img, size = 256):
        return self.danila.detail_classify(img, size)

    def detail_text_detect(self, img, size = 256):
        return self.danila.detail_text_detect(img, size)

    def detail_text_recognize(self, img, size = 256):
        return self.danila.detail_text_recognize(img, size)

    def rama_classify(self, img, size = 256):
        """rama_classify(Img : openCv frame): String - returns class of rama using CNN network"""
        """rama_classify uses Rama_classify_class method - classify(Img)"""
        return self.danila.rama_classify(img, size)

    # returns openCV frame with rama from openCV frame\
    # def rama_detect(self, img, size = 256):
    #     """rama_detect(img : openCV img) -> openCV image with drawn rama rectangle"""
    #     return self.danila.rama_detect(img, size)
    #
    # # returns openCV image with cut_rama
    # def rama_cut(self, img, size = 256):
    #     """rama_cut(img : openCV img) -> openCV image of rama rectangle"""
    #     return self.danila.rama_cut(img, size)

    #
    # returns openCV cut rama with drawn text areas
    def rama_text_detect_cut(self, img, size = 256):
        """returns openCV cut rama with drawn text areas"""
        return self.danila.rama_text_detect_cut(img, size)

    # returns openCV img with drawn text areas
    # def rama_text_detect(self, img, size = 256):
    #     """returns openCV img with drawn text areas"""
    #     return self.danila.text_detect(img, size)
    # returns dict {'number', 'prod', 'year'} for openCV rama img or 'no_rama'
    def rama_text_recognize(self, img, size = 256):
        """returns dict {'number', 'prod', 'year'} for openCV rama img or 'no_rama'"""
        return self.danila.rama_text_recognize(img, size)

    # returns openCV img with drawn number areas
    def vagon_number_detect(self, img, size = 256):
        """returns openCV img with drawn number areas"""
        return self.danila.vagon_number_detect(img, size)

    def vagon_number_recognize(self, img, size = 256):
        return self.danila.vagon_number_recognize(img,size)