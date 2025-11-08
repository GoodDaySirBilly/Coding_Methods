import numpy as np

from .Coder import *

class ClassicCoder(Coder):

    def __init__(self,
        code_length: int, base_length: int, gf: GaluaField
    ):
        super().__init__(code_length, base_length, gf)

    def code_words(self, words):
        
        return words @ self.generator_matrix % self.gf.chr