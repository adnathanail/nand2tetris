from constants import KEYWORDS, SYMBOLS, SYMBOL_LOOKUP, TOKEN_TYPES
from utils import strip_comments_and_whitespace


class JackTokenizer:
    def __init__(self, jack_code: str):
        self._text = strip_comments_and_whitespace(jack_code)
        self._tokenStart: int = 0
        self._tokenEnd: int = 0
        self.tokenType: None | TOKEN_TYPES = None
        self.token: None | int | str = None
        self.nextTokenType: None | TOKEN_TYPES = None
        self.nextToken: None | int | str = None
        self.advance()

    def hasMoreTokens(self) -> bool:
        return self.nextToken is not None

    def _lexKeyWord(self) -> int | bool:
        for kw in KEYWORDS:
            if kw == self._text[self._tokenStart : self._tokenStart + len(kw)] and not self._text[self._tokenStart + len(kw)].isalpha():
                return self._tokenStart + len(kw)
        return False

    def _lexSymbol(self) -> int | bool:
        if self._text[self._tokenStart] in SYMBOLS:
            return self._tokenStart + 1
        return False

    def _lexIntegerConstant(self) -> int | bool:
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

    def _lexStringConstant(self) -> int | bool:
        if self._text[self._tokenStart] != '"':
            return False
        endInd = self._tokenStart + 1
        while self._text[endInd] not in ['"', "\n"]:
            endInd += 1
        if self._text[endInd] == '"':
            return endInd + 1
        return False

    def _lexIdentifier(self) -> int | bool:
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
        while (
            self._tokenStart < len(self._text) and self._text[self._tokenStart] == " "
        ):
            self._tokenStart += 1

    def keyWord(self) -> str:
        return self._text[self._tokenStart : self._tokenEnd]

    def intVal(self) -> int:
        return int(self._text[self._tokenStart : self._tokenEnd])

    def stringVal(self) -> str:
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

        self.token = self.nextToken
        self.tokenType = self.nextTokenType

        if self._tokenStart < len(self._text):
            if nextInd := self._lexKeyWord():
                self._tokenEnd = nextInd
                self.nextTokenType = "keyword"
                self.nextToken = self.keyWord()
            elif nextInd := self._lexSymbol():
                self._tokenEnd = nextInd
                self.nextTokenType = "symbol"
                self.nextToken = self.symbol()
            elif nextInd := self._lexIntegerConstant():
                self._tokenEnd = nextInd
                self.nextTokenType = "integerConstant"
                self.nextToken = self.intVal()
            elif nextInd := self._lexStringConstant():
                self._tokenEnd = nextInd
                self.nextTokenType = "stringConstant"
                self.nextToken = self.stringVal()
            elif nextInd := self._lexIdentifier():
                self._tokenEnd = nextInd
                self.nextTokenType = "identifier"
                self.nextToken = self.identifier()
            else:
                raise Exception(
                    f"Couldn't tokenize from '{self._text[self._tokenStart : self._tokenStart + 5]}'"
                )
        elif self.nextToken is None:
            raise Exception("No more tokens")
        else:
            self.nextToken = None
            self.nextTokenType = None
