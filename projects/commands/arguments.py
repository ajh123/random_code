from typing import List, Optional, Any
from tokens import BooleanToken, FloatingNumber, IntegerToken, StringToken, LiteralToken, Token

class ArgumentType:
    def parse(self, tokens: List[Token]):
        raise NotImplementedError()

    def display(self):
        raise NotImplementedError()


class BooleanArgument(ArgumentType):
    def parse(self, tokens: List[Token]):
        if isinstance(tokens[0], BooleanToken):
            return tokens.pop(0).to_python_type()
        raise ValueError(f"Unexpected value {tokens[0].value}")

    def display(self):
        return "true or false"


class FloatArgument(ArgumentType):
    def parse(self, tokens: List[Token]):
        if isinstance(tokens[0], FloatingNumber):
            return tokens.pop(0).to_python_type()
        raise ValueError(f"Unexpected value {tokens[0].value}")

    def display(self):
        return "a floating point number"

class IntegerArgument(ArgumentType):
    def parse(self, tokens: List[Token]):
        if isinstance(tokens[0], IntegerToken):
            return tokens.pop(0).to_python_type()
        raise ValueError(f"Unexpected value {tokens[0].value}")

    def display(self):
        return "a whole integer"

class StringArgument(ArgumentType):
    def parse(self, tokens: List[Token]):
        if isinstance(tokens[0], StringToken):
            return tokens.pop(0).to_python_type()
        raise ValueError(f"Unexpected value {tokens[0].value}")

    def display(self):
        return "a string value"

class LiteralArgument(ArgumentType):
    def __init__(self, value: Optional[str] = None):
        self.value = value        

    def parse(self, tokens: List[Token]):
        if self.value is not None:
            if isinstance(tokens[0], LiteralToken):
                if tokens[0].to_python_type() == self.value:
                    return tokens.pop(0).to_python_type()
                else:
                     raise ValueError(f"Unexpected value {tokens[0].value}, expected {self.value}")

        if isinstance(tokens[0], LiteralToken):
            return tokens.pop(0).to_python_type()
        raise ValueError(f"Unexpected value {tokens[0].value}")

    def display(self):
        return f"{self.value}"

class ArrayArgument(ArgumentType):
    def __init__(self, length: Optional[int] = None):
        self.length = length
    
    def parse(self, tokens: List[Token]):
        args = []
        for i in range(0, len(tokens)):
            if self.length is not None and self.length == i:
                break
            arg = tokens.pop(0)
            args.append(arg.to_python_type())
        return args

    def display(self):
        return f"array of things"

class EnumArgument(ArgumentType):
    def __init__(self, values: List[Any]):
        self.values = values
    
    def parse(self, tokens: List[Token]):
        if not tokens[0].to_python_type() in self.values:
            raise ValueError(f"Unexptected value {tokens[0]}, expected any of {self.values}")
        return tokens.pop(0).to_python_type()
    
    def display(self):
        return f"any of {self.values}"