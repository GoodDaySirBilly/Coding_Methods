import numpy as np

from .ClassicCoder import *
from .ExtendedCoder import *
from .ShortenedCoder import *

def run_all_tests():

    classic_check()
    extended_check()
    shortened_check()
    print("All Coder tests passed")

def classic_check():
    code_length = 7
    base_length = 4
    
    exss_length = code_length - base_length

    # hamming_code = (code_length, base_length)

    gf1 = GaluaField(2, exss_length, [1, 0, 1, 1])

    coder = ClassicCoder(code_length=code_length, base_length=base_length, gf=gf1)

    words = np.array([
        [1, 0, 1, 0],
        [0, 1, 1, 0],
        [0, 0, 0, 1]
    ])

    #inf bits, code bits

    coded_words = coder.code_words(words)

    true_coded_words = np.array([
        [1, 0, 1, 0, 1, 1, 0],
        [0, 1, 1, 0, 1, 0, 0],
        [0, 0, 0, 1, 1, 1, 0]
    ])

    assert np.all(coded_words == true_coded_words)


def extended_check():
    code_length = 7
    base_length = 4

    exss_length = code_length - base_length

    # hamming_code = (code_length, base_length)

    gf1 = GaluaField(2, exss_length, [1, 0, 1, 1])

    coder = ExtendedCoder(code_length, base_length, gf1)

    words = np.array([
        [1, 0, 1, 0],
        [0, 1, 1, 0],
        [0, 0, 0, 1]
    ])

    #inf bits, code bits, even_bit

    coded_words = coder.code_words(words)

    true_coded_words = np.array([
        [1, 0, 1, 0, 1, 1, 0, 0],
        [0, 1, 1, 0, 1, 0, 0, 1],
        [0, 0, 0, 1, 1, 1, 0, 1]
    ])

    assert np.all(coded_words == true_coded_words)

def shortened_check():
    
    code_length = 7
    base_length = 4

    exss_length = code_length - base_length

    # hamming_code = (code_length, base_length)

    gf1 = GaluaField(2, exss_length, [1, 0, 1, 1])

    coder = ShortenedCoder(code_length, base_length, gf1, 1, 0)

    words = np.array([
        [0, 1, 0],
        [1, 1, 0],
        [0, 0, 1]
    ])

    # short inf bits, code bits, even_bit

    coded_words = coder.code_words(words)

    true_coded_words = np.array([
        [0, 1, 0, 0, 1, 1],
        [1, 1, 0, 1, 0, 0],
        [0, 0, 1, 1, 1, 0]
    ])
    
    assert np.all(coded_words == true_coded_words)