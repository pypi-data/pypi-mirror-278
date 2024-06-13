import cv2
from tensorflow import keras
import numpy as np

from data.neuro.models import *
from data.result.Class_im import *
import zipfile
import requests
from urllib.parse import urlencode

class Detail_classify_class:
    def __init__(self, detail_classify_model_path):
        base_url = 'https://cloud-api.yandex.net/v1/disk/public/resources/download?'
        public_key = 'https://disk.yandex.ru/d/k6Wx0bD98fpswQ'  # Сюда вписываете вашу ссылку

        public_key = detail_classify_model_path  # Сюда вписываете вашу ссылку
        # Получаем загрузочную ссылку
        final_url = base_url + urlencode(dict(public_key=public_key))
        response = requests.get(final_url)
        download_url = response.json()['href']

        # Загружаем файл и сохраняем его
        download_response = requests.get(download_url)
        # print(download_response.content)

        # print(download_response.content)
        with open('detail_classify_model.zip', 'wb') as f:
            f.write(download_response.content)

        with zipfile.ZipFile('detail_classify_model.zip', 'r') as zip_ref:
            zip_ref.extractall()
        self.detail_classify_model = keras.models.load_model('detail_classify_model.h5')

    def prepare_img(self, img):
        img_grey = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        img_grey_size = cv2.resize(img_grey, (512, 512))
        data = np.array(img_grey_size, dtype="float") / 255.0
        data = data.reshape((1, 512, 512))
        return data

    def work_img(self, img):
        """work_img(img:openCV frame):Double[0..1] list - classify openCV img with CNN, returns list with double[0..1] values"""
        data = self.prepare_img(img)
        res = self.detail_classify_model.predict(data)
        res_list = res[0].tolist()
        return res_list

    def classify(self, image_initial):
        """classify(img:openCV frame):Class_im - classify openCV img with CNN, returns Class_im"""
        res_list = self.work_img(image_initial)
        res_index = res_list.index(max(res_list))
        class_detail = Class_detail(res_index)
        conf = res_list[res_index]
        return Class_detail_result(class_detail, round(conf, 2))