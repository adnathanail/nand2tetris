from typing import Literal


SYMBOL_KINDS = Literal["STATIC", "FIELD", "ARG", "VAR"]


class SymbolTable:
    def __init__(self):
        pass

    def reset(self):
        pass

    def define(self, name: str, type: str, kind: SYMBOL_KINDS):
        pass

    def varCount(self, kind: SYMBOL_KINDS):
        pass

    def kindOf(self, name: str):
        pass

    def typeOf(self, name: str):
        pass

    def indexOf(self, name: str):
        pass

