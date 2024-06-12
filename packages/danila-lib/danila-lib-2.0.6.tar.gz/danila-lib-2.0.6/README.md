# danila_lib v1.3.7
 python library for Danila

# To install project made 
    pip install danila-lib


# To use in your project 
    from danila.danila import Danila

# All use methods are in 
    class Danila

# main method returns dict {'number', 'prod', 'year'} for openCV rama img or 'no_rama'
    def text_recognize(self, img):

# steps for algorythm

# returns string - class of rama, img - openCV frame
    def rama_classify(self, img):

# returns openCV frame with rama from openCV frame
    def rama_detect(self, img):

# returns openCV image with cut_rama
    def rama_cut(self, img):

# returns openCV cut rama with drawn text areas
    def text_detect_cut(self, img):

# returns openCV img with drawn text areas
    def text_detect(self, img):

# in package data/neuro there is module Rama_classify_class
    class Rama_classify_class

# reads CNN taught model and includes it in class example
    def __init__():

# makes grey NumPy Array(1,512,512) of doubles[0..1] from openCV image
    def prepare_img(img : openCV frame): NumPy Array(1,512,512)[0..1]

# classify openCV img with CNN, returns list with double[0..1] values 
    def work_img(img : openCV frame): Double[0..1] list

# classify openCV img with CNN, returns Class_im
    def classify(img : openCV frame): Class_im

# in package data/neuro there is module Rama_detect_class
    class Rama_detect_class
# reads yolov5 taught model from yandex-disk and includes it in class example
    def __init__(self, model_path, model_name, yolo_path):
# получить JSON с результатами yolo
    def work_img(self, img_path):
# получить координаты прямоугольника с рамой
    def rama_detect(self, img_path):

# in package data/neuro there is module Text_detect_class
    class Text_detect_class

# reads yolov5 taught model from yandex-disk and includes it in class example
    def __init__(self, model_path, model_name, yolo_path):

# find text areas on img from img_path with yolov5, returns yolojson
    def work_img(self, img_path):

# find text areas on img from img_path with yolov5, returns dict with rects for each text class
    def text_detect(self, img_path):

# draw img_text_areas on img, returns opencv img
    def draw_text_areas_in_opencv(self, image_text_areas, img):

# in package data/neuro there is module Letters_recognize
    class Letters_recognize:

# main_method takes all image_text_areas from image_rama_cut and recognize text 
    def work_image_cut(self, image_text_areas, image_rama_cut, number_length, prod_length, year_length):

# read CNN model from yandex and put into object
    def __init__(self):

# cut text_areas imgs for each Rect from rect_array returns openCv imgs list
    def make_cuts(self, img_rama_cut, rect_array):

# for every text_class recognize text from all areas of text_class, length is depends on class and prod, returns string 
    def work_image_cuts(self, number_image_cuts, length):

# recognize one word of given length from one img, returns str
    def work_img_word(self, image_number, letter_number):

# prepare img of one letter for CNN, returns np_array(1,28,28,1) of Double[0..1]
    def prepare_img_letter(self, image_letter):

# recognize img of one letter with CNN, returns list[10] of p
    def work_img_letter(self, image_initial):

# recognize img of one letter with CNN, returns letter in str
    def classify_letter(self, image_letter):

# in package data/result Rect module for rectangle operations
# прочитать из json результата йоло
    @staticmethod
    def get_rect_from_yolo_json(yolo_json):
# makes Rect object from xmin, xmax, ymin, ymax
    def __init__(self, xmin=0, xmax=0, ymin=0, ymax=0):
# Найти IOU между этим прямоугольником и другим, данным в объекте
    def IoU(self, rect):
# makes string from object
    def __str__(self):

# find intersection square between object and other rectangle
    def intersection(self, rect):
# find union RECT between object and other rectangle
    def union(self, rect):
# in package data/result Class_im
    class Class_im(Enum):
        rama_no_spring = 0
        rama_spring = 1

# in package data/result class Text_area
    def __init__(self, dict_text_area):
        self.class_im = Class_text(dict_text_area['class'])
        self.rect = Rect(...)

# in package data/result class image_text_areas
# class contains dict with Rects list for each text_class
    class Image_text_areas:

# makes dict {Class_text.number : [], Class_text.prod : [], Class_text.text : [], Class_text.year : []} 
    def __init__(self):

# add text area to dict
    def add_area(self, text_area):

# add list of text areas
    def fill_in_with_areas(self, areas):

# delete all cases in which two areas are intersected
    def correct_intersections(self):

# changes Rects coordinates from cut_img to whole_img from rama Rect
    def explore_to_whole_image(self, rama_rect):

# exapmles of using you can find 
https://github.com/Arseniy-Zhuck/danila_lib_demo