from galua.tests import run_all_tests as run_galua_tests
from hamming.tests import run_all_tests as run_hamming_tests
from linalg.tests import run_all_tests as run_linalg_tests
from hamming.codec.coder.tests import run_all_tests as run_coder_tests
from hamming.codec.decoder.tests import run_all_tests as run_decoder_tests
from scenario import run_scenario

def main():

    run_galua_tests()
    
    run_hamming_tests()

    run_linalg_tests()

    run_coder_tests()

    run_decoder_tests()

    run_scenario()

if __name__ == '__main__':
    main()