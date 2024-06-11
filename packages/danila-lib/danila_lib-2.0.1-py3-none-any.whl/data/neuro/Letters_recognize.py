import os
import zipfile
import requests
from urllib.parse import urlencode

import cv2
import keras
import numpy as np

from data.neuro.models import *
from data.result.Class_text import Class_text
from data.result.Label_area import Label_area
"""class for recognizing letters in text_area"""

class Letters_recognize:
    """class for recognizing letters in text_area"""
    # read CNN model from yandex and put into object
    def __init__(self):
        """read CNN model from yandex and put into object"""
        base_url = 'https://cloud-api.yandex.net/v1/disk/public/resources/download?'
        public_key = LETTERS_RECOGNIZE  # Сюда вписываете вашу ссылку
        # Получаем загрузочную ссылку
        final_url = base_url + urlencode(dict(public_key=public_key))
        response = requests.get(final_url)
        download_url = response.json()['href']
        # Загружаем файл и сохраняем его
        download_response = requests.get(download_url)

        # print(download_response.content)
        with open('letters_recognize.zip', 'wb') as f:
            f.write(download_response.content)

        with zipfile.ZipFile('letters_recognize.zip', 'r') as zip_ref:
            zip_ref.extractall()

        self.letter_classify_model = keras.models.load_model('letters_recognize')

    # cut text_areas imgs for each Rect from rect_array returns openCv imgs list
    def make_cuts(self, img_rama_cut, rect_array):
        """cut text_areas imgs for each Rect from rect_array returns openCv imgs list"""
        number_image_cuts = []
        for rect in rect_array:
            number_image_cuts.append(img_rama_cut[rect.ymin:rect.ymax, rect.xmin:rect.xmax])
        return number_image_cuts

    # for every text_class try to recognize text from all areas of text_class, length is depends on class and prod, returns string
    def work_image_cuts(self, number_image_cuts, length):
        """for every text_class try to recognize text from all areas of text_class, length is depends on class and prod, returns string """
        str = ''
        for number_image_cut in number_image_cuts:
            # cv2.imwrite('data/neuro_classes/cut.jpg', number_image_cut)
            cur_str = self.work_img_word(number_image_cut, length)
            if len(cur_str) > len(str):
                str = cur_str
        return str

    # main_method takes all image_text_areas from image_rama_cut and recognize text
    def work_image_cut(self, image_text_areas, image_rama_cut, number_length, prod_length, year_length):
        """main_method takes all image_text_areas from image_rama_cut and recognize text"""
        number_image_rects = image_text_areas.areas[Class_text.number]
        number_image_cuts = self.make_cuts(image_rama_cut, number_image_rects)
        number = self.work_image_cuts(number_image_cuts, number_length)
        prod_image_rects = image_text_areas.areas[Class_text.prod]
        prod_image_cuts = self.make_cuts(image_rama_cut, prod_image_rects)
        prod = self.work_image_cuts(prod_image_cuts, prod_length)
        year_image_rects = image_text_areas.areas[Class_text.year]
        year_image_cuts = self.make_cuts(image_rama_cut, year_image_rects)
        year = self.work_image_cuts(year_image_cuts, year_length)
        label_area = Label_area()
        label_area.labels[Class_text.number] = number
        label_area.labels[Class_text.prod] = prod
        label_area.labels[Class_text.year] = year
        return label_area

    # recognize one word of given length from one img, returns str
    def work_img_word(self, image_number, letter_number):
        """recognize one word of given length from one img, returns str"""
        h, w = image_number.shape[:2]
        left_border = 0
        right_border = int(w / letter_number)
        res = ''
        for i in range(letter_number):
            left_border_cur = left_border
            right_border_cur = right_border
            # if (left_border_cur > 0):
            #     left_border_cur -= int(w / 16)
            # if (right_border_cur < w -1):
            #     right_border_cur -= int(w / 16)
            letter_img = image_number[0:h, left_border_cur:right_border_cur]
            letter_str = self.classify_letter(letter_img)
            res += letter_str
            left_border = right_border
            right_border = left_border + int(w / 6)
        return res

    # prepare img of one letter for CNN, returns np_array(1,28,28,1) of Double[0..1]
    def prepare_img_letter(self, image_letter):
        """prepare img of one letter for CNN, returns np_array(1,28,28,1) of Double[0..1]"""
        img_grey = cv2.cvtColor(image_letter, cv2.COLOR_BGR2GRAY)
        img_grey_size = cv2.resize(img_grey, (28, 28))
        data = np.array(img_grey_size, dtype="float32") / 255.0
        data = data.reshape((1, 28, 28, 1))
        return data

    # recognize img of one letter with CNN, returns list[10] of p
    def work_img_letter(self, image_initial):
        """recognize img of one letter with CNN, returns list[10] of p"""
        data = self.prepare_img_letter(image_initial)
        res = self.letter_classify_model.predict(data)
        res_list = res[0].tolist()
        return res_list

    # recognize img of one letter with CNN, returns letter in str
    def classify_letter(self, image_letter):
        """recognize img of one letter with CNN, returns letter in str"""
        res_list = self.work_img_letter(image_letter)
        res_index = res_list.index(max(res_list))
        return str(res_index)

