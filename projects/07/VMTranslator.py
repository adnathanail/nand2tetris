import sys


def translate_cmd(cmd, out):
    cmd_parts = cmd.split(" ")

    if cmd_parts[0] == "push":
        if cmd_parts[1] == "constant":
            out.append(f"// {cmd}")
            out.append(f"@{cmd_parts[2]}")
            out.append("D=A")
            out.append(f"@SP")
            out.append("A=M")
            out.append("M=D")
            out.append("@SP")
            out.append("M=M+1")
    elif cmd_parts[0] == "add":
        out.append("@SP")
        out.append("M=M-1")
        out.append("A=M")
        out.append("D=M")
        out.append("@SP")
        out.append("M=M-1")
        out.append("A=M")
        out.append("M=M+D")
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