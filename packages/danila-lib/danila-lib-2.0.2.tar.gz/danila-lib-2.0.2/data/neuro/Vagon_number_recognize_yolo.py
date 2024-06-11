import hashlib
import json
import os
import zipfile
from datetime import datetime

import cv2
import requests
from urllib.parse import urlencode
import torch

from data.neuro.letters_in_image import Letters_In_Image
from data.result.Class_text import Class_text
from data.result.Label_area import Label_area
from easyocr import easyocr


class Vagon_number_recognize_yolo:
    def __init__(self, model_path, yolo_path):
        """reads yolov5 taught model from yandex-disk and includes it in class example"""
        base_url = 'https://cloud-api.yandex.net/v1/disk/public/resources/download?'
        public_key = model_path  # Сюда вписываете вашу ссылку
        # Получаем загрузочную ссылку
        final_url = base_url + urlencode(dict(public_key=public_key))
        response = requests.get(final_url)
        download_url = response.json()['href']
        # Загружаем файл и сохраняем его
        download_response = requests.get(download_url)
        zip_path = 'text_recognize_yolo.zip'
        # print(download_response.content)
        with open(zip_path, 'wb') as f:
            f.write(download_response.content)

        with zipfile.ZipFile(zip_path, 'r') as zip_ref:
            zip_ref.extractall()
        # weights_file_path = model_name + '_weights.pt'
        self.model = torch.hub.load(yolo_path, 'custom', 'text_recognize_yolo.pt', source='local')

    def work_image_cut(self, number_image_cut, l, number_h, number_w):
        h, w = number_image_cut.shape[:2]
        hash_object = hashlib.md5(bytes(str(datetime.now()), 'utf-8'))
        hash_str = hash_object.hexdigest()
        img_cut_path = 'cut_text_img' + hash_str + '.jpg'
        cv2.imwrite(img_cut_path, number_image_cut)
        # self.model.max_det = l
        results = self.model(img_cut_path, size=(number_h, number_w))
        json_res = results.pandas().xyxy[0].to_json(orient="records")
        res2 = json.loads(json_res)
        img_letters = Letters_In_Image.get_letters_in_image_from_yolo_json(res2)
        img_letters.sort_letters()
        img_letters.delete_intersections()
        img_letters.delete_x_intersections()
        if len(img_letters.letters) > 8:
            img_letters.letters = img_letters.letters[0:8]
        os.remove(img_cut_path)
        return img_letters.make_word(), img_letters.get_avg_conf()

    def make_cuts(self, img_vagon, rect_array):
        number_image_cuts = []
        for rect in rect_array:
            number_image_cuts.append(img_vagon[rect.ymin:rect.ymax, rect.xmin:rect.xmax])
        return number_image_cuts

    def work_image(self, img_vagon, rect_array):
        image_text_areas = self.make_cuts(img_vagon, rect_array)
        numbers = []
        for image_text_area in image_text_areas:
            number = {'image_text_area' : image_text_area, 'text' : '', 's' : 0, 'conf' : 0.0}
            h, w = image_text_area.shape[:2]
            number['s'] = h * w
            (text, conf) = self.work_image_cut(image_text_area, 8, 128, 320)
            number['text'] = text
            number['conf'] = conf
            numbers.append(number)
        numbers.sort(key= lambda number : number['s'], reverse=True)
        if len(numbers) == 1:
            return (numbers[0]['text'], numbers[0]['conf'])
        else:
            if (len(numbers[0]['text']) != 8) and (len(numbers[1]['text']) == 8):
                return (numbers[1]['text'], numbers[1]['conf'])
            elif (len(numbers[0]['text']) == 8) and (len(numbers[1]['text']) != 8):
                return (numbers[0]['text'], numbers[0]['conf'])
            else:
                ans = sorted(numbers[0:2], key = lambda number : number['conf'], reverse=True)[0]
                return ans['text'], ans['conf']