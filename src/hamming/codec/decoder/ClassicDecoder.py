import numpy as np

from .Decoder import *

class ClassicDecoder(Decoder):

    def __init__(self,
        code_length: int, base_length: int, gf: GaluaField
    ):
        super().__init__(code_length, base_length, gf)


    def find_errors(self, words: np.ndarray):
        return super().find_errors(words)


    def detect_and_correct(self, words: np.ndarray): 
        return super().detect_and_correct(words)


    def find_erasures(self, words: np.ndarray):
        return super().find_erasures(words)