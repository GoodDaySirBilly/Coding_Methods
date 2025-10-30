from .code_matrix import *

class Hamming:

    code_types = ["classic", "shortened", "extended"]

    def __init__(self,
                 code_length: int,
                 base_length: int,
                 gf: GaluaField,
                 type="shortened"):
        self.code_length = code_length
        self.base_length = base_length
        self.exss_length = code_length - base_length
        self.type = type
        self.gf = gf

        self.H = build_parity_check_matrix(self.code_length, self.exss_length, gf)
        self.G = build_generator_matrix(self.H)

    # ------------------- Кодирование -------------------
    def code_words(self, words: np.ndarray) -> np.ndarray:
        match self.type:
            case "classic":
                return self.__classic_code(words)
            case "shortened":
                return self.__shortened_code(words)
            case "extended":
                return self.__extended_code(words)
            case _:
                raise ValueError(f"Unknown code type {self.type}")

    def __classic_code(self, words: np.ndarray) -> np.ndarray:
        info_vectors = words.copy().astype(np.int32)
        k, n = self.G.shape
        codewords = np.zeros((info_vectors.shape[0], n), dtype=np.int32)

        for idx, u in enumerate(info_vectors):
            c = np.zeros(n, dtype=np.int32)
            for j in range(n):
                sum_elem = 0
                for i in range(k):
                    sum_elem = (sum_elem + u[i] * self.G[i, j].value[0]) % self.gf.chr
                c[j] = sum_elem
            codewords[idx] = c
        return codewords.astype(str)

    def __shortened_code(self, words: np.ndarray) -> np.ndarray:
        return self.__classic_code(words)

    def __extended_code(self, words: np.ndarray) -> np.ndarray:
        codewords_numeric = self.__classic_code(words).astype(np.int32)
        parity_bits = np.sum(codewords_numeric, axis=1, keepdims=True) % self.gf.chr
        extended = np.hstack([codewords_numeric, parity_bits])
        return extended.astype(str)

    def decode_words(self, codewords: np.ndarray, mode: str = "error_correction") -> np.ndarray:
        """
        mode:
            "error_correction" - исправление одиночных ошибок
            "error_detection_and_correction" - исправление + обнаружение двойных ошибок
            "erasure_correction" - исправление стираний
        """
        match mode:
            case "error_correction":
                return self.__decode_errors(codewords)
            case "error_detection_and_correction":
                return self.__decode_detect_and_correct(codewords)
            case "erasure_correction":
                return self.__decode_erasures(codewords)
            case _:
                raise ValueError(f"Unknown decoding mode {mode}")

    def __decode_errors(self, codewords: np.ndarray) -> np.ndarray:
        codewords_numeric = codewords.astype(np.int32)
        decoded = []

        H_num = self.H_numeric()
        for c in codewords_numeric:
            s = (H_num @ c.T) % self.gf.chr
            error_pos = self.__syndrome_to_error_pos(s)
            if error_pos is not None and error_pos < len(c):
                c[error_pos] = (c[error_pos] + 1) % self.gf.chr
            decoded.append(c[:self.base_length])
        return np.array(decoded).astype(str)

    def __decode_detect_and_correct(self, codewords: np.ndarray) -> np.ndarray:
        codewords_numeric = codewords.astype(np.int32)
        decoded = []

        H_num = self.H_numeric()
        for c in codewords_numeric:
            s = (H_num @ c.T) % self.gf.chr
            error_pos = self.__syndrome_to_error_pos(s)
            if error_pos is None:
                # ошибок нет
                decoded.append(c[:self.base_length])
                continue
            elif error_pos < len(c):
                # исправляем одиночную ошибку
                c[error_pos] = (c[error_pos] + 1) % self.gf.chr
                decoded.append(c[:self.base_length])
            else:
                # обнаружена двойная ошибка, которую нельзя исправить
                decoded.append(np.array(["?"]*self.base_length))
        return np.array(decoded)

    def __decode_erasures(self, codewords: np.ndarray, erasure_positions: list = None) -> np.ndarray:
        """
        erasure_positions: список списков с индексами стираний для каждого слова
        """
        codewords_numeric = codewords.astype(np.int32)
        decoded = []

        H_num = self.H_numeric()
        for idx, c in enumerate(codewords_numeric):
            unknowns = erasure_positions[idx] if erasure_positions else []
            if not unknowns:
                decoded.append(c[:self.base_length])
                continue
            # Решаем H * c^T = 0 для неизвестных
            s = (H_num @ c.T) % self.gf.chr
            # Простая реализация для одного стирания
            if len(unknowns) == 1:
                pos = unknowns[0]
                # сумма известных битов
                sum_known = sum(H_num[:, j]*c[j] for j in range(len(c)) if j != pos) % self.gf.chr
                # вычисляем стирание
                c[pos] = (-sum_known.sum()) % self.gf.chr
            decoded.append(c[:self.base_length])
        return np.array(decoded).astype(str)

    def __syndrome_to_error_pos(self, syndrome: np.ndarray) -> int | None:
        pos = 0
        for i, bit in enumerate(syndrome):
            pos += bit * (2 ** i)
        if pos == 0:
            return None
        return pos - 1

    def H_numeric(self) -> np.ndarray:
        r, n = self.H.shape
        H_num = np.zeros((r, n), dtype=np.int32)
        for i in range(r):
            for j in range(n):
                H_num[i, j] = self.H[i, j].value[0]
        return H_num

