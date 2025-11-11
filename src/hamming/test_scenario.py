from hamming.codec.HammingCodec import HammingCodec
from galua.GaluaField import GaluaField
from hamming.ThreadGenerator import ThreadGenerator
import numpy as np


def run_scenario():
    q = 5
    n = 4
    k = 2
    r = n - k
    # Use base field GF(q): degree 1, monic linear polynomial (e.g., x)
    gf = GaluaField(q, r, [1, 0, 1])
    codec = HammingCodec("classic", n, k, gf)

    # Print matrices
    print("Generator matrix G [k x n]:")
    print(codec.coder.generator_matrix)
    print("Parity-check matrix H [r x n]:")
    print(codec.decoder.parity_check_matrix)
    print()

    # Use alphabet with erasure symbol 'z'
    base = ThreadGenerator.make_base(q, with_erasure=True)
    gen = ThreadGenerator(base, n, k)
    words = gen.generate_words_thread(8)  # words of length k

    coded = codec.encode(words)

    noisy = gen.generate_data_thread(
        coded.astype(str),  # map to symbol strings for channel
        [0.0, 0.0],         # disable random probabilities
        one_error_per_word=True,  # add one error per word
        fixed_erasures_per_word=0 # number of erasures per word
    )
    # pass symbols directly to decoder
    received = noisy

    decoded_info, corrected = codec.decode(received)

    # Simple check: shapes should match
    assert decoded_info.shape == (words.shape[0], k)

    # Print scenario rows: input info | received (with errors/erasures) | decoded info
    print("Scenario (info | received_with_errors_incl_z | decoded):")
    for i in range(words.shape[0]):
        info_str = ''.join(map(str, words[i].tolist()))
        recv_str = ''.join(received[i].tolist())
        dec_str = ''.join(map(str, decoded_info[i].tolist()))
        print(f"{info_str} | {recv_str} | {dec_str}")

    # Report detected-but-not-corrected and still-syndrome rows
    q_char = codec.decoder.gf.chr
    H = codec.decoder.parity_check_matrix
    # map received symbols to ints
    if received.dtype.kind in ('U', 'S'):
        to_int = {str(i): i for i in range(q_char)}
        numeric_received = np.vectorize(lambda c: 0 if c == 'z' else to_int[str(c)])(received)
    else:
        numeric_received = (received % q_char).astype(int)
    S_before = (H @ numeric_received.T) % q_char
    S_before = S_before.T
    corrected_num = (corrected % q_char).astype(int)
    S_after = (H @ corrected_num.T) % q_char
    S_after = S_after.T
    rows_detected = np.where(np.any(S_before != 0, axis=1))[0]
    rows_no_change = rows_detected[np.where(~np.any((corrected_num != numeric_received)[rows_detected], axis=1))[0]]
    rows_still_syndrome = np.where(np.any(S_after != 0, axis=1))[0]
    print()
    print("Detected (syndrome != 0):", rows_detected.tolist())
    print("Detected but not corrected (no change):", rows_no_change.tolist())
    print("After correction syndrome still != 0:", rows_still_syndrome.tolist())

    # ------- Extended binary scenario: detect-but-not-correct (double errors) -------
    print("\n=== Extended binary Hamming: detection without correction ===")
    q2 = 2
    n2, k2 = 7, 4
    r2 = n2 - k2
    gf2 = GaluaField(q2, r2, [1, 0, 1, 1])  # GF(2^3) for binary case
    codec_ext = HammingCodec("extended", n2, k2, gf2)

    print("Generator matrix G [k x (n)]:")
    print(codec_ext.coder.generator_matrix)
    print("Parity-check matrix H [r x (n)]:")
    print(codec_ext.decoder.parity_check_matrix)
    print()

    gen2 = ThreadGenerator(ThreadGenerator.base_2, n2, k2)
    words2 = gen2.generate_words_thread(6)
    code2 = codec_ext.encode(words2)  # shape: [m, n2+1] (with parity)

    # Inject two data-bit errors per word to trigger: syndrome != 0 and total parity == 0
    rng = np.random.default_rng(7)
    code2_err = code2.copy()
    for i in range(code2_err.shape[0]):
        # choose two distinct positions among first n2
        j1, j2 = rng.choice(n2, size=2, replace=False)
        code2_err[i, j1] ^= 1
        code2_err[i, j2] ^= 1

    info2_dec, corrected2 = codec_ext.decode(code2_err)

    print("Extended scenario (info | received(two errors) | decoded):")
    for i in range(words2.shape[0]):
        info_str = ''.join(map(str, words2[i].tolist()))
        recv_str = ''.join(map(str, code2_err[i].tolist()))
        dec_str = ''.join(map(str, info2_dec[i].tolist()))
        print(f"{info_str} | {recv_str} | {dec_str}")

    # Diagnostics for extended: expect detection without correction
    q_char2 = codec_ext.decoder.gf.chr
    H2 = codec_ext.decoder.parity_check_matrix
    numeric_received2 = (code2_err % q_char2).astype(int)
    S2_before = (H2 @ numeric_received2[:, :n2].T) % q_char2  # parity bit is last, compute on first n2
    S2_before = S2_before.T
    corrected2_num = (corrected2 % q_char2).astype(int)
    S2_after = (H2 @ corrected2_num[:, :n2].T) % q_char2
    S2_after = S2_after.T
    rows2_detected = np.where(np.any(S2_before != 0, axis=1))[0]
    rows2_no_change = rows2_detected[np.where(~np.any((corrected2_num != numeric_received2)[rows2_detected], axis=1))[0]]
    rows2_still_syndrome = np.where(np.any(S2_after != 0, axis=1))[0]
    print()
    print("Detected (syndrome != 0):", rows2_detected.tolist())
    print("Detected but not corrected (no change):", rows2_no_change.tolist())
    print("After correction syndrome still != 0:", rows2_still_syndrome.tolist())

    # ------- Shortened binary scenario -------
    print("\n=== Shortened binary Hamming: correction and erasure limits ===")
    # Base (7,4) shortened by 1 -> (6,3)
    short_remove = 1
    n_full, k_full = 7, 4
    r_full = n_full - k_full
    n_short = n_full - short_remove
    k_short = k_full - short_remove
    gf_bin = GaluaField(2, r_full, [1, 0, 1, 1])
    codec_short = HammingCodec("shortened", n_full, k_full, gf_bin,
                               short_code_length=short_remove, short_base_length=0)

    print("Parity-check matrix H (full) [r x n]:")
    print(codec_short.decoder.parity_check_matrix)
    print(f"Shortened lengths: n'={n_short}, k'={k_short}")
    print()

    # Use alphabet with erasures for demonstration
    gen_short = ThreadGenerator(ThreadGenerator.base_2er, n_short, k_short)
    words_s = gen_short.generate_words_thread(6)
    code_s = codec_short.encode(words_s)  # shape: [m, n']

    # 1) Single-error correction in transmitted segment
    rng = np.random.default_rng(11)
    code_s_err = code_s.copy()
    flip_pos = rng.integers(0, n_short, size=(code_s.shape[0],))
    for i in range(code_s_err.shape[0]):
        j = int(flip_pos[i])
        code_s_err[i, j] ^= 1

    info_s_dec, corrected_s = codec_short.decode(code_s_err)
    print("Shortened scenario (info' | received'(1 error) | decoded'):")
    for i in range(words_s.shape[0]):
        info_str = ''.join(map(str, words_s[i].tolist()))
        recv_str = ''.join(map(str, code_s_err[i].tolist()))
        dec_str = ''.join(map(str, info_s_dec[i].tolist()))
        print(f"{info_str} | {recv_str} | {dec_str}")

    # Diagnostics: compute syndromes on embedded full vectors
    Hs = codec_short.decoder.parity_check_matrix
    def embed_short(arr):
        out = np.zeros((arr.shape[0], n_full), dtype=int)
        out[:, short_remove:] = arr % 2
        return out
    rec_full = embed_short(code_s_err)
    corr_full = embed_short(corrected_s)
    S_s_before = (Hs @ rec_full.T) % 2
    S_s_after = (Hs @ corr_full.T) % 2
    rows_s_detected = np.where(np.any(S_s_before.T != 0, axis=1))[0]
    rows_s_still = np.where(np.any(S_s_after.T != 0, axis=1))[0]
    print("Detected (syndrome != 0):", rows_s_detected.tolist())
    print("After correction syndrome still != 0:", rows_s_still.tolist())

    # 2) Too many erasures (uncorrectable): set > r erasures
    code_s_er = code_s.copy().astype(np.str_)
    code_s_er = gen_short.generate_data_thread(code_s_er, [0.0, 0.0], fixed_erasures_per_word=r_full + 1)
    info_s_er_dec, corrected_s_er = codec_short.decode(code_s_er)
    print("\nShortened scenario with >r erasures (info' | received' with 'z' | decoded'):")
    for i in range(words_s.shape[0]):
        info_str = ''.join(map(str, words_s[i].tolist()))
        recv_str = ''.join(code_s_er[i].tolist())
        dec_str = ''.join(map(str, info_s_er_dec[i].tolist()))
        print(f"{info_str} | {recv_str} | {dec_str}")

    # Diagnostics for erasures case
    # Map 'z' -> 0 for syndrome calculation
    to_int = {'0': 0, '1': 1}
    rec_er_short_num = np.zeros_like(code_s, dtype=int)
    for i in range(code_s_er.shape[0]):
        for j in range(code_s_er.shape[1]):
            rec_er_short_num[i, j] = 0 if code_s_er[i, j] == 'z' else to_int[code_s_er[i, j]]
    rec_er_full = embed_short(rec_er_short_num)
    corr_er_full = embed_short(corrected_s_er % 2)
    S_er_before = (Hs @ rec_er_full.T) % 2
    S_er_after = (Hs @ corr_er_full.T) % 2
    rows_er_detected = np.where(np.any(S_er_before.T != 0, axis=1))[0]
    rows_er_still = np.where(np.any(S_er_after.T != 0, axis=1))[0]
    print("Detected (syndrome != 0):", rows_er_detected.tolist())
    print("After correction syndrome still != 0:", rows_er_still.tolist())

