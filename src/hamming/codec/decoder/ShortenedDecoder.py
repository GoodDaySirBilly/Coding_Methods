import numpy as np

from .Decoder import *

class ShortenedDecoder(Decoder):

    def __init__(self,
        code_length: int, base_length: int, gf: GaluaField,
        short_code_length: int, short_base_length: int
    ):
        super().__init__(code_length, base_length, gf)

        self._short_code_length = short_code_length
        self._short_base_length = short_base_length

    @property 
    def short_code_length(self):
        return self._short_code_length

    @property 
    def short_base_length(self):
        return self._short_base_length
    

    def find_errors(self, words: np.ndarray):
        # Embed shortened codewords by prefixing zeros for the shortened columns
        if words.size == 0:
            return np.empty((0, self.exss_length), dtype=int)

        n_full = self.code_length
        n_short_removed = self.short_code_length

        embedded = np.zeros((words.shape[0], n_full), dtype=int)
        embedded[:, n_short_removed:] = words

        H = self.parity_check_matrix
        q = self.gf.chr
        syndromes = (H @ embedded.T) % q
        return syndromes.T


    def detect_and_correct(self, words: np.ndarray): 
        if words.size == 0:
            return words

        n_full = self.code_length
        n_short_removed = self.short_code_length
        q = self.gf.chr
        H = self.parity_check_matrix

        # Handle erasures: if words contain 'z', solve for transmitted positions
        if words.dtype.type is np.str_ or words.dtype.kind in ('U', 'S'):
            sym = words
            corrected_full = np.zeros((words.shape[0], n_full), dtype=int)
            for i in range(sym.shape[0]):
                row = sym[i]
                
                y = np.zeros(n_full, dtype=int)
                seg = row
                er_mask_short = (seg == 'z')
                known_short = np.zeros(seg.shape, dtype=int)
                known_short[~(er_mask_short)] = np.array([int(c) for c in seg[~er_mask_short]], dtype=int)
                y[n_short_removed:] = known_short

                er_full_mask = np.zeros(n_full, dtype=bool)
                er_full_mask[n_short_removed:] = er_mask_short
                s = (H @ y) % q

                if np.any(er_full_mask):
                    from linalg.code_matrix import solve_linear_mod
                    A = H[:, er_full_mask]
                    b = (-s) % q
                    x, ok = solve_linear_mod(A, b, q)
                    if ok:
                        y[er_full_mask] = x % q
                corrected_full[i] = y

            return corrected_full[:, n_short_removed:]

        corrected_full = np.zeros((words.shape[0], n_full), dtype=int)
        corrected_full[:, n_short_removed:] = words

        for i in range(corrected_full.shape[0]):
            y = corrected_full[i]
            s = (H @ y) % q
            if np.all(s == 0):
                continue
            from linalg.code_matrix import find_error_with_scalar
            j, a = find_error_with_scalar(s, H, q)
            if j is not None and a is not None:
                # only transmitted positions can be flipped
                if j >= n_short_removed:
                    corrected_full[i, j] = (corrected_full[i, j] - a) % q
                else:
                    # error localized to a punctured position; cannot correct
                    pass

        # return only shortened part
        return corrected_full[:, n_short_removed:]


    def find_erasures(self, words: np.ndarray):
        if words.dtype.type is np.str_ or words.dtype.kind in ('U', 'S'):
            return words == 'z'
        return np.zeros_like(words, dtype=bool)