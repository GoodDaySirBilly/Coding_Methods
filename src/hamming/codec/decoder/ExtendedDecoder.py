import numpy as np

from .Decoder import *

class ExtendedDecoder(Decoder):

    def __init__(self,
        code_length: int, base_length: int, gf: GaluaField
    ):
        super().__init__(code_length, base_length, gf)

        self._extend_code_length = code_length + 1

    @property
    def extend_code_length(self):
        return self._extend_code_length
        

    def find_errors(self, words: np.ndarray):
        # words shape [m, n+1]; parity is last column
        if words.size == 0:
            return np.empty((0, self.exss_length), dtype=int)
        data = words[:, :self.code_length]
        H = self.parity_check_matrix
        q = self.gf.chr
        syndromes = (H @ data.T) % q
        return syndromes.T


    def detect_and_correct(self, words: np.ndarray):
        if words.size == 0:
            return words

        # Handle erasures when symbols with 'z' are provided
        if words.dtype.type is np.str_ or words.dtype.kind in ('U', 'S'):
            sym = words
            n = self.code_length
            H = self.parity_check_matrix
            q = self.gf.chr
            corrected = np.zeros(sym.shape, dtype=int)

            for i in range(sym.shape[0]):
                row = sym[i]
                data_sym = row[:n]
                parity_sym = row[n]

                er_mask = (data_sym == 'z')
                data_int = np.zeros(data_sym.shape, dtype=int)
                data_int[~er_mask] = np.array([int(c) for c in data_sym[~er_mask]], dtype=int)

                # compute syndrome on known part
                s = (H @ data_int) % q
                if np.any(er_mask):
                    from linalg.code_matrix import solve_linear_mod
                    A = H[:, er_mask]
                    b = (-s) % q
                    x, ok = solve_linear_mod(A, b, q)
                    if ok:
                        data_int[er_mask] = x % q
                    # recompute syndrome after filling erasures
                    s = (H @ data_int) % q

                # handle parity symbol and possible single-error correction
                parity_int = int(parity_sym) if parity_sym != 'z' else 0
                total_parity = (np.sum(data_int) + parity_int) % q

                if np.all(s == 0):
                    # no data error; if parity inconsistent, fix parity
                    if total_parity != 0:
                        parity_int = (-np.sum(data_int)) % q
                else:
                    # non-zero syndrome: if parity inconsistent, try single data-symbol correction
                    if total_parity != 0:
                        from linalg.code_matrix import find_error_with_scalar
                        j, a = find_error_with_scalar(s, H, q)
                        if j is not None and a is not None:
                            data_int[j] = (data_int[j] - a) % q
                            # after correction, enforce parity consistency
                            parity_int = (-np.sum(data_int)) % q
                    # else: detected double-error; leave as-is

                corrected[i, :n] = data_int % q
                corrected[i, n] = parity_int % q
            return corrected

        corrected = words.copy()
        n = self.code_length
        H = self.parity_check_matrix
        q = self.gf.chr

        for i in range(corrected.shape[0]):
            y = corrected[i, :n]
            parity_bit = corrected[i, n]

            s = (H @ y) % q
            total_parity = (np.sum(y) + parity_bit) % q  # should be 0 for even parity in GF(2)

            if np.all(s == 0):
                if total_parity != 0:
                    corrected[i, n] = (-np.sum(y)) % q
                continue

            # non-zero syndrome
            from linalg.code_matrix import find_error_with_scalar
            j, a = find_error_with_scalar(s, H, q)
            if j is not None and a is not None and total_parity != 0:
                # single data-symbol error with magnitude a
                corrected[i, j] = (corrected[i, j] - a) % q
            else:
                # double-error detected (uncorrectable in extended Hamming)
                # leave as-is
                pass

        return corrected


    def find_erasures(self, words: np.ndarray):
        if words.dtype.type is np.str_ or words.dtype.kind in ('U', 'S'):
            return words == 'z'
        return np.zeros_like(words, dtype=bool)