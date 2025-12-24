from typing import List, Optional, Tuple
from .new_field import GF2m
from .poly import Polynomial
from .ronaldo import berlekamp_massey, compute_syndromes


class BCHDecoder:
    def __init__(self, n: int, k: int, t: int, m: int,
                 primitive_poly: Optional[List[int]] = None,
                 first_consecutive_root: int = 0):
        self.n = n
        self.k = k
        self.t = t
        self.m = m
        self.first_root = first_consecutive_root

        # Создание поля Галуа
        self.field = GF2m(m, primitive_poly)

        # Проверка корректности параметров
        if n > self.field.size - 1:
            raise ValueError(f"Длина кода n={n} превышает максимальную для GF(2^{m})")

    def decode(self, received: List[int], algorithm: str = 'berlekamp-massey') -> Tuple[List[int], int]:
        if len(received) != self.n:
            raise ValueError(f"Длина принятого слова {len(received)} не совпадает с n={self.n}")

        # Шаг 1: Вычисление синдромов
        syndromes = self._compute_syndromes(received)
        # print(f'Вычисленные синдромы: {syndromes}')

        # Проверка наличия ошибок
        if all(s == 0 for s in syndromes):
            # Ошибок нет
            return received[:], 0

        # Шаг 2: Нахождение многочлена локаторов ошибок
        if algorithm == 'berlekamp-massey':
            Lambda = berlekamp_massey(syndromes, self.field)

        # Шаг 3: Нахождение позиций ошибок
        error_positions = self._chien_search(Lambda)
        print(f'Вычисленные позиции ошибок {error_positions}')

        # Проверка количества найденных ошибок
        num_errors = len(error_positions)
        if num_errors > self.t:
            raise ValueError(f"Обнаружено {num_errors} ошибок, но код может исправить только {self.t}")


        # Шаг 4: Исправление ошибок
        decoded = received[:]
        for pos in error_positions:
            decoded[pos] = 1 - decoded[pos]  # Инверсия бита (для двоичного кода)

        return decoded, num_errors

    def _compute_syndromes(self, received: List[int]) -> List[int]:
        """
        Вычисление синдромов.

        Синдромы S_i = R(alpha^i) для i = first_root, first_root+1, ..., first_root+2t-1
        """
        alpha_powers = list(range(self.first_root, self.first_root + 2 * self.t))
        return compute_syndromes(received, alpha_powers, self.field, 2 * self.t)

    def _chien_search(self, Lambda: Polynomial) -> List[int]:
        """
        Если Lambda(alpha^{-i}) = 0, то ошибка в позиции i.

        """
        error_positions = []

        # Проверяем все возможные позиции
        for i in range(self.n):
            # Вычисляем alpha^{-i}
            alpha_inv_i = self.field.alpha_power(-i)

            # Проверяем, является ли alpha^{-i} корнем Lambda(x)
            value = Lambda.evaluate(alpha_inv_i)

            if value == 0:
                error_positions.append(i)

        return error_positions

    def get_info(self) -> str:
        """Получение информации о декодере."""
        return f"""BCH({self.n}, {self.k}, {self.t})
Поле: GF(2^{self.m})
Корректирующая способность: {self.t} ошибок
"""
