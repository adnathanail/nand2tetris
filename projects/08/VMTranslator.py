import os
import sys
from pathlib import Path


eq_n = 0
calls_n = {}


def translate_cmd(filename, cmd, out):
    global eq_n, calls_n

    out.append(f"// {cmd}")
    cmd_parts = cmd.split(" ")

    if cmd_parts[0] == "push":
        if cmd_parts[1] == "constant":
            out.append(f"@{cmd_parts[2]}")
            out.append("D=A")
            out.append(f"@SP")
            out.append("A=M")
            out.append("M=D")
            out.append("@SP")
            out.append("M=M+1")
        else:
            if cmd_parts[1] == "temp":
                out.append(f"@{5 + int(cmd_parts[2])}")
                out.append("D=M")
            elif cmd_parts[1] == "static":
                out.append(f"@{filename}.{16 + int(cmd_parts[2])}")
                out.append("D=M")
            elif cmd_parts[1] == "pointer":
                if cmd_parts[2] == "0":
                    out.append(f"@THIS")
                else:
                    out.append(f"@THAT")
                out.append("D=M")
            else:
                if cmd_parts[1] == "local":
                    out.append("@LCL")
                elif cmd_parts[1] == "argument":
                    out.append("@ARG")
                elif cmd_parts[1] == "this":
                    out.append("@THIS")
                elif cmd_parts[1] == "that":
                    out.append("@THAT")
                else:
                    print(cmd)

                out.append("D=M")
                out.append(f"@{cmd_parts[2]}")
                out.append("D=D+A")

                out.append("A=D")
                out.append("D=M")

            out.append("@SP")
            out.append("A=M")
            out.append("M=D")

            out.append("@SP")
            out.append("M=M+1")
    elif cmd_parts[0] == "pop":
        if cmd_parts[1] == "temp":
            out.append(f"@{5 + int(cmd_parts[2])}")
            out.append("D=A")
            out.append("@13")
            out.append("M=D")
        elif cmd_parts[1] == "static":
            out.append(f"@{filename}.{16 + int(cmd_parts[2])}")
            out.append("D=A")
            out.append("@13")
            out.append("M=D")
        elif cmd_parts[1] == "pointer":
            if cmd_parts[2] == "0":
                out.append(f"@THIS")
            else:
                out.append(f"@THAT")
            out.append("D=A")
            out.append("@13")
            out.append("M=D")
        else:
            if cmd_parts[1] == "local":
                out.append("@LCL")
            elif cmd_parts[1] == "argument":
                out.append("@ARG")
            elif cmd_parts[1] == "this":
                out.append("@THIS")
            elif cmd_parts[1] == "that":
                out.append("@THAT")
            else:
                print(cmd)

            out.append("D=M")
            out.append(f"@{cmd_parts[2]}")
            out.append("D=D+A")
            out.append("@13")
            out.append("M=D")

        # Pop stack to D
        out.append("@SP")
        out.append("M=M-1")
        out.append("A=M")
        out.append("D=M")

        out.append("@13")
        out.append("A=M")
        out.append("M=D")
    elif cmd_parts[0] == "label":
        out.append(f"({cmd_parts[1]})")
    elif cmd_parts[0] == "goto":
        out.append(f"@{cmd_parts[1]}")
        out.append("0;JMP")
    elif cmd_parts[0] == "if-goto":
        # Pop stack to D
        out.append("@SP")
        out.append("M=M-1")
        out.append("A=M")
        out.append("D=M")
        # Jump to the specified label if the top stack value wasn't zero (i.e. was not false, i.e. was true)
        out.append(f"@{cmd_parts[1]}")
        out.append("D;JNE")
    elif cmd_parts[0] == "function":
        out.append(f"({cmd_parts[1]})")

        # Add nArgs zeroes to the LCL segment for the function to use
        nArgs = int(cmd_parts[2])
        for _ in range(nArgs):
            out.append(f"@SP")
            out.append("A=M")
            out.append("M=0")
            out.append("@SP")
            out.append("M=M+1")
    elif cmd_parts[0] == "return":
        out.append("@LCL")
        out.append("D=M")
        out.append("@endFrame")
        out.append("M=D")
        
        out.append("@5")
        out.append("D=D-A")
        out.append("A=D")
        out.append("D=M")
        out.append("@retAddr")
        out.append("M=D")

        # Pop stack to D
        out.append("@SP")
        out.append("M=M-1")
        out.append("A=M")
        out.append("D=M")
        # Put this value in @ARG
        out.append("@ARG")
        out.append("A=M")
        out.append("M=D")

        # Put the stack pointer just above the new ARG
        out.append("@ARG")
        out.append("D=M+1")
        out.append("@SP")
        out.append("M=D")

        # THAT = *(endFrame - 1)
        out.append("@endFrame")
        out.append("M=M-1")
        out.append("A=M")
        out.append("D=M")
        out.append("@THAT")
        out.append("M=D")

        # THIS = *(endFrame - 2)
        out.append("@endFrame")
        out.append("M=M-1")
        out.append("A=M")
        out.append("D=M")
        out.append("@THIS")
        out.append("M=D")

        # ARG = *(endFrame - 3)
        out.append("@endFrame")
        out.append("M=M-1")
        out.append("A=M")
        out.append("D=M")
        out.append("@ARG")
        out.append("M=D")

        # LCL = *(endFrame - 4)
        out.append("@endFrame")
        out.append("M=M-1")
        out.append("A=M")
        out.append("D=M")
        out.append("@LCL")
        out.append("M=D")

        # goto endFrame - 5
        out.append("@retAddr")
        out.append("A=M")
        out.append("0;JMP")
    elif cmd_parts[0] == "call":  #  call XX.YY n
        if cmd_parts[1] not in calls_n:
            calls_n[cmd_parts[1]] = 0
        calls_n[cmd_parts[1]] += 1
        # Push XX.YY.return label onto stack
        out.append(f"@{cmd_parts[1]}.{calls_n[cmd_parts[1]]}.return")
        out.append("D=A")
        out.append(f"@SP")
        out.append("A=M")
        out.append("M=D")
        out.append("@SP")
        out.append("M=M+1")
        # Push LCL onto stack
        out.append(f"@LCL")
        out.append("D=M")
        out.append(f"@SP")
        out.append("A=M")
        out.append("M=D")
        out.append("@SP")
        out.append("M=M+1")
        # Push ARG onto stack
        out.append(f"@ARG")
        out.append("D=M")
        out.append(f"@SP")
        out.append("A=M")
        out.append("M=D")
        out.append("@SP")
        out.append("M=M+1")
        # Push THIS onto stack
        out.append(f"@THIS")
        out.append("D=M")
        out.append(f"@SP")
        out.append("A=M")
        out.append("M=D")
        out.append("@SP")
        out.append("M=M+1")
        # Push THAT onto stack
        out.append(f"@THAT")
        out.append("D=M")
        out.append(f"@SP")
        out.append("A=M")
        out.append("M=D")
        out.append("@SP")
        out.append("M=M+1")
        # ARG = SP – 5 – nArgs
        out.append("@SP")
        out.append("D=M")
        nArgs = int(cmd_parts[2])
        out.append(f"@{5 + nArgs}")
        out.append("D=D-A")
        out.append("@ARG")
        out.append("M=D")
        # LCL = SP
        out.append("@SP")
        out.append("D=M")
        out.append("@LCL")
        out.append("M=D")
        # goto XX.YY
        out.append(f"@{cmd_parts[1]}")
        out.append("0;JMP")
        # Add return label
        out.append(f"({cmd_parts[1]}.{calls_n[cmd_parts[1]]}.return)")
    elif len(cmd_parts) == 1:
        out.append("@SP")
        out.append("M=M-1")
        out.append("A=M")

        if cmd_parts[0] == "neg":
            out.append("M=-M")
        elif cmd_parts[0] == "not":
            out.append("M=!M")
        else:
            out.append("D=M")
            out.append("@SP")
            out.append("M=M-1")
            out.append("A=M")

            if cmd_parts[0] == "add":
                out.append("M=M+D")
            elif cmd_parts[0] == "sub":
                out.append("M=M-D")
            elif cmd_parts[0] == "and":
                out.append("M=M&D")
            elif cmd_parts[0] == "or":
                out.append("M=M|D")
            elif cmd_parts[0] in ["eq", "lt", "gt"]:
                # subtract values on stack from each other
                out.append("D=M-D")
                # go to EQT if diff was 0 (i.e. they are equal)
                out.append(f"@EQT{eq_n}")
                out.append(f"D;J{cmd_parts[0].upper()}")
                # still here? not equal, append 0 to stack and jump to EQC
                out.append("@SP")
                out.append("A=M")
                out.append("M=0")
                out.append(f"@EQC{eq_n}")
                out.append("0;JMP")
                # they were equal? append 1 to stack
                out.append(f"(EQT{eq_n})")
                out.append("@SP")
                out.append("A=M")
                out.append("M=-1")
                out.append(f"(EQC{eq_n})")
                eq_n += 1
            else:
                print(cmd)

        out.append("@SP")
        out.append("M=M+1")
    else:
        print(cmd)

    return out


def translate(vm_codes, add_bootstrap=False):
    out = []

    if add_bootstrap:
        # Initialise SP, LCL, ARG, THIS, THAT
        out.append("// SP = 256")
        out.append("@256")
        out.append("D=A")
        out.append("@SP")
        out.append("M=D")

        # Call Sys.init
        translate_cmd("", "call Sys.init 0", out)

    for (filename, vm_code) in vm_codes:
        for row in vm_code:
            if row and row[0] == "#":
                out.append("")
                out.append("// " + "-" * (len(row) - 1))
                out.append(row.replace("#", "//"))
                out.append("// " + "-" * (len(row) - 1))
                out.append("")
                continue
            # Remove comments
            if "//" in row:
                row_no_comments = row[:row.find("//")]
            else:
                row_no_comments = row

            # Remove whitespace
            command = row_no_comments.strip()

            # Ignore empty rows
            if command == "":
                continue

            translate_cmd(filename, command, out)

    return out


def add_line_numbers(vm_code):
    max_line_length = max(len(l) for l in vm_code)
    out = []
    i = 0
    for row in vm_code:
        if not row or row[0] == "(" or row[:2] == "//":  # leave empty lines, labels, and comments
            out.append(row)
        else:
            out.append(f"{row}{' ' * (max_line_length - len(row) + 5)}// line {i}")
            i += 1
    return out


if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python3 VMTranslator.py <path>")
        sys.exit(1)

    input_path = Path(sys.argv[1])
    file_paths = []
    add_startup_code = False

    # Single file translation
    if input_path.is_file():
        file_paths.append(input_path)
        asm_file = input_path.parent / input_path.name.replace(".vm", ".asm")
    # Multiple file translation
    elif input_path.is_dir():
        add_startup_code = True
        asm_file = input_path / (input_path.name + ".asm")
        for fp in os.listdir(input_path):
            if fp.split(".")[-1] == "vm":
                file_paths.append(input_path / fp)

    # Read files
    vm_codes = []  # List of tuples of filename and file contents e.g. [("Class1.vm", ["push 1", "return"])]
    for path in file_paths:
        with open(path) as f:
            vm_code = f.read().split("\n")
        vm_code.insert(0, f"# {path.name}")
        vm_codes.append((path.name, vm_code))

    # Translate VM code
    asm_code = translate(vm_codes, add_startup_code)

    asm_code = add_line_numbers(asm_code)

    # Write VM code
    with open(asm_file, "w") as f:
        f.write("\n".join(asm_code))