import numpy as np

from linalg.code_matrix import *

class HammingCodec:

    code_types = ["classic", "shortened", "extended"]

    def __init__(self,
        code_type: str,
        code_length: int,
        base_length: int,
        gf: GaluaField,
        short_code_length: int | None = None,
        short_base_length: int | None = None
    ) -> None:
        if code_type not in self.code_types:
            raise ValueError(f"Unsupported code_type: {code_type}")

        self._type = code_type
        self._n = code_length
        self._k = base_length
        self._gf = gf

        if code_type == "classic":
            from .coder.ClassicCoder import ClassicCoder
            from .decoder.ClassicDecoder import ClassicDecoder
            self.coder = ClassicCoder(code_length, base_length, gf)
            self.decoder = ClassicDecoder(code_length, base_length, gf)

        elif code_type == "extended":
            from .coder.ExtendedCoder import ExtendedCoder
            from .decoder.ExtendedDecoder import ExtendedDecoder
            self.coder = ExtendedCoder(code_length, base_length, gf)
            self.decoder = ExtendedDecoder(code_length, base_length, gf)

        elif code_type == "shortened":
            from .coder.ShortenedCoder import ShortenedCoder
            from .decoder.ShortenedDecoder import ShortenedDecoder
            self.coder = ShortenedCoder(code_length, base_length, gf, short_code_length, short_base_length)
            self.decoder = ShortenedDecoder(code_length, base_length, gf, short_code_length, short_base_length)
            self._short_n = code_length - short_code_length
            self._short_k = base_length - short_code_length
        else:
            raise ValueError(f"Unsupported code_type: {code_type}")

    def encode(self, info_words: np.ndarray) -> np.ndarray:
        return self.coder.code_words(info_words.astype(int))

    def decode(self, received: np.ndarray) -> tuple[np.ndarray, np.ndarray]:
        """
        Returns (decoded_info, corrected_codewords)
        """
        corrected = self.decoder.detect_and_correct(received)

        if self._type == "classic":
            info = corrected[:, :self._k]
        elif self._type == "extended":
            info = corrected[:, :self._k]  # parity bit last, discard
        elif self._type == "shortened":
            info = corrected[:, :self._short_k]
        else:
            raise RuntimeError("Unknown codec type")

        return info, corrected
