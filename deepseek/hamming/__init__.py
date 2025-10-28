"""
Hamming error correction coding system
"""

from .common import (
    build_parity_check_matrix,
    build_generator_matrix,
    syndrom,
    strings_to_int_array,
    int_array_to_strings,
    validate_array_radix,
    get_primitive_polynomial
)

from .coder import Coder
from .coder.strategies import (
    CodingStrategy,
    ClassicCodingStrategy,
    ShortenedCodingStrategy,
    ExtendedCodingStrategy
)

__all__ = [
    'Coder',
    'CodingStrategy',
    'ClassicCodingStrategy',
    'ShortenedCodingStrategy', 
    'ExtendedCodingStrategy',
    'build_parity_check_matrix',
    'build_generator_matrix',
    'syndrom',
    'strings_to_int_array',
    'int_array_to_strings',
    'validate_array_radix',
    'get_primitive_polynomial'
]