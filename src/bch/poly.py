from typing import List
from .new_field import GF2m


class Polynomial:
    def __init__(self, coefficients: List[int], field: GF2m):
        self.field = field
        self.coeffs = self._trim(coefficients)

    def _trim(self, coeffs: List[int]) -> List[int]:
        while len(coeffs) > 1 and coeffs[-1] == 0:
            coeffs.pop()
        return coeffs if coeffs else [0]

    def degree(self) -> int:
        return len(self.coeffs) - 1

    def __repr__(self) -> str:
        if self.coeffs == [0]:
            return "0"

        terms = []
        for i, coef in enumerate(self.coeffs):
            if coef != 0:
                if i == 0:
                    terms.append(f"{coef}")
                elif i == 1:
                    terms.append(f"{coef}*x")
                else:
                    terms.append(f"{coef}*x^{i}")

        return " + ".join(reversed(terms)) if terms else "0"

    def __add__(self, other: 'Polynomial') -> 'Polynomial':
        max_len = max(len(self.coeffs), len(other.coeffs))
        result = [0] * max_len

        for i in range(len(self.coeffs)):
            result[i] = self.coeffs[i]

        for i in range(len(other.coeffs)):
            result[i] = self.field.add(result[i], other.coeffs[i])

        return Polynomial(result, self.field)

    def __sub__(self, other: 'Polynomial') -> 'Polynomial':
        return self.__add__(other)

    def __mul__(self, other: 'Polynomial') -> 'Polynomial':
        if self.coeffs == [0] or other.coeffs == [0]:
            return Polynomial([0], self.field)

        result_degree = self.degree() + other.degree()
        result = [0] * (result_degree + 1)

        for i, a in enumerate(self.coeffs):
            for j, b in enumerate(other.coeffs):
                prod = self.field.multiply(a, b)
                result[i + j] = self.field.add(result[i + j], prod)

        return Polynomial(result, self.field)

    def __truediv__(self, other: 'Polynomial') -> tuple['Polynomial', 'Polynomial']:
        return self.divmod(other)

    def divmod(self, divisor: 'Polynomial') -> tuple['Polynomial', 'Polynomial']:
        if divisor.coeffs == [0]:
            raise ZeroDivisionError("Деление многочлена на ноль")

        quotient = Polynomial([0], self.field)
        remainder = Polynomial(self.coeffs[:], self.field)

        divisor_degree = divisor.degree()
        divisor_leading_coef = divisor.coeffs[-1]

        while remainder.degree() >= divisor_degree and remainder.coeffs != [0]:
            # Степень текущего члена частного
            degree_diff = remainder.degree() - divisor_degree

            # Коэффициент текущего члена частного
            coef = self.field.divide(remainder.coeffs[-1], divisor_leading_coef)

            # Создаем одночлен
            term_coeffs = [0] * (degree_diff + 1)
            term_coeffs[degree_diff] = coef
            term = Polynomial(term_coeffs, self.field)

            # Обновляем частное и остаток
            quotient = quotient + term
            remainder = remainder - (divisor * term)

        return quotient, remainder

    def evaluate(self, x: int) -> int:
        result = 0
        x_power = 1  # x^i

        for coef in self.coeffs:
            term = self.field.multiply(coef, x_power)
            result = self.field.add(result, term)
            x_power = self.field.multiply(x_power, x)

        return result

    def scale(self, scalar: int) -> 'Polynomial':
        if scalar == 0:
            return Polynomial([0], self.field)

        result = [self.field.multiply(c, scalar) for c in self.coeffs]
        return Polynomial(result, self.field)

    @staticmethod
    def gcd(a: 'Polynomial', b: 'Polynomial') -> 'Polynomial':
        while b.coeffs != [0]:
            a, b = b, a.divmod(b)[1]
        return a

    @staticmethod
    def extended_gcd(a: 'Polynomial', b: 'Polynomial') -> tuple['Polynomial', 'Polynomial', 'Polynomial']:
        field = a.field

        # Инициализация
        old_r, r = a, b
        old_s, s = Polynomial([1], field), Polynomial([0], field)
        old_t, t = Polynomial([0], field), Polynomial([1], field)

        while r.coeffs != [0]:
            quotient, remainder = old_r.divmod(r)

            old_r, r = r, remainder
            old_s, s = s, old_s - quotient * s
            old_t, t = t, old_t - quotient * t

        # Нормализация (чтобы старший коэффициент gcd был равен 1)
        gcd = old_r
        if gcd.coeffs[-1] != 1:
            inv = field.inverse(gcd.coeffs[-1])
            gcd = gcd.scale(inv)
            old_s = old_s.scale(inv)
            old_t = old_t.scale(inv)

        return gcd, old_s, old_t

    def derivative(self) -> 'Polynomial':
        if self.degree() == 0:
            return Polynomial([0], self.field)

        result = []
        for i in range(1, len(self.coeffs)):
            if i % 2 == 1:  # В GF(2) коэффициент i обнуляется при четном i
                result.append(self.coeffs[i])
            else:
                result.append(0)

        return Polynomial(result if result else [0], self.field)
