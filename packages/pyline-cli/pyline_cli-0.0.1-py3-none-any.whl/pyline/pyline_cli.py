import ast
import inspect
from typing import Any, Callable
from fuzzywuzzy import process


def parse_input_arguments(input_arguments: list[str]) -> list[Any]:
    parsed_arguments = []
    for input_argument in input_arguments:
        parsed_arguments.append(ast.literal_eval(input_argument))

    return parsed_arguments


class Cli:
    def __init__(self) -> None:
        self.commands = {}

    def add_command(self, command_name: str = None, command_doc: str = None) -> Callable:

        def decorator(func: Callable) -> None:
            nonlocal command_name, command_doc

            if not command_name:
                command_name = func.__name__
            if not command_doc:
                command_doc = func.__doc__

            self.commands[command_name] = {'func': func, 'desc': command_doc, 'args': inspect.getfullargspec(func).args}

        return decorator

    def parse_command(self, text: str) -> (Any, int):
        tokens = text.split(' ')

        # Get info from the tokens
        command_to_call = tokens[0]
        input_args = tokens[1:]

        # Check if the command exists
        if command_to_call not in self.commands:
            best_match, score = process.extractOne(command_to_call, list(self.commands))
            if score >= 80:
                return f'No command called: "{command_to_call}" exists! did you mean: "{best_match}"', 1
            else:
                return f'No command called: "{command_to_call}" exists!', 1

        # Get the command
        command = self.commands[command_to_call]

        # Check if the right amount if arguments were given
        if len(input_args) != len(command['args']):
            return f'{len(command['args'])} arguments were expected but got {len(input_args)}', 1

        # Parse the input arguments
        parsed_input_args = parse_input_arguments(input_args)

        # Run the command
        command_result = command['func'](*parsed_input_args)

        return command_result, 0
