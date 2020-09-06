from typing import Callable, Sequence, Tuple, Optional, List, Any
import os

class UsageException(Exception):
    '''An exception to signal, that the parsing of an argument failed / that it has an invalid value.'''
    pass


class GenericOption:
    def __init__(self, arg_str) -> None:
        '''Parse the value. It may throw an exception (of class UsageException), if the argument is malformatted / invalid'''
        self.raw = arg_str

    def value(self) -> Any:
        return self.raw

    @classmethod
    def complete(cls, my_shell, argument_up_to_cursor: str, text: str) -> List[str]:
        return []

    @classmethod
    def describe(cls) -> str:
        return 'No description available'


class OptionList(GenericOption):
    options: List[str] = []

    def __init__(self, arg_value):
        super().__init__(arg_value)

        if len(self.options) < 2:
            raise Exception('Has to has at least two options')

        if arg_value not in self.options:
            raise UsageException(f'Invalid option: got "{arg_value}", but expected one of {self.pretty_options()}')

    @classmethod
    def pretty_options(cls) -> str:
        joined = '", "'.join(cls.options)
        return f'"{joined}"'

    @classmethod
    def complete(cls, my_shell, argument_up_to_cursor: str, text: str) -> List[str]:
        return [o for o in cls.options if o.startswith(text)]

    @classmethod
    def describe(cls) -> str:
        return 'Valid values: ' + cls.pretty_options()

    @classmethod
    def parse(cls, arg: str) -> str:
        '''Parse the value. It may throw an UsageException, if the argument is malformatted / invalid'''
        if arg not in cls.options:
            raise UsageException(f'Invalid option: got "{arg}", but expected one of {cls.pretty_options()}')
        else:
            return arg

class BoolOption(OptionList):
    options = ['true', 'false']

    def value(self) -> bool:
        return self.raw == 'true'


def complete_path(current_directory: str, fn_list_files_in_folder: Callable,
                  argument_up_to_cursor: str, text: str) -> List[str]:
    folder = os.path.dirname(argument_up_to_cursor + 'handle_trailing_slash_correctly')
    folder_path = os.path.join(current_directory, folder) if folder else current_directory

    file_names = fn_list_files_in_folder(folder_path)
    matches = [name for name in file_names if name.startswith(text)]
    return matches
