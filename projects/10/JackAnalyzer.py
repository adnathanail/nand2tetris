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
        self.ind = 0
        self._tokenType = None
        self._keyWord = None
        self._symbol = None
        self._identifier = None
        self._intVal = None
        self._stringVal = None

    def hasMoreTokens(self) -> bool:
        return (self.ind + 1) < len(self.text)

    def advance(self):
        if kwNextInd := self._lexKeyWord():
            (self._keyWord, self.ind) = kwNextInd
            self._tokenType = "keyword"
            # print(self._tokenType, f"'{self._keyWord}'")
        elif symbolNextInd := self._lexSymbol():
            (self._symbol, self.ind) = symbolNextInd
            self._tokenType = "symbol"
            # print(self._tokenType, f"'{self._symbol}'")
        elif identifierNextInd := self._lexIdentifier():
            (self._identifier, self.ind) = identifierNextInd
            self._tokenType = "identifier"
            # print(self._tokenType, f"'{self._identifier}'")
        else:
            raise Exception()
        self._chew()
        # print()

    def _chew(self):
        while self.text[self.ind] == " ":
            self.ind += 1

    def tokenType(self) -> Literal["keyword", "symbol", "identifier", "int_const", "string_const"]:
        return self._tokenType
    
    def _lexKeyWord(self):
        for kw in KEYWORDS:
            if kw == self.text[self.ind:self.ind + len(kw)]:
                return self.text[self.ind:self.ind + len(kw)], self.ind + len(kw)
        return False

    def _lexSymbol(self) -> str:
        if self.text[self.ind] in SYMBOLS:
            return self.text[self.ind], self.ind + 1
        return False

    def _lexIdentifier(self) -> str:
        endInd = self.ind
        if not self.text[endInd].isalpha() and self.text[endInd] != "_":
            return False
        while self.text[endInd].isalpha() or self.text[endInd].isdigit() or self.text[endInd] == "_":
            endInd += 1
        return self.text[self.ind:endInd], endInd

    def keyWord(self):
        return self._keyWord

    def symbol(self) -> str:
        return self._symbol

    def identifier(self) -> str:
        return self._identifier

    def intVal(self) -> int:
        pass

    def stringVal(self) -> int:
        pass


def parse(inp):
    out = "<tokens>\n"
    tokenizer = JackTokenizer(inp)
    while tokenizer.hasMoreTokens():
        tokenizer.advance()
        tokenType = tokenizer.tokenType()
        out += f"<{tokenType}> "
        if tokenType == "keyword":
            out += tokenizer.keyWord()
        elif tokenType == "identifier":
            out += tokenizer.identifier()
        elif tokenType == "symbol":
            out += tokenizer.symbol()
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
        break  # TODO remove
