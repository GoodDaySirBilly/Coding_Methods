from hamming.ThreadGenerator import ThreadGenerator
import numpy as np


def run_all_tests():
    test_generate_data_thread_binary_flip_all()
    test_generate_data_thread_binary_erase_all()
    test_generate_data_thread_binary_flip_respects_erasures()
    test_generate_data_thread_ternary_flip_changes()
    test_generate_data_thread_no_change_zero_probs()
    print("All Generator tests passed")


def test_generate_data_thread_binary_flip_all():
    words = np.array([
        ['0', '1', '0', '1'],
        ['1', '1', '0', '0']
    ], dtype=np.str_)
    G = np.array([[1, 0, 1, 0]], dtype=np.int32)
    gen = ThreadGenerator(ThreadGenerator.base_2, G)

    flipped = gen.generate_data_thread(words, [1.0])

    expected = np.array([
        ['1', '0', '1', '0'],
        ['0', '0', '1', '1']
    ], dtype=np.str_)
    assert np.array_equal(flipped, expected)


def test_generate_data_thread_binary_erase_all():
    words = np.array([
        ['0', '1', '0'],
        ['1', '0', '1']
    ], dtype=np.str_)
    G = np.array([[1, 1, 1]], dtype=np.int32)
    gen = ThreadGenerator(ThreadGenerator.base_2er, G)

    erased = gen.generate_data_thread(words, [0.0, 1.0])
    assert np.all(erased == 'z')


def test_generate_data_thread_binary_flip_respects_erasures():
    words = np.array([
        ['0', 'z', '1', 'z'],
        ['z', '1', 'z', '0']
    ], dtype=np.str_)
    G = np.array([[1, 0, 1, 0]], dtype=np.int32)
    gen = ThreadGenerator(ThreadGenerator.base_2er, G)

    flipped = gen.generate_data_thread(words, [1.0, 0.0])

    z_mask = (words == 'z')
    assert np.array_equal(flipped[z_mask], words[z_mask])

    non_z = np.logical_not(z_mask)
    expected_non_z = words.copy()
    expected_non_z[words == '0'] = '1'
    expected_non_z[words == '1'] = '0'
    assert np.array_equal(flipped[non_z], expected_non_z[non_z])


def test_generate_data_thread_ternary_flip_changes():
    words = np.array([
        ['0', '1', '2'],
        ['2', '0', '1']
    ], dtype=np.str_)
    G = np.array([[1, 0, 0]], dtype=np.int32)
    gen = ThreadGenerator(ThreadGenerator.base_3, G)

    result = gen.generate_data_thread(words, [1.0])

    assert np.all(result != words)
    assert set(np.unique(result)).issubset({'0', '1', '2'})


def test_generate_data_thread_no_change_zero_probs():
    words_bin = np.array([
        ['0', '1', '0'],
        ['1', '0', '1']
    ], dtype=np.str_)
    G = np.array([[1, 0, 1]], dtype=np.int32)
    gen_bin = ThreadGenerator(ThreadGenerator.base_2, G)
    same_bin = gen_bin.generate_data_thread(words_bin, [0.0])
    assert np.array_equal(same_bin, words_bin)

    words_ter = np.array([
        ['0', '1', '2'],
        ['1', '2', '0']
    ], dtype=np.str_)
    gen_ter = ThreadGenerator(ThreadGenerator.base_3, G)
    same_ter = gen_ter.generate_data_thread(words_ter, [0.0])
    assert np.array_equal(same_ter, words_ter)
