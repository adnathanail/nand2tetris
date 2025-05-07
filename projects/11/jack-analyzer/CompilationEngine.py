from constants import PRIMITIVE_TYPES, KEYWORD_CONSTANTS, OPS, UNARY_OPS
from JackTokenizer import JackTokenizer
from SymbolTable import SymbolTable
from VMWriter import VMWriter


class CompilationError(Exception):
    pass


class CompilationEngine:
    def __init__(self, in_file, vm_writer):
        self.tokenizer = JackTokenizer(in_file.read())
        self.class_symbol_table = SymbolTable()
        self.method_symbol_table = SymbolTable()
        self.vm_writer = vm_writer
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

    def _parseSymbol(self, expectedSymbols):
        self.tokenizer.advance()
        if (
            self.tokenizer.tokenType == "symbol"
            and self.tokenizer.token in expectedSymbols
        ):
            return f"<symbol> {self.tokenizer.token} </symbol>"
        else:
            raise CompilationError(
                f"Expected symbol(s) {expectedSymbols}, got {self.tokenizer.tokenType} {self.tokenizer.token}"
            )

    def _parseIntegerConstant(self):
        self.tokenizer.advance()
        if self.tokenizer.tokenType == "integerConstant":
            return f"<integerConstant> {self.tokenizer.token} </integerConstant>"
        else:
            raise CompilationError(
                f"Expected integer constant, got {self.tokenizer.tokenType} {self.tokenizer.token}"
            )

    def _parseStringConstant(self):
        self.tokenizer.advance()
        if self.tokenizer.tokenType == "stringConstant":
            return f"<stringConstant> {self.tokenizer.token} </stringConstant>"
        else:
            raise CompilationError(
                f"Expected string constant, got {self.tokenizer.tokenType} {self.tokenizer.token}"
            )

    def _parseIdentifier(self):
        self.tokenizer.advance()
        if self.tokenizer.tokenType == "identifier":
            return f"<identifier> {self.tokenizer.token} </identifier>"
        else:
            raise CompilationError(
                f"Expected identifier, got {self.tokenizer.tokenType} {self.tokenizer.token}"
            )

    def compileClass(self, indent=0):
        self.vm_writer._xmlOutput("<class>", indent)

        self.vm_writer._xmlOutput(self._parseKeyword(["class"]), indent + 1)
        self.vm_writer._xmlOutput(self._parseIdentifier(), indent + 1)

        self.vm_writer._xmlOutput(self._parseSymbol(["{"]), indent + 1)

        while (
            self.tokenizer.nextTokenType == "keyword"
            and self.tokenizer.nextToken in ("static", "field")
        ):
            self.compileClassVarDec(indent + 1)

        while (
            self.tokenizer.nextTokenType == "keyword"
            and self.tokenizer.nextToken in ("constructor", "function", "method")
        ):
            self.compileSubroutine(indent + 1)

        self.vm_writer._xmlOutput(self._parseSymbol(["}"]), indent + 1)

        self.vm_writer._xmlOutput("</class>", indent)

        if self.tokenizer.hasMoreTokens():
            self.tokenizer.advance()
            raise CompilationError(
                f"Nothing expected after class definition, got {self.tokenizer.tokenType} {self.tokenizer.token}"
            )

    def _parseType(self, *, include_void=False):
        if self.tokenizer.nextTokenType == "keyword" and (
            self.tokenizer.nextToken in PRIMITIVE_TYPES
            or (include_void and self.tokenizer.nextToken == "void")
        ):
            return self._parseKeyword(
                PRIMITIVE_TYPES + (("void",) if include_void else ())
            )
        else:
            return self._parseIdentifier()

    def compileClassVarDec(self, indent):
        self.vm_writer._xmlOutput("<classVarDec>", indent)

        self.vm_writer._xmlOutput(self._parseKeyword(["static", "field"]), indent + 1)
        self.vm_writer._xmlOutput(self._parseType(), indent + 1)
        self.vm_writer._xmlOutput(self._parseIdentifier(), indent + 1)

        while (
            self.tokenizer.nextTokenType == "symbol" and self.tokenizer.nextToken == ","
        ):
            self.vm_writer._xmlOutput(self._parseSymbol([","]), indent + 1)
            self.vm_writer._xmlOutput(self._parseIdentifier(), indent + 1)

        self.vm_writer._xmlOutput(self._parseSymbol([";"]), indent + 1)
        self.vm_writer._xmlOutput("</classVarDec>", indent)

    def compileSubroutine(self, indent):
        self.vm_writer._xmlOutput("<subroutineDec>", indent)
        self.vm_writer._xmlOutput(
            self._parseKeyword(["constructor", "function", "method"]), indent + 1
        )
        self.vm_writer._xmlOutput(self._parseType(include_void=True), indent + 1)
        self.vm_writer._xmlOutput(self._parseIdentifier(), indent + 1)

        self.vm_writer._xmlOutput(self._parseSymbol(["("]), indent + 1)
        self.compileParameterList(indent + 1)
        self.vm_writer._xmlOutput(self._parseSymbol([")"]), indent + 1)

        self.compileSubroutineBody(indent + 1)

        self.vm_writer._xmlOutput("</subroutineDec>", indent)

    def compileParameterList(self, indent):
        self.vm_writer._xmlOutput("<parameterList>", indent)

        if self.tokenizer.nextTokenType in ["keyword", "identifier"]:
            self.vm_writer._xmlOutput(self._parseType(), indent + 1)
            self.vm_writer._xmlOutput(self._parseIdentifier(), indent + 1)

        while (
            self.tokenizer.nextTokenType == "symbol" and self.tokenizer.nextToken == ","
        ):
            self.vm_writer._xmlOutput(self._parseSymbol([","]), indent + 1)
            self.vm_writer._xmlOutput(self._parseType(), indent + 1)
            self.vm_writer._xmlOutput(self._parseIdentifier(), indent + 1)

        self.vm_writer._xmlOutput("</parameterList>", indent)

    def compileSubroutineBody(self, indent):
        self.vm_writer._xmlOutput("<subroutineBody>", indent)

        self.vm_writer._xmlOutput(self._parseSymbol(["{"]), indent + 1)
        while (
            self.tokenizer.nextTokenType == "keyword"
            and self.tokenizer.nextToken == "var"
        ):
            self.compileVarDec(indent + 1)
        self.compileStatements(indent + 1)
        self.vm_writer._xmlOutput(self._parseSymbol(["}"]), indent + 1)

        self.vm_writer._xmlOutput("</subroutineBody>", indent)

    def compileVarDec(self, indent):
        self.vm_writer._xmlOutput("<varDec>", indent)

        self.vm_writer._xmlOutput(self._parseKeyword(["var"]), indent + 1)
        self.vm_writer._xmlOutput(self._parseType(), indent + 1)
        self.vm_writer._xmlOutput(self._parseIdentifier(), indent + 1)

        while (
            self.tokenizer.nextTokenType == "symbol" and self.tokenizer.nextToken == ","
        ):
            self.vm_writer._xmlOutput(self._parseSymbol([","]), indent + 1)
            self.vm_writer._xmlOutput(self._parseIdentifier(), indent + 1)

        self.vm_writer._xmlOutput(self._parseSymbol([";"]), indent + 1)
        self.vm_writer._xmlOutput("</varDec>", indent)

    def compileStatements(self, indent):
        self.vm_writer._xmlOutput("<statements>", indent)
        while (
            self.tokenizer.nextTokenType == "keyword"
            and self.tokenizer.nextToken in ["let", "if", "while", "do", "return"]
        ):
            if self.tokenizer.nextToken == "let":
                self.compileLet(indent + 1)
            elif self.tokenizer.nextToken == "if":
                self.compileIf(indent + 1)
            elif self.tokenizer.nextToken == "while":
                self.compileWhile(indent + 1)
            elif self.tokenizer.nextToken == "do":
                self.compileDo(indent + 1)
            elif self.tokenizer.nextToken == "return":
                self.compileReturn(indent + 1)
        self.vm_writer._xmlOutput("</statements>", indent)

    def compileLet(self, indent):
        self.vm_writer._xmlOutput("<letStatement>", indent)
        self.vm_writer._xmlOutput(self._parseKeyword(["let"]), indent + 1)
        self.vm_writer._xmlOutput(self._parseIdentifier(), indent + 1)

        if self.tokenizer.nextToken == "[":
            self.vm_writer._xmlOutput(self._parseSymbol(["["]), indent + 1)
            self.compileExpression(indent + 1)
            self.vm_writer._xmlOutput(self._parseSymbol(["]"]), indent + 1)

        self.vm_writer._xmlOutput(self._parseSymbol(["="]), indent + 1)

        self.compileExpression(indent + 1)

        self.vm_writer._xmlOutput(self._parseSymbol([";"]), indent + 1)
        self.vm_writer._xmlOutput("</letStatement>", indent)

    def compileIf(self, indent):
        self.vm_writer._xmlOutput("<ifStatement>", indent)

        self.vm_writer._xmlOutput(self._parseKeyword(["if"]), indent + 1)

        self.vm_writer._xmlOutput(self._parseSymbol(["("]), indent + 1)
        self.compileExpression(indent + 1)
        self.vm_writer._xmlOutput(self._parseSymbol([")"]), indent + 1)

        self.vm_writer._xmlOutput(self._parseSymbol(["{"]), indent + 1)
        self.compileStatements(indent + 1)
        self.vm_writer._xmlOutput(self._parseSymbol(["}"]), indent + 1)

        if (
            self.tokenizer.nextTokenType == "keyword"
            and self.tokenizer.nextToken == "else"
        ):
            self.vm_writer._xmlOutput(self._parseKeyword(["else"]), indent + 1)
            self.vm_writer._xmlOutput(self._parseSymbol(["{"]), indent + 1)
            self.compileStatements(indent + 1)
            self.vm_writer._xmlOutput(self._parseSymbol(["}"]), indent + 1)

        self.vm_writer._xmlOutput("</ifStatement>", indent)

    def compileWhile(self, indent):
        self.vm_writer._xmlOutput("<whileStatement>", indent)
        self.vm_writer._xmlOutput(self._parseKeyword(["while"]), indent + 1)

        self.vm_writer._xmlOutput(self._parseSymbol(["("]), indent + 1)
        self.compileExpression(indent + 1)
        self.vm_writer._xmlOutput(self._parseSymbol([")"]), indent + 1)

        self.vm_writer._xmlOutput(self._parseSymbol(["{"]), indent + 1)
        self.compileStatements(indent + 1)
        self.vm_writer._xmlOutput(self._parseSymbol(["}"]), indent + 1)

        self.vm_writer._xmlOutput("</whileStatement>", indent)

    def _compileSubroutineCall(self, indent):
        if self.tokenizer.nextTokenType == "symbol" and self.tokenizer.nextToken == ".":
            self.vm_writer._xmlOutput(self._parseSymbol(["."]), indent)
            self.vm_writer._xmlOutput(self._parseIdentifier(), indent)

        self.vm_writer._xmlOutput(self._parseSymbol(["("]), indent)
        self.compileExpressionList(indent)
        self.vm_writer._xmlOutput(self._parseSymbol([")"]), indent)

    def compileDo(self, indent):
        self.vm_writer._xmlOutput("<doStatement>", indent)
        self.vm_writer._xmlOutput(self._parseKeyword(["do"]), indent + 1)
        self.vm_writer._xmlOutput(self._parseIdentifier(), indent + 1)
        self._compileSubroutineCall(indent + 1)
        self.vm_writer._xmlOutput(self._parseSymbol([";"]), indent + 1)
        self.vm_writer._xmlOutput("</doStatement>", indent)

    def compileReturn(self, indent):
        self.vm_writer._xmlOutput("<returnStatement>", indent)
        self.vm_writer._xmlOutput(self._parseKeyword(["return"]), indent + 1)
        if not (
            self.tokenizer.nextTokenType == "symbol" and self.tokenizer.nextToken == ";"
        ):
            self.compileExpression(indent + 1)
        self.vm_writer._xmlOutput(self._parseSymbol([";"]), indent + 1)
        self.vm_writer._xmlOutput("</returnStatement>", indent)

    def compileExpression(self, indent):
        self.vm_writer._xmlOutput("<expression>", indent)
        self.compileTerm(indent + 1)
        if self.tokenizer.nextTokenType == "symbol" and self.tokenizer.nextToken in OPS:
            self.vm_writer._xmlOutput(self._parseSymbol(OPS), indent + 1)
            self.compileTerm(indent + 1)
        self.vm_writer._xmlOutput("</expression>", indent)

    def compileTerm(self, indent):
        self.vm_writer._xmlOutput("<term>", indent)
        if self.tokenizer.nextTokenType == "integerConstant":
            self.vm_writer._xmlOutput(self._parseIntegerConstant(), indent + 1)
        if self.tokenizer.nextTokenType == "stringConstant":
            self.vm_writer._xmlOutput(self._parseStringConstant(), indent + 1)
        elif self.tokenizer.nextTokenType == "identifier":
            self.vm_writer._xmlOutput(self._parseIdentifier(), indent + 1)
            if self.tokenizer.nextTokenType == "symbol":
                if self.tokenizer.nextToken in [".", "("]:
                    self._compileSubroutineCall(indent + 1)
                elif self.tokenizer.nextToken == "[":
                    self.vm_writer._xmlOutput(self._parseSymbol(["["]), indent + 1)
                    self.compileExpression(indent + 1)
                    self.vm_writer._xmlOutput(self._parseSymbol(["]"]), indent + 1)
        elif self.tokenizer.nextTokenType == "keyword":
            self.vm_writer._xmlOutput(self._parseKeyword(KEYWORD_CONSTANTS), indent + 1)
        elif self.tokenizer.nextTokenType == "symbol":
            if self.tokenizer.nextToken == "(":
                self.vm_writer._xmlOutput(self._parseSymbol(["("]), indent + 1)
                self.compileExpression(indent + 1)
                self.vm_writer._xmlOutput(self._parseSymbol([")"]), indent + 1)
            elif self.tokenizer.nextToken in UNARY_OPS:
                self.vm_writer._xmlOutput(self._parseSymbol(UNARY_OPS), indent + 1)
                self.compileTerm(indent + 1)
        self.vm_writer._xmlOutput("</term>", indent)

    def compileExpressionList(self, indent):
        self.vm_writer._xmlOutput("<expressionList>", indent)

        if not (
            self.tokenizer.nextTokenType == "symbol" and self.tokenizer.nextToken == ")"
        ):
            self.compileExpression(indent + 1)
            while (
                self.tokenizer.nextTokenType == "symbol"
                and self.tokenizer.nextToken == ","
            ):
                self.vm_writer._xmlOutput(self._parseSymbol([","]), indent + 1)
                self.compileExpression(indent + 1)

        self.vm_writer._xmlOutput("</expressionList>", indent)
