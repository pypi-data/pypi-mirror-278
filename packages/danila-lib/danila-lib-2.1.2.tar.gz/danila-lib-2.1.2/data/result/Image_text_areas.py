from data.result.Class_text import Class_text

"""class contains dict with Rects list for each text_class"""
#class contains dict with Rects list for each text_class
class Image_text_areas:
    """class contains dict with Rects list for each text_class"""
    # makes dict {Class_text.number : [], Class_text.prod : [], Class_text.text : [], Class_text.year : []}
    def __init__(self):
        """makes dict {Class_text.number : [], Class_text.prod : [], Class_text.text : [], Class_text.year : []} """
        self.areas = dict(
            {
                        Class_text.number : [],
                        Class_text.prod : [],
                        Class_text.text : [],
                        Class_text.year : []
            }
        )

    # add text area to dict
    def add_area(self, text_area):
        """add text area to dict"""
        self.areas[text_area.class_im].append(text_area.rect)

    # add list of text areas
    def fill_in_with_areas(self, areas):
        """add list of text areas"""
        for area in areas:
            self.add_area(area)

    # delete all cases in which two areas are intersected
    def correct_intersections(self):
        """delete all cases in which two areas are intersected"""
        for class_im in self.areas:
            flag = True
            while (flag):
                flag = False
                for i in range(len(self.areas[class_im])):
                    for j in range(i+1, len(self.areas[class_im])):
                        if (self.areas[class_im][i].intersection(self.areas[class_im][j])) > 20:
                            flag = True
                            break
                    if flag:
                        break
                if (flag):
                    rect1 = self.areas[class_im][i]
                    rect2 = self.areas[class_im][j]
                    new_rect = rect1.union(rect2)
                    self.areas[class_im].remove(rect1)
                    self.areas[class_im].remove(rect2)
                    self.areas[class_im].append(new_rect)
    # changes Rects coordinates from cut_img to whole_img from rama Rect
    def explore_to_whole_image(self, rama_rect):
        """changes Rects coordinates from cut_img to whole_img"""
        for class_im in self.areas:
            for rect_text in self.areas[class_im]:
                new_xmin = rect_text.xmin + rama_rect.xmin
                new_xmax = rect_text.xmax + rama_rect.xmin
                new_ymin = rect_text.ymin + rama_rect.ymin
                new_ymax = rect_text.ymax + rama_rect.ymin
                rect_text.ymin = new_ymin
                rect_text.xmin = new_xmin
                rect_text.xmax = new_xmax
                rect_text.ymax = new_ymax

