import json
import os

import cv2
import torch
import zipfile
import requests
from urllib.parse import urlencode
from data.result.Rect import Rect

"""module for detecting number in vagon"""
class Vagon_number_detect_class:
    """module for detecting number in vagon"""

    # reads yolov5 taught model from yandex-disk and includes it in class example
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
        zip_path = 'vagon_number_detect.zip'
        # print(download_response.content)
        with open(zip_path, 'wb') as f:
            f.write(download_response.content)

        with zipfile.ZipFile(zip_path, 'r') as zip_ref:
            zip_ref.extractall()
        weights_file_path = 'vagon_number_detect.pt'
        self.model = torch.hub.load(yolo_path, 'custom', weights_file_path, source='local')



    #получить JSON с результатами yolo
    def work_img(self, img_path, size):
        """get JSON with yolo_results from img from img_path"""
        results = self.model([img_path], size=size)
        json_res = results.pandas().xyxy[0].to_json(orient="records")
        res2 = json.loads(json_res)
        return res2

    # получить координаты прямоугольников с номерами
    def vagon_rama_detect(self, img_path, size):
        """get Rect object with rama coordinates from img from img_path"""
        json_res = self.work_img(img_path, size)
        number_rects = []
        for dict_text_area in json_res:
            if dict_text_area['confidence']>0.25:
                number_rect = Rect(   xmin=int(float(dict_text_area['xmin'])),
                                        xmax=int(float(dict_text_area['xmax'])),
                                        ymin=int(float(dict_text_area['ymin'])),
                                        ymax=int(float(dict_text_area['ymax']))
                                )
                number_rects.append(number_rect)
        return number_rects


