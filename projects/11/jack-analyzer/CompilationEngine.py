from constants import PRIMITIVE_TYPES, KEYWORD_CONSTANTS, OPS, UNARY_OPS
from JackTokenizer import JackTokenizer
from SymbolTable import SymbolTable
from VMWriter import VMWriter


class CompilationError(Exception):
    pass


class CompilationEngine:
    def __init__(self, in_file, vm_writer: VMWriter):
        self.tokenizer = JackTokenizer(in_file.read())
        self.class_symbol_table = SymbolTable()
        self.method_symbol_table = SymbolTable()
        self.vm_writer = vm_writer
        self.output = ""

    def _parseKeyword(self, expectedKeywords) -> tuple[str, str]:
        self.tokenizer.advance()
        if (
            self.tokenizer.tokenType == "keyword"
            and self.tokenizer.token in expectedKeywords
        ):
            return f"<keyword> {self.tokenizer.token} </keyword>", self.tokenizer.token
        else:
            raise CompilationError(
                f"Expected keyword(s) {expectedKeywords}, got {self.tokenizer.tokenType} {self.tokenizer.token}"
            )

    def _parseSymbol(self, expectedSymbols) -> tuple[str, str]:
        self.tokenizer.advance()
        if (
            self.tokenizer.tokenType == "symbol"
            and self.tokenizer.token in expectedSymbols
        ):
            return f"<symbol> {self.tokenizer.token} </symbol>", self.tokenizer.token
        else:
            raise CompilationError(
                f"Expected symbol(s) {expectedSymbols}, got {self.tokenizer.tokenType} {self.tokenizer.token}"
            )

    def _parseIntegerConstant(self) -> tuple[str, int]:
        self.tokenizer.advance()
        if self.tokenizer.tokenType == "integerConstant":
            return f"<integerConstant> {self.tokenizer.token} </integerConstant>", int(self.tokenizer.token)
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

    def _parseIdentifier(self) -> tuple[str, str]:
        self.tokenizer.advance()
        if self.tokenizer.tokenType == "identifier":
            return f"<identifier> {self.tokenizer.token} </identifier>", self.tokenizer.token
        else:
            raise CompilationError(
                f"Expected identifier, got {self.tokenizer.tokenType} {self.tokenizer.token}"
            )

    def compileClass(self, indent=0):
        self.vm_writer._xmlOutput("<class>", indent)

        self.vm_writer._xmlOutput(self._parseKeyword(["class"])[0], indent + 1)
        identifier_xml, class_name = self._parseIdentifier()
        self.vm_writer._xmlOutput(identifier_xml, indent + 1)

        self.vm_writer._xmlOutput(self._parseSymbol(["{"])[0], indent + 1)

        while (
            self.tokenizer.nextTokenType == "keyword"
            and self.tokenizer.nextToken in ("static", "field")
        ):
            self.compileClassVarDec(indent + 1)

        while (
            self.tokenizer.nextTokenType == "keyword"
            and self.tokenizer.nextToken in ("constructor", "function", "method")
        ):
            self.compileSubroutine(indent + 1, class_name)

        self.vm_writer._xmlOutput(self._parseSymbol(["}"])[0], indent + 1)

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
            )[0]
        else:
            return self._parseIdentifier()[0]

    def compileClassVarDec(self, indent):
        self.vm_writer._xmlOutput("<classVarDec>", indent)

        self.vm_writer._xmlOutput(self._parseKeyword(["static", "field"])[0], indent + 1)
        self.vm_writer._xmlOutput(self._parseType(), indent + 1)
        self.vm_writer._xmlOutput(self._parseIdentifier()[0], indent + 1)

        while (
            self.tokenizer.nextTokenType == "symbol" and self.tokenizer.nextToken == ","
        ):
            self.vm_writer._xmlOutput(self._parseSymbol([","])[0], indent + 1)
            self.vm_writer._xmlOutput(self._parseIdentifier()[0], indent + 1)

        self.vm_writer._xmlOutput(self._parseSymbol([";"])[0], indent + 1)
        self.vm_writer._xmlOutput("</classVarDec>", indent)

    def compileSubroutine(self, indent, class_name):
        self.vm_writer._xmlOutput("<subroutineDec>", indent)
        self.vm_writer._xmlOutput(
            self._parseKeyword(["constructor", "function", "method"])[0], indent + 1
        )
        self.vm_writer._xmlOutput(self._parseType(include_void=True), indent + 1)
        identifier_xml, subroutine_name = self._parseIdentifier()
        self.vm_writer._xmlOutput(identifier_xml, indent + 1)

        self.vm_writer._xmlOutput(self._parseSymbol(["("])[0], indent + 1)
        num_parameters = self.compileParameterList(indent + 1)
        self.vm_writer._xmlOutput(self._parseSymbol([")"])[0], indent + 1)

        self.vm_writer.writeFunction(f"{subroutine_name}.{class_name}", num_parameters)

        self.compileSubroutineBody(indent + 1)

        self.vm_writer._xmlOutput("</subroutineDec>", indent)

    def compileParameterList(self, indent) -> int:
        self.vm_writer._xmlOutput("<parameterList>", indent)

        num_parameters = 0

        if self.tokenizer.nextTokenType in ["keyword", "identifier"]:
            self.vm_writer._xmlOutput(self._parseType(), indent + 1)
            self.vm_writer._xmlOutput(self._parseIdentifier()[0], indent + 1)
            num_parameters += 1

        while (
            self.tokenizer.nextTokenType == "symbol" and self.tokenizer.nextToken == ","
        ):
            self.vm_writer._xmlOutput(self._parseSymbol([","])[0], indent + 1)
            self.vm_writer._xmlOutput(self._parseType(), indent + 1)
            self.vm_writer._xmlOutput(self._parseIdentifier()[0], indent + 1)
            num_parameters += 1

        self.vm_writer._xmlOutput("</parameterList>", indent)
        return num_parameters

    def compileSubroutineBody(self, indent):
        self.vm_writer._xmlOutput("<subroutineBody>", indent)

        self.vm_writer._xmlOutput(self._parseSymbol(["{"])[0], indent + 1)
        while (
            self.tokenizer.nextTokenType == "keyword"
            and self.tokenizer.nextToken == "var"
        ):
            self.compileVarDec(indent + 1)
        self.compileStatements(indent + 1)
        self.vm_writer._xmlOutput(self._parseSymbol(["}"])[0], indent + 1)

        self.vm_writer._xmlOutput("</subroutineBody>", indent)

    def compileVarDec(self, indent):
        self.vm_writer._xmlOutput("<varDec>", indent)

        self.vm_writer._xmlOutput(self._parseKeyword(["var"])[0], indent + 1)
        self.vm_writer._xmlOutput(self._parseType(), indent + 1)
        self.vm_writer._xmlOutput(self._parseIdentifier()[0], indent + 1)

        while (
            self.tokenizer.nextTokenType == "symbol" and self.tokenizer.nextToken == ","
        ):
            self.vm_writer._xmlOutput(self._parseSymbol([","])[0], indent + 1)
            self.vm_writer._xmlOutput(self._parseIdentifier()[0], indent + 1)

        self.vm_writer._xmlOutput(self._parseSymbol([";"])[0], indent + 1)
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
        self.vm_writer._xmlOutput(self._parseKeyword(["let"])[0], indent + 1)
        self.vm_writer._xmlOutput(self._parseIdentifier()[0], indent + 1)

        if self.tokenizer.nextToken == "[":
            self.vm_writer._xmlOutput(self._parseSymbol(["["])[0], indent + 1)
            self.compileExpression(indent + 1)
            self.vm_writer._xmlOutput(self._parseSymbol(["]"])[0], indent + 1)

        self.vm_writer._xmlOutput(self._parseSymbol(["="])[0], indent + 1)

        self.compileExpression(indent + 1)

        self.vm_writer._xmlOutput(self._parseSymbol([";"])[0], indent + 1)
        self.vm_writer._xmlOutput("</letStatement>", indent)

    def compileIf(self, indent):
        self.vm_writer._xmlOutput("<ifStatement>", indent)

        self.vm_writer._xmlOutput(self._parseKeyword(["if"])[0], indent + 1)

        self.vm_writer._xmlOutput(self._parseSymbol(["("])[0], indent + 1)
        self.compileExpression(indent + 1)
        self.vm_writer._xmlOutput(self._parseSymbol([")"])[0], indent + 1)

        self.vm_writer._xmlOutput(self._parseSymbol(["{"])[0], indent + 1)
        self.compileStatements(indent + 1)
        self.vm_writer._xmlOutput(self._parseSymbol(["}"])[0], indent + 1)

        if (
            self.tokenizer.nextTokenType == "keyword"
            and self.tokenizer.nextToken == "else"
        ):
            self.vm_writer._xmlOutput(self._parseKeyword(["else"])[0], indent + 1)
            self.vm_writer._xmlOutput(self._parseSymbol(["{"])[0], indent + 1)
            self.compileStatements(indent + 1)
            self.vm_writer._xmlOutput(self._parseSymbol(["}"])[0], indent + 1)

        self.vm_writer._xmlOutput("</ifStatement>", indent)

    def compileWhile(self, indent):
        self.vm_writer._xmlOutput("<whileStatement>", indent)
        self.vm_writer._xmlOutput(self._parseKeyword(["while"])[0], indent + 1)

        self.vm_writer._xmlOutput(self._parseSymbol(["("])[0], indent + 1)
        self.compileExpression(indent + 1)
        self.vm_writer._xmlOutput(self._parseSymbol([")"])[0], indent + 1)

        self.vm_writer._xmlOutput(self._parseSymbol(["{"])[0], indent + 1)
        self.compileStatements(indent + 1)
        self.vm_writer._xmlOutput(self._parseSymbol(["}"])[0], indent + 1)

        self.vm_writer._xmlOutput("</whileStatement>", indent)

    def compileDo(self, indent):
        self.vm_writer._xmlOutput("<doStatement>", indent)
        self.vm_writer._xmlOutput(self._parseKeyword(["do"])[0], indent + 1)
        self.compileExpression(indent + 1)
        self.vm_writer._xmlOutput(self._parseSymbol([";"])[0], indent + 1)
        self.vm_writer._xmlOutput("</doStatement>", indent)

        self.vm_writer.writePop("temp", 0)

    def compileReturn(self, indent):
        self.vm_writer._xmlOutput("<returnStatement>", indent)
        self.vm_writer._xmlOutput(self._parseKeyword(["return"])[0], indent + 1)
        if not (
            self.tokenizer.nextTokenType == "symbol" and self.tokenizer.nextToken == ";"
        ):
            self.compileExpression(indent + 1)
        self.vm_writer._xmlOutput(self._parseSymbol([";"])[0], indent + 1)
        self.vm_writer._xmlOutput("</returnStatement>", indent)

        self.vm_writer.writeReturn()

    def compileExpression(self, indent):
        self.vm_writer._xmlOutput("<expression>", indent)
        self.compileTerm(indent + 1)
        if self.tokenizer.nextTokenType == "symbol" and self.tokenizer.nextToken in OPS:
            self.vm_writer._xmlOutput(self._parseSymbol(OPS)[0], indent + 1)
            self.compileTerm(indent + 1)
        self.vm_writer._xmlOutput("</expression>", indent)

    def compileTerm(self, indent):
        self.vm_writer._xmlOutput("<term>", indent)
        if self.tokenizer.nextTokenType == "integerConstant":
            integer_xml, integer_value = self._parseIntegerConstant()
            self.vm_writer._xmlOutput(integer_xml, indent + 1)
            self.vm_writer.writePush("constant", integer_value)
        if self.tokenizer.nextTokenType == "stringConstant":
            self.vm_writer._xmlOutput(self._parseStringConstant(), indent + 1)
        elif self.tokenizer.nextTokenType == "identifier":
            identifier_xml, identifier_name = self._parseIdentifier()
            self.vm_writer._xmlOutput(identifier_xml, indent + 1)
            if self.tokenizer.nextTokenType == "symbol":
                if self.tokenizer.nextToken in [".", "("]:
                    callee_name = identifier_name
                    if self.tokenizer.nextTokenType == "symbol" and self.tokenizer.nextToken == ".":
                        self.vm_writer._xmlOutput(self._parseSymbol(["."])[0], indent + 1)
                        identifier_xml, method_name = self._parseIdentifier()
                        callee_name += f".{method_name}"
                        self.vm_writer._xmlOutput(identifier_xml, indent + 1)

                    self.vm_writer._xmlOutput(self._parseSymbol(["("])[0], indent + 1)
                    num_arguments = self.compileExpressionList(indent + 1)
                    self.vm_writer._xmlOutput(self._parseSymbol([")"])[0], indent + 1)
                    self.vm_writer.writeCall(callee_name, num_arguments)
                elif self.tokenizer.nextToken == "[":
                    self.vm_writer._xmlOutput(self._parseSymbol(["["])[0], indent + 1)
                    self.compileExpression(indent + 1)
                    self.vm_writer._xmlOutput(self._parseSymbol(["]"])[0], indent + 1)
        elif self.tokenizer.nextTokenType == "keyword":
            self.vm_writer._xmlOutput(self._parseKeyword(KEYWORD_CONSTANTS)[0], indent + 1)
        elif self.tokenizer.nextTokenType == "symbol":
            if self.tokenizer.nextToken == "(":
                self.vm_writer._xmlOutput(self._parseSymbol(["("])[0], indent + 1)
                self.compileExpression(indent + 1)
                self.vm_writer._xmlOutput(self._parseSymbol([")"])[0], indent + 1)
            elif self.tokenizer.nextToken in UNARY_OPS:
                self.vm_writer._xmlOutput(self._parseSymbol(UNARY_OPS)[0], indent + 1)
                self.compileTerm(indent + 1)
        self.vm_writer._xmlOutput("</term>", indent)

    def compileExpressionList(self, indent) -> int:
        self.vm_writer._xmlOutput("<expressionList>", indent)

        num_arguments = 0

        if not (
            self.tokenizer.nextTokenType == "symbol" and self.tokenizer.nextToken == ")"
        ):
            self.compileExpression(indent + 1)
            num_arguments += 1
            while (
                self.tokenizer.nextTokenType == "symbol"
                and self.tokenizer.nextToken == ","
            ):
                self.vm_writer._xmlOutput(self._parseSymbol([","])[0], indent + 1)
                self.compileExpression(indent + 1)
                num_arguments += 1

        self.vm_writer._xmlOutput("</expressionList>", indent)
        return num_arguments
