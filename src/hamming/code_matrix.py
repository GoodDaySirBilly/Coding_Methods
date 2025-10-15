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

    identity = np.eye(base_length, dtype=np.int32)
    gf1 = gf(2, code_length - base_length, )#np.array([2, 2, 1]))
    parity_check_matrix = np.hstack([gf1,identity])
    return parity_check_matrix



def build_generator_matrix(
    parity_check_matrix: np.ndarray[np.int32, np.int32]
) -> np.ndarray[np.int32, np.int32]:

    identity = np.eye(parity_check_matrix.base_length, dtype=np.int32)
    P_submatrix = parity_check_matrix[:, :parity_check_matrix.code_length-parity_check_matrix.base_length + 1]
    P_transposed = P_submatrix.T  # Транспонирование
    generator_matrix = np.hstack([identity, P_transposed]);
    return generator_matrix