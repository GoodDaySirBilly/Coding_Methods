from .GaluaField import *

class GaluaElement:
    
    def __init__(self, gf: GaluaField, value: np.ndarray):

        if type(gf) == GaluaField:
            self.__gf = gf
        else:
            raise ValueError("Incorrect gf")

        if (type(value) == np.ndarray) and (value.dtype == 'int32') and \
            np.all(value >= 0) and np.all(value < gf.chr) and (value.size == gf.orp):
            self.__value = value
        else:
            raise ValueError("Incorrect value")

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
        i = self.find_index()
        j = other.find_index()

        z = 1 if i + j > self.gf.pow else 0

        value = self.gf.values[(i + j - 1) % self.gf.pow + z]

        if i == 0 or j == 0:
            value = self.gf.values[0]

        return GaluaElement(self.gf, value.reshape(self.gf.orp))
    
    def __floordiv__(self, other):
        i = self.find_index()
        j = other.find_index()
        
        if j == 0:
            raise ZeroDivisionError("Field does not has zero divisors")
        elif j == 1:
            return self * GaluaElement(self.gf, self.gf.values[1].reshape(self.gf.orp))
        else:
            return self * GaluaElement(self.gf, self.gf.values[1 + self.gf.pow - j].reshape(self.gf.orp))
    
    def __eq__(self, other):

        return (self.gf == other.gf) and (np.all(self.value == other.value))

    def __str__(self):
        i = self.find_index()[0]
        return f"{'v^'+str(i-1) if i>1 else i} : " + str(self.value)

    def find_index(self):
        return np.where(np.all(self.gf.values == self.value, axis=1))[0]

    # def __mul_shft(self, a, b):
    #     i = np.where(self.gf.values == self.value)[0]
    #     j = np.where(self.gf.values == self.value)[0]
    #     return GaluaElement(self.gf, self.gf.values[(a + b) % self.gf.pow])

