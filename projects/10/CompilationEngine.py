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

        while self.tokenizer.nextTokenType == "keyword" and self.tokenizer.nextToken in ("constructor", "function", "method"):
            self.compileSubroutine(indent + 1)

        print(make_indent(indent + 1) + self._parseSymbol("}"))
        print(make_indent(indent) + "</class>")

        if self.tokenizer.hasMoreTokens():
            self.tokenizer.advance()
            raise CompilationError(
                f"Nothing expected after class definition, got {self.tokenizer.tokenType} {self.tokenizer.token}"
            )

    def _parseType(self, *, include_void=False):
        if self.tokenizer.nextTokenType == "keyword" and (self.tokenizer.nextToken in PRIMITIVE_TYPES or (include_void and self.tokenizer.nextToken == "void")):
            return self._parseKeyword(PRIMITIVE_TYPES + (("void",) if include_void else ()))
        else:
            return self._parseIdentifier()


    def compileClassVarDec(self, indent):
        print(make_indent(indent) + "<classVarDec>")
        print(make_indent(indent + 1) + self._parseKeyword(["static", "field"]))
        print(make_indent(indent + 1) + self._parseType())
        print(make_indent(indent + 1) + self._parseIdentifier())
        print(make_indent(indent + 1) + self._parseSymbol(";"))
        print(make_indent(indent) + "</classVarDec>")

    def compileSubroutine(self, indent):
        print(make_indent(indent) + "<subroutineDec>")
        print(make_indent(indent + 1) + self._parseKeyword(["constructor", "function", "method"]))
        print(make_indent(indent + 1) + self._parseType(include_void=True))
        print(make_indent(indent + 1) + self._parseIdentifier())
        print(make_indent(indent + 1) + self._parseSymbol("("))
        # TODO
        print(make_indent(indent + 1) + self._parseSymbol(")"))
        self.compileSubroutineBody(indent + 1)

    def compileSubroutineBody(self, indent):
        print(make_indent(indent) + "<subroutineDec>")
        print(make_indent(indent + 1) + self._parseSymbol("{"))
        while self.tokenizer.nextTokenType == "keyword" and self.tokenizer.nextToken == "var":
            self.compileVarDec(indent + 1)
        self.compileStatements(indent + 1)
        print(make_indent(indent + 1) + self._parseSymbol("}"))
        print(make_indent(indent) + "</subroutineDec>")
    
    def compileVarDec(self, indent):
        print(make_indent(indent) + "<varDec>")
        print(make_indent(indent + 1) + self._parseKeyword(["var"]))
        print(make_indent(indent + 1) + self._parseType())
        print(make_indent(indent + 1) + self._parseIdentifier())
        while self.tokenizer.nextTokenType == "symbol" and self.tokenizer.nextToken == ",":
            print(make_indent(indent + 1) + self._parseSymbol(","))
            print(make_indent(indent + 1) + self._parseIdentifier())
        print(make_indent(indent + 1) + self._parseSymbol(";"))
        print(make_indent(indent) + "</varDec>")
    
    def compileStatements(self, indent):
        if self.tokenizer.nextTokenType != "keyword" or self.tokenizer.nextToken not in ["let", "if", "while", "do", "return"]:
            return
        print(make_indent(indent) + "<statements>")
        while self.tokenizer.nextTokenType == "keyword" and self.tokenizer.nextToken in ["let", "if", "while", "do", "return"]:
            if self.tokenizer.nextToken == "let":
                self.compileLetStatement(indent + 1)
            elif self.tokenizer.nextToken == "do":
                self.compileDoStatement(indent + 1)
        print(make_indent(indent) + "</statements>")
    
    def compileLetStatement(self, indent):
        print(make_indent(indent) + "<letStatement>")
        print(make_indent(indent + 1) + self._parseKeyword(["let"]))
        print(make_indent(indent + 1) + self._parseIdentifier())
        print(make_indent(indent + 1) + self._parseSymbol("="))
        print(make_indent(indent + 1) + self._parseIdentifier())
        print(make_indent(indent + 1) + self._parseSymbol(";"))
        print(make_indent(indent) + "</letStatement>")
    
    def _parseSubroutineCall(self):
        out = (self._parseIdentifier(),)
        while self.tokenizer.nextTokenType == "symbol" and self.tokenizer.nextToken == ".":
            out += (
                self._parseSymbol("."),
                self._parseIdentifier()
                )
        out += (
            self._parseSymbol("("),
            # self._parseIdentifier()
            self._parseSymbol(")"),
        )
        return out

    def compileDoStatement(self, indent):
        print(make_indent(indent) + "<doStatement>")
        print(make_indent(indent + 1) + self._parseKeyword(["do"]))
        for item in self._parseSubroutineCall():
            print(make_indent(indent + 1) + item)
        print(make_indent(indent + 1) + self._parseSymbol(";"))
        print(make_indent(indent) + "</doStatement>")