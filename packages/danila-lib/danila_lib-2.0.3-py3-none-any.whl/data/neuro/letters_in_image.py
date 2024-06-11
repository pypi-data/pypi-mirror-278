from data.result.word_compare_result import Word_compare_result


class Rect:
    # прочитать из json результата йоло

    @staticmethod
    def get_rect_from_yolo_json(yolo_json):
        xmin = int(float(yolo_json['xmin']))
        xmax = int(float(yolo_json['xmax']))
        ymin = int(float(yolo_json['ymin']))
        ymax = int(float(yolo_json['ymax']))
        rect = Rect(xmin, xmax, ymin, ymax)
        return rect

    def __init__(self, xmin=0, xmax=0, ymin=0, ymax=0):
        self.xmin = xmin
        self.xmax = xmax
        self.ymin = ymin
        self.ymax = ymax

    # Найти IOU между этим прямоугольником и другим, данным в объекте
    def IoU(self, rect):
        def IOU(xmin, xmax, ymin, ymax, xmin_t, xmax_t, ymin_t, ymax_t):
            I = 0
            U = 0
            xmin_U = min(xmin, xmin_t)
            xmax_U = max(xmax, xmax_t)
            ymin_U = min(ymin, ymin_t)
            ymax_U = max(ymax, ymax_t)
            h = ymax_U - ymin_U
            w = xmax_U - xmin_U
            for i in range(xmin_U, xmax_U):
                for j in range(ymin_U, ymax_U):
                    flag = ((i <= xmax) and (i >= xmin) and (j <= ymax) and (j >= ymin))
                    flag_t = ((i <= xmax_t) and (i >= xmin_t) and (j <= ymax_t) and (j >= ymin_t))
                    if (flag and flag_t):
                        I += 1
                    if (flag or flag_t):
                        U += 1
            resultat = I / float(U)
            return resultat
        return IOU(self.xmin, self.xmax, self.ymin, self.ymax,
                   rect.xmin, rect.xmax, rect.ymin, rect.ymax)

    def __str__(self):
        res = ('xmin = ' + str(self.xmin) + ', xmax = ' + str(self.xmax) + ', ymin = ' + str(self.ymin) +
               ', ymax = ' + str(self.ymax))
        return res

    def intersection(self, rect):
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
        new_xmin = min(self.xmin, rect.xmin)
        new_ymin = min(self.ymin, rect.ymin)
        new_xmax = max(self.xmax, rect.xmax)
        new_ymax = max(self.ymax, rect.ymax)
        return Rect(new_xmin, new_xmax, new_ymin, new_ymax)

    def sort_rects_for_w_min(self, rect):
        if (self.xmax - self.xmin) < (rect.xmax - rect.xmin):
            return self, rect
        else:
            return rect, self

    def equal_x_for_percent(self, rect, percent):
        min_rect, max_rect = self.sort_rects_for_w_min(rect)
        x_intersect = min(max_rect.xmax - min_rect.xmin, min_rect.xmax - max_rect.xmin)
        if x_intersect < 0:
            x_intersect = 0
        wmin = min_rect.xmax - min_rect.xmin
        cur_percent = x_intersect / float(wmin)
        return (cur_percent > percent)

class Yolo_label_Rect:

    @staticmethod
    def build_from_2D_array(data, h, w):
        return Yolo_label_Rect(data[1], data[3], data[2], data[4], h, w)

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


class Letter_In_Image:
    def __init__(self, letter, rect = None, confidence=0.0):
        self.letter = letter
        self.rect = rect
        self.confidence = float(confidence)


    @staticmethod
    def get_letter_in_image_from_yolo_json(letter_json):
        return Letter_In_Image(letter_json['name'], Rect.get_rect_from_yolo_json(letter_json), letter_json['confidence'])

    def __eq__(self, other):
        return (other is Letter_In_Image) & (self.letter == other.letter)

    def __hash__(self):
        return hash(self.letter)

    def __str__(self):
        res_dict = {'letter' : self.letter, 'xmin' : self.rect.xmin, 'xmax' : self.rect.xmax, 'ymin' : self.rect.ymin, 'ymax' : self.rect.ymax, 'confidence' : self.confidence}
        return str(res_dict)


class Letters_In_Image:
    def __init__(self):
        self.letters = []



    @staticmethod
    def compare(letters1, letters2):
        if len(letters1.letters) == 0:
            return Word_compare_result(0)
        else:
            let1 = letters1.make_word()
            let2 = letters2.make_word()
            if let1 == let2:
                return Word_compare_result(3)
            count = 0
            for l in let1:
                if let2.find(l) > -1:
                    count += 1
            per_cent = count / float(len(let2))
            return Word_compare_result(1) if per_cent < 0.5 else Word_compare_result(2)


    @staticmethod
    def get_letters_in_image_from_yolo_json(letters_json):
        letters_in_image = Letters_In_Image()
        for letter_json in letters_json:
            letters_in_image.letters.append(Letter_In_Image.get_letter_in_image_from_yolo_json(letter_json))
        return letters_in_image

    def sort_letters(self):
        self.letters.sort(key = lambda letter_in_image: letter_in_image.rect.xmin)

    def delete_intersections_iter(self):
        new_letters = []
        i = 0
        while i < len(self.letters) - 1:
            IoU = self.letters[i].rect.IoU(self.letters[i+1].rect)
            if IoU > 0.5:
                new_letter = self.letters[i] if self.letters[i].confidence > self.letters[i + 1].confidence else self.letters[i + 1]
                i += 2
            else:
                new_letter = self.letters[i]
                i += 1
            new_letters.append(new_letter)
        if (i == len(self.letters) - 1):
            new_letters.append(self.letters[i])
        self.letters = new_letters

    def find_x_intersection(self):
        otvet_index_1 = 0
        otvet_index_2 = 0
        index1 = 0
        flag = False
        while not(flag) and (index1 < len(self.letters) - 1):
            index2 = index1 + 1
            while not(flag) and (index2 < len(self.letters)):
                if self.letters[index1].rect.equal_x_for_percent(self.letters[index2].rect, 0.6):
                    flag = True
                    otvet_index_1 = index1
                    otvet_index_2 = index2
                index2 += 1
            index1 += 1
        return (flag, otvet_index_1, otvet_index_2)

    def delete_intersections(self):
        has_intersections_flag = self.has_intersections()
        while has_intersections_flag:
            self.delete_intersections_iter()
            has_intersections_flag = self.has_intersections()

    def has_intersections(self):
        index1 = 0
        flag = False
        while not (flag) and (index1 < len(self.letters) - 1):
            index2 = index1 + 1
            while not (flag) and (index2 < len(self.letters)):
                if self.letters[index1].rect.IoU(self.letters[index2].rect) > 0.5:
                    flag = True
                index2 += 1
            index1 += 1
        return flag



    def delete_x_intersections(self):
        (flag, index1, index2) = self.find_x_intersection()
        while flag:
            if flag:
                if (self.letters[index1].rect.xmax - self.letters[index1].rect.xmin) < (self.letters[index2].rect.xmax - self.letters[index2].rect.xmin):
                    self.letters.remove(self.letters[index1])
                else:
                    self.letters.remove(self.letters[index2])
            (flag, index1, index2) = self.find_x_intersection()

    def make_word(self):
        if (len(self.letters) == 0):
            return '_'
        else:
            res = ''
            for letter in self.letters:
                res += letter.letter
            return res

    def get_avg_conf(self):
        sum_conf = 0.0
        count_conf = 0
        for letter in self.letters:
            sum_conf = sum_conf + letter.confidence
            count_conf += 1
        if count_conf==0:
            res = 0.0
        else:
            res = sum_conf / count_conf
        return res

    def __str__(self):
        res = ''
        for letter_in_image in self.letters:
            res = res + letter_in_image.__str__() + '\n'
        return res

