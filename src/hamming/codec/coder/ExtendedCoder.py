import numpy as np

from .Coder import *

class ExtendedCoder(Coder):

    def __init__(self,
        code_length: int, base_length: int, gf: GaluaField
    ):
        super().__init__(code_length, base_length, gf)

        self.extend_parity = np.copy(self.parity_check_matrix)

        rows, cols = self.extend_parity.shape

        self.extend_parity = np.concatenate([
            self.extend_parity, np.zeros([rows, 1], dtype=int), 
        ], axis=1)

        self.extend_parity = np.concatenate([
            np.ones([1, cols + 1], dtype=int), self.extend_parity
        ], axis=0)
        

    def code_words(self, words):

        result = words @ self.generator_matrix % self.gf.chr
        even_bits = np.sum(result, axis=1) % self.gf.chr
        even_bits = even_bits[:, np.newaxis]

        result = np.concatenate([result, even_bits], axis=1)

        return result