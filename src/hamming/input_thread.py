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

        pass


    def generate_words_thread(self, 
        words_num: int
    ) -> np.ndarray[np.str_, np.str_]:
        
        '''
        Generate threads of words (clear) made by linear combination of G rows
        Every word on every row -> size = [num_words, len_word]
        '''

        pass
        

    def generate_data_thread(self, 
        words_thread: np.ndarray[np.str_, np.str_],
        awgn_params: list
    ) -> np.ndarray[np.str_, np.str_]:
        
        '''
        Generate threads of data (nonclear) made by adding error with AWGN probability
        '''

        pass