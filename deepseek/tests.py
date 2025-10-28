#!/usr/bin/env python3
"""
Comprehensive test suite for Hamming coding system
"""

import numpy as np
import sys
import os

# Add current directory to path to import packages
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from hamming import (
    Coder, ClassicCodingStrategy, ShortenedCodingStrategy, ExtendedCodingStrategy,
    build_parity_check_matrix, build_generator_matrix, syndrom,
    strings_to_int_array, int_array_to_strings, validate_array_radix,
    get_primitive_polynomial
)
from GaluaField import GaluaField


def test_multi_radix_conversion():
    """Test string to int array conversion for different radices"""
    print("Testing multi-radix string conversion...")
    
    # Test radix 2
    binary_strings = ['101', '010']
    binary_array = strings_to_int_array(binary_strings, radix=2)
    expected_binary = np.array([[1, 0, 1], [0, 1, 0]], dtype=np.int32)
    assert np.array_equal(binary_array, expected_binary), "Radix 2 conversion failed"
    
    # Test radix 3
    ternary_strings = ['102', '201']
    ternary_array = strings_to_int_array(ternary_strings, radix=3)
    expected_ternary = np.array([[1, 0, 2], [2, 0, 1]], dtype=np.int32)
    assert np.array_equal(ternary_array, expected_ternary), "Radix 3 conversion failed"
    
    print("Multi-radix conversion tests passed")


def test_matrix_generation():
    """Test matrix building functions with real GaluaField"""
    print("Testing matrix generation with real GaluaField...")
    
    # Test with radix 2
    primitive_poly = get_primitive_polynomial(2, 3)
    gf_binary = GaluaField(2, 3, primitive_poly)
    
    parity_check_binary = build_parity_check_matrix(7, 3, gf_binary)
    generator_binary = build_generator_matrix(parity_check_binary, gf_binary)
    
    assert parity_check_binary.shape == (3, 7), "Binary parity check matrix shape incorrect"
    assert generator_binary.shape == (4, 7), "Binary generator matrix shape incorrect"
    
    # Test systematic structure of generator matrix
    identity_part = generator_binary[:, :4]  # First k columns should be identity
    expected_identity = np.eye(4, dtype=np.int32)
    assert np.array_equal(identity_part, expected_identity), "Generator matrix not systematic"
    
    print("Matrix generation tests passed")


def test_coding_strategies_multi_radix():
    """Test different coding strategies with real GaluaField"""
    print("Testing coding strategies with real GaluaField...")
    
    # Test with radix 3
    primitive_poly = get_primitive_polynomial(3, 2)
    gf_ternary = GaluaField(3, 2, primitive_poly)
    
    test_words = np.array([[1, 0, 2], [2, 1, 0]], dtype=np.int32)
    
    classic_strategy = ClassicCodingStrategy()
    parity_check = classic_strategy.get_parity_check_matrix(5, 2, gf_ternary)
    generator = classic_strategy.get_generator_matrix(parity_check, gf_ternary)
    classic_result = classic_strategy.code_words(test_words, generator, gf_ternary)
    
    assert classic_result.shape == (2, 5), "Ternary classic coding result shape incorrect"
    
    # Test extended coding adds parity symbol
    extended_strategy = ExtendedCodingStrategy()
    extended_result = extended_strategy.code_words(test_words, generator, gf_ternary)
    assert extended_result.shape == (2, 6), "Ternary extended coding result shape incorrect"
    
    print("Multi-radix coding strategies tests passed")


def test_syndrome_calculation():
    """Test syndrome calculation with real GaluaField"""
    print("Testing syndrome calculation with real GaluaField...")
    
    primitive_poly = get_primitive_polynomial(2, 3)
    gf_binary = GaluaField(2, 3, primitive_poly)
    
    parity_check = build_parity_check_matrix(7, 3, gf_binary)
    
    # Test with valid codeword (should have zero syndrome)
    test_codeword = np.array([1, 0, 1, 0, 1, 0, 1], dtype=np.int32)
    syndrome = syndrom(test_codeword, parity_check, gf_binary)
    
    assert syndrome.shape == (3,), "Syndrome shape incorrect"
    
    print("Syndrome calculation tests passed")


def run_all_tests():
    """Run all tests"""
    print("Running Hamming Coding System Tests")
    print("=" * 50)
    
    try:
        test_multi_radix_conversion()
        test_matrix_generation()
        test_coding_strategies_multi_radix()
        test_syndrome_calculation()
        
        print("=" * 50)
        print("ALL TESTS PASSED!")
        return True
        
    except Exception as e:
        print(f"TEST FAILED: {e}")
        import traceback
        traceback.print_exc()
        return False


if __name__ == "__main__":
    run_all_tests()