import str_1, str_2


def main():
    
    a = str_1.ClassicCoder(5, 4)
    b = str_2.ShortenedCoder(7, 8)

    print(a.code_word())
    print(a.code_word_array())
    print(b.code_word())
    print(b.code_word_array())

    print(a.code_length)
    print(a.base_length)
    
    print(b.code_length)
    print(b.base_length)

if __name__ == '__main__':
    main()