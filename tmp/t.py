from abc import ABC, abstractmethod

class Coder(ABC):
    def __init__(self, code_length, base_length):
        self.code_length = code_length
        self.base_length = base_length
    
    @abstractmethod
    def code_word(self):
        pass
    
    @abstractmethod
    def code_word_array(self):
        pass

class ClassicCoder(Coder):
    def code_word(self):
        return "I am classic coder - single word"
    
    def code_word_array(self):
        return "I am classic coder - array of words"

class ShortenedCoder(Coder):
    def code_word(self):
        return "I am shortened coder - single word"
    
    def code_word_array(self):
        return "I am shortened coder - array of words"

# Example usage
if __name__ == "__main__":
    classic = ClassicCoder(10, 5)
    shortened = ShortenedCoder(8, 4)
    
    print(classic.code_word())
    print(classic.code_word_array())
    print(f"Classic coder lengths: {classic.code_length}, {classic.base_length}")
    
    print("\n" + shortened.code_word())
    print(shortened.code_word_array())
    print(f"Shortened coder lengths: {shortened.code_length}, {shortened.base_length}")