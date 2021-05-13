from tokentypes import *
class Token:
    def __init__(self,tokenKind,tokenText) -> None:
        self.tokenKind = tokenKind
        self.tokenText = tokenText
    @staticmethod
    def checkIfKeyword(string):
        for word in Tokens:
            if string == word.name and word.value>=100 and word.value<=200:
                return word
        return None 