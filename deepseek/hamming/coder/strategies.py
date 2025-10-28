import numpy as np
from accessify import private, protected
from abc import ABC, abstractmethod
from ..common import build_parity_check_matrix, build_generator_matrix


class CodingStrategy(ABC):
    """Strategy interface for coding algorithms"""
    
    @abstractmethod
    def code_words(self, words: np.ndarray, generator_matrix: np.ndarray, gf) -> np.ndarray:
        pass
    
    def get_parity_check_matrix(self, code_length: int, exss_length: int, gf) -> np.ndarray:
        """Common implementation for all strategies"""
        return build_parity_check_matrix(code_length, exss_length, gf)
    
    def get_generator_matrix(self, parity_check_matrix: np.ndarray, gf) -> np.ndarray:
        """Common implementation for all strategies"""
        return build_generator_matrix(parity_check_matrix, gf)


class ClassicCodingStrategy(CodingStrategy):
    
    @private
    def validate_input(self, words: np.ndarray, gf):
        """Private validation method"""
        if words.size == 0:
            raise ValueError("Input words cannot be empty")
        # Validate input is within radix range
        if not np.all(np.isin(words, range(gf.chr))):
            raise ValueError(f"Input contains values outside valid range for radix {gf.chr}")
    
    @protected
    def transform_input(self, words: np.ndarray) -> np.ndarray:
        """Protected method for input transformation"""
        return words.astype(np.int32)
    
    def code_words(self, words: np.ndarray, generator_matrix: np.ndarray, gf) -> np.ndarray:
        self.validate_input(words, gf)
        info_vectors = self.transform_input(words)
        
        codewords_numeric = (info_vectors @ generator_matrix) % gf.chr
        return codewords_numeric


class ShortenedCodingStrategy(CodingStrategy):
    
    def code_words(self, words: np.ndarray, generator_matrix: np.ndarray, gf) -> np.ndarray:
        """Shortened coding uses the same matrix operations as classic"""
        info_vectors = words.astype(np.int32)
        codewords_numeric = (info_vectors @ generator_matrix) % gf.chr
        return codewords_numeric


class ExtendedCodingStrategy(CodingStrategy):
    
    @private
    def add_parity_symbol(self, codewords: np.ndarray, gf) -> np.ndarray:
        """Private method to extend codewords with parity symbol"""
        extended = np.zeros(
            (codewords.shape[0], codewords.shape[1] + 1), 
            dtype=np.int32
        )
        for i in range(codewords.shape[0]):
            extended[i, :-1] = codewords[i]
            # Calculate parity symbol (sum modulo radix)
            extended[i, -1] = np.sum(codewords[i]) % gf.chr
        return extended
    
    def code_words(self, words: np.ndarray, generator_matrix: np.ndarray, gf) -> np.ndarray:
        info_vectors = words.astype(np.int32)
        codewords_numeric = (info_vectors @ generator_matrix) % gf.chr
        extended_codewords = self.add_parity_symbol(codewords_numeric, gf)
        return extended_codewords