import re


class CommandContext:
    def __init__(self, sender, arguments):
        self.sender = sender
        self.arguments = arguments

    def get_argument(self, name):
        return self.arguments.get(name)


class CommandNode:
    def __init__(self, name, argument_type=None, action=None):
        self.name = name
        self.argument_type = argument_type  # None for literal nodes
        self.action = action
        self.children = {}

    def add_child(self, child):
        self.children[child.name] = child

    def execute(self, context):
        if self.action:
            return self.action(context)
        raise ValueError(f"Cannot execute command node '{self.name}' directly.")


class CommandDispatcher:
    def __init__(self):
        self.root = CommandNode("root")

    def register(self, root_node):
        self.root.add_child(root_node)

    def parse_and_execute(self, command_line, sender):
        parts = self._split_command(command_line)
        current = self.root
        arguments = {}

        print(parts, command_line)
        while parts:
            part = parts.pop(0)

            if part in current.children:
                current = current.children[part]
            elif current.argument_type:
                # If the argument type requires a list (recursive), handle that
                if isinstance(current.argument_type, CommandArgumentType):
                    # Recursively handle nested commands
                    arguments[current.name] = current.argument_type.parse(parts)
                else:
                    # Otherwise, handle single argument types
                    arguments[current.name] = current.argument_type.parse(part)
                current = next(iter(current.children.values()), None)  # Move to next node
            else:
                print(parts)
                raise ValueError(f"Unexpected input: {part}")

            if current is None:
                raise ValueError("Command ended prematurely")

        if current.action:
            context = CommandContext(sender, arguments)
            return current.execute(context)
        else:
            raise ValueError("Incomplete or invalid command")

    def _split_command(self, command_line):
        """
        Split the command line into arguments, correctly handling quoted strings
        and nested commands.
        """
        # Regular expression to split the command line, preserving quoted strings as single tokens
        # This ensures no empty string is added at the start
        return re.findall(r'\"([^\"]+)\"|\S+', command_line.strip())


# Base class for ArgumentTypes
class ArgumentType:
    def parse(self, value):
        raise NotImplementedError(f"Parse method not implemented for {self.__class__.__name__}")


# Specific argument types
class BoolArgumentType(ArgumentType):
    def parse(self, value):
        if value.lower() in ("true", "false"):
            return value.lower() == "true"
        raise ValueError(f"Invalid boolean value: {value}")


class FloatArgumentType(ArgumentType):
    def parse(self, value):
        try:
            return float(value)
        except ValueError:
            raise ValueError(f"Invalid float value: {value}")


class IntegerArgumentType(ArgumentType):
    def parse(self, value):
        try:
            return int(value)
        except ValueError:
            raise ValueError(f"Invalid integer value: {value}")


class StringArgumentType(ArgumentType):
    def parse(self, value):
        # Handle string arguments, e.g., allowing quoted strings
        return value


class LiteralArgumentType(ArgumentType):
    def __init__(self, literal_value):
        self.literal_value = literal_value

    def parse(self, value):
        if value == self.literal_value:
            return value
        raise ValueError(f"Invalid literal value: {value}, expected: {self.literal_value}")


# Argument type for recursive command (i.e., command arguments that are themselves commands)
class CommandArgumentType(ArgumentType):
    def __init__(self, dispatcher):
        self.dispatcher = dispatcher

    def parse(self, parts):
        # Here, we'll parse the parts as another command
        # Recursively call parse_and_execute to handle nested commands
        command = ' '.join(parts)  # Join the rest of the parts into a full command
        return command


# Helper functions to create nodes
def literal(name):
    return CommandNode(name)


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

# Define "say" command
say = literal("say")
message = argument("message", StringArgumentType())
message.action = lambda ctx: ctx.sender.send_message(f"Message: {ctx.get_argument('message')}")
say.add_child(message)

# Define "execute" command with nested command (recursive command)
execute = literal("execute")
as_player = argument("as", StringArgumentType())  # No action
execute.add_child(as_player)

command_to_run = argument("command", CommandArgumentType(dispatcher))  # A nested command argument
execute.add_child(command_to_run)

dispatcher.register(say)
dispatcher.register(execute)

# Create a custom sender
sender = CommandSender(dispatcher)

# Execute commands
try:
    sender.run_command('say "Hello world"')  # Simple say command
    sender.run_command('execute as "Player1" command say "Hello from Player1"')  # Execute nested command
except ValueError as e:
    print(e)
