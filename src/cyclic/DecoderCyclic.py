import numpy as np

class Decoder:
    def __init__(self, k, n, vect):
        self.k = k
        self.n = n
        self.vect = vect
        self.r = n - k

        self.check_matrix = np.zeros((self.r, n), dtype=int)
        self.check_matrix[0, -len(vect):] = vect
        for i in range(1, self.r):
            self.check_matrix[i] = np.roll(self.check_matrix[i - 1], -1)

    def detect_and_correct(self, words: np.ndarray):
        if words.size == 0:
            return words

        if words.dtype.type is np.str_ or words.dtype.kind in ('U', 'S'):
            sym = words
            corrected = np.zeros(sym.shape, dtype=int)
            H = self.check_matrix
            q = 2
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
        H = self.check_matrix
        q = 2

        for i in range(corrected.shape[0]):
            y = corrected[i]
            s = (H @ y) % q

            if np.all(s == 0):
                continue

            from linalg.code_matrix import find_error_with_scalar
            j, a = find_error_with_scalar(s, H, q)
            if j is not None and a is not None:
                corrected[i, j] = (corrected[i, j] - a) % q

        return corrected