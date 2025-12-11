import numpy as np

class Coder:
    def __init__(self, k, n, vect):
        self.k = k
        self.n = n
        self.vect = vect
        
        self.generator_matrix = np.zeros((k, n), dtype=int)
        self.generator_matrix[0, :len(vect)] = vect
        for i in range(1, k):
            self.generator_matrix[i] = np.roll(self.generator_matrix[i - 1], 1)
    
    def coding(self, words):
        return words @ self.generator_matrix % 2
