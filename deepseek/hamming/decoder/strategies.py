import numpy as np
from accessify import private
from abc import ABC, abstractmethod
from ..common import build_parity_check_matrix, syndrom


class DecodingStrategy(ABC):
    """Strategy interface for decoding algorithms"""
    
    def __init__(self, code_length: int, base_length: int, gf):
        self.code_length = code_length
        self.base_length = base_length
        self.gf = gf
        self.exss_length = code_length - base_length
        self.H = build_parity_check_matrix(code_length, self.exss_length, gf)
    
    @abstractmethod
    def decode_words(self, coded_words: np.ndarray) -> np.ndarray:
        pass
    
    def calculate_syndrome(self, code_word: np.ndarray) -> np.ndarray:
        """Reuse the same syndrome function as encoder"""
        return syndrom(code_word, self.H, self.gf)