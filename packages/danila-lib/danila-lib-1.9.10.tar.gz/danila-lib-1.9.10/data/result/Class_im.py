from enum import Enum
class Class_detail(Enum):
    rama = 0
    vagon = 1

class Class_detail_result:
    def __init__(self, class_detail, conf):
        self.class_detail = class_detail
        self.conf = conf