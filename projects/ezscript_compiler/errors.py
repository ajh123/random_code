class LexerError(Exception):
    def __init__(self, message: str, line: int, col: int, source: str, length: int = 1):
        self.message = message
        self.line = line
        self.col = col
        self.source = source
        self.length = length
        super().__init__(message)

    def __str__(self):
        lines = self.source.splitlines()
        error_line = lines[self.line - 1] if self.line - 1 < len(lines) else ""
        pointer = " " * (self.col - 1) + "^" * self.length
        return (
            f"  File \"<stdin>\", line {self.line}\n"
            f"    {error_line}\n"
            f"    {pointer}\n"
            f"SyntaxError: {self.message}"
        )


def raise_lexer_error(message: str, source: str, pos: int, length: int = 1):
    lines = source[:pos + 1].splitlines()
    line = len(lines)
    col = len(lines[-1])
    raise LexerError(message, line, col, source, length)