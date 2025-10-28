from abc import ABC, abstractmethod

class Coder(ABC):
    def __init__(self, code_length, base_length):
        self.code_length = code_length
        self.base_length = base_length
    
    @abstractmethod
    def code_word(self):
        pass
    
    @abstractmethod
    def code_word_array(self):
        pass

