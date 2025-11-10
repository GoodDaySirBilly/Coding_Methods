import numpy as np

from .Decoder import *

class ClassicDecoder(Decoder):

    def __init__(self,
        code_length: int, base_length: int, gf: GaluaField
    ):
        super().__init__(code_length, base_length, gf)


    def find_errors(self, words: np.ndarray):
        if words.size == 0:
            return np.empty((0, self.exss_length), dtype=int)

        H = self.parity_check_matrix
        q = self.gf.chr

        # words expected shape: [m, n]
        syndromes = (H @ words.T) % q
        return syndromes.T


    def detect_and_correct(self, words: np.ndarray): 
        if words.size == 0:
            return words

        # Support both numeric arrays and symbol arrays with 'z' for erasures
        if words.dtype.type is np.str_ or words.dtype.kind in ('U', 'S'):
            sym = words
            corrected = np.zeros(sym.shape, dtype=int)
            # decode row-wise with erasures
            H = self.parity_check_matrix
            q = self.gf.chr
            for i in range(sym.shape[0]):
                row = sym[i]
                er_mask = (row == 'z')

                known_int = np.zeros(row.shape, dtype=int)
                known_int[~er_mask] = np.array([int(c) for c in row[~er_mask]], dtype=int)
                s = (H @ known_int) % q
                if np.any(er_mask):
                    from linalg.code_matrix import solve_linear_mod
                    A = H[:, er_mask]
                    b = (-s) % q
                    x, ok = solve_linear_mod(A, b, q)
                    if ok:
                        fill = known_int.copy()
                        fill[er_mask] = x
                        corrected[i] = fill % q
                        continue

                y = known_int.copy()
                s = (H @ y) % q
                if np.all(s == 0):
                    corrected[i] = y
                    continue
                from linalg.code_matrix import find_error_with_scalar
                j, a = find_error_with_scalar(s, H, q)
                if j is not None and a is not None:
                    y[j] = (y[j] - a) % q
                corrected[i] = y
            return corrected

        corrected = words.copy()
        H = self.parity_check_matrix
        q = self.gf.chr

        # row-wise correction
        for i in range(corrected.shape[0]):
            y = corrected[i]
            s = (H @ y) % q

            # zero syndrome -> no error
            if np.all(s == 0):
                continue

            # General GF(q): find j
            from linalg.code_matrix import find_error_with_scalar
            j, a = find_error_with_scalar(s, H, q)
            if j is not None and a is not None:
                corrected[i, j] = (corrected[i, j] - a) % q

        return corrected


    def find_erasures(self, words: np.ndarray):
        if words.dtype.type is np.str_ or words.dtype.kind in ('U', 'S'):
            return words == 'z'
        return np.zeros_like(words, dtype=bool)