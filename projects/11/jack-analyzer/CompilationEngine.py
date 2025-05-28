from io import TextIOWrapper
from typing import Sequence, Tuple, NoReturn
from constants import PRIMITIVE_TYPES, KEYWORD_CONSTANTS, OPS, UNARY_OPS, SYMBOL_SEGMENTS
from JackTokenizer import JackTokenizer
from SymbolTable import SymbolTable
from VMWriter import VMWriter


class CompilationError(Exception):
    pass


class CompilationEngine:
    def __init__(self, in_file: TextIOWrapper, vm_writer: VMWriter):
        self.file_path = in_file.name
        self.tokenizer = JackTokenizer(in_file.read())
        self.class_symbol_table = SymbolTable()
        self.method_symbol_table = SymbolTable()
        self.vm_writer = vm_writer
        self.output = ""
        # Counter used to generate unique labels for while loops
        self._num_whiles: int = 0
        self._num_ifs: int = 0
        self._current_class_name: str = ""
        self._current_subroutine_name: str = ""
        # Boolean used to keep track of if we've seen a return in a subroutine yet
        self._return_seen_this_sub = False

    def _raise_compilation_error(self, msg) -> NoReturn:
        out = f"\nFile: {self.file_path}:{self.tokenizer.tokenLineNumber + 1}"
        if self._current_class_name:
            out += f"\nSubroutine: {self._current_class_name}.{self._current_subroutine_name}"
        out += f"\n{msg}"
        raise CompilationError(out)

    def _symbol_tables_lookup(self, variable_identifier: str) -> Tuple[SYMBOL_SEGMENTS, int, str]:
        if self.method_symbol_table.hasEntry(variable_identifier):
            return (
                self.method_symbol_table.kindOf(variable_identifier),
                self.method_symbol_table.indexOf(variable_identifier),
                self.method_symbol_table.typeOf(variable_identifier),
            )
        elif self.class_symbol_table.hasEntry(variable_identifier):
            return (
                self.class_symbol_table.kindOf(variable_identifier),
                self.class_symbol_table.indexOf(variable_identifier),
                self.class_symbol_table.typeOf(variable_identifier),
            )
        else:
            return self._raise_compilation_error(f"Couldn't find identifier {variable_identifier}")

    def _symbol_tables_have_entry(self, variable_identifier: str) -> bool:
        return self.method_symbol_table.hasEntry(variable_identifier) or self.class_symbol_table.hasEntry(variable_identifier)

    def _parseKeyword(self, expectedKeywords: Sequence[str], indent: int) -> str:
        self.tokenizer.advance()
        if self.tokenizer.tokenType == "keyword" and self.tokenizer.token is not None and self.tokenizer.token in expectedKeywords:
            return self.tokenizer.token
        else:
            return self._raise_compilation_error(f"Expected keyword(s) {expectedKeywords}, got {self.tokenizer.tokenType} {self.tokenizer.token}")

    def _parseSymbol(self, expectedSymbols: Sequence[str], indent: int) -> str:
        self.tokenizer.advance()
        if self.tokenizer.tokenType == "symbol" and self.tokenizer.token is not None and self.tokenizer.token in expectedSymbols:
            return self.tokenizer.token
        else:
            return self._raise_compilation_error(f"Expected symbol(s) {expectedSymbols}, got {self.tokenizer.tokenType} {self.tokenizer.token}")

    def _parseIntegerConstant(self, indent: int) -> int:
        self.tokenizer.advance()
        if self.tokenizer.tokenType == "integerConstant" and self.tokenizer.token is not None:
            return int(self.tokenizer.token)
        else:
            return self._raise_compilation_error(f"Expected integer constant, got {self.tokenizer.tokenType} {self.tokenizer.token}")

    def _parseStringConstant(self, indent: int) -> str:
        self.tokenizer.advance()
        if self.tokenizer.tokenType == "stringConstant" and self.tokenizer.token is not None:
            return self.tokenizer.token[1:-1]
        else:
            return self._raise_compilation_error(f"Expected string constant, got {self.tokenizer.tokenType} {self.tokenizer.token}")

    def _parseIdentifier(self, indent: int) -> str:
        self.tokenizer.advance()
        if self.tokenizer.tokenType == "identifier" and self.tokenizer.token is not None:
            return self.tokenizer.token
        else:
            return self._raise_compilation_error(f"Expected identifier, got {self.tokenizer.tokenType} {self.tokenizer.token}")

    def compileClass(self, indent: int = 0):
        self._parseKeyword(["class"], indent + 1)
        self._current_class_name = self._parseIdentifier(indent + 1)

        self._parseSymbol(["{"], indent + 1)

        while self.tokenizer.nextTokenType == "keyword" and self.tokenizer.nextToken in ("static", "field"):
            self.compileClassVarDec(indent + 1)

        while self.tokenizer.nextTokenType == "keyword" and self.tokenizer.nextToken in ("constructor", "function", "method"):
            self.compileSubroutine(indent + 1)

        self._parseSymbol(["}"], indent + 1)

        if self.tokenizer.hasMoreTokens():
            self.tokenizer.advance()
            self._raise_compilation_error(f"Nothing expected after class definition, got {self.tokenizer.tokenType} {self.tokenizer.token}")

    def _parseType(self, indent: int, *, include_void: bool = False):
        if self.tokenizer.nextTokenType == "keyword" and (
            self.tokenizer.nextToken in PRIMITIVE_TYPES or (include_void and self.tokenizer.nextToken == "void")
        ):
            return self._parseKeyword(PRIMITIVE_TYPES + (("void",) if include_void else ()), indent)
        else:
            return self._parseIdentifier(indent)

    def compileClassVarDec(self, indent: int):
        if self._parseKeyword(["static", "field"], indent + 1) == "static":
            var_kind = "static"
        else:
            var_kind = "this"
        var_type = self._parseType(indent + 1)
        var_name = self._parseIdentifier(indent + 1)
        self.class_symbol_table.define(var_name, var_type, var_kind)

        while self.tokenizer.nextTokenType == "symbol" and self.tokenizer.nextToken == ",":
            self._parseSymbol([","], indent + 1)
            var_name = self._parseIdentifier(indent + 1)
            self.class_symbol_table.define(var_name, var_type, var_kind)

        self._parseSymbol([";"], indent + 1)

    def compileSubroutine(self, indent: int):
        subroutine_type = self._parseKeyword(["constructor", "function", "method"], indent + 1)
        self._parseType(indent + 1, include_void=True)
        self._current_subroutine_name = self._parseIdentifier(indent + 1)

        if subroutine_type == "method":
            # Add this to the argument list for a method automatically
            self.method_symbol_table.define("this", self._current_class_name, "argument")

        self._parseSymbol(["("], indent + 1)
        self.compileParameterList(indent + 1)
        self._parseSymbol([")"], indent + 1)

        self.compileSubroutineBody(subroutine_type, self._current_subroutine_name, indent + 1)

        self.method_symbol_table.reset()
        self._return_seen_this_sub = False

    def compileParameterList(self, indent: int):
        if self.tokenizer.nextTokenType in ["keyword", "identifier"]:
            param_type = self._parseType(indent + 1)
            param_name = self._parseIdentifier(indent + 1)
            self.method_symbol_table.define(param_name, param_type, "argument")

        while self.tokenizer.nextTokenType == "symbol" and self.tokenizer.nextToken == ",":
            self._parseSymbol([","], indent + 1)
            param_type = self._parseType(indent + 1)
            param_name = self._parseIdentifier(indent + 1)
            self.method_symbol_table.define(param_name, param_type, "argument")

    def compileSubroutineBody(self, subroutine_type: str, subroutine_name: str, indent: int):
        self._parseSymbol(["{"], indent + 1)
        num_locals = 0
        while self.tokenizer.nextTokenType == "keyword" and self.tokenizer.nextToken == "var":
            num_locals += self.compileVarDec(indent + 1)

        self.vm_writer.writeFunction(f"{self._current_class_name}.{subroutine_name}", num_locals)

        if subroutine_type == "method":
            # The object that the method is called on is automatically added as the first argument
            #   this code then copies it into the pointer segment, so that field references work properly
            self.vm_writer.writePush("argument", 0)
            self.vm_writer.writePop("pointer", 0)
        elif subroutine_type == "constructor":
            # Add memory allocation for the objects fields to the start of the constructor
            self.vm_writer.writePush("constant", self.class_symbol_table.varCount("this"))
            self.vm_writer.writeCall("Memory.alloc", 1)
            self.vm_writer.writePop("pointer", 0)

        self.compileStatements(indent + 1)
        self._parseSymbol(["}"], indent + 1)
        if not self._return_seen_this_sub:
            self._raise_compilation_error(f"return must be called at least once per function")

    def compileVarDec(self, indent: int):
        num_locals = 0

        self._parseKeyword(["var"], indent + 1)
        var_type = self._parseType(indent + 1)
        var_identifier = self._parseIdentifier(indent + 1)
        self.method_symbol_table.define(var_identifier, var_type, "local")
        num_locals += 1

        while self.tokenizer.nextTokenType == "symbol" and self.tokenizer.nextToken == ",":
            self._parseSymbol([","], indent + 1)
            var_identifier = self._parseIdentifier(indent + 1)
            self.method_symbol_table.define(var_identifier, var_type, "local")
            num_locals += 1

        self._parseSymbol([";"], indent + 1)
        return num_locals

    def compileStatements(self, indent: int):
        while self.tokenizer.nextTokenType == "keyword" and self.tokenizer.nextToken in ["let", "if", "while", "do", "return"]:
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

    def compileLet(self, indent: int):
        self.vm_writer.writeComment("let")

        self._parseKeyword(["let"], indent + 1)
        variable_identifier = self._parseIdentifier(indent + 1)

        segment, index, _type = self._symbol_tables_lookup(variable_identifier)

        # Whether the address to save the result in is sitting just below the expression result in the stack
        #   i.e. we are storing the output in an array
        output_address_in_stack = False

        if self.tokenizer.nextToken == "[":
            self.vm_writer.writePush(segment, index)
            self._parseSymbol(["["], indent + 1)
            self.compileExpression(indent + 1)
            self._parseSymbol(["]"], indent + 1)
            self.vm_writer.writeArithmetic("add")
            output_address_in_stack = True

        self._parseSymbol(["="], indent + 1)

        self.compileExpression(indent + 1)
        if output_address_in_stack:
            self.vm_writer.writePop("temp", 0)
            self.vm_writer.writePop("pointer", 1)
            self.vm_writer.writePush("temp", 0)
            self.vm_writer.writePop("that", 0)
        else:
            self.vm_writer.writePop(segment, index)

        self._parseSymbol([";"], indent + 1)

    def compileIf(self, indent: int):
        self.vm_writer.writeComment("if")

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

        if self.tokenizer.nextTokenType == "keyword" and self.tokenizer.nextToken == "else":
            self._parseKeyword(["else"], indent + 1)
            self._parseSymbol(["{"], indent + 1)
            self.compileStatements(indent + 1)
            self._parseSymbol(["}"], indent + 1)

        self.vm_writer.writeLabel(f"{if_label}L2")

    def compileWhile(self, indent: int):
        self.vm_writer.writeComment("while")

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

    def compileDo(self, indent: int):
        self.vm_writer.writeComment("do")

        self._parseKeyword(["do"], indent + 1)
        self.compileExpression(indent + 1)
        self._parseSymbol([";"], indent + 1)

        self.vm_writer.writePop("temp", 0)

    def compileReturn(self, indent: int):
        self.vm_writer.writeComment("return")

        self._parseKeyword(["return"], indent + 1)
        self._return_seen_this_sub = True
        if not (self.tokenizer.nextTokenType == "symbol" and self.tokenizer.nextToken == ";"):
            self.compileExpression(indent + 1)
        else:
            # Return 0 if no expression
            self.vm_writer.writePush("constant", 0)

        self._parseSymbol([";"], indent + 1)

        self.vm_writer.writeReturn()

    def compileExpression(self, indent: int):
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
            elif operator_symbol == "&":
                self.vm_writer.writeArithmetic("and")
            elif operator_symbol == "|":
                self.vm_writer.writeArithmetic("or")
            elif operator_symbol == "<":
                self.vm_writer.writeArithmetic("lt")
            elif operator_symbol == ">":
                self.vm_writer.writeArithmetic("gt")
            elif operator_symbol == "=":
                self.vm_writer.writeArithmetic("eq")
            else:
                self._raise_compilation_error(f"compileExpression: invalid operator '{operator_symbol}'")

    def compileTerm(self, indent: int):
        if self.tokenizer.nextTokenType == "integerConstant":
            integer_value = self._parseIntegerConstant(indent + 1)
            self.vm_writer.writePush("constant", integer_value)
        elif self.tokenizer.nextTokenType == "stringConstant":
            string_value = self._parseStringConstant(indent + 1)
            self.vm_writer.writePush("constant", len(string_value))
            self.vm_writer.writeCall("String.new", 1)
            for c in string_value:
                self.vm_writer.writePush("constant", ord(c))
                self.vm_writer.writeCall("String.appendChar", 2)
        elif self.tokenizer.nextTokenType == "identifier":
            # Could be:
            #   a simple variable 'x'
            #   an object variable 'x' in 'x.blah'
            #   an object method 'x' in 'x.run()'
            #   a class function 'X' in 'X.parse()'
            identifier_name = self._parseIdentifier(indent + 1)
            if self.tokenizer.nextTokenType == "symbol" and self.tokenizer.nextToken in [".", "(", "["]:  # type: ignore
                if self.tokenizer.nextToken in [".", "("]:
                    # Function/Method call
                    if self.tokenizer.nextTokenType == "symbol" and self.tokenizer.nextToken == ".":
                        self._parseSymbol(["."], indent + 1)
                        method_name = self._parseIdentifier(indent + 1)
                        # If it's a defined variable, then we are calling a method on an object
                        if self._symbol_tables_have_entry(identifier_name):
                            identifier_kind, identifier_index, identifier_type = self._symbol_tables_lookup(identifier_name)
                            self.vm_writer.writePush(identifier_kind, identifier_index)
                            callee_name = f"{identifier_type}.{method_name}"
                            num_arguments = 1
                        # Otherwise we are calling a funtion on a class
                        else:
                            callee_name = f"{identifier_name}.{method_name}"
                            num_arguments = 0
                    else:
                        callee_name = f"{self._current_class_name}.{identifier_name}"
                        num_arguments = 1
                        self.vm_writer.writePush("pointer", 0)

                    self._parseSymbol(["("], indent + 1)
                    num_arguments += self.compileExpressionList(indent + 1)
                    self._parseSymbol([")"], indent + 1)
                    self.vm_writer.writeCall(callee_name, num_arguments)
                else:
                    identifier_kind, identifier_index, identifier_type = self._symbol_tables_lookup(identifier_name)
                    self.vm_writer.writePush(identifier_kind, identifier_index)
                    # Array access
                    self._parseSymbol(["["], indent + 1)
                    self.compileExpression(indent + 1)
                    self._parseSymbol(["]"], indent + 1)
                    self.vm_writer.writeArithmetic("add")
                    self.vm_writer.writePop("pointer", 1)
                    self.vm_writer.writePush("that", 0)
            else:
                segment, index, _type = self._symbol_tables_lookup(identifier_name)
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
                self.vm_writer.writePush("pointer", 0)
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

    def compileExpressionList(self, indent: int) -> int:
        num_arguments = 0

        if not (self.tokenizer.nextTokenType == "symbol" and self.tokenizer.nextToken == ")"):
            self.compileExpression(indent + 1)
            num_arguments += 1
            while self.tokenizer.nextTokenType == "symbol" and self.tokenizer.nextToken == ",":
                self._parseSymbol([","], indent + 1)
                self.compileExpression(indent + 1)
                num_arguments += 1

        return num_arguments
