import numpy as np

from .Coder import *

class ShortenedCoder(Coder):

    def __init__(self,
        code_length: int, base_length: int, gf: GaluaField,
        short_code_length: int, short_base_length: int
    ):
        super().__init__(code_length, base_length, gf)

        self.short_code_length = short_code_length
        self.short_base_length = short_base_length

        if short_code_length >= code_length or \
            short_base_length > base_length:
            raise ValueError("short length >= common lengh")
        
        self.parity_check_matrix = self.parity_check_matrix[
            :, short_code_length:
        ]

        self.generator_matrix = self.generator_matrix[
            short_code_length:, short_code_length:
        ]


        HGt = self.parity_check_matrix @ self.generator_matrix.T % self.gf.chr

        if not np.all(HGt == 0):
            raise ValueError("matrix ortoghonal error")
    

    def code_words(self, words):
        return words @ self.generator_matrix % self.gf.chr