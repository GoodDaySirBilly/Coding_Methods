import numpy as np
from src.galua.GaluaField import GaluaField
from src.hamming.ham_coder import Hamming  # твой класс Hamming

def main():
    gf = GaluaField(chr=2, orp=1, pol=np.array([1,1], dtype=np.int32))

    n = 55
    k = 49
    num_words = 5

    hamming_code = Hamming(code_length=n, base_length=k, gf=gf, type="shortened")

    H_num = hamming_code.H_numeric()
    print("\nПроверочная матрица H (первые 10 строк и столбцов):")
    print(H_num[:10, :10])

    k_rows, n_cols = hamming_code.G.shape
    G_num = np.zeros((k_rows, n_cols), dtype=np.int32)
    for i in range(k_rows):
        for j in range(n_cols):
            G_num[i, j] = hamming_code.G[i, j].value[0]

    print("\nПорождающая матрица G (первые 10 строк и столбцов):")
    print(G_num)

    info_words = np.random.randint(0, 2, size=(num_words, k))
    print("\nИнформационные слова:")
    print(info_words)

    codewords = hamming_code.code_words(info_words)
    print("\nКодированные слова:")
    print(codewords)

    decoded_words = hamming_code.decode_words(codewords, mode="error_correction")
    print("\nДекодированные слова (исправление ошибок):")
    print(decoded_words)

    print("\nПроверка совпадения с исходными информационными словами:")
    for i in range(num_words):
        match = "OK" if np.array_equal(info_words[i], decoded_words[i].astype(np.int32)) else "ERROR"
        print(f"Слово {i+1}: {match}")

if __name__ == "__main__":
    main()
