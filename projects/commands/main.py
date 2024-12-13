from typing import List, Optional, Dict, Any
from tokens import Tokeniser, Token
from arguments import ArgumentType, ArrayArgument, BooleanArgument, FloatArgument, IntegerArgument, LiteralArgument, StringArgument, EnumArgument


class CommandContext:
    def __init__(self, sender: 'CommandSender', arguments: Dict[str, Any]):
        self.sender = sender
        self.arguments = arguments

    def get_argument(self, name):
        return self.arguments.get(name)


class CommandNode:
    def __init__(self, name, argument_type: Optional[ArgumentType] = None, action=None):
        self.name = name
        self.argument_type = argument_type
        self.action = action
        self.children: List['CommandNode'] = []

    def add_child(self, child: 'CommandNode'):
        self.children.append(child)

    def execute(self, context: CommandContext):
        if self.action:
            return self.action(context)
        raise ValueError(f"Cannot execute command node '{self.name}' directly.")


class CommandDispatcher:
    def __init__(self):
        self.root = CommandNode("root")

    def register(self, root_node: CommandNode):
        self.root.add_child(root_node)

    def parse_and_execute(self, command_line: str, sender: 'CommandSender'):
        tokeniser = Tokeniser(command_line)
        tokens = tokeniser.tokenise()

        current = self.root
        arguments = {}

        while tokens:
            token = tokens[0]
            found = False
            for child in current.children:
                if isinstance(child.argument_type, LiteralArgument) and child.argument_type.value == token.value:
                    current = child
                    tokens.pop(0)
                    found = True
                    break
                elif child.argument_type:
                    try:
                        arguments[child.name] = child.argument_type.parse(tokens)
                        current = child
                        found = True
                        break
                    except ValueError:
                        continue
            if not found:
                raise ValueError(f"Unknown command or argument: {token.value}, expected {child.argument_type.display()}")

        context = CommandContext(sender, arguments)
        current.execute(context)


# Helper functions to create nodes
def literal(name):
    return CommandNode(name, argument_type=LiteralArgument(name))


def argument(name, argument_type):
    return CommandNode(name, argument_type=argument_type)


# Define a custom CommandSender class
class CommandSender:
    def __init__(self, dispatcher):
        self.dispatcher = dispatcher

    def send_message(self, message):
        print(f"[{self.__class__.__name__}] {message}")

    def run_command(self, command):
        return self.dispatcher.parse_and_execute(command, self)


# Example usage
dispatcher = CommandDispatcher()

players = [
    "Bob",
    "Banana man",
    "Player1"
]

def make_say_commmand():
    say = literal("say")

    message = argument("message", StringArgument())
    message.action = lambda ctx: ctx.sender.send_message(f"Message: {ctx.get_argument('message')}")
    say.add_child(message)
    dispatcher.register(say)

def make_execute_command():
    execute = literal("execute")
    as_player = argument("as", LiteralArgument("as"))
    execute.add_child(as_player)

    p = argument("player", EnumArgument(players))
    as_player.add_child(p)

    command_to_run = argument("command", ArrayArgument())
    command_to_run.action = lambda ctx: ctx.sender.send_message(f"Message: {ctx.arguments}")
    p.add_child(command_to_run)

    dispatcher.register(execute)

make_say_commmand()
make_execute_command()

# Create a custom sender
sender = CommandSender(dispatcher)

# Execute commands
try:
    sender.run_command('say "Hello world"')  # Simple say command
    sender.run_command('execute as Player1 say "Hello from Player1"')  # Execute nested command
except ValueError as e:
    print(e)
