import numpy as np

'''
File that has functions to build matricies by code params for another purposes 
'''

def build_generator_matrix(
    code_length: int, # n
    base_length: int  # k
) -> np.ndarray[np.int32, np.int32]:
    
    '''
    Return generator matrix G of linear block (n, k) code [k x n] size
    '''

    result = np.empty([base_length, code_length]) # sizes of result

    return result


def build_parity_check_matrix(
    generator_matrix: np.ndarray[np.int32, np.int32] # G
) -> np.ndarray[np.int32, np.int32]:
    
    '''
    Return parity-check matrix H of linear block (n, k) code [r x n] size
    r = n - k
    '''
    
    # find shapes of G
    base_length, code_length = generator_matrix.shape

    # find nmber of excess symbols
    exss_length = code_length - base_length



    result = np.empty([exss_length, code_length]) # sizes of result

    return result