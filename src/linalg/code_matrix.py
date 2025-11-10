import numpy as np

from galua.GaluaField import GaluaField
from galua.GaluaElement import GaluaElement


'''
File that has functions to build matricies by code params for another purposes 
'''

def build_parity_check_matrix(
    code_length: int, # n
    exss_length: int, # r
    gf: GaluaField
) -> np.ndarray[np.int32, np.int32]:
    
    '''
    Return parity-check matrix H of linear block (n, k) code [r x n] size
    r = n - k
    '''

    r = exss_length
    n = code_length
    q = gf.chr

    # Work on a copy to avoid mutating gf.values globally across coder/decoder builds
    H_full = gf.values[1:, :].copy()  # shape: (q^r - 1) x r

    if q == 2:
        # Legacy binary layout that existing tests rely on
        H = H_full
        H[0:exss_length] = np.flip(H[0:exss_length], axis=1)
        H[exss_length:] = np.flip(H[exss_length:], axis=0)

        H = H.T
        H = np.flip(H, axis = 0)
        H = np.flip(H, axis = 1)
        H[:, -exss_length:] = np.eye(exss_length, dtype=int)
        return H

    # For q>2, build the full projective set of columns over F_q^r
    # Enumerate all non-zero vectors in F_q^r, normalize by the first non-zero coordinate to 1,
    # and keep one representative per 1-D subspace.
    seen: set[tuple[int, ...]] = set()
    proj_cols: list[np.ndarray] = []
    # generate all r-length vectors over [0..q-1] except the all-zero vector
    # iterate in lexicographic order for determinism
    for digits in np.ndindex(*(q for _ in range(r))):
        v = np.array(digits, dtype=int) % q
        if np.all(v == 0):
            continue
        nz = np.where(v != 0)[0]
        i0 = nz[0]
        inv = pow(int(v[i0]) % q, q - 2, q)
        v_norm = (v * inv) % q
        key = tuple(int(x) for x in v_norm.tolist())
        if key in seen:
            continue
        seen.add(key)
        proj_cols.append(v_norm.astype(int))
        if len(proj_cols) == n:
            break

    # If for any reason we collected fewer than n, pad with distinct standard basis and zeros (shouldn't happen)
    if len(proj_cols) < n:
        basis = [np.eye(r, dtype=int)[:, i] for i in range(r)]
        for b in basis:
            if len(proj_cols) == n:
                break
            key = tuple(int(x) for x in b.tolist())
            if key not in seen:
                proj_cols.append(b.copy())
                seen.add(key)
        while len(proj_cols) < n:
            proj_cols.append(np.zeros(r, dtype=int))

    # Reorder columns to systematic form: last r columns are the identity vectors e_0..e_{r-1}
    identity_cols = [tuple(int(x) for x in np.eye(r, dtype=int)[:, i].tolist()) for i in range(r)]
    non_identity = [c for c in proj_cols if tuple(int(x) for x in c.tolist()) not in identity_cols]
    # Ensure we have exactly n - r non-identity columns first, then the r identity columns
    ordered_cols: list[np.ndarray] = []
    ordered_cols.extend(non_identity[: max(0, n - r)])
    ordered_cols.extend([np.eye(r, dtype=int)[:, i] for i in range(r)])

    H = np.zeros((r, n), dtype=int)
    for j, col in enumerate(ordered_cols):
        H[:, j] = col % q

    return H


def build_generator_matrix(
    parity_check_matrix: np.ndarray[np.int32, np.int32] # H
) -> np.ndarray[np.int32, np.int32]:
    
    '''
    Return generator matrix G of linear block (n, k) code [k x n] size
    '''

    H = parity_check_matrix
    r, n = H.shape
    k = n - r

    # For systematic form, assume H = [P^T | I_r] with shape r x n
    # Then G = [I_k | -P] with shape k x n (note: minus is essential for q>2)
    P = H[:, :k].T

    G = np.concatenate([np.eye(k, dtype=int), (-P) %  (np.max(H) + 1 if np.max(H) > 1 else 2)], axis=1)

    return G

def syndrom(
    code_word: np.ndarray[np.int32],
    parity_check_matrix: np.ndarray[np.int32, np.int32]
) -> np.ndarray[np.int32]:

    return parity_check_matrix @ code_word

def find_error(
    syndrom: np.ndarray[np.int32],
    parity_check_matrix: np.ndarray[np.int32, np.int32]
) -> int:
    
    equal_columns_mask = np.all(
        parity_check_matrix == syndrom[:, np.newaxis], axis=0
    )

    indices_of_equal_columns = np.where(equal_columns_mask)[0]

    return indices_of_equal_columns


def find_error_with_scalar(
    syndrom: np.ndarray, parity_check_matrix: np.ndarray, q: int
) -> tuple[int | None, int | None]:
    """
    Find column j and scalar a in GF(q) such that syndrom == a * H[:, j] (mod q).
    Returns (j, a) or (None, None) if not found or zero syndrome.
    """
    s = np.array(syndrom, dtype=int) % q
    if np.all(s == 0):
        return None, None
    H = np.array(parity_check_matrix, dtype=int) % q
    r, n = H.shape
    for j in range(n):
        h = H[:, j]
        # find first non-zero component in h to compute candidate a
        nz = np.where(h % q != 0)[0]
        if nz.size == 0:
            continue
        i0 = nz[0]
        inv = pow(int(h[i0]) % q, q - 2, q)  # q assumed prime characteristic
        a = (int(s[i0]) * inv) % q
        if np.all((a * h) % q == s % q):
            return j, int(a)
    return None, None


def _modinv(a: int, q: int) -> int:
    a = a % q
    if a == 0:
        raise ZeroDivisionError("No modular inverse for 0")
    return pow(a, q - 2, q)


def solve_linear_mod(
    A: np.ndarray, b: np.ndarray, q: int
) -> tuple[np.ndarray | None, bool]:
    """
    Solve A x = b over GF(q).
    Returns (x, ok) where ok=False if no unique solution.
    """
    if A.size == 0:
        return np.array([], dtype=int), True
    A = (A % q).astype(int).copy()
    b = (b % q).astype(int).copy()

    r, c = A.shape
    # augment
    aug = np.concatenate([A, b.reshape(-1, 1)], axis=1)

    row = 0
    pivots: list[int] = []
    for col in range(c):
        # find pivot
        pivot_row = None
        for rr in range(row, r):
            if aug[rr, col] % q != 0:
                pivot_row = rr
                break
        if pivot_row is None:
            continue
        # swap
        if pivot_row != row:
            tmp = aug[row, :].copy()
            aug[row, :] = aug[pivot_row, :]
            aug[pivot_row, :] = tmp
        # normalize
        inv = _modinv(int(aug[row, col]), q)
        aug[row, :] = (aug[row, :] * inv) % q
        # eliminate other rows
        for rr in range(r):
            if rr == row:
                continue
            factor = aug[rr, col] % q
            if factor != 0:
                aug[rr, :] = (aug[rr, :] - factor * aug[row, :]) % q
        pivots.append(col)
        row += 1
        if row == r:
            break

    # check consistency
    # any row with all-zero A part but non-zero RHS -> inconsistent
    for rr in range(r):
        if np.all(aug[rr, :c] % q == 0) and (aug[rr, c] % q != 0):
            return None, False

    # unique solution only if number of pivots == number of variables
    if len(pivots) != c:
        return None, False

    x = aug[:c, c] % q  # after RREF, top c rows correspond to variables
    return x.astype(int), True