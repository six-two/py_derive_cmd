from typing import List, Sequence, Optional, Tuple, Any
from inspect import Parameter
import shlex
# Local
from .complete import UsageException


class ArgParser:
    def __init__(self, print_debug: bool = False) -> None:
        self.debug_printing_enabled = print_debug

    def print_debug(self, message: str) -> None:
        if self.debug_printing_enabled:
            print(message)

    def split_incomplete_args(self, incomplete_arg_str: str) -> List[str]:
        # add character to test if the last param should be extended
        # or if a new argument should be started
        TEST_STRING = '__cursor__'
        before_cursor = incomplete_arg_str + TEST_STRING
        args = self.split_args(before_cursor, may_be_cut_off=True)
        # Remove TEST_STRING
        if args[-1] == TEST_STRING:
            # Keep the empty argument to complete
            args[-1] = ''
        elif args[-1].endswith(TEST_STRING):
            args[-1] = args[-1][:-len(TEST_STRING)]
        else:
            print('BUG: Argument parsing: WTF happened to the test string?')
            print(args)

        self.print_debug(f'Arguments after split_incomplete_args: {args}')
        return args

    def split_args(self, arg_str: str, may_be_cut_off=False) -> List[str]:
        if arg_str:
            # TODO figure out how to handle a cutof arg that is quoted (avoid "ValueError: No closing quotation")
            return shlex.split(arg_str)
        else:
            return []

    def parse_args(self, params: Sequence[Parameter], args: Sequence[str]) -> List:
        parsed = []
        self.print_debug(f'before parse: {args}')
        for i in range(len(args)):
            # Get the class of the parameter
            param_cls = params[i].annotation
            arg: Any = args[i]

            if param_cls != Parameter.empty:
                try:
                    # Replace the argument with its parsed value
                    arg = param_cls(arg)
                except UsageException as ex:
                    error_message = f'Usage error in argument {i+1}: {ex}'
                    raise UsageException(error_message)
                    # Print an error message and
                    # print(err())
                    # return None
                self.print_debug(f'Param converted to {param_cls}')
            else:
                self.print_debug('Param {i}: No type in method signature')

            parsed.append(arg)

        self.print_debug(f'after parse: {parsed}')
        return parsed

