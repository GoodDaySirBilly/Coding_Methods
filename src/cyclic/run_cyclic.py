from .CoderCyclic import Coder
from .DecoderCyclic import Decoder
from .cyclic_check import run_cyclic_check
from hamming.ThreadGenerator import ThreadGenerator

def run_cyclic():
    k = 8
    n = 17
    q = 2
    r = n - k
    poly = [1, 0, 0, 1, 1, 1, 1, 0, 0, 1]
    coder = Coder(k, n, poly)
    #coder = Coder(k, n, [1, 0, 1, 1])

    print(f"---- Generator matrix {k} x {n} ----")
    print(coder.generator_matrix)

    base = ThreadGenerator.make_base(q, with_erasure=True)
    gen = ThreadGenerator(base, n, k)
    words = gen.generate_words_thread(10)

    coded = coder.coding(words)
    noisy = gen.generate_data_thread(
        coded.astype(str),
        [0.0, 0.0],         
        one_error_per_word=True, 
        fixed_erasures_per_word=0 
    )

    received = noisy
    received_int = received.astype(int)
    decoder = Decoder(k, n, poly)
    print(f"\n\n---- Check matrix {r} x {n} ----")
    print(decoder.check_matrix)
    print()
    decoded = decoder.detect_and_correct(received_int)
    print("   info  |       coded       |      decoded ")
    for i in range(words.shape[0]): 
        s_info = ''.join(map(str, words[i].tolist()))
        s_code = ''.join(map(str, coded[i].tolist()))
        s_dec = ''.join(map(str, decoded[i].tolist()))
        print(f"{s_info} | {s_code} |{s_dec}")
    
    run_cyclic_check(n, k, poly)