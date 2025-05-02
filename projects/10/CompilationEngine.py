class CompilationError(Exception):
    pass


class CompilationEngine:
    def __init__(self, tokenizer):
        self.tokenizer = tokenizer
        self.output = ""

    def compileClass(self):
        self.tokenizer.advance()
        if (self.tokenizer.tokenType, self.tokenizer.token) == ("keyword", "class"):
            print("<class>")
            print(f"<keyword> {self.tokenizer.token} </keyword>")
        else:
            raise CompilationError(f"Expected keyword class, got {self.tokenizer.tokenType} {self.tokenizer.token}")

        self.tokenizer.advance()
        if self.tokenizer.tokenType == "identifier":
            print(f"<identifier> {self.tokenizer.token} </identifier>")
        else:
            raise CompilationError(f"Expected className identifier, got {self.tokenizer.tokenType} {self.tokenizer.token}")

        self.tokenizer.advance()
        if (self.tokenizer.tokenType, self.tokenizer.token) == ("symbol", "{"):
            print("<identifier> { </identifier>")
        else:
            raise CompilationError(f"Expected symbol {{, got {self.tokenizer.tokenType} {self.tokenizer.token}")

        # classVarDec*

        # subroutineDec*

        self.tokenizer.advance()
        if (self.tokenizer.tokenType, self.tokenizer.token) == ("symbol", "}"):
            print("<identifier> } </identifier>")
            print("</class>")
        else:
            raise CompilationEngine(f"Expected symbol }}, got {self.tokenizer.tokenType} {self.tokenizer.token}")
        
        if self.tokenizer.hasMoreTokens():
            self.tokenizer.advance()
            raise CompilationError(f"Nothing expected after class definition, got {self.tokenizer.tokenType} {self.tokenizer.token}")