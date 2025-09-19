from GaluaField import *

class GaluaElement:
    
    def __init__(self, gf: GaluaField, value: np.ndarray):
        self.__gf = gf
        self.__value = value

    @property
    def gf(self):
        return self.__gf
    
    @property
    def value(self):
        return self.__value
    
    def __add__(self, other):
        if self.gf == other.gf:
            return GaluaElement(self.gf, (self.value + other.value) % self.gf.chr) 
        else:
            raise ValueError
        
    def __sub__(self, other):
        if self.gf == other.gf:
            return GaluaElement(self.gf, (self.value - other.value) % self.gf.chr) 
        else:
            raise ValueError
    
    def __mul__(self, other):
        index_a = np.where(self.gf.values == self.value)[0]
        index_b = np.where(self.gf.values == other.value)[0]
        return GaluaElement(self.gf, self.gf.values[(index_a + index_b) % self.gf.pow])

    # def __mul_shft(self, a, b):
    #     index_a = np.where(self.gf.values == self.value)[0]
    #     index_b = np.where(self.gf.values == self.value)[0]
    #     return GaluaElement(self.gf, self.gf.values[(a + b) % self.gf.pow])

