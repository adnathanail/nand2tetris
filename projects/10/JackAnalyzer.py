import os
import sys
from pathlib import Path
from typing import Literal
from typing import Generator


KEYWORDS = (
    "class", "constructor", "function", "method", "field", "static", "var",
    "int", "char", "boolean", "void", "true", "false", "null", "this", "let",
    "do", "if", "else", "while", "return"
)

SYMBOLS = (
    "{", "}", "(", ")", "[", "]", ".", ",", ";", "+", "-", "*", "/", "&",
    "|", "<", ">", "=", "~"
)

SYMBOL_LOOKUP = {
    "<": "&lt;",
    ">": "&gt;",
    '"': "&quot;",
    "&": "&amp;",
}

def _strip_comments_and_whitespace(in_text: str) -> str:
    lines = in_text.splitlines()
    i = 0
    in_comment = False

    out = ""
    while i < len(lines):
        line = lines[i]
        # Currently inside multiline comment
        if in_comment:
            # If closing */, remove everything up to it
            if "*/" in line:
                line = line[line.index("*/") + 2:]
                in_comment = False
            # If no closing */, skip the line
            else:
                i += 1
                continue
        # Remove all /* XXX */ sections, and enter multiline comment mode if we see a /* without a */
        while "/*" in line:
            if "*/" in line:
                line = line[:line.index("/*")] + line[line.index("*/") + 2:]
            else:
                line = line[:line.index("/*")]
                in_comment = True
                break
        # Remove single line comment
        if "//" in line:
            line = line[:line.index("//")]
        # Remove whitespace
        line = line.strip()
        # Output next line of code (no comments no spaces)
        if line:
            out += line
        i += 1
    return out


class JackTokenizer:
    def __init__(self, jack_code):
        self.text = _strip_comments_and_whitespace(jack_code)
        self.tokenStart = 0
        self.tokenEnd = 0
        self._tokenType = None

    def hasMoreTokens(self) -> bool:
        return (self.tokenStart + 1) < len(self.text)
    
    def _lexKeyWord(self):
        for kw in KEYWORDS:
            if kw == self.text[self.tokenStart:self.tokenStart + len(kw)]:
                return self.tokenStart + len(kw)
        return False

    def _lexSymbol(self) -> str:
        if self.text[self.tokenStart] in SYMBOLS:
            return self.tokenStart + 1
        return False

    def _lexIntegerConstant(self) -> str:
        if not self.text[self.tokenStart].isdigit():
            return False
        endInd = self.tokenStart + 1
        decimal_used = False
        while self.text[endInd].isdigit() or (not decimal_used and self.text[endInd] == "."):
            if self.text[endInd] == ".":
                decimal_used = True
            endInd += 1
        return endInd

    def _lexStringConstant(self) -> str:
        if self.text[self.tokenStart] != '"':
            return False
        endInd = self.tokenStart + 1
        while self.text[endInd] not in ['"', "\n"]:
            endInd += 1
        if self.text[endInd] == '"':
            return endInd + 1
        return False

    def _lexIdentifier(self) -> str:
        endInd = self.tokenStart
        if not self.text[endInd].isalpha() and self.text[endInd] != "_":
            return False
        while self.text[endInd].isalpha() or self.text[endInd].isdigit() or self.text[endInd] == "_":
            endInd += 1
        return endInd

    def _chew(self):
        while self.text[self.tokenStart] == " ":
            self.tokenStart += 1

    def advance(self):
        self.tokenStart = self.tokenEnd
        self._chew()
        if nextInd := self._lexKeyWord():
            self.tokenEnd = nextInd
            self._tokenType = "keyword"
        elif nextInd := self._lexSymbol():
            self.tokenEnd = nextInd
            self._tokenType = "symbol"
        elif nextInd := self._lexIntegerConstant():
            self.tokenEnd = nextInd
            self._tokenType = "integerConstant"
        elif nextInd := self._lexStringConstant():
            self.tokenEnd = nextInd
            self._tokenType = "stringConstant"
        elif nextInd := self._lexIdentifier():
            self.tokenEnd = nextInd
            self._tokenType = "identifier"
        else:
            raise Exception()

    def tokenType(self):
        return self._tokenType

    def keyWord(self):
        return self.text[self.tokenStart:self.tokenEnd]

    def intVal(self) -> int:
        return self.text[self.tokenStart:self.tokenEnd]

    def stringVal(self) -> int:
        return self.text[self.tokenStart + 1:self.tokenEnd - 1]

    def symbol(self) -> str:
        symb = self.text[self.tokenStart:self.tokenEnd]
        if symb in SYMBOL_LOOKUP:
            return SYMBOL_LOOKUP[symb]
        return symb

    def identifier(self) -> str:
        return self.text[self.tokenStart:self.tokenEnd]


def parse(inp):
    out = "<tokens>\n"
    tokenizer = JackTokenizer(inp)
    while tokenizer.hasMoreTokens():
        tokenizer.advance()
        tokenType = tokenizer.tokenType()
        out += f"<{tokenType}> "
        if tokenType == "keyword":
            print(tokenizer.keyWord())
            out += tokenizer.keyWord()
        elif tokenType == "symbol":
            print(tokenizer.symbol())
            out += tokenizer.symbol()
        elif tokenType == "integerConstant":
            print(tokenizer.intVal())
            out += tokenizer.intVal()
        elif tokenType == "stringConstant":
            print(tokenizer.stringVal())
            out += tokenizer.stringVal()
        elif tokenType == "identifier":
            print(tokenizer.identifier())
            out += tokenizer.identifier()
        else:
            raise Exception(f"Invalid token type '{tokenType}'")
        out += f" </{tokenType}>\n"
    out += "</tokens>\n"
    return out


if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python3 JackAnalyzer.py <path>")
        sys.exit(1)

    input_path = Path(sys.argv[1])
    file_paths = []

    # Single file translation
    if input_path.is_file():
        file_paths.append(input_path)
    # Multiple file translation
    elif input_path.is_dir():
        for fp in os.listdir(input_path):
            if fp.split(".")[-1] == "jack":
                file_paths.append(input_path / fp)
    else:
        raise Exception(f"'{input_path}' is not a file or a dir")

    for fp in file_paths:
        print(f"Parsing: {fp.name}")
        out_dir = fp.parent / "out"
        if not os.path.exists(out_dir):
            os.mkdir(out_dir)

        with open(fp) as f:
            xml_output = parse(f.read())

        out_file_name = ".".join(fp.name.split(".")[:-1]) + ".xml"
        with open(out_dir / out_file_name, "w") as f:
            f.write(xml_output)
