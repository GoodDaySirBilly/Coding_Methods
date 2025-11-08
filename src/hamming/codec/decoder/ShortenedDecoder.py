import numpy as np

from .Decoder import *

class ShortenedDecoder(Decoder):

    def __init__(self,
        code_length: int, base_length: int, gf: GaluaField,
        short_code_length: int, short_base_length: int
    ):
        super().__init__(code_length, base_length, gf)

        self.short_code_length = short_code_length
        self.short_base_length = short_base_length

    @property 
    def short_code_length(self):
        return self.short_code_length

    @property 
    def short_base_length(self):
        return self.short_base_length
    

    def find_errors(self, words: np.ndarray):
        return super().find_errors(words)


    def detect_and_correct(self, words: np.ndarray): 
        return super().detect_and_correct(words)


    def find_erasures(self, words: np.ndarray):
        return super().find_erasures(words)