import numpy as np

from linalg.code_matrix import *

from abc import ABC, abstractmethod

class Decoder(ABC):

    def __init__(self, code_length: int, base_length: int, gf: GaluaField):
        self._code_length = code_length
        self._base_length = base_length
        self._exss_length = code_length - base_length
        self._gf = gf

        self._parity_check_matrix = build_parity_check_matrix(
            self._code_length, self._exss_length, gf
        )

        self._generator_matrix = build_generator_matrix(self._parity_check_matrix)

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
    def find_errors(self, words: np.ndarray): pass

    @abstractmethod
    def detect_and_correct(self, words: np.ndarray): pass

    @abstractmethod
    def find_erasures(self, words: np.ndarray): pass

    

    