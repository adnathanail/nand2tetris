from constants import KEYWORDS, SYMBOLS, SYMBOL_LOOKUP
from utils import strip_comments_and_whitespace


class JackTokenizer:
    def __init__(self, jack_code):
        self._text = strip_comments_and_whitespace(jack_code)
        self._tokenStart = 0
        self._tokenEnd = 0
        self.tokenType = None
        self.token = None

    def hasMoreTokens(self) -> bool:
        return (self._tokenStart + 1) < len(self._text)

    def _lexKeyWord(self):
        for kw in KEYWORDS:
            if kw == self._text[self._tokenStart : self._tokenStart + len(kw)]:
                return self._tokenStart + len(kw)
        return False

    def _lexSymbol(self) -> str:
        if self._text[self._tokenStart] in SYMBOLS:
            return self._tokenStart + 1
        return False

    def _lexIntegerConstant(self) -> str:
        if not self._text[self._tokenStart].isdigit():
            return False
        endInd = self._tokenStart + 1
        decimal_used = False
        while self._text[endInd].isdigit() or (
            not decimal_used and self._text[endInd] == "."
        ):
            if self._text[endInd] == ".":
                decimal_used = True
            endInd += 1
        return endInd

    def _lexStringConstant(self) -> str:
        if self._text[self._tokenStart] != '"':
            return False
        endInd = self._tokenStart + 1
        while self._text[endInd] not in ['"', "\n"]:
            endInd += 1
        if self._text[endInd] == '"':
            return endInd + 1
        return False

    def _lexIdentifier(self) -> str:
        endInd = self._tokenStart
        if not self._text[endInd].isalpha() and self._text[endInd] != "_":
            return False
        while (
            self._text[endInd].isalpha()
            or self._text[endInd].isdigit()
            or self._text[endInd] == "_"
        ):
            endInd += 1
        return endInd

    def _chew(self):
        while self._text[self._tokenStart] == " ":
            self._tokenStart += 1

    def keyWord(self):
        return self._text[self._tokenStart : self._tokenEnd]

    def intVal(self) -> int:
        return self._text[self._tokenStart : self._tokenEnd]

    def stringVal(self) -> int:
        return self._text[self._tokenStart + 1 : self._tokenEnd - 1]

    def symbol(self) -> str:
        symb = self._text[self._tokenStart : self._tokenEnd]
        if symb in SYMBOL_LOOKUP:
            return SYMBOL_LOOKUP[symb]
        return symb

    def identifier(self) -> str:
        return self._text[self._tokenStart : self._tokenEnd]

    def advance(self):
        self._tokenStart = self._tokenEnd
        self._chew()
        if nextInd := self._lexKeyWord():
            self._tokenEnd = nextInd
            self.tokenType = "keyword"
            self.token = self.keyWord()
        elif nextInd := self._lexSymbol():
            self._tokenEnd = nextInd
            self.tokenType = "symbol"
            self.token = self.symbol()
        elif nextInd := self._lexIntegerConstant():
            self._tokenEnd = nextInd
            self.tokenType = "integerConstant"
            self.token = self.intVal()
        elif nextInd := self._lexStringConstant():
            self._tokenEnd = nextInd
            self.tokenType = "stringConstant"
            self.token = self.stringVal()
        elif nextInd := self._lexIdentifier():
            self._tokenEnd = nextInd
            self.tokenType = "identifier"
            self.token = self.identifier()
        else:
            raise Exception()