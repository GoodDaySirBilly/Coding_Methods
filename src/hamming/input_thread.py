import numpy as np


class ThreadGenerator:

    base_2 =      ['0', '1']
    base_2er =    ['0', '1', 'z']
    base_3 =      ['0', '1', '2']

    def __init__(self,
        base: list[str],
        generator_matrix: np.ndarray[np.int32, np.int32],
    ) -> None:
        '''
        Create object of thread of data generator
        base can be base_2, base_3, base_2er
        '''

        self.base = base

        # determine symbol alphabet
        self._digits = [s for s in base if s != 'z']
        if len(self._digits) not in (2, 3):
            raise ValueError("Unsupported base length; expected 2 or 3")

        self._q = len(self._digits)

        # store generator matrix
        self._G = np.asarray(generator_matrix, dtype=np.int32)

        self._k, self._n = self._G.shape


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

        # linear combination over GF(q)
        codewords_numeric = (info_vectors @ self._G) % self._q

        # map numeric symbols to string symbols
        symbol_map = np.array(self._digits, dtype=np.str_)
        words_thread = symbol_map[codewords_numeric]

        return words_thread
        

    def generate_data_thread(self, 
        words_thread: np.ndarray[np.str_, np.str_],
        awgn_params: list
    ) -> np.ndarray[np.str_, np.str_]:
        
        '''
        Generate threads of data (nonclear) made by adding error with AWGN probability
        '''

        if words_thread.size == 0:
            return words_thread

        result = words_thread.copy().astype(np.str_)

        # probabilities
        p_flip = float(awgn_params[0]) if len(awgn_params) >= 1 else 0.0
        p_erase = float(awgn_params[1]) if (len(awgn_params) >= 2 and 'z' in self.base) else 0.0

        rows, cols = result.shape

        # handle erasures if base supports 'z'
        if 'z' in self.base and p_erase > 0.0:
            erase_mask = np.random.rand(rows, cols) < p_erase
            result[erase_mask] = 'z'

        # flipping/errors for remaining symbols
        if self._q == 2 and p_flip > 0.0:
            flip_mask = np.random.rand(rows, cols) < p_flip

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

            flip_mask = np.random.rand(rows, cols) < p_flip

            # choose +1 or +2 (mod 3)
            step = np.random.randint(1, 3, size=(rows, cols))
            numeric_new = (numeric + step) % 3
            numeric[flip_mask] = numeric_new[flip_mask]

            # map back to symbols
            result = from_index[numeric]

        return result