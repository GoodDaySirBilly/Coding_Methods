from .bch_decoder import BCHDecoder
import random

def run_bch():
    print("\nСоздание декодера БЧХ(31, 10, 5)")
    n = 31
    k = 10
    m = 5
    t = 5
    decoder = BCHDecoder(n, k, t, m)
    print(decoder.get_info())

    for example_num in range(1, 4):
            # Генерируем случайные позиции ошибок
            error_positions = random.sample(range(n), t)
            error_positions.sort()
            
            # Создаем кодовое слово (все нули)
            codeword = [0] * n
            
            # Добавляем ошибки
            received = codeword[:]
            for pos in error_positions: received[pos] = 1
            
            print(f"Исходное кодовое слово:")
            print(f"  {codeword}")
            
            print(f"\nПринятое слово с ошибками:")
            print(f"  {received}")
            
            # Декодируем
            decoded, num_errors = decoder.decode(received, algorithm='berlekamp-massey')
            
            print(f"\nРезультат декодирования:")
            print(f"  Исправлено ошибок: {num_errors}")
            print(f"  Декодированное слово:")
            print(f"  {decoded}")
            print()

