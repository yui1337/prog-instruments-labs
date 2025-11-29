class Encryptor:
    SHIFT = 2

    def shiftChar(self, ch) -> str:
        return chr(ord(ch) + self.SHIFT)

    def check_spaces(self, word) -> None:
        if " " in word:
            raise ValueError("This string contains spaces!")

    def cryptWord(self, word) -> str:
        self.check_spaces(word)
        return "".join(self.shiftChar(ch) for ch in word)

    def cryptWordToNumbers(self, word):
        self.check_spaces(word)
        return "".join(str(ord(ch) + self.SHIFT) for ch in word)

    def cryptWordWithCharsToReplace(self, word, chars_to_replace):
        self.check_spaces(word)
        replace_set = set(chars_to_replace)
        result_chars = [self.shiftChar(ch) if ch in replace_set
                        else ch for ch in word]
        return "".join(result_chars)

    def cryptSentence(self, sentence):
        return "".join(self.shiftChar(ch) for ch in sentence)

    def getWords(self, sentence):
        return sentence.split()

    def printWords(self, sentence):
        words = self.getWords(sentence)
        for word in words:
            print("<%s>" % word)
