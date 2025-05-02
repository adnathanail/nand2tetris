class CompilationEngine:
    def __init__(self, tokenizer):
        self.tokenizer = tokenizer
        self.output = "<tokens>\n"
        while tokenizer.hasMoreTokens():
            tokenizer.advance()
            self.output += f"<{tokenizer.tokenType}> {tokenizer.token} </{tokenizer.tokenType}>\n"
        self.output += "</tokens>\n"
