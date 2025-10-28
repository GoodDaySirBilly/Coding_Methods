#!/usr/bin/env python3
"""
Main entry point for Hamming coding system
Run tests or scenarios based on command line arguments
"""

import sys
import os
import argparse

def main():
    parser = argparse.ArgumentParser(description='Hamming Coding System')
    subparsers = parser.add_subparsers(dest='command', help='Command to run')
    
    # Tests command
    tests_parser = subparsers.add_parser('tests', help='Run all tests')
    
    # Scenario command with parameters
    scenario_parser = subparsers.add_parser('scenario', help='Run demonstration scenarios')
    scenario_parser.add_argument('scenario_name', 
                               choices=['classic', 'shortened', 'extended', 'ternary'],
                               help='Scenario to run')
    scenario_parser.add_argument('--code_length', '-n', type=int, default=7,
                               help='Code length (n) - total symbols in codeword')
    scenario_parser.add_argument('--base_length', '-k', type=int, default=4,
                               help='Base length (k) - information symbols')
    scenario_parser.add_argument('--radix', '-r', type=int, choices=[2, 3, 5], default=2,
                               help='Prime radix for the field')
    scenario_parser.add_argument('--sample_count', '-s', type=int, default=2,
                               help='Number of sample words to encode')
    scenario_parser.add_argument('--show_syndrome', action='store_true',
                               help='Show syndrome calculation')
    
    # Parse arguments
    args = parser.parse_args()
    
    if args.command == 'tests':
        from tests import run_all_tests
        success = run_all_tests()
        sys.exit(0 if success else 1)
    
    elif args.command == 'scenario':
        from scenario_n import run_scenario_with_args
        run_scenario_with_args(
            args.scenario_name,
            args.code_length,
            args.base_length, 
            args.radix,
            args.sample_count,
            args.show_syndrome
        )
    
    else:
        # Default: run all scenarios
        from scenario_n import run_all_scenarios
        run_all_scenarios()

if __name__ == "__main__":
    main()