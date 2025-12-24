from typing import List, Optional


class GF2m:
    "Спизженный класс для полей"

    PRIMITIVE_POLYNOMIALS = {
        2: [1, 1, 1],           # x^2 + x + 1
        3: [1, 0, 1, 1],        # x^3 + x + 1
        4: [1, 0, 0, 1, 1],     # x^4 + x + 1
        5: [1, 0, 0, 1, 0, 1],  # x^5 + x^2 + 1
        6: [1, 0, 0, 0, 0, 1, 1],  # x^6 + x + 1
        7: [1, 0, 0, 0, 0, 0, 1, 1],  # x^7 + x + 1
        8: [1, 0, 0, 0, 1, 1, 1, 0, 1],  # x^8 + x^4 + x^3 + x^2 + 1
    }

    def __init__(self, m: int, primitive_poly: Optional[List[int]] = None):
        self.m = m
        self.size = 2 ** m  # Количество элементов в поле

        # Примитивный многочлен
        if primitive_poly is None:
            if m not in self.PRIMITIVE_POLYNOMIALS:
                raise ValueError(f"Примитивный многочлен для GF(2^{m}) не определен")
            self.primitive_poly = self.PRIMITIVE_POLYNOMIALS[m]
        else:
            self.primitive_poly = primitive_poly

        # Таблицы для быстрого преобразования между представлениями
        self._build_tables()

    def _build_tables(self):
        self.exp_table = [0] * (self.size)  # alpha^i
        self.log_table = [0] * self.size    # обратная таблица

        # alpha^0 = 1
        self.exp_table[0] = 1
        self.log_table[1] = 0

        # Построение таблицы степеней alpha
        value = 1
        for i in range(1, self.size - 1):
            # Умножение на alpha (сдвиг влево)
            value <<= 1

            # Если вышли за границы поля, применяем редукцию
            if value & self.size:  # Проверка старшего бита
                value ^= self._poly_to_int(self.primitive_poly)

            self.exp_table[i] = value
            self.log_table[value] = i

    def _poly_to_int(self, poly: List[int]) -> int:
        result = 0
        for coef in poly:
            result = (result << 1) | coef
        return result

    def add(self, a: int, b: int) -> int:
        return a ^ b

    def multiply(self, a: int, b: int) -> int:
        if a == 0 or b == 0:
            return 0

        # Используем логарифмы: a * b = alpha^(log(a) + log(b))
        log_sum = (self.log_table[a] + self.log_table[b]) % (self.size - 1)
        return self.exp_table[log_sum]

    def divide(self, a: int, b: int) -> int:
        if b == 0:
            raise ZeroDivisionError("Деление на ноль в поле Галуа")
        if a == 0:
            return 0

        # Используем логарифмы: a / b = alpha^(log(a) - log(b))
        log_diff = (self.log_table[a] - self.log_table[b]) % (self.size - 1)
        return self.exp_table[log_diff]

    def power(self, a: int, n: int) -> int:
        if a == 0:
            return 0 if n > 0 else 1

        # Используем логарифмы: a^n = alpha^(n * log(a))
        log_result = (n * self.log_table[a]) % (self.size - 1)
        return self.exp_table[log_result]

    def inverse(self, a: int) -> int:
        if a == 0:
            raise ZeroDivisionError("Обратный элемент для нуля не существует")

        # a^(-1) = alpha^(-log(a)) = alpha^(q-1-log(a))
        log_inv = (self.size - 1 - self.log_table[a]) % (self.size - 1)
        return self.exp_table[log_inv]

    def alpha_power(self, i: int) -> int:
        if i < 0:
            i = i % (self.size - 1)
        return self.exp_table[i % (self.size - 1)]

    def log_alpha(self, a: int) -> int:
        if a == 0:
            raise ValueError("Логарифм нуля не определен")
        return self.log_table[a]
