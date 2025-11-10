import numpy as np


class ThreadGenerator:

    base_2 =      ['0', '1']
    base_2er =    ['0', '1', 'z']
    base_3 =      ['0', '1', '2']

    @staticmethod
    def make_base(q: int, with_erasure: bool = False) -> list[str]:
        '''
        Build symbol alphabet for arbitrary q >= 2.
        If with_erasure=True, appends 'z' symbol for erasures.
        '''
        if q < 2:
            raise ValueError("q must be >= 2")
        digits = [str(i) for i in range(q)]
        if with_erasure:
            digits = digits + ['z']
        return digits

    def __init__(self,
        base: list[str], code_length: int, base_length: int
    ) -> None:
        '''
        Create object of thread of data generator
        base can be base_2, base_3, base_2er
        '''

        self.base = base

        # determine symbol alphabet
        self._digits = [s for s in base if s != 'z']
        if len(self._digits) < 2:
            raise ValueError("Unsupported base length; expected q >= 2")

        self._q = len(self._digits)

        self._n, self._k = code_length, base_length


    def generate_words_thread(self, 
        words_num: int
    ) -> np.ndarray[np.str_, np.str_]:
        
        '''
        Generate threads of words (clear) made by linear combination of G rows
        Every word on every row -> size = [num_words, len_word]
        '''

        if words_num <= 0:
            return np.empty((0, self._n), dtype=np.str_)

        # random information vectors over GF(q)
        info_vectors = np.random.randint(0, self._q, size=(words_num, self._k), dtype=np.int32)

        return info_vectors
        

    def generate_data_thread(self, 
        words_thread: np.ndarray[np.str_, np.str_],
        awgn_params: list,
        one_error_per_word: bool = False,
        fixed_erasures_per_word: int | None = None
    ) -> np.ndarray[np.str_, np.str_]:
        
        '''
        Generate threads of data (nonclear) made by adding error with AWGN probability
        '''

        if words_thread.size == 0:
            return words_thread

        result = words_thread.copy().astype(np.str_)

        # Optionally enforce a fixed number of erasures per word (uses 'z')
        if fixed_erasures_per_word and 'z' in self.base:
            rows, cols = result.shape
            e = max(0, min(int(fixed_erasures_per_word), cols))
            if e > 0:
                for i in range(rows):
                    # choose e distinct positions
                    idxs = np.random.choice(cols, size=e, replace=False)
                    result[i, idxs] = 'z'

        # Deterministic mode: flip exactly one symbol per word
        if one_error_per_word:
            rows, cols = result.shape
            rng_cols = np.random.randint(0, cols, size=rows)

            if self._q == 2:
                for i in range(rows):
                    j = rng_cols[i]
                    # ensure not erasure
                    if result[i, j] == 'z':
                        # pick next non-z position
                        for jj in range(cols):
                            if result[i, jj] != 'z':
                                j = jj
                                break
                    result[i, j] = '1' if result[i, j] == '0' else '0'
                return result

            elif self._q == 3:
                steps = np.random.randint(1, 3, size=rows)  # +1 or +2 mod 3
                for i in range(rows):
                    j = rng_cols[i]
                    if result[i, j] == 'z':
                        for jj in range(cols):
                            if result[i, jj] != 'z':
                                j = jj
                                break
                    # map char to int 0/1/2
                    v = 0 if result[i, j] == self._digits[0] else (1 if result[i, j] == self._digits[1] else 2)
                    v = (v + steps[i]) % 3
                    result[i, j] = self._digits[v]
                return result

            elif self._q > 3:
                steps = np.random.randint(1, self._q, size=rows)  # +step mod q
                to_numeric = {s: i for i, s in enumerate(self._digits)}
                for i in range(rows):
                    j = rng_cols[i]
                    if result[i, j] == 'z':
                        for jj in range(cols):
                            if result[i, jj] != 'z':
                                j = jj
                                break
                    v = to_numeric[str(result[i, j])]
                    v = (v + steps[i]) % self._q
                    result[i, j] = self._digits[v]
                return result

        # probabilities
        p_flip = float(awgn_params[0]) if len(awgn_params) >= 1 else 0.0
        p_erase = float(awgn_params[1]) if (len(awgn_params) >= 2 and 'z' in self.base) else 0.0

        rows, cols = result.shape

        if 'z' in self.base and p_erase > 0.0:
            if p_erase >= 1.0:
                erase_mask = np.ones((rows, cols), dtype=bool)
            else:
                u_uniform = np.random.randn(rows, cols)
                erase_mask = u_uniform < p_erase
            result[erase_mask] = 'z'

        # flipping/errors for remaining symbols
        if self._q == 2 and p_flip > 0.0:
            if p_flip >= 1.0:
                flip_mask = np.ones((rows, cols), dtype=bool)
            else:
                u_uniform = np.random.randn(rows, cols)
                flip_mask = u_uniform < p_flip

            if 'z' in self.base:
                # do not flip erased symbols
                flip_mask &= (result != 'z')

            # flip
            zero_mask = (result == '0') & flip_mask
            one_mask = (result == '1') & flip_mask
            
            result[zero_mask] = '1'
            result[one_mask] = '0'

        elif self._q == 3 and p_flip > 0.0:

            # map to numeric indices 0,1,2
            from_index = np.array(self._digits, dtype=np.str_)

            numeric = np.zeros((rows, cols), dtype=np.int32)
            numeric[result == '1'] = 1
            numeric[result == '2'] = 2

            if p_flip >= 1.0:
                flip_mask = np.ones((rows, cols), dtype=bool)
            else:
                u_uniform = np.random.randn(rows, cols)
                flip_mask = u_uniform < p_flip

            # choose +1 or +2 (mod 3)
            step = np.random.randint(1, 3, size=(rows, cols))
            numeric_new = (numeric + step) % 3
            numeric[flip_mask] = numeric_new[flip_mask]

            # map back to symbols
            result = from_index[numeric]

        elif self._q > 3 and p_flip > 0.0:

            # map to numeric indices 0..q-1
            from_index = np.array(self._digits, dtype=np.str_)
            to_numeric = {s: i for i, s in enumerate(self._digits)}

            numeric = np.zeros((rows, cols), dtype=np.int32)
            for s, i in to_numeric.items():
                numeric[result == s] = i

            if p_flip >= 1.0:
                flip_mask = np.ones((rows, cols), dtype=bool)
            else:
                u_uniform = np.random.randn(rows, cols)
                flip_mask = u_uniform < p_flip

            if 'z' in self.base:
                flip_mask &= (result != 'z')

            # choose +step (mod q) where step in {1..q-1}
            step = np.random.randint(1, self._q, size=(rows, cols))
            numeric_new = (numeric + step) % self._q
            numeric[flip_mask] = numeric_new[flip_mask]

            # map back to symbols
            result = from_index[numeric]

        return result