from typing import List


class Token:
    def __init__(self, value):
        self.value = value
    
    def to_python_type(self):
        raise NotImplementedError()


class StringToken(Token):
    def __init__(self, value):
        super().__init__(value)
    
    def to_python_type(self):
        return self.value


class IntegerToken(Token):
    def __init__(self, value):
        super().__init__(value)
    
    def to_python_type(self):
        return int(self.value)


class FloatingNumber(Token):
    def __init__(self, value):
        super().__init__(value)
    
    def to_python_type(self):
        return float(self.value)


class BooleanToken(Token):
    def __init__(self, value):
        super().__init__(value)
    
    def to_python_type(self):
        if self.value.lower() == "true":
            return True
        else:
            return False


class LiteralToken(Token):
    def __init__(self, value):
        super().__init__(value)
    
    def to_python_type(self):
        return self.value


class Tokeniser:
    def __init__(self, command: str):
        self.command = command
        self.index = 0
        self.chars = list(command)
    
    def match(self, char: str) -> str:
        temp = self.chars[self.index]
        if temp == char:
            self.pop()
            return temp
        else:
            raise ValueError(f"Unexpected character {temp}, expected {char}.")

    def peek(self) -> str:
        if self.index >= len(self.chars):
            return None
        return self.chars[self.index]
    
    def pop(self) -> str:
        if self.index >= len(self.chars):
            return None
        temp = self.chars[self.index]
        self.index += 1
        return temp

    def tokenise(self) -> List[Token]:
        tokens: List[Token] = []
        
        while self.index < len(self.chars):
            if self.peek() == " ":
                self.pop()
            elif self.peek() == "\"":
                self.pop()
                string_temp = ""
                while self.peek() != "\"":
                    string_temp += self.pop()
                self.pop()
                tokens.append(StringToken(string_temp))
            elif self.peek().isnumeric() or self.peek() == "." or self.peek() == "-":
                number_temp = ""
                while self.peek() and (self.peek().isnumeric() or self.peek() == "." or self.peek() == "-"):
                    number_temp += self.pop()

                if "-" in number_temp:
                    if number_temp[0] != "-":
                        raise ValueError(f"Minus sign must be a start of number {number_temp}")

                if "." in number_temp:
                    if number_temp.count(".") > 1:
                        raise ValueError(f"Too many decimal points in number {number_temp}")
                    tokens.append(FloatingNumber(number_temp))
                else:
                    tokens.append(IntegerToken(number_temp))
            elif self.peek().isalnum():
                literal_temp = ""
                while self.peek() and self.peek().isalnum():
                    literal_temp += self.pop()
                if literal_temp.lower() == "true" or literal_temp.lower() == "false":
                    tokens.append(BooleanToken(literal_temp))
                else:
                    tokens.append(LiteralToken(literal_temp))
            else:
                raise ValueError(f"Unexpected character {self.peek()}")

        return tokens

if __name__ == "__main__":
    string = "3232 \"hello\" .4567 true False fasly"
    tokeniser = Tokeniser(string)
    tokens = tokeniser.tokenise()
    for token in tokens:
        print(f"{token.__class__.__name__}: {token.value} {token.to_python_type()}")
