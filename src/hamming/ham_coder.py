import numpy as np

from code_matrix import *
from ..galua import GaluaElement

class Hamming:

    code_types = [
        "classic",
        "shortened",
        "extended"
    ]

    def __init__(self,
        code_length: int,
        base_length: int,
        gf: GaluaField.GaluaField,
        type = "classic"
    ):
        self.code_length = code_length
        self.base_length = base_length
        self.exss_length = code_length - code_length
        self.type = type

        self.H = build_parity_check_matrix(self.code_length, self.exss_length, gf)
        self.G = build_generator_matrix(self.H)

    def code_words(self,
        words: np.ndarray[np._str, np._str]
    ) -> np.ndarray[np._str, np._str]:
        
        match self.type:
            case "classic":
                return self.__classic_code(words)
            case "shortened":
                pass
            case "extended":
                pass
            case _:
                pass


    def __classic_code(self,
        words: np.ndarray[np._str, np._str]
    ) -> np.ndarray[np._str, np._str]:
        info_vectors = words.copy().astype(np.int32)

        codewords_numeric = (info_vectors @ self.G) % self.gf.chr

        codewords_str = codewords_numeric.copy().astype(np._str)

        return codewords_str


    def __shortened_code(self,
        words: np.ndarray[np._str, np._str]
    ) -> np.ndarray[np._str, np._str]:
        return self.__classic_code(words)

    
    def __extended_code(self,
        words: np.ndarray[np._str, np._str]
    ) -> np.ndarray[np._str, np._str]:
        
        info_vectors = words.copy().astype(np.int32)

        codewords_numeric = (info_vectors @ self.G) % self.gf.chr
        pre_code_shape = codewords_numeric.shape

        extended_matrix_numeric = np.zeros([
            pre_code_shape[0] + 1, 
            pre_code_shape[1] + 1
        ])

        extended_matrix_numeric[0, :] = np.ones([1, pre_code_shape[1] + 1])

        extended_matrix_numeric[1:, :] = codewords_numeric

        extended_matrix_numeric = extended_matrix_numeric.copy().astype(np._str)

        return extended_matrix_numeric




    