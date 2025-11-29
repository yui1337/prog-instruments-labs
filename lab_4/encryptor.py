class Encryptor:
    SHIFT = 2

    def shiftChar(self, ch: str) -> str:
        return chr(ord(ch) + self.SHIFT)

    def check_spaces(self, word: str) -> None:
        if " " in word:
            raise ValueError("This string contains spaces!")

    def cryptWord(self, word: str) -> str:
        self.check_spaces(word)
        return "".join(self.shiftChar(ch) for ch in word)

    def cryptWordToNumbers(self, word: str) -> str:
        self.check_spaces(word)
        return "".join(str(ord(ch) + self.SHIFT) for ch in word)

    def cryptWordWithCharsToReplace(self, word: str,
                                    chars_to_replace: str) -> str:
        self.check_spaces(word)
        replace_set = set(chars_to_replace)
        result_chars = [self.shiftChar(ch) if ch in replace_set
                        else ch for ch in word]
        return "".join(result_chars)

    def cryptSentence(self, sentence: str) -> str:
        return "".join(self.shiftChar(ch) for ch in sentence)

    def getWords(self, sentence) -> list[str]:
        return sentence.split()

def printWords(sentence: str) -> None:
    for word in sentence.split():
        print("<%s>" % word)
