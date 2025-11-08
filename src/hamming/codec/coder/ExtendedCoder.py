import numpy as np

from .Coder import *

class ClassicCoder(Coder):

    def __init__(self,
        code_length: int, base_length: int, gf: GaluaField
    ):
        super().__init__(code_length, base_length, gf)

        self.extend_code_length = code_length + 1

        self.extend_parity = np.copy(self.parity_check_matrix)

        rows, cols = self.extend_parity.shape

        self.extend_parity = np.concat([
            np.zeros([rows, 1]), self.extend_parity
        ], axis=1)

        self.extend_parity = np.concat([
            np.ones([1, cols + 1]), self.extend_parity
        ], axis=0)

        self.generator_matrix = build_generator_matrix(
            self.extend_parity
        )

    @property
    def extend_code_length(self):
        return self.extend_code_length
        

    def code_words(self, words):

        return words @ self.generator_matrix % self.gf.chr