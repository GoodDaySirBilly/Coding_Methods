from galua.tests import run_all_tests as run_galua_tests
from hamming.tests import run_all_tests as run_hamming_tests

def main():

    run_galua_tests()
    
    run_hamming_tests()


    
if __name__ == '__main__':
    main()