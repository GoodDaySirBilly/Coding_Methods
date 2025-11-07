import numpy as np

from .Coder import *

class ClassicCoder(Coder):

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
    

    def code_words(self, words):
        return super().code_words(words)