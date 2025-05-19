import os
import sys
from pathlib import Path
from typing import List
from CompilationEngine import CompilationEngine
from VMWriter import VMWriter


if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python3 JackCompiler.py <path>")
        sys.exit(1)

    input_path = Path(sys.argv[1])
    file_paths: List[Path] = []

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
        out_dir = fp.parent
        if not os.path.exists(out_dir):
            os.mkdir(out_dir)

        in_file_name_no_ext = ".".join(fp.name.split(".")[:-1])
        vm_writer = VMWriter(
            out_dir / f"{in_file_name_no_ext}.vm",
        )

        with open(fp) as f:
            engine = CompilationEngine(f, vm_writer)
            engine.compileClass()

        vm_writer.close()
