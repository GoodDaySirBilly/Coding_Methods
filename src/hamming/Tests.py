from .code_matrix import *
from .input_thread import *

def run_all_tests():
    
    test_example()


def test_example():

    assert np.all(np.zeros([3, 2]) == np.ones([3, 2]) * 0.)