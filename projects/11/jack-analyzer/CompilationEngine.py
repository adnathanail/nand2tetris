from constants import PRIMITIVE_TYPES, KEYWORD_CONSTANTS, OPS, UNARY_OPS, SEGMENTS
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
        # Counter used to generate unique labels for while loops
        self._num_whiles = 0
        self._num_ifs = 0

    def _symbol_tables_lookup(self, variable_identifier: str) -> tuple[SEGMENTS, int]:
        if variable_identifier in self.method_symbol_table._entries:
            return self.method_symbol_table.kindOf(variable_identifier), self.method_symbol_table.indexOf(variable_identifier)
        elif variable_identifier in self.class_symbol_table._entries:
            return self.class_symbol_table.kindOf(variable_identifier), self.class_symbol_table.indexOf(variable_identifier)
        else:
            raise CompilationError(f"Couldn't find identifier {variable_identifier}")

    def _parseKeyword(self, expectedKeywords, indent) -> str:
        self.tokenizer.advance()
        if (
            self.tokenizer.tokenType == "keyword"
            and type(self.tokenizer.token) is str
            and self.tokenizer.token in expectedKeywords
        ):
            self.vm_writer._xmlOutput(f"<keyword> {self.tokenizer.token} </keyword>", indent)
            return self.tokenizer.token
        else:
            raise CompilationError(
                f"Expected keyword(s) {expectedKeywords}, got {self.tokenizer.tokenType} {self.tokenizer.token}"
            )

    def _parseSymbol(self, expectedSymbols, indent) -> str:
        self.tokenizer.advance()
        if (
            self.tokenizer.tokenType == "symbol"
            and type(self.tokenizer.token) is str
            and self.tokenizer.token in expectedSymbols
        ):
            self.vm_writer._xmlOutput(f"<symbol> {self.tokenizer.token} </symbol>", indent)
            return self.tokenizer.token
        else:
            raise CompilationError(
                f"Expected symbol(s) {expectedSymbols}, got {self.tokenizer.tokenType} {self.tokenizer.token}"
            )

    def _parseIntegerConstant(self, indent) -> int:
        self.tokenizer.advance()
        if self.tokenizer.tokenType == "integerConstant" and type(self.tokenizer.token) is int:
            self.vm_writer._xmlOutput(f"<integerConstant> {self.tokenizer.token} </integerConstant>", indent)
            return self.tokenizer.token
        else:
            raise CompilationError(
                f"Expected integer constant, got {self.tokenizer.tokenType} {self.tokenizer.token}"
            )

    def _parseStringConstant(self, indent) -> str:
        self.tokenizer.advance()
        if self.tokenizer.tokenType == "stringConstant" and type(self.tokenizer.token) is str:
            self.vm_writer._xmlOutput(f"<stringConstant> {self.tokenizer.token} </stringConstant>", indent)
            return self.tokenizer.token
        else:
            raise CompilationError(
                f"Expected string constant, got {self.tokenizer.tokenType} {self.tokenizer.token}"
            )

    def _parseIdentifier(self, indent) -> str:
        self.tokenizer.advance()
        if self.tokenizer.tokenType == "identifier" and type(self.tokenizer.token) is str:
            self.vm_writer._xmlOutput(f"<identifier> {self.tokenizer.token} </identifier>", indent)
            return self.tokenizer.token
        else:
            raise CompilationError(
                f"Expected identifier, got {self.tokenizer.tokenType} {self.tokenizer.token}"
            )

    def compileClass(self, indent=0):
        self.vm_writer._xmlOutput("<class>", indent)

        self._parseKeyword(["class"], indent + 1)
        class_name = self._parseIdentifier(indent + 1)

        self._parseSymbol(["{"], indent + 1)

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

        self._parseSymbol(["}"], indent + 1)

        self.vm_writer._xmlOutput("</class>", indent)

        if self.tokenizer.hasMoreTokens():
            self.tokenizer.advance()
            raise CompilationError(
                f"Nothing expected after class definition, got {self.tokenizer.tokenType} {self.tokenizer.token}"
            )

    def _parseType(self, indent, *, include_void=False):
        if self.tokenizer.nextTokenType == "keyword" and (
            self.tokenizer.nextToken in PRIMITIVE_TYPES
            or (include_void and self.tokenizer.nextToken == "void")
        ):
            return self._parseKeyword(
                PRIMITIVE_TYPES + (("void",) if include_void else ()),
                indent
            )
        else:
            return self._parseIdentifier(indent)

    def compileClassVarDec(self, indent):
        self.vm_writer._xmlOutput("<classVarDec>", indent)

        self._parseKeyword(["static", "field"], indent + 1)
        self._parseType(indent + 1)
        self._parseIdentifier(indent + 1)

        while (
            self.tokenizer.nextTokenType == "symbol" and self.tokenizer.nextToken == ","
        ):
            self._parseSymbol([","], indent + 1)
            self._parseIdentifier(indent + 1)

        self._parseSymbol([";"], indent + 1)
        self.vm_writer._xmlOutput("</classVarDec>", indent)

    def compileSubroutine(self, indent, class_name):
        self.vm_writer._xmlOutput("<subroutineDec>", indent)
        self._parseKeyword(["constructor", "function", "method"], indent + 1)
        self._parseType(indent + 1, include_void=True)
        subroutine_name = self._parseIdentifier(indent + 1)

        self._parseSymbol(["("], indent + 1)
        self.compileParameterList(indent + 1)
        self._parseSymbol([")"], indent + 1)

        self.compileSubroutineBody(f"{class_name}.{subroutine_name}", indent + 1)

        self.vm_writer._xmlOutput("</subroutineDec>", indent)
        self.method_symbol_table.reset()
        

    def compileParameterList(self, indent):
        self.vm_writer._xmlOutput("<parameterList>", indent)

        if self.tokenizer.nextTokenType in ["keyword", "identifier"]:
            param_type = self._parseType(indent + 1)
            param_name = self._parseIdentifier(indent + 1)
            self.method_symbol_table.define(param_name, param_type, "argument")

        while (
            self.tokenizer.nextTokenType == "symbol" and self.tokenizer.nextToken == ","
        ):
            self._parseSymbol([","], indent + 1)
            param_type = self._parseType(indent + 1)
            param_name = self._parseIdentifier(indent + 1)
            self.method_symbol_table.define(param_name, param_type, "argument")

        self.vm_writer._xmlOutput("</parameterList>", indent)

    def compileSubroutineBody(self, subroutine_name, indent):
        self.vm_writer._xmlOutput("<subroutineBody>", indent)

        self._parseSymbol(["{"], indent + 1)
        num_locals = 0
        while (
            self.tokenizer.nextTokenType == "keyword"
            and self.tokenizer.nextToken == "var"
        ):
            num_locals += self.compileVarDec(indent + 1)

        self.vm_writer.writeFunction(subroutine_name, num_locals)

        self.compileStatements(indent + 1)
        self._parseSymbol(["}"], indent + 1)

        self.vm_writer._xmlOutput("</subroutineBody>", indent)

    def compileVarDec(self, indent):
        num_locals = 0

        self.vm_writer._xmlOutput("<varDec>", indent)

        self._parseKeyword(["var"], indent + 1)
        var_type = self._parseType(indent + 1)
        var_identifier = self._parseIdentifier(indent + 1)
        self.method_symbol_table.define(var_identifier, var_type, "local")
        num_locals += 1

        while (
            self.tokenizer.nextTokenType == "symbol" and self.tokenizer.nextToken == ","
        ):
            self._parseSymbol([","], indent + 1)
            var_identifier = self._parseIdentifier(indent + 1)
            self.method_symbol_table.define(var_identifier, var_type, "local")
            num_locals += 1

        self._parseSymbol([";"], indent + 1)
        self.vm_writer._xmlOutput("</varDec>", indent)
        return num_locals

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
        self.vm_writer.writeComment("let")

        self.vm_writer._xmlOutput("<letStatement>", indent)
        self._parseKeyword(["let"], indent + 1)
        variable_identifier = self._parseIdentifier(indent + 1)

        if self.tokenizer.nextToken == "[":
            self._parseSymbol(["["], indent + 1)
            self.compileExpression(indent + 1)
            self._parseSymbol(["]"], indent + 1)

        self._parseSymbol(["="], indent + 1)

        self.compileExpression(indent + 1)
        segment, index = self._symbol_tables_lookup(variable_identifier)
        self.vm_writer.writePop(segment, index)

        self._parseSymbol([";"], indent + 1)
        self.vm_writer._xmlOutput("</letStatement>", indent)

    def compileIf(self, indent):
        self.vm_writer.writeComment("if")

        self.vm_writer._xmlOutput("<ifStatement>", indent)
        self._parseKeyword(["if"], indent + 1)

        self._parseSymbol(["("], indent + 1)
        self.compileExpression(indent + 1)
        self._parseSymbol([")"], indent + 1)

        if_label = f"IF{self._num_ifs}"
        self._num_ifs += 1
        self.vm_writer.writeArithmetic("not")
        self.vm_writer.writeIf(f"{if_label}L1")

        self._parseSymbol(["{"], indent + 1)
        self.compileStatements(indent + 1)
        self._parseSymbol(["}"], indent + 1)

        self.vm_writer.writeGoto(f"{if_label}L2")
        self.vm_writer.writeLabel(f"{if_label}L1")

        if (
            self.tokenizer.nextTokenType == "keyword"
            and self.tokenizer.nextToken == "else"
        ):
            self._parseKeyword(["else"], indent + 1)
            self._parseSymbol(["{"], indent + 1)
            self.compileStatements(indent + 1)
            self._parseSymbol(["}"], indent + 1)

        self.vm_writer.writeLabel(f"{if_label}L2")

        self.vm_writer._xmlOutput("</ifStatement>", indent)

    def compileWhile(self, indent):
        self.vm_writer.writeComment("while")

        self.vm_writer._xmlOutput("<whileStatement>", indent)
        self._parseKeyword(["while"], indent + 1)

        while_label = f"WHILE{self._num_whiles}"
        self._num_whiles += 1
        self.vm_writer.writeLabel(f"{while_label}L1")

        self._parseSymbol(["("], indent + 1)
        self.compileExpression(indent + 1)
        self._parseSymbol([")"], indent + 1)

        self.vm_writer.writeArithmetic("not")
        self.vm_writer.writeIf(f"{while_label}L2")

        self._parseSymbol(["{"], indent + 1)
        self.compileStatements(indent + 1)
        self._parseSymbol(["}"], indent + 1)

        self.vm_writer.writeGoto(f"{while_label}L1")
        self.vm_writer.writeLabel(f"{while_label}L2")

        self.vm_writer._xmlOutput("</whileStatement>", indent)

    def compileDo(self, indent):
        self.vm_writer.writeComment("do")

        self.vm_writer._xmlOutput("<doStatement>", indent)
        self._parseKeyword(["do"], indent + 1)
        self.compileExpression(indent + 1)
        self._parseSymbol([";"], indent + 1)
        self.vm_writer._xmlOutput("</doStatement>", indent)

        self.vm_writer.writePop("temp", 0)

    def compileReturn(self, indent):
        self.vm_writer.writeComment("return")

        self.vm_writer._xmlOutput("<returnStatement>", indent)
        self._parseKeyword(["return"], indent + 1)
        if not (
            self.tokenizer.nextTokenType == "symbol" and self.tokenizer.nextToken == ";"
        ):
            self.compileExpression(indent + 1)
        else:
            # Return 0 if no expression
            self.vm_writer.writePush("constant", 0)

        self._parseSymbol([";"], indent + 1)
        self.vm_writer._xmlOutput("</returnStatement>", indent)

        self.vm_writer.writeReturn()

    def compileExpression(self, indent):
        self.vm_writer._xmlOutput("<expression>", indent)
        self.compileTerm(indent + 1)
        if self.tokenizer.nextTokenType == "symbol" and self.tokenizer.nextToken in OPS:
            operator_symbol = self._parseSymbol(OPS, indent + 1)
            self.compileTerm(indent + 1)
            if operator_symbol == "+":
                self.vm_writer.writeArithmetic("add")
            elif operator_symbol == "-":
                self.vm_writer.writeArithmetic("sub")
            elif operator_symbol == "*":
                self.vm_writer.writeCall("Math.multiply", 2)
            elif operator_symbol == "/":
                self.vm_writer.writeCall("Math.divide", 2)
            elif operator_symbol == "&amp;":
                self.vm_writer.writeArithmetic("and")
            elif operator_symbol == "|":
                self.vm_writer.writeArithmetic("or")
            elif operator_symbol == "&lt;":
                self.vm_writer.writeArithmetic("lt")
            elif operator_symbol == "&gt;":
                self.vm_writer.writeArithmetic("gt")
            elif operator_symbol == "=":
                self.vm_writer.writeArithmetic("eq")
            else:
                raise CompilationError(f"compileExpression: invalid operator '{operator_symbol}'")
        self.vm_writer._xmlOutput("</expression>", indent)

    def compileTerm(self, indent):
        self.vm_writer._xmlOutput("<term>", indent)
        if self.tokenizer.nextTokenType == "integerConstant":
            integer_value = self._parseIntegerConstant(indent + 1)
            self.vm_writer.writePush("constant", integer_value)
        if self.tokenizer.nextTokenType == "stringConstant":
            self._parseStringConstant(indent + 1)
        elif self.tokenizer.nextTokenType == "identifier":
            identifier_name = self._parseIdentifier(indent + 1)
            if self.tokenizer.nextTokenType == "symbol" and self.tokenizer.nextToken in [".", "(", "["]:
                if self.tokenizer.nextToken in [".", "("]:
                    # Function/Method call
                    callee_name = identifier_name
                    if self.tokenizer.nextTokenType == "symbol" and self.tokenizer.nextToken == ".":
                        self._parseSymbol(["."], indent + 1)
                        method_name = self._parseIdentifier(indent + 1)
                        callee_name += f".{method_name}"

                    self._parseSymbol(["("], indent + 1)
                    num_arguments = self.compileExpressionList(indent + 1)
                    self._parseSymbol([")"], indent + 1)
                    self.vm_writer.writeCall(callee_name, num_arguments)
                else:
                    # Array access
                    self._parseSymbol(["["], indent + 1)
                    self.compileExpression(indent + 1)
                    self._parseSymbol(["]"], indent + 1)
            else:
                segment, index = self._symbol_tables_lookup(identifier_name)
                self.vm_writer.writePush(segment, index)
        elif self.tokenizer.nextTokenType == "keyword":
            keyword_constant = self._parseKeyword(KEYWORD_CONSTANTS, indent + 1)
            if keyword_constant == "true":
                self.vm_writer.writePush("constant", 1)
                self.vm_writer.writeArithmetic("neg")
            elif keyword_constant == "false":
                self.vm_writer.writePush("constant", 0)
            elif keyword_constant == "null":
                self.vm_writer.writePush("constant", 0)
            elif keyword_constant == "this":
                self.vm_writer.writePush("pointer", 1)
        elif self.tokenizer.nextTokenType == "symbol":
            if self.tokenizer.nextToken == "(":
                self._parseSymbol(["("], indent + 1)
                self.compileExpression(indent + 1)
                self._parseSymbol([")"], indent + 1)
            elif self.tokenizer.nextToken in UNARY_OPS:
                operator_symbol = self._parseSymbol(UNARY_OPS, indent + 1)
                self.compileTerm(indent + 1)
                if operator_symbol == "-":
                    self.vm_writer.writeArithmetic("neg")
                elif operator_symbol == "~":
                    self.vm_writer.writeArithmetic("not")
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
                self._parseSymbol([","], indent + 1)
                self.compileExpression(indent + 1)
                num_arguments += 1

        self.vm_writer._xmlOutput("</expressionList>", indent)
        return num_arguments
