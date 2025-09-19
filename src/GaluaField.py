import numpy as np
import matplotlib.pyplot as plot

class GaluaField:
    
    def __init__(self, chr: int, orp: int, pol: np.array):
        
        if (type(chr) == int) and (chr > 0):
            self.__chr = chr
        else:
            raise ValueError("Incorrect chr")


        if (type(orp) == int) and (orp > 0):
            self.__orp = orp
        else:
            raise ValueError("Incorrect orp")

        
        if (type(pol) == np.ndarray) and (pol.dtype == 'int64') and \
            np.all(pol >= 0) and np.all(pol < chr) and (pol.size == orp + 1):
            self.__pol = pol
        else:
            raise ValueError("Incorrect pol")
        
        self.__values = np.zeros((np.pow(self.__chr, self.__orp), self.__orp))

        self.__calculate_values()
        
    @property
    def chr(self):
        return self.__chr
    
    @property
    def orp(self):
        return self.__orp
    
    @property
    def pol(self):
        return self.__pol
    
    @property
    def values(self):
        return self.__values
    
        
    def __eq__(self, other):
        result = True

        result = result and (self.orp == other.orp)
        result = result and (self.chr == other.chr)
        result = result and all(self.pol == other.pol)
        
        return result
    
    
    def __ne__(self, other):
        result = False

        result = result or (self.orp != other.orp)
        result = result or (self.chr != other.chr)
        result = result or any(self.pol != other.pol)
        
        return result


    def __str__(self):
        return f"GF({np.pow(self.chr, self.orp)} = {self.chr}^{self.orp})"
    
    def __calculate_values():
        pass


class GaluaFieldElement:
    
    def __init__(self, gf: GaluaField, value: int):
        self.__gf = gf
        self.__value = value % gf.chr if type(value) == int else -1
        if self.__value == -1:
            raise ValueError

    @property
    def gf(self):
        return self.__gf
    
    @property
    def value(self):
        return self.__value
    
    def __add__(self, other):
        pass 
    
    def __mul__(self, other):
        pass