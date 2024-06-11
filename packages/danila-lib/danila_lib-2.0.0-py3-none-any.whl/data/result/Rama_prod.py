from enum import Enum


class Rama_Prod(Enum):
    bejickaya = 0
    ruzhimmash = 1
    no_rama = 2

class Rama_Prod_Conf:

    def __init__(self, rama_prod, conf):
        self.rama_prod = rama_prod
        self.conf = conf