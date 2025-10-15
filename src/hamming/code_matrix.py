import numpy as np
from .GaluaField import GaluaField as gf
from .GaluaElement import GaluaElement as el
'''
File that has functions to build matricies by code params for another purposes 
'''


def build_parity_check_matrix(
        code_length: int,  # n
        base_length: int   # k
) -> np.ndarray[np.int32, np.int32]:

    identity = np.eye(code_length-base_length, dtype=np.int32)
    gf1 = gf(2, code_length - base_length, )#np.array([2, 2, 1]))
    P = np.empty([code_length - base_length, base_length])
    for i in range(0,code_length - base_length):
        P[i] = gf1[i]
    parity_check_matrix = np.hstack([P,identity])
    return parity_check_matrix



def build_generator_matrix(
    parity_check_matrix: np.ndarray[np.int32, np.int32]
) -> np.ndarray[np.int32, np.int32]:

    identity = np.eye(parity_check_matrix.base_length, dtype=np.int32)
    P_submatrix = parity_check_matrix[:, :parity_check_matrix.base_length]
    P_transposed = P_submatrix.T  # Транспонирование
    generator_matrix = np.hstack([identity, P_transposed]);
    return generator_matrix