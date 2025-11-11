from hamming.codec.HammingCodec import HammingCodec
from galua.GaluaField import GaluaField
from hamming.ThreadGenerator import ThreadGenerator
import numpy as np

def run_scenario_shortened():
    # Shortened binary Hamming: from (7,4) to (6,3) by removing 1 front column
    q = 3
    n_full, k_full = 15, 11
    r_full = n_full - k_full
    short_remove = 1
    n_short = n_full - short_remove
    k_short = k_full - short_remove
    gf = GaluaField(q, r_full, [1, 0, 0, 1, 1])
    codec = HammingCodec(
        "shortened", n_full, k_full, gf,
        short_code_length=short_remove, short_base_length=0
    )

    print("=== Shortened binary Hamming ===")
    print("Generator matrix G (full) [k x n]:")
    print(codec.coder.generator_matrix)
    print("Parity-check matrix H (full) [r x n]:")
    print(codec.decoder.parity_check_matrix)
    print(f"Shortened lengths: n'={n_short}, k'={k_short}")
    try:
        from linalg.code_matrix import build_generator_matrix
        H_full = codec.decoder.parity_check_matrix
        H_short = H_full[:, short_remove:]
        print("Parity-check matrix H' (shortened) [r x n']:")
        print(H_short)
        G_short = build_generator_matrix(H_short)
        print("Generator matrix G' (shortened, derived from H') [k' x n']:")
        print(G_short)
    except Exception as _:
        pass
    print()


    base = ThreadGenerator.make_base(q, with_erasure=True) # even if you don't need erasures, you still should set true :)
    gen = ThreadGenerator(base, n_short, k_short)
    words = gen.generate_words_thread(8)  # words of length k_short
    coded = codec.encode(words)

    noisy = gen.generate_data_thread(
        coded.astype(str),
        [0.5, 0.5], # first is flip probability, second is erasure probability if you need erasures only use [0.0, 0.0]
        one_error_per_word=True, # add only one error per word  
        fixed_erasures_per_word=0 # number of erasures per word
    )
    received = noisy

    info_dec, corrected = codec.decode(received)

    print("Scenario (info' | received' | decoded'):")
    for i in range(words.shape[0]):
        s_info = ''.join(map(str, words[i].tolist()))
        s_recv = ''.join(received[i].tolist())
        s_dec = ''.join(map(str, info_dec[i].tolist()))
        print(f"{s_info} | {s_recv} | {s_dec}")

    H = codec.decoder.parity_check_matrix
    qch = codec.decoder.gf.chr
    to_int = {str(i): i for i in range(qch)}
    rec_short_num = np.zeros_like(coded, dtype=int)
    for i in range(received.shape[0]):
        for j in range(received.shape[1]):
            c = received[i, j]
            rec_short_num[i, j] = 0 if c == 'z' else to_int[str(c)]
    rec_full = np.zeros((received.shape[0], n_full), dtype=int)
    rec_full[:, short_remove:] = rec_short_num % qch
    corr_full = np.zeros((corrected.shape[0], n_full), dtype=int)
    corr_full[:, short_remove:] = (corrected % qch)
    S_after = (H @ corr_full.T) % qch
    rows_still = np.where(np.any(S_after.T != 0, axis=1))[0]
    print("After correction syndrome still != 0:", rows_still.tolist())

