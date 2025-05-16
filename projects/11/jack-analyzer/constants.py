from typing import Literal


# Tokenizer
KEYWORDS = (
    "class",
    "constructor",
    "function",
    "method",
    "field",
    "static",
    "var",
    "int",
    "char",
    "boolean",
    "void",
    "true",
    "false",
    "null",
    "this",
    "let",
    "do",
    "if",
    "else",
    "while",
    "return",
)

SYMBOLS = (
    "{",
    "}",
    "(",
    ")",
    "[",
    "]",
    ".",
    ",",
    ";",
    "+",
    "-",
    "*",
    "/",
    "&",
    "|",
    "<",
    ">",
    "=",
    "~",
)

SYMBOL_LOOKUP = {
    "<": "&lt;",
    ">": "&gt;",
    '"': "&quot;",
    "&": "&amp;",
}

TOKEN_TYPES = Literal[
    "keyword", "symbol", "integerConstant", "stringConstant", "identifier"
]

# Parser
KEYWORD_CONSTANTS = (
    "true",
    "false",
    "null",
    "this",
)

PRIMITIVE_TYPES = ("int", "char", "boolean")

OPS = ("+", "-", "*", "/", "&amp;", "|", "&lt;", "&gt;", "=")

UNARY_OPS = ("-", "~")

SEGMENTS = Literal[
    "constant", "argument", "local", "static", "this", "that", "pointer", "temp"
]

# VM writer
ARITHMETIC_OPS = Literal["add", "sub", "neg", "eq", "gt", "lt", "and", "or", "not"]

# Symbol table
SYMBOL_SEGMENTS = Literal["static", "this", "argument", "local"]
