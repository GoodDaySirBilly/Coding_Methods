import numpy as np

from .Coder import *

class ClassicCoder(Coder):

    def __init__(self,
        code_length: int, base_length: int, gf: GaluaField
    ):
        super().__init__(code_length, base_length, gf)

        self.extend_code_length = code_length + 1

    @property
    def extend_code_length(self):
        return self.extend_code_length
        

    def code_words(self, words):
        return super().code_words(words)