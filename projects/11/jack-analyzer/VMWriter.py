from pathlib import Path
from constants import SEGMENTS, ARITHMETIC_OPS


class VMWriteError(Exception):
    pass


class VMWriter:
    def __init__(self, vm_out_file_path: Path):
        self.vm_out_file = open(vm_out_file_path, "w")

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
        self.vm_out_file.close()
