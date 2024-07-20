import os
import sys


eq_n = 0


def translate_cmd(cmd, out):
    global eq_n

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
                out.append(f"@{16 + int(cmd_parts[2])}")
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
            out.append(f"@{16 + int(cmd_parts[2])}")
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
        # Push XX.YY.return label onto stack
        out.append(f"@{cmd_parts[1]}.return")
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
        out.append(f"({cmd_parts[1]}.return)")
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


def translate(vm_code):
    out = []

    # Initialise SP, LCL, ARG, THIS, THAT
    out.append("// SP = 256")
    out.append("@256")
    out.append("D=A")
    out.append("@SP")
    out.append("M=D")
    out.append("// LCL = -1")
    out.append("@1")
    out.append("D=-A")
    out.append("@LCL")
    out.append("M=D")
    out.append("// ARG = -2")
    out.append("@2")
    out.append("D=-A")
    out.append("@ARG")
    out.append("M=D")
    out.append("// THIS = -3")
    out.append("@3")
    out.append("D=-A")
    out.append("@THIS")
    out.append("M=D")
    out.append("// THAT = -4")
    out.append("@4")
    out.append("D=-A")
    out.append("@THAT")
    out.append("M=D")

    vm_code.insert(0, "call Sys.init 0")

    for row in vm_code:
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

        translate_cmd(command, out)

    return out


if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python3 VMTranslator.py <path>")
        sys.exit(1)

    input_path = sys.argv[1]

    file_paths = []

    if os.path.isfile(input_path):
        file_paths.append(input_path)
        asm_file = input_path.replace(".vm", ".asm")
    else:
        asm_file = input_path + "/" + input_path.split("/")[-1] + ".asm"
        for fp in os.listdir(input_path):
            if fp.split(".")[-1] == "vm":
                file_paths.append(input_path + "/" + fp)

    print(asm_file)
    print(file_paths)

    lines = []
    for path in file_paths:
        with open(path) as f:
            lines += f.read().split("\n")

    vm_code = translate(lines)

    with open(asm_file, "w") as f:
        f.write("\n".join(vm_code))