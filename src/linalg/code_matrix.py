import numpy as np

from galua.GaluaField import GaluaField
from galua.GaluaElement import GaluaElement


'''
File that has functions to build matricies by code params for another purposes 
'''

def build_parity_check_matrix(
    code_length: int, # n
    exss_length: int, # r
    gf: GaluaField
) -> np.ndarray[np.int32, np.int32]:
    
    '''
    Return parity-check matrix H of linear block (n, k) code [r x n] size
    r = n - k
    '''

    r = exss_length
    n = code_length

    H = np.empty((r, n), dtype=object)

    for col in range(1, n + 1):
        bin_repr = [int(x) for x in format(col, f'0{r}b')]
        bin_repr.reverse()

        for row in range(r):
            value_array = np.zeros(gf.orp, dtype=np.int32)
            value_array[0] = bin_repr[row]  # ставим 0 или 1 в младший коэффициент
            H[row, col - 1] = GaluaElement(gf, value_array)

    return H


def build_generator_matrix(
    parity_check_matrix: np.ndarray[np.int32, np.int32] # H
) -> np.ndarray[np.int32, np.int32]:
    
    '''
    Return generator matrix G of linear block (n, k) code [k x n] size
    '''

    H = parity_check_matrix
    r, n = H.shape
    k = n - r

    gf = H[0, 0].gf

    # H = [P^T | I_r] -> P = (левая часть H)^T
    P_T = H[:, :k]  # r x k
    P = np.empty((k, r), dtype=object)
    for i in range(k):
        for j in range(r):
            P[i, j] = P_T[j, i]  # транспонируем

    G = np.empty((k, n), dtype=object)
    for i in range(k):
        for j in range(k):
            value_array = np.zeros(gf.orp, dtype=np.int32)
            value_array[0] = 1 if i == j else 0
            G[i, j] = GaluaElement(gf, value_array)
    for i in range(k):
        for j in range(r):
            G[i, k + j] = P[i, j]

    return G

def syndrom(
    code_word: np.ndarray[np.int32],
    parity_check_matrix: np.ndarray[np.int32, np.int32]
) -> np.ndarray[np.int32]:

    return code_word @ parity_check_matrix.T