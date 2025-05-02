from utils import make_indent
from constants import PRIMITIVE_TYPES


class CompilationError(Exception):
    pass


class CompilationEngine:
    def __init__(self, tokenizer):
        self.tokenizer = tokenizer
        self.output = ""

    def _parseKeyword(self, expectedKeywords):
        self.tokenizer.advance()
        if (
            self.tokenizer.tokenType == "keyword"
            and self.tokenizer.token in expectedKeywords
        ):
            return f"<keyword> {self.tokenizer.token} </keyword>"
        else:
            raise CompilationError(
                f"Expected keyword(s) {expectedKeywords}, got {self.tokenizer.tokenType} {self.tokenizer.token}"
            )

    def _parseSymbol(self, expectedSymbol):
        self.tokenizer.advance()
        if (self.tokenizer.tokenType, self.tokenizer.token) == (
            "symbol",
            expectedSymbol,
        ):
            return f"<symbol> {self.tokenizer.token} </symbol>"
        else:
            raise CompilationError(
                f"Expected symbol {expectedSymbol}, got {self.tokenizer.tokenType} {self.tokenizer.token}"
            )

    # parseIntegerConstant

    # parseStringConstant

    def _parseIdentifier(self):
        self.tokenizer.advance()
        if self.tokenizer.tokenType == "identifier":
            return f"<identifier> {self.tokenizer.token} </identifier>"
        else:
            raise CompilationError(
                f"Expected identifier, got {self.tokenizer.tokenType} {self.tokenizer.token}"
            )

    def compileClass(self, indent=0):
        print(make_indent(indent) + "<class>")
        print(make_indent(indent + 1) + self._parseKeyword(["class"]))
        print(make_indent(indent + 1) + self._parseIdentifier())
        print(make_indent(indent + 1) + self._parseSymbol("{"))

        while self.tokenizer.nextTokenType == "keyword" and self.tokenizer.nextToken in ("static", "field"):
            self.compileClassVarDec(indent + 1)

        # subroutineDec*

        print(make_indent(indent + 1) + self._parseSymbol("}"))
        print(make_indent(indent) + "</class>")

        if self.tokenizer.hasMoreTokens():
            self.tokenizer.advance()
            raise CompilationError(
                f"Nothing expected after class definition, got {self.tokenizer.tokenType} {self.tokenizer.token}"
            )

    def _parseType(self):
        if self.tokenizer.nextTokenType == "keyword" and self.tokenizer.nextToken in PRIMITIVE_TYPES:
            return self._parseKeyword(PRIMITIVE_TYPES)
        else:
            return self._parseIdentifier()


    def compileClassVarDec(self, indent):
        print(make_indent(indent) + "<classVarDec>")
        print(make_indent(indent + 1) + self._parseKeyword(["static", "field"]))
        print(make_indent(indent + 1) + self._parseType())
        print(make_indent(indent + 1) + self._parseIdentifier())
        print(make_indent(indent + 1) + self._parseSymbol(";"))
        print(make_indent(indent) + "</classVarDec>")
