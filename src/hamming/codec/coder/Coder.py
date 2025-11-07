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

        self.generator_matrix = build_generator_matrix(self.H)

    @property 
    def code_length(self):
        return self.code_length

    @property 
    def base_length(self):
        return self.base_length

    @property
    def exss_length(self):
        return self.exss_length

    @property 
    def parity_check_matrix(self):
        return self.parity_check_matrix
    
    @property
    def generator_matrix(self):
        return self.generator_matrix
    
    @property 
    def gf(self):
        return self.gf

    
    @abstractmethod
    def code_words(self, words: np.ndarray): pass

    