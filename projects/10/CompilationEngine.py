class CompilationError(Exception):
    pass


class CompilationEngine:
    def __init__(self, tokenizer):
        self.tokenizer = tokenizer
        self.output = ""

    def _parseKeyword(self, expectedKeyword):
        self.tokenizer.advance()
        if (self.tokenizer.tokenType, self.tokenizer.token) == ("keyword", expectedKeyword):
            return f"<keyword> {self.tokenizer.token} </keyword>"
        else:
            raise CompilationError(f"Expected keyword {expectedKeyword}, got {self.tokenizer.tokenType} {self.tokenizer.token}")

    def _parseSymbol(self, expectedSymbol):
        self.tokenizer.advance()
        if (self.tokenizer.tokenType, self.tokenizer.token) == ("symbol", expectedSymbol):
            return f"<symbol> {self.tokenizer.token} </symbol>"
        else:
            raise CompilationError(f"Expected symbol {expectedSymbol}, got {self.tokenizer.tokenType} {self.tokenizer.token}")

    # parseIntegerConstant

    # parseStringConstant

    def _parseIdentifier(self):
        self.tokenizer.advance()
        if self.tokenizer.tokenType == "identifier":
            return f"<identifier> {self.tokenizer.token} </identifier>"
        else:
            raise CompilationError(f"Expected identifier, got {self.tokenizer.tokenType} {self.tokenizer.token}")

    def compileClass(self):
        print("<class>")
        print(self._parseKeyword("class"))
        print(self._parseIdentifier())
        print(self._parseSymbol("{"))

        # classVarDec*

        # subroutineDec*

        print(self._parseSymbol("}"))
        print("</class>")

        if self.tokenizer.hasMoreTokens():
            self.tokenizer.advance()
            raise CompilationError(f"Nothing expected after class definition, got {self.tokenizer.tokenType} {self.tokenizer.token}")