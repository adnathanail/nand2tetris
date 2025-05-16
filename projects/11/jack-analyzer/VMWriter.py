from pathlib import Path
from utils import make_indent
from constants import SEGMENTS, ARITHMETIC_OPS


class VMWriteError(Exception):
    pass


class VMWriter:
    def __init__(self, xml_out_file_path: Path, vm_out_file_path: Path):
        self.xml_out_file = open(xml_out_file_path, "w")
        self.vm_out_file = open(vm_out_file_path, "w")

    def xmlOutput(self, line: str, indent: int):
        self.xml_out_file.write(make_indent(indent) + line + "\n")

    def _writeVMLine(self, line: str):
        self.vm_out_file.write(line + "\n")

    def writeComment(self, comment: str):
        self._writeVMLine(f"  // {comment}")

    def writePush(self, segment: SEGMENTS, index: int):
        self._writeVMLine(f"  push {segment} {index}")

    def writePop(self, segment: SEGMENTS, index: int):
        self._writeVMLine(f"  pop {segment} {index}")

    def writeArithmetic(self, command: ARITHMETIC_OPS):
        self._writeVMLine(f"  {command}")

    def writeLabel(self, label: str):
        self._writeVMLine(f"label {label}")

    def writeGoto(self, label: str):
        self._writeVMLine(f"  goto {label}")

    def writeIf(self, label: str):
        self._writeVMLine(f"  if-goto {label}")

    def writeCall(self, name: str, nArgs: int):
        self._writeVMLine(f"  call {name} {nArgs}")

    def writeFunction(self, name: str, nVars: int):
        self._writeVMLine(f"function {name} {nVars}")

    def writeReturn(self):
        self._writeVMLine("  return")

    def close(self):
        self.xml_out_file.close()
        self.vm_out_file.close()
