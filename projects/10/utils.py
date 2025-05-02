def strip_comments_and_whitespace(in_text: str) -> str:
    lines = in_text.splitlines()
    i = 0
    in_comment = False

    out = ""
    while i < len(lines):
        line = lines[i]
        # Currently inside multiline comment
        if in_comment:
            # If closing */, remove everything up to it
            if "*/" in line:
                line = line[line.index("*/") + 2 :]
                in_comment = False
            # If no closing */, skip the line
            else:
                i += 1
                continue
        # Remove all /* XXX */ sections, and enter multiline comment mode if we see a /* without a */
        while "/*" in line:
            if "*/" in line:
                line = line[: line.index("/*")] + line[line.index("*/") + 2 :]
            else:
                line = line[: line.index("/*")]
                in_comment = True
                break
        # Remove single line comment
        if "//" in line:
            line = line[: line.index("//")]
        # Remove whitespace
        line = line.strip()
        # Output next line of code (no comments no spaces)
        if line:
            out += line
        i += 1
    return out
