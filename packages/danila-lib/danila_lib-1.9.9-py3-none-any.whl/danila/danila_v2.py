import os

import cv2

from data.neuro.Letters_recognize import Letters_recognize
from data.neuro.Rama_detect_class import Rama_detect_class
from data.neuro.Text_detect_class import Text_detect_class
from data.neuro.models import *
from data.result.Class_im import Class_im
from data.result.Class_text import Class_text
from data.result.Rect import Rect

"""main module for user"""
from data.neuro.Rama_classify_class import Rama_classify_class
from data.neuro.text_recognize_yolo import Text_Recognize_yolo

class Danila_v2:
    """main class for user"""
    def __init__(self, yolov5_dir):

        self.rama_classify_model = Rama_classify_class()
        yolo_path = yolov5_dir
        rama_no_spring_detect_model_path = RAMA_BEGICKAYA_DETECT_MODEL_ADDRESS
        self.rama_no_spring_detect_model = Rama_detect_class(rama_no_spring_detect_model_path,
                                                             'rama_no_spring_detect', yolo_path)
        rama_spring_detect_model_path = RAMA_RUZHIMMASH_DETECT_MODEL_ADDRESS
        self.rama_spring_detect_model = Rama_detect_class(rama_spring_detect_model_path, 'rama_spring_detect',
                                                             yolo_path)
        rama_spring_ruzhimmash_text_detect_model_path = RAMA_RUZHIMMASH_TEXT_DETECT_MODEL_ADDRESS
        self.rama_spring_ruzhimmash_text_detect_model = Text_detect_class(rama_spring_ruzhimmash_text_detect_model_path,
                                                                          'rama_spring_ruzhimmash_text_detect', yolo_path)
        rama_no_spring_bejickaya_text_detect_model_path = RAMA_BEJICKAYA_TEXT_DETECT_MODEL_ADDRESS
        self.rama_no_spring_bejickaya_text_detect_model = Text_detect_class(rama_no_spring_bejickaya_text_detect_model_path,
                                                                            'rama_no_spring_bejickaya_text_detect', yolo_path)
        text_recognize_yolo_model_path = TEXT_RECOGNIZE_YOLO_MODEL_ADDRESS
        self.text_recognize_model = Text_Recognize_yolo(text_recognize_yolo_model_path, yolo_path)
    # returns string - class of rama using CNN network
    # img - openCV frame

    def rama_classify(self, img, size):
        """rama_classify(Img : openCv frame): String - returns class of rama using CNN network"""
        """rama_classify uses Rama_classify_class method - classify(Img)"""
        # img = cv2.imread(img_path)
        class_im = self.rama_classify_model.classify(img)
        res = class_im.name + ', '
        if (class_im == Class_im.rama_spring):
            res += 'ruzhimmash'
        else:
            res += 'bejickaya'
        return res

    # returns openCV frame with rama from openCV frame\
    def rama_detect(self, img, size):
        """rama_detect(img : openCV img) -> openCV image with drawn rama rectangle"""
        initial_image_path = 'initial_image.jpg'
        cv2.imwrite(initial_image_path, img)
        class_im = self.rama_classify_model.classify(img)
        rect = Rect()
        if (class_im == Class_im.rama_spring):
            rect = self.rama_spring_detect_model.rama_detect(initial_image_path)
        else:
            rect = self.rama_no_spring_detect_model.rama_detect(initial_image_path)
        new_img = img.copy()
        os.remove('initial_image.jpg')
        if rect is None:
            return img
        cv2.rectangle(new_img, (rect.xmin, rect.ymin), (rect.xmax, rect.ymax), (0, 0, 255), 2)
        cv2.putText(new_img, class_im.name, (rect.xmin, rect.ymin), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0,0,255), 2)
        return new_img

    # returns openCV image with cut_rama
    def rama_cut(self, img, size):
        """rama_cut(img : openCV img) -> openCV image of rama rectangle"""
        initial_image_path = 'initial_image.jpg'
        cv2.imwrite(initial_image_path, img)
        class_im = self.rama_classify_model.classify(img)
        rect = Rect()
        if (class_im == Class_im.rama_spring):
            rect = self.rama_spring_detect_model.rama_detect(initial_image_path)
        else:
            rect = self.rama_no_spring_detect_model.rama_detect(initial_image_path)
        if rect is None:
            return img
        img_res = img[rect.ymin:rect.ymax, rect.xmin:rect.xmax]
        os.remove('initial_image.jpg')
        return img_res
    #
    # returns openCV cut rama with drawn text areas
    def text_detect_cut(self, img, size):
        """returns openCV cut rama with drawn text areas"""
        initial_image_path = 'initial_image.jpg'
        cv2.imwrite(initial_image_path, img)
        class_im = self.rama_classify_model.classify(img)
        rect = Rect()
        if (class_im == Class_im.rama_spring):
            rect = self.rama_spring_detect_model.rama_detect(initial_image_path)
            if rect is None:
                return img
            img_cut = img[rect.ymin:rect.ymax, rect.xmin:rect.xmax]
            img_cut_path = 'cut_img.jpg'
            cv2.imwrite(img_cut_path, img_cut)
            image_text_areas = self.rama_spring_ruzhimmash_text_detect_model.text_detect(img_cut_path)
            image_drawn_text_areas = self.rama_spring_ruzhimmash_text_detect_model.draw_text_areas_in_opencv(image_text_areas, img_cut)
            os.remove(initial_image_path)
            os.remove(img_cut_path)
            return image_drawn_text_areas
        else:
            rect = self.rama_no_spring_detect_model.rama_detect(initial_image_path)
            if rect is None:
                return img
            img_cut = img[rect.ymin:rect.ymax, rect.xmin:rect.xmax]
            img_cut_path = 'cut_img.jpg'
            cv2.imwrite(img_cut_path, img_cut)
            image_text_areas = self.rama_no_spring_bejickaya_text_detect_model.text_detect(img_cut_path)
            image_drawn_text_areas = self.rama_no_spring_bejickaya_text_detect_model.draw_text_areas_in_opencv(image_text_areas, img_cut)
            os.remove(initial_image_path)
            os.remove(img_cut_path)
            return image_drawn_text_areas

    # returns openCV img with drawn text areas
    def text_detect(self, img, size):
        """returns openCV img with drawn text areas"""
        initial_image_path = 'initial_image.jpg'
        cv2.imwrite(initial_image_path, img)
        class_im = self.rama_classify_model.classify(img)
        rect = Rect()
        if (class_im == Class_im.rama_spring):
            rect = self.rama_spring_detect_model.rama_detect(initial_image_path)
            if rect is None:
                return img
            img_cut = img[rect.ymin:rect.ymax, rect.xmin:rect.xmax]
            img_cut_path = 'cut_img.jpg'
            cv2.imwrite(img_cut_path, img_cut)
            image_text_areas = self.rama_spring_ruzhimmash_text_detect_model.text_detect(img_cut_path)
            image_text_areas.explore_to_whole_image(rect)
            image_drawn_text_areas = self.rama_spring_ruzhimmash_text_detect_model.draw_text_areas_in_opencv(image_text_areas, img)
            os.remove(initial_image_path)
            os.remove(img_cut_path)
            return image_drawn_text_areas
        else:
            rect = self.rama_no_spring_detect_model.rama_detect(initial_image_path)
            if rect is None:
                return img
            img_cut = img[rect.ymin:rect.ymax, rect.xmin:rect.xmax]
            img_cut_path = 'cut_img.jpg'
            cv2.imwrite(img_cut_path, img_cut)
            image_text_areas = self.rama_no_spring_bejickaya_text_detect_model.text_detect(img_cut_path)
            image_text_areas.explore_to_whole_image(rect)
            image_drawn_text_areas = self.rama_no_spring_bejickaya_text_detect_model.draw_text_areas_in_opencv(image_text_areas, img)
            os.remove(initial_image_path)
            os.remove(img_cut_path)
            return image_drawn_text_areas

    # returns dict {'number', 'prod', 'year'} for openCV rama img or 'no_rama'
    def text_recognize(self, img, size):
        """returns dict {'number', 'prod', 'year'} for openCV rama img or 'no_rama'"""
        initial_image_path = 'initial_image.jpg'
        cv2.imwrite(initial_image_path, img)
        class_im = self.rama_classify_model.classify(img)
        rect = Rect()
        if (class_im == Class_im.rama_spring):
            rect = self.rama_spring_detect_model.rama_detect(initial_image_path)
            if rect is None:
                return {'result': 'no_rama'}
            img_cut = img[rect.ymin:rect.ymax, rect.xmin:rect.xmax]
            img_cut_path = 'cut_img.jpg'
            cv2.imwrite(img_cut_path, img_cut)
            image_text_areas = self.rama_spring_ruzhimmash_text_detect_model.text_detect(img_cut_path)
            label_area = self.text_recognize_model.work_image_cut(image_text_areas, img_cut, 5, 32,96,
                                                                  4, 64,64, 2, 64,64)
            res_labels = {}
            res_labels['number'] = label_area.labels[Class_text.number]
            res_labels['prod'] = label_area.labels[Class_text.prod]
            res_labels['year'] = label_area.labels[Class_text.year]
            return res_labels
        else:
            rect = self.rama_no_spring_detect_model.rama_detect(initial_image_path)
            if rect is None:
                return {"result" : "no_rama"}
            img_cut = img[rect.ymin:rect.ymax, rect.xmin:rect.xmax]
            img_cut_path = 'cut_img.jpg'
            cv2.imwrite(img_cut_path, img_cut)
            image_text_areas = self.rama_no_spring_bejickaya_text_detect_model.text_detect(img_cut_path)
            label_area = self.text_recognize_model.work_image_cut(image_text_areas, img_cut, 6, 64, 192,
                                                                  2, 64, 64, 2, 64,64)
            res_labels = {}
            res_labels['number'] = label_area.labels[Class_text.number]
            res_labels['prod'] = label_area.labels[Class_text.prod]
            res_labels['year'] = label_area.labels[Class_text.year]
            return res_labels
