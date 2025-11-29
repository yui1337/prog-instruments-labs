class Encryptor:
    SHIFT = 2

    def shiftChar(self, ch) -> str:
        return chr(ord(ch) + self.SHIFT)

    def check_spaces(self, word) -> None:
        if " " in word:
            raise ValueError("This string contains spaces!")

    def cryptWord(self, word) -> str:
        self.check_spaces(word)
        new_word = ""
        for i in range(len(word)):
            new_word += self.shiftChar(word[i])
        return new_word

    def cryptWordToNumbers(self, word):
        self.check_spaces(word)
        new_word = ""
        for i in range(len(word)):
            new_word += self.shiftChar(word[i])
        return new_word

    def cryptWordWithCharsToReplace(self, word, chars_to_replace):
        self.check_spaces(word)
        result = list(word)
        for i in range(len(word)):
            for j in range(len(chars_to_replace)):
                if chars_to_replace[j] == word[i]:
                    result[i] = self.shiftChar(word[i])
        return "".join(result)

    def cryptSentence(self, sentence):
        new_word = ""
        for i in range(len(sentence)):
            new_word += self.shiftChar(sentence[i])
        return new_word

    def getWords(self, sentence):
        return sentence.split()

    def printWords(self, sentence):
        words = self.getWords(sentence)
        for word in words:
            print("<%s>" % word)
