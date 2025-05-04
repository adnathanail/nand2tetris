from utils import make_indent
from constants import PRIMITIVE_TYPES


class CompilationError(Exception):
    pass


class CompilationEngine:
    def __init__(self, tokenizer):
        self.tokenizer = tokenizer
        self.output = ""

    def _output(self, line, indent):
        print(make_indent(indent) + line)
        self.output += make_indent(indent) + line + "\n"

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
        self._output("<class>", indent)
        self._output(self._parseKeyword(["class"]), indent + 1)
        self._output(self._parseIdentifier(), indent + 1)
        self._output(self._parseSymbol("{"), indent + 1)

        while self.tokenizer.nextTokenType == "keyword" and self.tokenizer.nextToken in ("static", "field"):
            self.compileClassVarDec(indent + 1)

        while self.tokenizer.nextTokenType == "keyword" and self.tokenizer.nextToken in ("constructor", "function", "method"):
            self.compileSubroutine(indent + 1)

        self._output(self._parseSymbol("}"), indent + 1)
        self._output("</class>", indent)

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
        self._output("<classVarDec>", indent)
        self._output(self._parseKeyword(["static", "field"]), indent + 1)
        self._output(self._parseType(), indent + 1)
        self._output(self._parseIdentifier(), indent + 1)
        self._output(self._parseSymbol(";"), indent + 1)
        self._output("</classVarDec>", indent)

    def compileSubroutine(self, indent):
        self._output("<subroutineDec>", indent)
        self._output(self._parseKeyword(["constructor", "function", "method"]), indent + 1)
        self._output(self._parseType(include_void=True), indent + 1)
        self._output(self._parseIdentifier(), indent + 1)
        self._output(self._parseSymbol("("), indent + 1)

        self._output("<parameterList>", indent + 1)
        self._output("</parameterList>", indent + 1)

        self._output(self._parseSymbol(")"), indent + 1)
        self.compileSubroutineBody(indent + 1)
        self._output("</subroutineDec>", indent)

    def compileSubroutineBody(self, indent):
        self._output("<subroutineBody>", indent)
        self._output(self._parseSymbol("{"), indent + 1)
        while self.tokenizer.nextTokenType == "keyword" and self.tokenizer.nextToken == "var":
            self.compileVarDec(indent + 1)
        self.compileStatements(indent + 1)
        self._output(self._parseSymbol("}"), indent + 1)
        self._output("</subroutineBody>", indent)
    
    def compileVarDec(self, indent):
        self._output("<varDec>", indent)
        self._output(self._parseKeyword(["var"]), indent + 1)
        self._output(self._parseType(), indent + 1)
        self._output(self._parseIdentifier(), indent + 1)
        while self.tokenizer.nextTokenType == "symbol" and self.tokenizer.nextToken == ",":
            self._output(self._parseSymbol(","), indent + 1)
            self._output(self._parseIdentifier(), indent + 1)
        self._output(self._parseSymbol(";"), indent + 1)
        self._output("</varDec>", indent)
    
    def compileStatements(self, indent):
        self._output("<statements>", indent)
        while self.tokenizer.nextTokenType == "keyword" and self.tokenizer.nextToken in ["let", "if", "while", "do", "return"]:
            if self.tokenizer.nextToken == "let":
                self.compileLetStatement(indent + 1)
            elif self.tokenizer.nextToken == "if":
                self.compileIfStatement(indent + 1)
            elif self.tokenizer.nextToken == "do":
                self.compileDoStatement(indent + 1)
            elif self.tokenizer.nextToken == "return":
                self.compileReturnStatement(indent + 1)
        self._output("</statements>", indent)
    
    def compileLetStatement(self, indent):
        self._output("<letStatement>", indent)
        self._output(self._parseKeyword(["let"]), indent + 1)
        self._output(self._parseIdentifier(), indent + 1)
        self._output(self._parseSymbol("="), indent + 1)

        self.compileExpression(indent + 1)

        self._output(self._parseSymbol(";"), indent + 1)
        self._output("</letStatement>", indent)
    
    def compileIfStatement(self, indent):
        self._output("<ifStatement>", indent)
        self._output(self._parseKeyword(["if"]), indent + 1)
        self._output(self._parseSymbol("("), indent + 1)

        self.compileExpression(indent + 1)

        self._output(self._parseSymbol(")"), indent + 1)
        self._output(self._parseSymbol("{"), indent + 1)
        self.compileStatements(indent + 1)
        self._output(self._parseSymbol("}"), indent + 1)
        if self.tokenizer.nextTokenType == "keyword" and self.tokenizer.nextToken == "else":
            self._output(self._parseKeyword(["else"]), indent + 1)
            self._output(self._parseSymbol("{"), indent + 1)
            self.compileStatements(indent + 1)
            self._output(self._parseSymbol("}"), indent + 1)
        self._output("</ifStatement>", indent)

    def _compileSubroutineCall(self, indent):
        # TODO remove indent gubbins?
        self._output(self._parseIdentifier(), indent)
        if self.tokenizer.nextTokenType == "symbol" and self.tokenizer.nextToken == ".":
            self._output(self._parseSymbol("."), indent)
            self._output(self._parseIdentifier(), indent)

        self._output(self._parseSymbol("("), indent)
        self._output("<expressionList>", indent)

        if self.tokenizer.nextTokenType == "identifier":
            self.compileExpression(indent + 1)

        self._output("</expressionList>", indent)
        self._output(self._parseSymbol(")"), indent)

    def compileDoStatement(self, indent):
        self._output("<doStatement>", indent)
        self._output(self._parseKeyword(["do"]), indent + 1)
        self._compileSubroutineCall(indent + 1)
        self._output(self._parseSymbol(";"), indent + 1)
        self._output("</doStatement>", indent)

    def compileReturnStatement(self, indent):
        self._output("<returnStatement>", indent)
        self._output(self._parseKeyword(["return"]), indent + 1)
        if self.tokenizer.nextTokenType == "identifier":
            self.compileExpression(indent + 1)
        self._output(self._parseSymbol(";"), indent + 1)
        self._output("</returnStatement>", indent)
    
    def compileExpression(self, indent):
        self._output("<expression>", indent)
        self._output("<term>", indent + 1)
        self._output(self._parseIdentifier(), indent + 2)
        self._output("</term>", indent + 1)
        self._output("</expression>", indent)