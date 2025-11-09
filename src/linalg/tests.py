import numpy as np

from linalg.code_matrix import *

def run_all_tests():

    parity_check()
    generator_check()
    syndrom_check()
    print("All Linalg tests passed")

def parity_check():

    code_length = 7
    base_length = 4
    exss_length = code_length - base_length

    hamming_code = (code_length, base_length)

    gf1 = GaluaField(2, exss_length, [1, 0, 1, 1])


    H = build_parity_check_matrix(code_length, exss_length, gf1)


    assert np.all(H.shape == (exss_length, code_length))
    assert np.all(H == 
        np.array([
            [1, 1, 0, 1, 1, 0, 0],
            [0, 1, 1, 1, 0, 1, 0],
            [1, 1, 1, 0, 0, 0, 1]
        ])
    )


def generator_check():

    H = np.array([
        [1, 1, 0, 1, 1, 0, 0],
        [0, 1, 1, 1, 0, 1, 0],
        [1, 1, 1, 0, 0, 0, 1]
    ])

    G = build_generator_matrix(H)

    assert np.all(G == 
        np.array([
            [1, 0, 0, 0, 1, 0, 1],
            [0, 1, 0, 0, 1, 1, 1],
            [0, 0, 1, 0, 0, 1, 1],
            [0, 0, 0, 1, 1, 1, 0]
        ])
    )


def syndrom_check():

    word = np.array([1, 0, 1, 0])

    H = np.array([
        [1, 1, 0, 1, 1, 0, 0],
        [0, 1, 1, 1, 0, 1, 0],
        [1, 1, 1, 0, 0, 0, 1]
    ])

    G = build_generator_matrix(H)

    word = word @ G % 2

    s = syndrom(word, H) % 2

    assert np.all(s == 0)

    e = np.array([0, 1, 0, 0, 0, 0, 0])

    word += e

    s = syndrom(word, H) % 2

    ind = find_error(s, H)

    assert np.all(s == H[:, ind])
