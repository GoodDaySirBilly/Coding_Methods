import numpy as np
from typing import List
import sys
import os

# Add parent directory to path to import GaluaField
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))
from GaluaField import GaluaField


def build_parity_check_matrix(
    code_length: int,
    exss_length: int,
    gf: GaluaField
) -> np.ndarray:
    """
    Return parity-check matrix H of linear block (n, k) code [r x n] size
    r = n - k
    Generates matrix using all non-zero elements of Galua Field (p^r)
    """
    r = exss_length
    n = code_length
    p = gf.chr  # Prime radix
    
    # Generate all non-zero elements of GF(p^r)
    # The GaluaField.values contains all elements, first element is zero
    non_zero_elements = gf.values[1:p**r]  # Skip the zero element
    
    # Create parity check matrix by taking first n non-zero elements as columns
    parity_check_matrix = np.zeros((r, n), dtype=np.int32)
    
    for i in range(min(n, len(non_zero_elements))):
        parity_check_matrix[:, i] = non_zero_elements[i]
    
    return parity_check_matrix


def build_generator_matrix(
    parity_check_matrix: np.ndarray,
    gf: GaluaField
) -> np.ndarray:
    """
    Return generator matrix G of linear block (n, k) code [k x n] size
    Structure: G = [I | P] where I is identity matrix and P is derived from H
    H has structure: H = [P^T | I]
    """
    r, n = parity_check_matrix.shape
    k = n - r
    p = gf.chr
    
    # Extract P^T from H (first k columns)
    P_transpose = parity_check_matrix[:, :k]
    
    # P is the transpose of P_transpose
    P = P_transpose.T
    
    # Create systematic generator matrix G = [I | P]
    generator_matrix = np.zeros((k, n), dtype=np.int32)
    
    # Identity part
    for i in range(k):
        generator_matrix[i, i] = 1
    
    # Parity part
    generator_matrix[:, k:] = P
    
    return generator_matrix


def syndrom(
    code_word: np.ndarray,
    parity_check_matrix: np.ndarray,
    gf: GaluaField
) -> np.ndarray:
    """Calculate syndrome for error detection"""
    return (code_word @ parity_check_matrix.T) % gf.chr


def strings_to_int_array(
    string_list: List[str],
    word_length: int = None,
    radix: int = 2
) -> np.ndarray:
    """
    Convert a list of strings (words of base alphabet) to 2D numpy array of integers.
    Supports radix 2, 3, and 5.
    """
    if radix not in [2, 3, 5]:
        raise ValueError(f"Unsupported radix: {radix}. Supported values: 2, 3, 5")
    
    if not string_list:
        return np.empty((0, 0), dtype=np.int32)
    
    # Determine word length
    if word_length is None:
        word_length = len(string_list[0])
    
    # Validate all strings have the same length
    for i, word in enumerate(string_list):
        if len(word) != word_length:
            raise ValueError(
                f"Word at index {i} has length {len(word)}, expected {word_length}. "
                f"Word: '{word}'"
            )
    
    # Convert to 2D integer array
    result = np.zeros((len(string_list), word_length), dtype=np.int32)
    
    valid_chars = {
        2: '01',
        3: '012',
        5: '01234'
    }[radix]
    
    for i, word in enumerate(string_list):
        for j, char in enumerate(word):
            if char not in valid_chars:
                raise ValueError(
                    f"Invalid character '{char}' in word '{word}'. "
                    f"Only characters from '{valid_chars}' are allowed for radix {radix}."
                )
            result[i, j] = int(char)
    
    return result


def int_array_to_strings(
    int_array: np.ndarray,
    radix: int = 2
) -> List[str]:
    """
    Convert a 2D numpy array of integers back to a list of strings.
    """
    if int_array.ndim != 2:
        raise ValueError(f"Expected 2D array, got {int_array.ndim}D array")
    
    # Validate values are within radix range
    if radix == 2:
        valid_range = [0, 1]
    elif radix == 3:
        valid_range = [0, 1, 2]
    elif radix == 5:
        valid_range = [0, 1, 2, 3, 4]
    else:
        raise ValueError(f"Unsupported radix: {radix}")
    
    if not np.all(np.isin(int_array, valid_range)):
        raise ValueError(f"Array contains values outside valid range for radix {radix}")
    
    string_list = []
    for row in int_array:
        word = ''.join(str(int(x)) for x in row)
        string_list.append(word)
    
    return string_list


def validate_array_radix(array: np.ndarray, radix: int):
    """Validate that array contains only values valid for the given radix"""
    if radix == 2:
        valid_values = [0, 1]
    elif radix == 3:
        valid_values = [0, 1, 2]
    elif radix == 5:
        valid_values = [0, 1, 2, 3, 4]
    else:
        raise ValueError(f"Unsupported radix: {radix}")
    
    if not np.all(np.isin(array, valid_values)):
        raise ValueError(f"Array contains values outside valid range for radix {radix}")


def get_primitive_polynomial(radix: int, order: int) -> np.ndarray:
    """
    Get primitive polynomial for given radix and order.
    For demonstration purposes, we use some common primitive polynomials.
    """
    if radix == 2:
        if order == 1:
            return np.array([1, 1], dtype=np.int32)  # x + 1
        elif order == 2:
            return np.array([1, 1, 1], dtype=np.int32)  # x^2 + x + 1
        elif order == 3:
            return np.array([1, 0, 1, 1], dtype=np.int32)  # x^3 + x + 1
        elif order == 4:
            return np.array([1, 0, 0, 1, 1], dtype=np.int32)  # x^4 + x + 1
    elif radix == 3:
        if order == 1:
            return np.array([1, 1], dtype=np.int32)  # x + 1
        elif order == 2:
            return np.array([1, 0, 1], dtype=np.int32)  # x^2 + 1
    elif radix == 5:
        if order == 1:
            return np.array([1, 1], dtype=np.int32)  # x + 1
        elif order == 2:
            return np.array([1, 0, 2], dtype=np.int32)  # x^2 + 2
    
    # Default: use a simple polynomial (may not be primitive for all cases)
    poly = np.zeros(order + 1, dtype=np.int32)
    poly[0] = 1
    poly[-1] = 1
    return poly