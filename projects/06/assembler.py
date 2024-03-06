COMPARISON_OPERATION_LOOKUP = {
    "0": "101010",
    "1": "111111",
    "-1": "111010",
    "D": "001100",
    "A": "110000",
    "!D": "001101",
    "!A": "110001",
    "-D": "001111",
    "-A": "110011",
    "D+1": "011111",
    "A+1": "110111",
    "D-1": "001110",
    "A-1": "110010",
    "D+A": "000010",
    "D-A": "010011",
    "A-D": "000111",
    "D&A": "000000",
    "D|A": "010101",
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

with open("projects/06/add/Add.asm") as f:
    x = f.read()
    for row in x.split("\n"):
        # Ignore empty rows
        if row == "":
            continue
        # Ignore comments
        if row[:2] == "//":
            continue
        # A instruction
        if row[0] == "@":
            out = "0"  # A starts with 0
            val_dec = int(row[1:])  # Value to be loaded into A-register in base 10
            val_binstr = bin(val_dec)[2:]  # Value in base 2
            padding = (15 - len(val_binstr))*"0"  # To make the resulting binary 15-bits (16 inc first 0)
            out += padding + val_binstr
        # C instruction
        else:
            out = "111"  # C starts with 1, next 2 bits aren't used
            out += "0"  # a
            if ";" in row:
                assignment, jump = row.split(";")
            else:
                assignment = row
                jump = ""
            destination, comparison = assignment.split("=")
            
            compbits = COMPARISON_OPERATION_LOOKUP[comparison]
            
            destbits = ""
            if "A" in destination:
                destbits += "1"
            else:
                destbits += "0"
            if "D" in destination:
                destbits += "1"
            else:
                destbits += "0"
            if "M" in destination:
                destbits += "1"
            else:
                destbits += "0"

            jumpbits = JUMP_OPERATION_LOOKUP[jump]
            # print(destination, comparison, jump)
            out += compbits + destbits + jumpbits
            print(out)
        print(out)
