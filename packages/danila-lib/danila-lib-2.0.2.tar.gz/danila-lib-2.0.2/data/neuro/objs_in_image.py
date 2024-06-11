from data.neuro.letters_in_image import Rect
from data.result.prod_classify_result import Prod_classify_result


class Prod_In_Image:
    def __init__(self, obj, rect = None, confidence=0.0):
        self.obj = obj
        self.rect = rect
        self.confidence = float(confidence)


    @staticmethod
    def get_obj_in_image_from_yolo_json(letter_json):
        return Prod_In_Image(letter_json['name'], Rect.get_rect_from_yolo_json(letter_json), letter_json['confidence'])

    def __eq__(self, other):
        return (other is Prod_In_Image) & (self.obj == other.obj)

    def __hash__(self):
        return hash(self.obj)

    def __str__(self):
        res_dict = {'obj' : self.obj, 'xmin' : self.rect.xmin, 'xmax' : self.rect.xmax, 'ymin' : self.rect.ymin, 'ymax' : self.rect.ymax, 'confidence' : self.confidence}
        return str(res_dict)


class Objs_In_Image:
    def __init__(self):
        self.objs = []

    def get_max_conf(self):
        max_conf = self.objs[0].confidence
        for prod_in_image in self.objs:
            if prod_in_image.confidence > max_conf:
                max_conf = prod_in_image.confidence
        return max_conf

    @staticmethod
    def get_objs_in_image_from_yolo_json(objs_json):
        objs_in_image = Objs_In_Image()
        for obj_json in objs_json:
            objs_in_image.objs.append(Prod_In_Image.get_obj_in_image_from_yolo_json(obj_json))
        return objs_in_image

    def delete_intersections(self):
        new_objs = []
        i = 0
        while i < len(self.objs) - 1:
            IoU = self.objs[i].rect.IoU(self.objs[i+1].rect)
            if IoU > 0.5:
                new_obj = self.objs[i] if self.objs[i].confidence > self.objs[i + 1].confidence else self.objs[i + 1]
                i += 2
            else:
                new_obj = self.objs[i]
                i += 1
            new_objs.append(new_obj)
        if (i == len(self.objs) - 1):
            new_objs.append(self.objs[i])
        self.objs = new_objs

    def __str__(self):
        res = ''
        for obj_in_image in self.objs:
            res = res + obj_in_image.__str__() + '\n'
        return res

    @staticmethod
    def compare_prods(image_objs, label_objs):
        b_list_r = any(obj.obj == 'bejickaya' for obj in image_objs.objs)
        r_list_r = any(obj.obj == 'ruzhimmash' for obj in image_objs.objs)
        b_list_l = any(obj.obj == 'bejickaya' for obj in label_objs.objs)
        r_list_l = any(obj.obj == 'ruzhimmash' for obj in image_objs.objs)
        if (b_list_r == False) and (r_list_r == False):
            return Prod_classify_result(3)
        else:
            if b_list_r and r_list_r:
                return Prod_classify_result(2)
            else:
                if b_list_r:
                    if b_list_l:
                        return Prod_classify_result.right
                    else:
                        return Prod_classify_result.wrong
                else:
                    if r_list_l:
                        return Prod_classify_result.right
                    else:
                        return Prod_classify_result.wrong

