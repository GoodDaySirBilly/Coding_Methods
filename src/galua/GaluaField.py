import numpy as np

class GaluaField:
    
    def __init__(self, chr: int, orp: int, pol: list[int]):
        
        if (not isinstance(chr, int)) or (not isinstance(orp, int)):
            raise ValueError("Incorrect datatype")

        if chr > 0:
            self.__chr = chr
        else:
            raise ValueError("Incorrect chr")


        if orp > 0:
            self.__orp = orp
        else:
            raise ValueError("Incorrect orp")

        
        if all([i>=0 for i in pol]) and all([i<chr for i in pol]) \
            and (len(pol) == orp + 1):
            self.__pol = np.array(pol)
            self.__local_dtype = self.pol.dtype
        else:
            raise ValueError("Incorrect pol")
        
        self.__pow = int(np.power(self.__chr, self.__orp))
        self.__values = np.zeros((self.__pow, self.__orp), dtype=self.local_dtype)

        self.__calculate_values()
        
    @property
    def local_dtype(self):
        return self.__local_dtype

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
    def pow(self):
        return self.__pow
    
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
        result = f"GF({self.pow} = {self.chr}^{self.orp})\n"
        for i, row in enumerate(self.values, 0):
            result += f'{"v^"+str(i-1) if i>1 else i}: {row}\n'
        return result

    @staticmethod
    def __modinv(value: int, modulus: int) -> int:
        # Extended Euclidean Algorithm
        value = value % modulus

        if value == 0:
            raise ValueError("Polynomial leading coefficient not invertible modulo chr")

        coefficient_prev, coefficient_curr = 0, 1
        remainder_prev, remainder_curr = modulus, value

        while remainder_curr != 0:

            quotient = remainder_prev // remainder_curr

            coefficient_prev, coefficient_curr = (coefficient_curr, coefficient_prev - quotient * coefficient_curr)
            remainder_prev, remainder_curr = (remainder_curr, remainder_prev - quotient * remainder_curr)

        if remainder_prev != 1:

            raise ValueError("chr must be prime and polynomial leading coefficient invertible")

        return coefficient_prev % modulus
    
    def __calculate_values(self):

        characteristic = self.chr
        extension_degree = self.orp

        # normalize polynomial to be monic
        modulus_polynomial = self.pol % characteristic
        leading_coefficient = modulus_polynomial[-1] % characteristic
        inverse_leading_coefficient = self.__modinv(leading_coefficient, characteristic)

        if leading_coefficient != 1:
            inverse_leading_coefficient = self.__modinv(leading_coefficient, characteristic)
        else:
            inverse_leading_coefficient = 1

        # reduction rule
        normalized_lower_coefficients = (modulus_polynomial[:extension_degree] * inverse_leading_coefficient) % characteristic
        reduction_coefficients = (-normalized_lower_coefficients) % characteristic  # vector length extension_degree

        values_table = np.zeros((self.pow, extension_degree), dtype=self.local_dtype)

        # zero element
        values_table[0, :] = 0

        #x^0
        current_element_coeffs = np.zeros(extension_degree, dtype=self.local_dtype)
        current_element_coeffs[0] = 1

        values_table[1, :] = current_element_coeffs

        # generate powers of x
        for _ in range(2, self.__pow):
            overflow_coefficient = int(current_element_coeffs[-1])
            # shift
            shifted_coeffs = np.zeros(extension_degree, dtype=self.local_dtype)
            shifted_coeffs[1:] = current_element_coeffs[:-1]

            if overflow_coefficient != 0:
                # reduce power overflow
                shifted_coeffs = (shifted_coeffs + (overflow_coefficient * reduction_coefficients) % characteristic) % characteristic

            current_element_coeffs = shifted_coeffs
            values_table[_ , :] = current_element_coeffs

        self.__values = values_table

