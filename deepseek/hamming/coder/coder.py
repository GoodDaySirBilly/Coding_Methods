import numpy as np
from accessify import private
from .strategies import ClassicCodingStrategy, CodingStrategy
from ..common import syndrom


class Coder:
    """
    Context class that uses a CodingStrategy with access control
    """
    
    def __init__(self, code_length: int, base_length: int, gf, strategy: CodingStrategy = None):
        self.code_length = code_length
        self.base_length = base_length
        self.gf = gf
        self.exss_length = code_length - base_length
        
        self.strategy = strategy or ClassicCodingStrategy()
        self._build_matrices()
    
    @private
    def _build_matrices(self):
        """Private method to build matrices using the current strategy"""
        self.parity_check_matrix = self.strategy.get_parity_check_matrix(
            self.code_length, self.exss_length, self.gf
        )
        self.generator_matrix = self.strategy.get_generator_matrix(
            self.parity_check_matrix, self.gf
        )
    
    def code_words(self, words: np.ndarray) -> np.ndarray:
        """Public method - main coding interface"""
        return self.strategy.code_words(words, self.generator_matrix, self.gf)
    
    def set_strategy(self, strategy: CodingStrategy):
        """Allow changing strategy at runtime"""
        self.strategy = strategy
        self._build_matrices()
    
    # Property accessors for read-only access
    @property
    def parity_check_matrix_prop(self) -> np.ndarray:
        return self.parity_check_matrix.copy()
    
    @property
    def generator_matrix_prop(self) -> np.ndarray:
        return self.generator_matrix.copy()
    
    def calculate_syndrome(self, code_word: np.ndarray) -> np.ndarray:
        """Use shared syndrome function"""
        return syndrom(code_word, self.parity_check_matrix, self.gf)