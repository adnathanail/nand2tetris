from typing import TypedDict
from utils import rows_to_table
from constants import SYMBOL_SEGMENTS


class SymbolTableError(Exception):
    pass


class SymbolTableEntry(TypedDict):
    type: str
    kind: SYMBOL_SEGMENTS
    index: int


class SymbolTable:
    def __init__(self):
        self._entries: dict[str, SymbolTableEntry] = {}
        self._static_counter: int = 0
        self._this_counter: int = 0
        self._argument_counter: int = 0
        self._local_counter: int = 0

    def __str__(self):
        rows = [["Name", "Type", "Kind", "Index"]]
        for name in self._entries:
            entry = self._entries[name]
            rows.append([name, entry["type"], entry["kind"], str(entry["index"])])
        return rows_to_table(rows)

    def hasEntry(self, identifier: str):
        return identifier in self._entries

    def reset(self):
        self._entries = {}
        self._static_counter = 0
        self._this_counter = 0
        self._argument_counter = 0
        self._local_counter = 0

    def define(self, name: str, ttype: str, kind: SYMBOL_SEGMENTS):
        self._entries[name] = {
            "type": ttype,
            "kind": kind,
            "index": self.varCount(kind),
        }
        if kind == "static":
            self._static_counter += 1
        elif kind == "this":
            self._this_counter += 1
        elif kind == "argument":
            self._argument_counter += 1
        elif kind == "local":
            self._local_counter += 1
        else:
            raise SymbolTableError(f"define: invalid kind '{kind}'")

    def varCount(self, kind: SYMBOL_SEGMENTS):
        if kind == "static":
            return self._static_counter
        elif kind == "this":
            return self._this_counter
        elif kind == "argument":
            return self._argument_counter
        elif kind == "local":
            return self._local_counter
        else:
            raise SymbolTableError(f"varCount: invalid kind '{kind}'")

    def kindOf(self, name: str) -> SYMBOL_SEGMENTS:
        return self._entries[name]["kind"]

    def typeOf(self, name: str) -> str:
        return self._entries[name]["type"]

    def indexOf(self, name: str) -> int:
        return self._entries[name]["index"]
