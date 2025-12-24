from galua.tests import run_all_tests as run_galua_tests
from hamming.tests import run_all_tests as run_hamming_tests
from linalg.tests import run_all_tests as run_linalg_tests
from hamming.codec.coder.tests import run_all_tests as run_coder_tests
from hamming.codec.decoder.tests import run_all_tests as run_decoder_tests
from hamming.test_scenario import run_scenario
from hamming.scenario_classic import run_scenario_classic
from hamming.scenario_shortened import run_scenario_shortened
from hamming.scenario_extended import run_scenario_extended
from cyclic.run_cyclic import run_cyclic
from bch.run_bch import run_bch

def main():

    #run_galua_tests()
    
    #run_hamming_tests()

    #run_linalg_tests()

    #run_coder_tests()

    #run_decoder_tests()

    #run_scenario()

    #run_scenario_classic()

    #run_scenario_shortened()

    #run_scenario_extended()

    #run_cyclic()

    run_bch()

if __name__ == '__main__':
    main()