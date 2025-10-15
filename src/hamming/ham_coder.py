import numpy as np

from code_matrix import *

class Hamming:

    code_types = [
        "classic",
        "shortened",
        "extended"
    ]

    def __init__(self,
        code_length: int,
        base_length: int,
        type = "classic"
    ):
        self.code_length = code_length
        self.base_length = base_length
        self.type = type

        

    