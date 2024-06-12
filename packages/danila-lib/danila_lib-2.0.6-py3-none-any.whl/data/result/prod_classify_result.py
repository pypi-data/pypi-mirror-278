from enum import Enum


class Prod_classify_result(Enum):
    wrong = 0
    right = 1
    two_prods = 2
    no_prod = 3