import numpy as np

from galua.GaluaField import GaluaField
from hamming.codec.HammingCodec import HammingCodec
from hamming.ThreadGenerator import ThreadGenerator

def run_all_tests():
    test_classic_decoder_corrects_single_error()
    test_extended_decoder_corrects_single_error_and_parity()
    test_shortened_decoder_corrects_single_error()
    test_codec_round_trip_classic()
    test_classic_decoder_q3_corrects_single_symbol_error()
    test_classic_decoder_q5_corrects_single_symbol_error()
    print("All Decoder tests passed")


def _gf_2_r(r: int) -> GaluaField:
    # polynomial x^3 + x + 1 for r=3 example; caller must supply correct length
    default_polys = {
        2: [1, 1, 1],
        3: [1, 0, 1, 1],
        4: [1, 0, 0, 1, 1],
    }
    pol = default_polys.get(r, [1, 0, 1, 1])
    return GaluaField(2, r, pol)


def test_classic_decoder_corrects_single_error():
    n, k = 7, 4
    gf = _gf_2_r(n - k)
    codec = HammingCodec("classic", n, k, gf)

    words = np.array([
        [1, 0, 1, 0],
        [0, 1, 1, 0],
    ], dtype=int)
    code = codec.encode(words)
    # flip a single bit in each codeword
    code_err = code.copy()
    code_err[0, 2] ^= 1
    code_err[1, 5] ^= 1

    info_dec, corrected = codec.decode(code_err)
    assert np.array_equal(info_dec, words)
    assert np.array_equal(corrected, code)


def test_extended_decoder_corrects_single_error_and_parity():
    n, k = 7, 4
    gf = _gf_2_r(n - k)
    codec = HammingCodec("extended", n, k, gf)

    words = np.array([
        [1, 0, 1, 0],
        [0, 1, 1, 0],
    ], dtype=int)
    code = codec.encode(words)
    code_err = code.copy()
    # flip a data bit and the parity bit in different codewords
    code_err[0, 1] ^= 1
    code_err[1, -1] ^= 1

    info_dec, corrected = codec.decode(code_err)
    assert np.array_equal(info_dec, words)
    assert np.array_equal(corrected, code)


def test_shortened_decoder_corrects_single_error():
    n, k = 7, 4
    short_n_remove, short_k_remove = 1, 0
    gf = _gf_2_r(n - k)
    codec = HammingCodec(
        "shortened", n, k, gf,
        short_code_length=short_n_remove,
        short_base_length=short_k_remove
    )

    words = np.array([
        [0, 1, 0],  # k' = 3
        [1, 1, 0],
    ], dtype=int)
    code = codec.encode(words)
    code_err = code.copy()
    code_err[0, 2] ^= 1
    code_err[1, 4] ^= 1

    info_dec, corrected = codec.decode(code_err)
    assert np.array_equal(info_dec, words)
    assert np.array_equal(corrected, code)


def test_codec_round_trip_classic():
    n, k = 7, 4
    gf = _gf_2_r(n - k)
    codec = HammingCodec("classic", n, k, gf)
    gen = ThreadGenerator(ThreadGenerator.base_2, n, k)

    words = gen.generate_words_thread(10)
    code = codec.encode(words)
    # introduce one random single-bit error per codeword
    rng = np.random.default_rng(42)
    idx = rng.integers(0, n, size=(words.shape[0],))
    code_err = code.copy()
    for i, j in enumerate(idx):
        code_err[i, j] ^= 1

    info_dec, corrected = codec.decode(code_err)
    assert np.array_equal(info_dec, words)


def _gf_q_r(q: int, r: int) -> GaluaField:
    # Minimal polynomials for small q,r used in tests
    if q == 3 and r == 2:
        # x^2 + 1 over F3 (irreducible)
        pol = [1, 0, 1]
    elif q == 5 and r == 2:
        # x^2 + 2 over F5 (irreducible)
        pol = [2, 0, 1]
    else:
        # fallback monic
        pol = [0]*(r+1)
        pol[0] = 1
        pol[-1] = 1
    return GaluaField(q, r, pol)


def test_classic_decoder_q3_corrects_single_symbol_error():
    q = 3
    n = 4
    k = 2
    r = n - k
    gf = _gf_q_r(q, r)
    codec = HammingCodec("classic", n, k, gf)

    # generate a few words over GF(3)
    words = np.array([
        [0, 1],
        [1, 2],
        [2, 0],
    ], dtype=int)
    code = codec.encode(words)
    code_err = code.copy()
    # inject single-symbol errors with random magnitude 1..q-1
    rng = np.random.default_rng(123)
    idx = rng.integers(0, n, size=(words.shape[0],))
    magnitudes = rng.integers(1, q, size=(words.shape[0],))
    for i, j in enumerate(idx):
        code_err[i, j] = (code_err[i, j] + magnitudes[i]) % q

    info_dec, corrected = codec.decode(code_err)
    assert np.array_equal(info_dec % q, words % q)

def test_extended_decoder_q3_corrects_single_symbol_error_and_parity():
    q = 3
    n = 4
    k = 2
    r = n - k
    gf = _gf_q_r(q, r)
    codec = HammingCodec("extended", n, k, gf)

    words = np.array([
        [0, 1],
        [2, 2],
    ], dtype=int)
    code = codec.encode(words)  # shape [m, n+1]
    code_err = code.copy()
    rng = np.random.default_rng(777)
    # Row 0: flip a data symbol by a random non-zero magnitude
    j0 = int(rng.integers(0, n))
    a0 = int(rng.integers(1, q))
    code_err[0, j0] = (code_err[0, j0] + a0) % q
    # Row 1: flip only the parity symbol
    a1 = int(rng.integers(1, q))
    code_err[1, n] = (code_err[1, n] + a1) % q

    info_dec, corrected = codec.decode(code_err)
    assert np.array_equal(info_dec % q, words % q)
    assert np.array_equal(corrected % q, code % q)


def test_classic_decoder_q5_corrects_single_symbol_error():
    q = 5
    k = 4
    n = 6
    r = n - k
    gf = _gf_q_r(q, r)
    codec = HammingCodec("classic", n, k, gf)

    words = np.array([
        [0, 1, 2, 3],
        [4, 0, 1, 2],
    ], dtype=int)
    code = codec.encode(words)
    code_err = code.copy()
    rng = np.random.default_rng(321)
    idx = rng.integers(0, n, size=(words.shape[0],))
    magnitudes = rng.integers(1, q, size=(words.shape[0],))
    for i, j in enumerate(idx):
        code_err[i, j] = (code_err[i, j] + magnitudes[i]) % q

    info_dec, corrected = codec.decode(code_err)
    assert np.array_equal(info_dec % q, words % q)

def test_shortened_decoder_q3_corrects_single_symbol_error():
    q = 3
    n = 4
    k = 2
    r = n - k
    gf = _gf_q_r(q, r)
    # shorten by removing 1 code symbol from the front, keep k' = k - 1 = 1
    short_n_remove, short_k_remove = 1, 0
    codec = HammingCodec(
        "shortened", n, k, gf,
        short_code_length=short_n_remove,
        short_base_length=short_k_remove
    )

    words = np.array([
        [0],  # k' = 1
        [2],
    ], dtype=int)
    code = codec.encode(words)
    code_err = code.copy()
    # flip a transmitted symbol
    rng = np.random.default_rng(987)
    j = int(rng.integers(0, code.shape[1]))
    a = int(rng.integers(1, q))
    code_err[0, j] = (code_err[0, j] + a) % q

    info_dec, corrected = codec.decode(code_err)
    assert np.array_equal(info_dec % q, words % q)
    assert np.array_equal(corrected % q, code % q)
