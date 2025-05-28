from typing import Union, Optional
from constants import KEYWORDS, SYMBOLS, TOKEN_TYPES
from utils import strip_comments_and_whitespace


class JackTokenizer:
    def __init__(self, jack_code: str):
        self._lines = strip_comments_and_whitespace(jack_code)
        self._lineNumber = 0
        self._tokenStart: int = 0
        self._tokenEnd: int = 0

        self.tokenLineNumber: int = 0
        self.nextTokenLineNumber: int = 0
        self.tokenType: None | TOKEN_TYPES = None
        self.token: None | str = None
        self.nextTokenType: None | TOKEN_TYPES = None
        self.nextToken: None | str = None

        self.advance()

    def hasMoreTokens(self) -> bool:
        return self.nextToken is not None

    def _getCurrentLine(self) -> str:
        return self._lines[self._lineNumber]

    def _lexKeyWord(self) -> Union[int, bool]:
        for kw in KEYWORDS:
            if kw == self._getCurrentLine()[self._tokenStart : self._tokenStart + len(kw)] and not self._getCurrentLine()[self._tokenStart + len(kw)].isalpha():
                return self._tokenStart + len(kw)
        return False

    def _lexSymbol(self) -> Union[int, bool]:
        if self._getCurrentLine()[self._tokenStart] in SYMBOLS:
            return self._tokenStart + 1
        return False

    def _lexIntegerConstant(self) -> Union[int, bool]:
        if not self._getCurrentLine()[self._tokenStart].isdigit():
            return False
        endInd = self._tokenStart + 1
        decimal_used = False
        while self._getCurrentLine()[endInd].isdigit() or (not decimal_used and self._getCurrentLine()[endInd] == "."):
            if self._getCurrentLine()[endInd] == ".":
                decimal_used = True
            endInd += 1
        return endInd

    def _lexStringConstant(self) -> Union[int, bool]:
        if self._getCurrentLine()[self._tokenStart] != '"':
            return False
        endInd: int = self._tokenStart + 1
        while self._getCurrentLine()[endInd] not in ['"', "\n"]:
            endInd += 1
        if self._getCurrentLine()[endInd] == '"':
            return endInd + 1
        return False

    def _lexIdentifier(self) -> Union[int, bool]:
        endInd = self._tokenStart
        if not self._getCurrentLine()[endInd].isalpha() and self._getCurrentLine()[endInd] != "_":
            return False
        while self._getCurrentLine()[endInd].isalpha() or self._getCurrentLine()[endInd].isdigit() or self._getCurrentLine()[endInd] == "_":
            endInd += 1
        return endInd

    def _chew(self):
        while self._tokenStart < len(self._getCurrentLine()) and self._getCurrentLine()[self._tokenStart] == " ":
            self._tokenStart += 1

    def advance(self):
        self._tokenStart = self._tokenEnd
        self._chew()

        self.token = self.nextToken
        self.tokenType = self.nextTokenType
        self.tokenLineNumber = self.nextTokenLineNumber

        if self._tokenStart < len(self._getCurrentLine()):
            if nextInd := self._lexKeyWord():
                self._tokenEnd = nextInd
                self.nextTokenType = "keyword"
            elif nextInd := self._lexSymbol():
                self._tokenEnd = nextInd
                self.nextTokenType = "symbol"
            elif nextInd := self._lexIntegerConstant():
                self._tokenEnd = nextInd
                self.nextTokenType = "integerConstant"
            elif nextInd := self._lexStringConstant():
                self._tokenEnd = nextInd
                self.nextTokenType = "stringConstant"
            elif nextInd := self._lexIdentifier():
                self._tokenEnd = nextInd
                self.nextTokenType = "identifier"
            else:
                raise Exception(f"Couldn't tokenize from '{self._getCurrentLine()[self._tokenStart : self._tokenStart + 5]}'")
            self.nextToken = self._getCurrentLine()[self._tokenStart : self._tokenEnd]
            self.nextTokenLineNumber = self._lineNumber
        elif self._lineNumber < (len(self._lines) - 1):
            self._lineNumber += 1
            self._tokenStart = 0
            self._tokenEnd = 0
            self.advance()
        elif self.nextToken is None:
            raise Exception("No more tokens")
        else:
            self.nextToken = None
            self.nextTokenType = None
