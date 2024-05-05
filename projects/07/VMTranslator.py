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
    elif len(cmd_parts) == 1:
        out.append("@SP")
        out.append("M=M-1")
        out.append("A=M")
        out.append("D=M")
        out.append("@SP")
        out.append("M=M-1")
        out.append("A=M")

        if cmd_parts[0] == "add":
            out.append("M=M+D")
        elif cmd_parts[0] == "eq":
            # subtract values on stack from each other
            out.append("D=D-M")
            # go to EQT if diff was 0 (i.e. they are equal)
            out.append(f"@EQT{eq_n}")
            out.append("D;JEQ")
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
            out.append("M=1")
            out.append(f"(EQC{eq_n})")
            eq_n += 1

        out.append("@SP")
        out.append("M=M+1")

    return out


def translate(vm_code):
    out = []

    # Initialise SP
    out.append("// SP = 256")
    out.append("@256")
    out.append("D=A")
    out.append("@SP")
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