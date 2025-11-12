import numpy as np

from galua.GaluaField import GaluaField
from hamming.codec.HammingCodec import HammingCodec
from hamming.ThreadGenerator import ThreadGenerator


def run_scenario_extended():
    # Extended binary Hamming
    q = 2
    n, k = 32, 26
    r = n - k

    gf = GaluaField(q, r, [1, 1, 0, 0, 0, 0, 1])
    codec = HammingCodec("extended", n, k, gf)

    print("=== Extended binary Hamming ===")
    print("Generator matrix G [k x n]:")
    print(codec.coder.generator_matrix)
    print("Parity-check matrix H [r x n]:")
    print(codec.decoder.parity_check_matrix)

    try:
        H_ext = codec.coder.extend_parity 
        print("Extended parity-check matrix H_ext [(r+1) x (n+1)]:")
        print(H_ext)
    except Exception:
        pass

    try:
        G = codec.coder.generator_matrix
        p = (np.sum(G, axis=1) % gf.chr)[:, np.newaxis]
        G_ext = np.concatenate([G, p], axis=1)
        print("Extended generator matrix G_ext [k x (n+1)]:")
        print(G_ext)
    except Exception:
        pass
    print()

    base = ThreadGenerator.make_base(q, with_erasure=True) # even if you don't need erasures, you still should set true :)
    gen = ThreadGenerator(base, n, k)
    words = gen.generate_words_thread(6)  # words of length k
    coded = codec.encode(words)  # shape [m, n+1]

    noisy = gen.generate_data_thread(
        coded.astype(str), 
        [0.0, 0.0], # first is flip probability, second is erasure probability if you need erasures only use [0.0, 0.0]
        one_error_per_word=False, # add only one error per word
        fixed_erasures_per_word=3 # number of erasures per word
    )
    received = noisy

    decoded_info, corrected = codec.decode(received)

    print("Scenario (info | received_with_errors | decoded):")
    for i in range(words.shape[0]):
        s_info = ''.join(map(str, words[i].tolist()))
        s_recv = ''.join(received[i].tolist())
        s_dec = ''.join(map(str, decoded_info[i].tolist()))
        print(f"{s_info} | {s_recv} | {s_dec}")

    H = codec.decoder.parity_check_matrix
    qch = codec.decoder.gf.chr
    to_int = {str(i): i for i in range(qch)}
    numeric_received = np.zeros_like(coded, dtype=int)
    for i in range(received.shape[0]):
        for j in range(received.shape[1]):
            c = received[i, j]
            numeric_received[i, j] = 0 if c == 'z' else to_int[str(c)]
    S_before = (H @ numeric_received[:, :n].T) % qch
    S_after = (H @ corrected[:, :n].T) % qch
    rows_detected = np.where(np.any(S_before.T != 0, axis=1))[0]
    rows_no_change = rows_detected[np.where(~np.any((corrected != numeric_received)[rows_detected], axis=1))[0]]
    rows_still = np.where(np.any(S_after.T != 0, axis=1))[0]
    if rows_no_change.size > 0:
        print("Detected but not corrected (no change):", rows_no_change.tolist())
    if rows_still.size > 0:
        print("After correction syndrome still != 0:", rows_still.tolist())

if __name__ == "__main__":
    run_scenario_extended()


