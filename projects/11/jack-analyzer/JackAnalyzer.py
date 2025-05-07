import os
import sys
from pathlib import Path
from JackTokenizer import JackTokenizer
from CompilationEngine import CompilationEngine


def parse(inp):
    tokenizer = JackTokenizer(inp)
    engine = CompilationEngine(tokenizer)
    engine.compileClass()
    return engine.output


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
        out_dir = fp.parent
        if not os.path.exists(out_dir):
            os.mkdir(out_dir)

        with open(fp) as f:
            xml_output = parse(f.read())

        out_file_name = ".".join(fp.name.split(".")[:-1]) + ".xml"
        with open(out_dir / out_file_name, "w") as f:
            f.write(xml_output)
