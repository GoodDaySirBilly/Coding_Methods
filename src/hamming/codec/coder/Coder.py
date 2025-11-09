import numpy as np

from linalg.code_matrix import *

from abc import ABC, abstractmethod

class Coder(ABC):

    def __init__(self, code_length: int, base_length: int, gf: GaluaField):
        self.code_length = code_length
        self.base_length = base_length
        self.exss_length = code_length - base_length
        self.type = type
        self.gf = gf

        self.parity_check_matrix = build_parity_check_matrix(
            self.code_length, self.exss_length, gf
        )

        self.generator_matrix = build_generator_matrix(self.parity_check_matrix)

    @property 
    def code_length(self):
        return self._code_length

    @property 
    def base_length(self):
        return self._base_length

    @property
    def exss_length(self):
        return self._exss_length

    @property 
    def parity_check_matrix(self):
        return self._parity_check_matrix
    
    @property
    def generator_matrix(self):
        return self._generator_matrix
    
    @property 
    def gf(self):
        return self._gf
    
    @code_length.setter
    def code_length(self, value):
        self._code_length = value

    @base_length.setter
    def base_length(self, value):
        self._base_length = value

    @exss_length.setter
    def exss_length(self, value):
        self._exss_length = value

    @parity_check_matrix.setter
    def parity_check_matrix(self, value):
        self._parity_check_matrix = value

    @generator_matrix.setter
    def generator_matrix(self, value):
        self._generator_matrix = value

    @gf.setter
    def gf(self, value):
        self._gf = value

    
    @abstractmethod
    def code_words(self, words: np.ndarray): pass

    