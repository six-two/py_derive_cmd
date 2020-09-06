from typing import Any, Callable, List, Type, TYPE_CHECKING
import cmd
import traceback
import functools
from inspect import Parameter
# Local
from .arguments import ArgParser
if TYPE_CHECKING:
    from .command import CommandInfo

class Settings:
    '''By modifying this class you can change the default behaviour and settings of this package.
    You can also hook yourself into any of the methods here
    '''

    def __init__(self, cmd_class: Type[cmd.Cmd], arg_parser: ArgParser = None, print_warnings: bool = True) -> None:
        self.cmd_class = cmd_class
        self.arg_parser = ArgParser() if arg_parser is None else arg_parser
        self.print_warnings = print_warnings
        self.split_command_line = None
        self.format_string_required_argument = '<{}>'
        self.format_string_optional_argument = '[{}]'
        from .command import CommandInfo
        self.registered_commands: List[CommandInfo] = []

    def make_box_message(self, title: str, message: str, line_length: int = 80, fillchar: str = '=') -> str:
        header = f' {title} '.center(line_length, '=')
        end = '=' * line_length
        return f'\n{header}\n{message.strip()}\n{end}'

    def param_to_help_text(self, p: Parameter) -> str:
        name = p.name.upper()
        optional = p.default != Parameter.empty
        format_string = self.format_string_optional_argument if optional else self.format_string_required_argument
        return format_string.format(name)

    def print_warning(self, message: str) -> None:
        if self.print_warnings:
            print(self.use_color(f'[py_derive_cmd] Warning: {message}', 'yellow'))

    def print_error(self, message: str) -> None:
        print(self.use_color(message, 'red'))

    def use_color(self, message: str, color: str) -> str:
        try:
            # Color the text if termcolor is installed
            import termcolor
            return termcolor.colored(message, color)
        except:
            return message

    def add_to_cmd(self, name: str, value: Any) -> None:
        if getattr(self.cmd_class, name, None) is not None:
            raise Exception(f'Trying to create method / property "{name}" of class {self.cmd_class}, but it already exists!')
        else:
            setattr(self.cmd_class, name, value)

    def handle_exceptions(self, command: 'CommandInfo', function_that_might_fail: Callable) -> Callable:
        '''
        A wrapper method (decorator) that should catch all exceptions and log / print them.
        It is used for created do_command and complete_command functions
        '''
        @functools.wraps(function_that_might_fail)
        def wrapper_print_exceptions(*args, **kwargs):
            try:
                return function_that_might_fail(*args, **kwargs)
            except Exception:
                self.print_error(self.make_box_message('Internal error', traceback.format_exc()))
        return wrapper_print_exceptions
