from typing import List
from .new_field import GF2m
from .poly import Polynomial

def berlekamp_massey(syndromes: List[int], field: GF2m) -> Polynomial:
    n = len(syndromes)
    # Lambda(x) - текущий многочлен локаторов ошибок
    Lambda = Polynomial([1], field)
    # B(x) - предыдущий многочлен локаторов ошибок
    B = Polynomial([1], field)
    # L - текущая степень Lambda(x)
    L = 0
    # m - количество итераций с момента последнего обновления L
    m = 1
    # b - значение невязки на предыдущем шаге, когда L было обновлено
    b = 1

    for r in range(n):
        # Вычисление невязки (discrepancy)
        # Delta = S_r + Lambda_1*S_{r-1} + ... + Lambda_L*S_{r-L}
        Delta = syndromes[r]

        for i in range(1, L + 1):
            if i < len(Lambda.coeffs):
                term = field.multiply(Lambda.coeffs[i], syndromes[r - i])
                Delta = field.add(Delta, term)

        if Delta == 0:
            # Невязка равна нулю - Lambda(x) остается без изменений
            m += 1
        else:
            # Обновление Lambda(x)
            # T(x) = Lambda(x) - (Delta / b) * x^m * B(x)
            T = Polynomial(Lambda.coeffs[:], field)

            # Вычисление коэффициента Delta / b
            coef = field.divide(Delta, b)

            # Создание x^m * B(x)
            xm_B_coeffs = [0] * m + B.coeffs
            xm_B = Polynomial(xm_B_coeffs, field)

            # Вычитание
            correction = xm_B.scale(coef)
            Lambda = Lambda - correction

            if 2 * L <= r:
                # Обновление L, B и b
                L = r + 1 - L
                B = T
                b = Delta
                m = 1
            else:
                m += 1

    return Lambda


def compute_syndromes(received: List[int], alpha_powers: List[int], field: GF2m,
                     num_syndromes: int) -> List[int]:
    syndromes = []
    n = len(received)

    for i in alpha_powers:
        syndrome = 0
        alpha_power = 1  # alpha^{i*0}

        for j in range(n):
            if received[j] == 1:
                syndrome = field.add(syndrome, alpha_power)

            # alpha^{i*j} -> alpha^{i*(j+1)}
            alpha_i = field.alpha_power(i)
            alpha_power = field.multiply(alpha_power, alpha_i)

        syndromes.append(syndrome)

    return syndromes
