import sys

def translate(vm_code):
    out = []

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

        out.append(row)

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