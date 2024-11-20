class Token:
    def __init__(self, value: str, token_type: str) -> None:
        self.value = value
        self.token_type = token_type

    def __str__(self) -> str:
        return f"Token({self.token_type}) = {self.value}"

class Keyword(Token):
    def __init__(self, value: str) -> None:
        super().__init__(value, "KEYWORD")

class PrimitiveType(Token):
    def __init__(self, value: str) -> None:
        super().__init__(value, "PRIMITIVE")

class Identifier(Token):
    def __init__(self, value: str) -> None:
        super().__init__(value, "IDENTIFIER")

class Operator(Token):
    def __init__(self, value: str) -> None:
        super().__init__(value, "OPERATOR")

class Literal(Token):
    def __init__(self, value: str, type: PrimitiveType) -> None:
        super().__init__(value, "LITERAL"),
        self.type = type

    def __str__(self) -> str:
        return f"Token({self.token_type}:{self.type.value}) = {self.value}"

primitives = {
    "int" : PrimitiveType("int"),
    "void" : PrimitiveType("void"),
    "float": PrimitiveType("float"),
    "string": PrimitiveType("string")
}

keywords = {
    "return" : Keyword("return"),
    "import" : Keyword("import"),
    "do" : Keyword("do"),
    "end" : Keyword("end"),
    "function" : Keyword("function")
}

operators = {
    "+" : Operator("+"),
    "-" : Operator("-"),
    "/" : Operator("/"),
    "*" : Operator("*"),
    ">" : Operator(">"),
    "<" : Operator("<"),
    ":": Operator(":"),
    "(": Operator("("),
    ")": Operator(")"),
    ";": Operator(";"),
    ",": Operator(",")
}