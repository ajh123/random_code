from typing import List, Optional, Dict, Any
from tokens import *
from errors import raise_parser_error

class Parser:
    def __init__(self, tokens: List[Token], source: str) -> None:
        self.tokens: List[Token] = tokens
        self.pos: int = 0
        self.ast: List[Dict[str, Any]] = []
        self.source = source

    def current_token(self) -> Optional[Token]:
        return self.tokens[self.pos] if self.pos < len(self.tokens) else None

    def match(self, expected_type: Optional[str] = None, expected_value: Optional[str] = None) -> Token:
        token = self.current_token()
        if token and ((not expected_type or token.token_type == expected_type) and
                      (not expected_value or token.value == expected_value)):
            self.pos += 1
            return token
        raise_parser_error(f"Unexpected {token.token_type.lower()} token: `{token.value}`", self.tokens, self.pos, self.source)

    def parse(self) -> List[Dict[str, Any]]:
        while self.pos < len(self.tokens):
            token = self.current_token()
            if isinstance(token, Keyword):
                if token.value == "import":
                    self.ast.append(self.parse_import())
                elif token.value == "function":
                    self.ast.append(self.parse_function())
                else:
                    raise_parser_error(f"Unhandled keyword: {token.value}", self.tokens, self.pos, self.source)
            else:
                raise_parser_error(f"Unexpected token: {token}", self.tokens, self.pos, self.source)
        return self.ast

    def parse_import(self) -> Dict[str, str]:
        self.match("KEYWORD", "import")
        module_name = self.match("LITERAL").value
        self.match("OPERATOR", ";")
        return {"type": "import", "module": module_name}

    def parse_function(self) -> Dict[str, Any]:
        self.match("KEYWORD", "function")
        name = self.match("IDENTIFIER").value
        self.match("OPERATOR", "(")
        args = self.parse_arguments()
        self.match("OPERATOR", ")")
        return_type: Optional[str] = None
        if self.current_token() and self.current_token().value == ":":
            self.match("OPERATOR", ":")
            return_type = self.match("PRIMITIVE").value
        self.match("KEYWORD", "do")
        body = self.parse_block()
        self.match("KEYWORD", "end")
        return {"type": "function", "name": name, "args": args, "return_type": return_type, "body": body}

    def parse_arguments(self) -> List[Dict[str, str]]:
        args: List[Dict[str, str]] = []
        while self.current_token() and self.current_token().value != ")":
            arg_type = self.match("PRIMITIVE").value
            arg_name = self.match("IDENTIFIER").value
            args.append({"type": arg_type, "name": arg_name})
            if self.current_token() and self.current_token().value == ",":
                self.match("OPERATOR", ",")
        return args

    def parse_block(self) -> List[Dict[str, Any]]:
        block: List[Dict[str, Any]] = []
        while self.current_token() and self.current_token().value != "end":
            token = self.current_token()
            if isinstance(token, Keyword) and token.value == "return":
                block.append(self.parse_return())
            elif isinstance(token, Identifier):
                block.append(self.parse_statement())
            else:
                raise_parser_error(f"Unexpected token in block: `{token.value}`", self.tokens, self.pos, self.source)
        return block

    def parse_statement(self) -> Dict[str, Any]:
        token = self.current_token()
        if isinstance(token, Identifier):
            return self.parse_function_call()
        else:
            raise_parser_error(f"Unexpected statement start: `{token.value}`", self.tokens, self.pos, self.source)

    def parse_function_call(self) -> Dict[str, Any]:
        name = self.match("IDENTIFIER").value
        self.match("OPERATOR", "(")
        args = self.parse_call_arguments()
        self.match("OPERATOR", ")")
        self.match("OPERATOR", ";")
        return {"type": "call", "name": name, "args": args}

    def parse_call_arguments(self) -> List[str]:
        args: List[str] = []
        while self.current_token() and self.current_token().value != ")":
            token = self.current_token()

            # Check if we encounter an opening parenthesis, which indicates a nested function call
            if isinstance(token, Operator) and token.value == "(":
                args.append(self.parse_function_call())  # Parse the nested function call

            elif isinstance(token, Literal):
                args.append(self.match("LITERAL").value)

            elif isinstance(token, Identifier):
                args.append(self.match("IDENTIFIER").value)

            else:
                raise_parser_error(f"Unexpected token in function call arguments: `{token.value}`", self.tokens, self.pos, self.source)

            # Handle argument separation by commas
            if self.current_token() and self.current_token().value == ",":
                self.match("OPERATOR", ",")

        return args

    def parse_return(self) -> Dict[str, Any]:
        self.match("KEYWORD", "return")
        value = self.match("LITERAL" if isinstance(self.current_token(), Literal) else "IDENTIFIER").value
        self.match("OPERATOR", ";")
        return {"type": "return", "value": value}
