import numpy as np

from galua.GaluaField import GaluaField
from hamming.codec.HammingCodec import HammingCodec
from hamming.ThreadGenerator import ThreadGenerator


def run_scenario_classic():
    # q-ary classic Hamming over base field GF(q)
    q = 2
    n = 31
    k = 26
    r = n - k
    gf = GaluaField(q, r, [1, 0, 1, 0, 0, 1])
    codec = HammingCodec("classic", n, k, gf)

    print("=== Classic q-ary Hamming scenario (q=5) ===")
    print("Generator matrix G [k x n]:")
    print(codec.coder.generator_matrix)
    print("Parity-check matrix H [r x n]:")
    print(codec.decoder.parity_check_matrix)
    print()

    base = ThreadGenerator.make_base(q, with_erasure=True) # even if you don't need erasures, you still should set true :)
    gen = ThreadGenerator(base, n, k)
    words = gen.generate_words_thread(8)  # words of length k
    coded = codec.encode(words)

    noisy = gen.generate_data_thread(
        coded.astype(str),  # map to symbol strings for channel
        [0.5, 0.5],         # first is flip probability, second is erasure probability if you need erasures only use [0.0, 0.0]
        one_error_per_word=True, # add only one error per word
        fixed_erasures_per_word=0 # number of erasures per word
    )
    received = noisy

    decoded_info, corrected = codec.decode(received)

    print("Scenario (info | received_with_errors_incl_z | decoded):")
    for i in range(words.shape[0]):
        s_info = ''.join(map(str, words[i].tolist()))
        s_recv = ''.join(received[i].tolist())
        s_dec = ''.join(map(str, decoded_info[i].tolist()))
        print(f"{s_info} | {s_recv} | {s_dec}")

if __name__ == "__main__":
    run_scenario_classic()


