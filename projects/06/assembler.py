import argparse

# X represents either A (a = 0) or M (a = 1)
COMPARISON_OPERATION_LOOKUP = {
    "0": "101010",
    "1": "111111",
    "-1": "111010",
    "D": "001100",
    "X": "110000",
    "!D": "001101",
    "!X": "110001",
    "-D": "001111",
    "-X": "110011",
    "D+1": "011111",
    "X+1": "110111",
    "D-1": "001110",
    "X-1": "110010",
    "D+X": "000010",
    "D-X": "010011",
    "X-D": "000111",
    "D&X": "000000",
    "D|X": "010101",
}

JUMP_OPERATION_LOOKUP = {
    "": "000",
    "JGT": "001",
    "JEQ": "010",
    "JGE": "011",
    "JLT": "100",
    "JNE": "101",
    "JLE": "110",
    "JMP": "111",
}


def assemble(source_assembly, outpath):
    compiled_hack_code = []
    for row in source_assembly:
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

        # A instruction
        if command[0] == "@":
            val_dec = int(command[1:])  # Value to be loaded into A-register in base 10
            val_binstr = bin(val_dec)[2:]  # Value in base 2
            # To make the resulting binary 15-bits (16 inc first 0)
            padding = (15 - len(val_binstr)) * "0"
            # A starts with 0
            out = "0" + padding + val_binstr
        # C instruction
        else:
            # Split out jump
            if ";" in command:
                assignment, jump = command.split(";")
            else:
                assignment = command
                jump = ""

            # Split out assignment
            if "=" in assignment:
                destination, comparison = assignment.split("=")
            else:
                destination = ""
                comparison = command

            # a and c bits
            if (clu := comparison.replace("A", "X")) in COMPARISON_OPERATION_LOOKUP:
                compbits = COMPARISON_OPERATION_LOOKUP[clu]
                abit = "0"
            elif (clu := comparison.replace("M", "X")) in COMPARISON_OPERATION_LOOKUP:
                compbits = COMPARISON_OPERATION_LOOKUP[clu]
                abit = "1"

            # d bits
            destbits = ""
            destbits += "1" if "A" in destination else "0"
            destbits += "1" if "D" in destination else "0"
            destbits += "1" if "M" in destination else "0"

            # j bit
            jumpbits = JUMP_OPERATION_LOOKUP[jump]

            # C starts with 1, next 2 bits aren't used
            out = "111" + abit + compbits + destbits + jumpbits
        print(out)
        compiled_hack_code.append(out + "\n")

    with open(outpath, "w") as f:
        f.writelines(compiled_hack_code)


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("assembly_file", type=argparse.FileType("r"))
    args = parser.parse_args()
    assembly_file_contents = args.assembly_file.readlines()

    input_file_path = args.assembly_file.name
    output_file_path = input_file_path[: input_file_path.rfind(".")] + ".hack"

    assemble(assembly_file_contents, output_file_path)
