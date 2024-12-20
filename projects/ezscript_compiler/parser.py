from typing import List, Optional, Dict, Any
from tokens import *
from errors import raise_parser_error

class Parser:
    def __init__(self, tokens: List[TokenWithPos], source: str) -> None:
        self.tokens: List[TokenWithPos] = tokens
        self.pos: int = 0
        self.ast: List[Dict[str, Any]] = []
        self.source = source

    def current_token(self) -> Optional[TokenWithPos]:
        return self.tokens[self.pos] if self.pos < len(self.tokens) else None

    def peek_token(self, offset = 1) -> Optional[TokenWithPos]:
        return self.tokens[self.pos + offset] if self.pos + offset < len(self.tokens) else None

    def match(self, expected_type: Optional[str] = None, expected_value: Optional[str] = None) -> TokenWithPos:
        token = self.current_token()
        if token and ((not expected_type or token.token.token_type == expected_type) and
                      (not expected_value or token.token.value == expected_value)):
            self.pos += 1
            return token
        raise_parser_error(f"Unexpected {token.token.token_type.lower()} token: `{token.token.value}`. Expected `{expected_value}`.", token, self.source)

    def parse(self) -> List[Dict[str, Any]]:
        while self.pos < len(self.tokens):
            token = self.current_token()
            if isinstance(token.token, Keyword):
                if token.token.value == "import":
                    self.ast.append(self.parse_import())
                elif token.token.value == "function":
                    self.ast.append(self.parse_function())
                else:
                    raise_parser_error(f"Unhandled keyword: {token.token.value}", token, self.source)
            else:
                raise_parser_error(f"Unexpected token: {token.token.token_type.lower()} token: `{token.token.value}`.", token, self.source)
        return self.ast

    def parse_import(self) -> Dict[str, str]:
        self.match("KEYWORD", "import")
        module_name = self.match("LITERAL").token.value
        self.match("OPERATOR", ";")
        return {"type": "import", "module": module_name}

    def parse_function(self) -> Dict[str, Any]:
        self.match("KEYWORD", "function")
        name = self.match("IDENTIFIER").token.value
        self.match("OPERATOR", "(")
        args = self.parse_arguments()
        self.match("OPERATOR", ")")
        return_type: Optional[str] = "void"
        if self.current_token() and self.current_token().token.value == ":":
            self.match("OPERATOR", ":")
            return_type = self.match("PRIMITIVE").token.value
        self.match("KEYWORD", "do")
        body = self.parse_block()
        self.match("KEYWORD", "end")
        return {"type": "function", "name": name, "args": args, "return_type": return_type, "body": body}

    def parse_arguments(self) -> List[Dict[str, str]]:
        args: List[Dict[str, str]] = []
        while self.current_token() and self.current_token().token.value != ")":
            arg_type = self.match("PRIMITIVE").token.value
            arg_name = self.match("IDENTIFIER").token.value
            args.append({"type": arg_type, "name": arg_name})
            if self.current_token() and self.current_token().token.value == ",":
                self.match("OPERATOR", ",")
        return args

    def parse_block(self) -> List[Dict[str, Any]]:
        block: List[Dict[str, Any]] = []
        while self.current_token() and self.current_token().token.value != "end":
            token = self.current_token()
            if isinstance(token.token, Keyword) and token.token.value == "return":
                block.append(self.parse_return())
            elif isinstance(token.token, PrimitiveType):
                block.append(self.parse_variable_define())
            elif isinstance(token.token, Identifier):
                block.append(self.parse_statement())
            else:
                raise_parser_error(f"Unexpected token in block: `{token.token.value}`", token, self.source)
        return block

    def parse_variable_define(self) -> Dict[str, Any]:
        type = self.match("PRIMITIVE").token.value
        name = self.match("IDENTIFIER").token.value
        # Check if we are assigning.
        if isinstance(self.current_token().token, Operator) and self.current_token().token.value == "=":
            # self.pos -= 1
            self.match("OPERATOR", "=")
            # Check if we are assigning an variable or function call result.
            if isinstance(self.current_token().token, Identifier):
                value = None
                # Check for a function call result
                if isinstance(self.peek_token(1).token, Operator) and self.peek_token(1).token.value == "(":
                    value = self.parse_function_call()
                    return {"type": "variable_define", "name": name, "data_type": type, "value": value}
                # Otherwise we are assigning a variable to another one.
                else:
                    identifier = self.match("IDENTIFIER").token.value
                    value = identifier
                    self.match("OPERATOR", ";")
                return {"type": "variable_define", "name": name, "data_type": type, "value": value}
            # Check if we are assigning a literal value, like an int or string.
            elif isinstance(self.current_token().token, Literal):
                identifier = self.match("LITERAL").token.value
                value = identifier
                self.match("OPERATOR", ";")
                return {"type": "variable_define", "name": name, "data_type": type, "value": value}
        elif isinstance(self.current_token().token, Operator) and self.current_token().token.value == ";":
            self.match("OPERATOR", ";")
            return {"type": "variable_define", "name": name, "data_type": type}

    def parse_variable_assignment(self) -> Dict[str, Any]:
        dest = self.match("IDENTIFIER").token.value
        self.match("OPERATOR", "=")
        source = self.match("IDENTIFIER").token.value
        self.match("OPERATOR", ";")
        return {"type": "variable_assign", "dest": dest, "source": source}

    def parse_statement(self) -> Dict[str, Any]:
        token = self.current_token()
        if isinstance(token.token, Identifier):
            if isinstance(self.peek_token().token, Operator) and self.peek_token().token.value == "(":
                return self.parse_function_call()
            elif isinstance(self.peek_token().token, Operator) and self.peek_token().token.value == "=":
                return self.parse_variable_assignment()
            else:
                raise_parser_error(f"Unexpected identifier: `{token.token.value}`", token, self.source)
        else:
            raise_parser_error(f"Unexpected statement start: `{token.token.value}`", token, self.source)

    def parse_function_call(self) -> Dict[str, Any]:
        name = self.match("IDENTIFIER").token.value
        self.match("OPERATOR", "(")
        args = self.parse_call_arguments()
        self.match("OPERATOR", ")")
        self.match("OPERATOR", ";")
        return {"type": "call", "name": name, "args": args}

    def parse_call_arguments(self) -> List[str]:
        args: List[str] = []
        while self.current_token() and self.current_token().token.value != ")":
            token = self.current_token()

            # Check if we encounter an opening parenthesis, which indicates a nested function call
            if isinstance(token.token, Operator) and token.token.value == "(":
                args.append(self.parse_function_call())  # Parse the nested function call

            elif isinstance(token.token, Literal):
                args.append(self.match("LITERAL").token.value)

            elif isinstance(token.token, Identifier):
                args.append(self.match("IDENTIFIER").token.value)

            else:
                raise_parser_error(f"Unexpected token in function call arguments: `{token.token.value}`", token, self.source)

            # Handle argument separation by commas
            if self.current_token() and self.current_token().token.value == ",":
                self.match("OPERATOR", ",")

        return args

    def parse_return(self) -> Dict[str, Any]:
        self.match("KEYWORD", "return")
        value = self.match("LITERAL" if isinstance(self.current_token().token, Literal) else "IDENTIFIER").token.value
        self.match("OPERATOR", ";")
        return {"type": "return", "value": value}
