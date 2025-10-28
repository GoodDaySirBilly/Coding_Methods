from str_interface import Coder

class ShortenedCoder(Coder):
    def code_word(self):
        return "I am shortened coder - single word"
    
    def code_word_array(self):
        return "I am shortened coder - array of words"