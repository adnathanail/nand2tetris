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
            if cmd_parts[1] == "static":
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
        if cmd_parts[1] == "static":
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

        out.append("@SP")
        out.append("M=M-1")
        out.append("A=M")
        out.append("D=M")

        out.append("@13")
        out.append("A=M")
        out.append("M=D")
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

    # Initialise SP
    out.append("// SP = 256")
    out.append("@256")
    out.append("D=A")
    out.append("@SP")
    out.append("M=D")
    out.append("// LCL = 300")
    out.append("@300")
    out.append("D=A")
    out.append("@LCL")
    out.append("M=D")
    out.append("// ARG = 400")
    out.append("@400")
    out.append("D=A")
    out.append("@ARG")
    out.append("M=D")
    out.append("// THIS = 3000")
    out.append("@3000")
    out.append("D=A")
    out.append("@THIS")
    out.append("M=D")
    out.append("// THAT = 3010")
    out.append("@3010")
    out.append("D=A")
    out.append("@THAT")
    out.append("M=D")

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

    path = sys.argv[1]
    with open(path) as f:
        lines = f.read().split("\n")
    
    vm_code = translate(lines)
    asm_file = path.replace(".vm", ".asm")
    with open(asm_file, "w") as f:
        f.write("\n".join(vm_code))