#!/usr/bin/env python3
"""
Demonstration scenarios for Hamming coding system with parameter support
"""

import numpy as np
import sys
import os
import argparse

# Add current directory to path to import packages
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from hamming import (
    Coder, ClassicCodingStrategy, ShortenedCodingStrategy, ExtendedCodingStrategy,
    strings_to_int_array, int_array_to_strings, get_primitive_polynomial
)
from GaluaField import GaluaField


def scenario_classic(args):
    """Scenario: Classic Hamming Code"""
    print(f"Scenario: Classic Hamming Code ({args.code_length},{args.base_length})")
    print("=" * 50)
    
    # Calculate field parameters
    r = args.code_length - args.base_length
    primitive_poly = get_primitive_polynomial(args.radix, r)
    
    # Create real GaluaField
    gf = GaluaField(args.radix, r, primitive_poly)
    
    # Create classic Hamming coder
    coder = Coder(args.code_length, args.base_length, gf, ClassicCodingStrategy())
    
    # Generate input data based on parameters
    input_strings = generate_input_strings(args.base_length, args.radix, args.sample_count)
    print(f"Input words: {input_strings}")
    
    # Convert to numeric
    input_array = strings_to_int_array(input_strings, radix=args.radix)
    print(f"Input array shape: {input_array.shape}")
    
    # Encode
    encoded_array = coder.code_words(input_array)
    encoded_strings = int_array_to_strings(encoded_array, radix=args.radix)
    
    print(f"Encoded words: {encoded_strings}")
    print(f"Generator matrix shape: {coder.generator_matrix_prop.shape}")
    print(f"Parity check matrix shape: {coder.parity_check_matrix_prop.shape}")
    
    # Verify systematic structure
    identity_part = coder.generator_matrix_prop[:, :args.base_length]
    parity_part = coder.generator_matrix_prop[:, args.base_length:]
    print(f"Identity part of G (first {args.base_length} columns):")
    print(identity_part)
    print(f"Parity part of G (last {args.code_length - args.base_length} columns):")
    print(parity_part)
    
    # Demonstrate syndrome calculation if requested
    if args.show_syndrome:
        test_code_word = encoded_array[0]
        syndrome = coder.calculate_syndrome(test_code_word)
        print(f"Syndrome for first codeword: {syndrome}")
    
    print("Classic Hamming scenario completed")


def scenario_shortened(args):
    """Scenario: Shortened Hamming Code"""
    print(f"Scenario: Shortened Hamming Code ({args.code_length},{args.base_length})")
    print("=" * 50)
    
    # Calculate field parameters
    r = args.code_length - args.base_length
    primitive_poly = get_primitive_polynomial(args.radix, r)
    
    # Create real GaluaField
    gf = GaluaField(args.radix, r, primitive_poly)
    
    # Create shortened Hamming coder
    coder = Coder(args.code_length, args.base_length, gf, ShortenedCodingStrategy())
    
    # Generate input data
    input_strings = generate_input_strings(args.base_length, args.radix, args.sample_count)
    print(f"Input words: {input_strings}")
    
    # Convert to numeric
    input_array = strings_to_int_array(input_strings, radix=args.radix)
    
    # Encode
    encoded_array = coder.code_words(input_array)
    encoded_strings = int_array_to_strings(encoded_array, radix=args.radix)
    
    print(f"Encoded words: {encoded_strings}")
    print(f"Generator matrix shape: {coder.generator_matrix_prop.shape}")
    print(f"Parity check matrix shape: {coder.parity_check_matrix_prop.shape}")
    
    print("Shortened Hamming scenario completed")


def scenario_extended(args):
    """Scenario: Extended Hamming Code"""
    print(f"Scenario: Extended Hamming Code ({args.code_length},{args.base_length})")
    print("=" * 50)
    
    # For extended codes, we use the base code parameters
    base_code_length = args.code_length - 1
    base_base_length = args.base_length
    r = base_code_length - base_base_length
    primitive_poly = get_primitive_polynomial(args.radix, r)
    
    # Create real GaluaField
    gf = GaluaField(args.radix, r, primitive_poly)
    
    # Create extended Hamming coder
    coder = Coder(base_code_length, base_base_length, gf, ExtendedCodingStrategy())
    
    # Generate input data
    input_strings = generate_input_strings(base_base_length, args.radix, args.sample_count)
    print(f"Input words: {input_strings}")
    
    # Convert and encode
    input_array = strings_to_int_array(input_strings, radix=args.radix)
    encoded_array = coder.code_words(input_array)
    encoded_strings = int_array_to_strings(encoded_array, radix=args.radix)
    
    print(f"Encoded words: {encoded_strings}")
    print(f"Extended from {input_array.shape[1]} to {encoded_array.shape[1]} symbols")
    print(f"Generator matrix shape: {coder.generator_matrix_prop.shape}")
    
    print("Extended Hamming scenario completed")


def scenario_ternary(args):
    """Scenario: Ternary Hamming Code"""
    print(f"Scenario: Ternary Hamming Code ({args.code_length},{args.base_length})")
    print("=" * 50)
    
    # Calculate field parameters
    r = args.code_length - args.base_length
    primitive_poly = get_primitive_polynomial(3, r)  # Always use radix 3 for ternary
    
    # Create real GaluaField
    gf = GaluaField(3, r, primitive_poly)
    
    # Create ternary Hamming coder
    coder = Coder(args.code_length, args.base_length, gf, ClassicCodingStrategy())
    
    # Generate input data
    input_strings = generate_input_strings(args.base_length, 3, args.sample_count)
    print(f"Input words: {input_strings}")
    
    # Convert to numeric
    input_array = strings_to_int_array(input_strings, radix=3)
    
    # Encode
    encoded_array = coder.code_words(input_array)
    encoded_strings = int_array_to_strings(encoded_array, radix=3)
    
    print(f"Encoded words: {encoded_strings}")
    print(f"Generator matrix shape: {coder.generator_matrix_prop.shape}")
    print(coder.generator_matrix_prop)
    
    
    print("Ternary Hamming scenario completed")


def generate_input_strings(word_length, radix, count=2):
    """Generate sample input strings for demonstration"""
    strings = []
    for i in range(count):
        # Create patterns that are easy to recognize
        if radix == 2:
            # Binary patterns
            pattern = format(i % (2 ** word_length), f'0{word_length}b')
        elif radix == 3:
            # Ternary patterns (cyclic)
            pattern = ''
            for j in range(word_length):
                pattern += str((i + j) % 3)
        else:
            # General radix patterns
            pattern = ''
            for j in range(word_length):
                pattern += str((i + j) % radix)
        strings.append(pattern)
    return strings


def parse_scenario_arguments():
    """Parse command line arguments for scenarios"""
    parser = argparse.ArgumentParser(description='Run Hamming coding scenarios')
    
    # Scenario selection
    parser.add_argument('scenario', 
                       choices=['classic', 'shortened', 'extended', 'ternary'],
                       help='Scenario to run')
    
    # Code parameters
    parser.add_argument('--code_length', '-n', type=int, default=7,
                       help='Code length (n) - total symbols in codeword')
    parser.add_argument('--base_length', '-k', type=int, default=4,
                       help='Base length (k) - information symbols')
    parser.add_argument('--radix', '-r', type=int, choices=[2, 3, 5], default=2,
                       help='Prime radix for the field (default: 2)')
    
    # Additional parameters
    parser.add_argument('--sample_count', '-s', type=int, default=2,
                       help='Number of sample words to encode (default: 2)')
    parser.add_argument('--show_syndrome', action='store_true',
                       help='Show syndrome calculation for first codeword')
    
    return parser.parse_args()


def run_scenario_with_args(scenario_name, code_length=None, base_length=None, 
                          radix=None, sample_count=None, show_syndrome=None):
    """Run a specific scenario with given parameters"""
    # Create args object
    class Args:
        def __init__(self):
            self.scenario = scenario_name
            self.code_length = code_length or 7
            self.base_length = base_length or 4
            self.radix = radix or 2
            self.sample_count = sample_count or 2
            self.show_syndrome = show_syndrome or False
    
    args = Args()
    
    scenarios = {
        "classic": scenario_classic,
        "shortened": scenario_shortened,
        "extended": scenario_extended,
        "ternary": scenario_ternary
    }
    
    if scenario_name in scenarios:
        print()
        scenarios[scenario_name](args)
        print()
    else:
        print(f"Unknown scenario: {scenario_name}")
        print("Available scenarios: classic, shortened, ternary, extended")


def run_all_scenarios():
    """Run all demonstration scenarios with default parameters"""
    print("Hamming Coding System Demonstration Scenarios")
    print("=" * 50)
    
    # Run each scenario with sensible defaults
    run_scenario_with_args("classic", 7, 4, 2, 3)
    run_scenario_with_args("shortened", 6, 4, 2, 2)
    run_scenario_with_args("ternary", 4, 2, 3, 2)
    run_scenario_with_args("extended", 8, 4, 2, 2, True)
    
    print("=" * 50)
    print("All demonstration scenarios completed!")


if __name__ == "__main__":
    if len(sys.argv) > 1 and not sys.argv[1].startswith('-'):
        # Parse command line arguments
        args = parse_scenario_arguments()
        run_scenario_with_args(
            args.scenario, 
            args.code_length, 
            args.base_length, 
            args.radix, 
            args.sample_count, 
            args.show_syndrome
        )
    else:
        run_all_scenarios()