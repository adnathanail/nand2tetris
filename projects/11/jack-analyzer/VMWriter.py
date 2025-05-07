from typing import Literal


SEGMENTS = Literal["CONSTANT", "ARGUMENT", "LOCAL", "STATIC", "THIS", "THAT", "POINTER", "TEMP"]
ARITHMETIC_OPS = Literal["ADD", "SUB", "NEG", "EQ", "GT", "LT", "AND", "OR", "NOT"]


class VMWriter:
    def writePush(self, segment: SEGMENTS, index: int):
        pass

    def writePop(self, segment: SEGMENTS, index: int):
        pass

    def writeArithmetic(self, command: ARITHMETIC_OPS):
        pass

    def writeLabel(self, label: str):
        pass

    def writeGoto(self, label: str):
        pass

    def writeIf(self, label: str):
        pass

    def writeCall(self, name: str, nArgs: int):
        pass

    def writeFunction(self, name: str, nVars: int):
        pass

    def writeReturn(self):
        pass

    def close(self):
        pass