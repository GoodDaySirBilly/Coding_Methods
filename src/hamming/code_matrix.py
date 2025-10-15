import numpy as np
from ..galua import GaluaField


'''
File that has functions to build matricies by code params for another purposes 
'''

def build_parity_check_matrix(
    code_length: int, # n
    exss_length: int, # r
    gf: GaluaField.GaluaField
) -> np.ndarray[np.int32, np.int32]:
    
    '''
    Return parity-check matrix H of linear block (n, k) code [r x n] size
    r = n - k
    '''

    result = np.empty([exss_length, code_length]) # sizes of result

    return result


def build_generator_matrix(
    parity_check_matrix: np.ndarray[np.int32, np.int32] # H
) -> np.ndarray[np.int32, np.int32]:
    
    '''
    Return generator matrix G of linear block (n, k) code [k x n] size
    '''

    
    # find shapes of G
    exss_length, code_length = parity_check_matrix.shape

    # find nmber of excess symbols
    base_length = code_length - exss_length

    result = np.empty([base_length, code_length]) # sizes of result

    return result

def syndrom(
    code_word: np.ndarray[np.int32],
    parity_check_matrix: np.ndarray[np.int32, np.int32]
) -> np.ndarray[np.int32]:
    
    return code_word @ parity_check_matrix.T