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

    H = gf.values[1:, :]
    H[0:exss_length] = np.flip(H[0:exss_length], axis=1)
    H[exss_length:] = np.flip(H[exss_length:], axis=0)

    H = H.T
    H = np.flip(H, axis = 0)
    H = np.flip(H, axis = 1)
    H[:, -exss_length:] = np.eye(exss_length, dtype=int)

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

    P = H[:, 0:r+1].T

    G = np.concat([np.eye(k, dtype=int), P], axis = 1)

    return G

def syndrom(
    code_word: np.ndarray[np.int32],
    parity_check_matrix: np.ndarray[np.int32, np.int32]
) -> np.ndarray[np.int32]:

    return parity_check_matrix @ code_word

def find_error(
    syndrom: np.ndarray[np.int32],
    parity_check_matrix: np.ndarray[np.int32, np.int32]
) -> int:
    
    equal_columns_mask = np.all(
        parity_check_matrix == syndrom[:, np.newaxis], axis=0
    )

    indices_of_equal_columns = np.where(equal_columns_mask)[0]

    return indices_of_equal_columns