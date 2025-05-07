from utils import make_indent
from typing import Literal


SEGMENTS = Literal["constant", "argument", "local", "static", "this", "that", "pointer", "temp"]
ARITHMETIC_OPS = Literal["add", "sub", "neg", "eq", "gt", "lt", "and", "or", "not"]


class VMWriter:
    def __init__(self, xml_out_file_path, vm_out_file_path):
        self.xml_out_file = open(xml_out_file_path, "w")
        self.vm_out_file = open(vm_out_file_path, "w")

    def _xmlOutput(self, line: str, indent: int):
        self.xml_out_file.write(make_indent(indent) + line + "\n")

    def _writeVMLine(self, line):
        self.vm_out_file.write(line + "\n")

    def writePush(self, segment: SEGMENTS, index: int):
        self._writeVMLine(f"push {segment} {index}")

    def writePop(self, segment: SEGMENTS, index: int):
        self._writeVMLine(f"pop {segment} {index}")

    def writeArithmetic(self, command: ARITHMETIC_OPS):
        pass

    def writeLabel(self, label: str):
        pass

    def writeGoto(self, label: str):
        pass

    def writeIf(self, label: str):
        pass

    def writeCall(self, name: str, nArgs: int):
        self._writeVMLine(f"call {name} {nArgs}")

    def writeFunction(self, name: str, nVars: int):
        self._writeVMLine(f"function {name} {nVars}")

    def writeReturn(self):
        self._writeVMLine("return")

    def close(self):
        self.xml_out_file.close()
        self.vm_out_file.close()