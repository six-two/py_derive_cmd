from typing import List, Sequence, Callable
import cmd
# Local
from .command import CommandInfo
from .common import pluralize
from .complete import UsageException


def create_do_command(command: CommandInfo, name: str) -> Callable:
    settings = command.settings

    def wrapper_do_command(self_of_cmd, args_str: str) -> bool:
        if command.use_raw_arg:
            return bool(command.fn(self_of_cmd, args_str))
        else:
            args = settings.arg_parser.split_args(args_str)

            if command.min_args <= len(args) <= command.max_args:
                try:
                    parsed_args = settings.arg_parser.parse_args(command.params, args)
                    ret = command.fn(self_of_cmd, *parsed_args)
                    return bool(ret)
                except UsageException as ex:
                    settings.print_error(str(ex))
                    return False
            else:
                real_arg_count = pluralize(len(args), 'argument')
                error_message = command.err_arg_count.format(real_arg_count)
                settings.print_error(error_message)
                print(f'Usage: {name} {command.usage_params}')
                return False

    return settings.print_exceptions(wrapper_do_command)

def create_help_method(command: CommandInfo) -> Callable:
    def wrapper_help_method(self_of_cmd: cmd.Cmd):
        print(f'Usage: {command.names[0]} {command.usage_params}')
        aliases = command.aliases()
        if len(aliases) >= 1:
            print(f'Aliases:', ', '.join(aliases))
        if command.full_description:
            print('\n' + command.full_description)

    return command.settings.print_exceptions(wrapper_help_method)

def create_complete_command(command: CommandInfo) -> Callable:
    settings = command.settings

    def wrapper_complete_command(self_of_cmd, text: str, line: str, begidx: int, endidx: int) -> List[str]:
        # Cut it off at the cursor
        before_cursor = line[:endidx]
        # Remove the command name
        before_cursor = before_cursor.split(' ', maxsplit=1)[1]
        args = settings.arg_parser.split_incomplete_args(before_cursor)

        if len(args) > command.max_args:
            settings.print_warning('Too many args!')
            # There are already too many arguments
            return []
        
        arg_index = len(args) - 1
        last_arg = args[arg_index]
        try:
            # Get the class of the parameter
            param_cls = command.params[arg_index].annotation
            # Call the complete function, if it is defineed
            return param_cls.complete(self_of_cmd, last_arg, text)
        except Exception as ex:
            settings.print_warning(f'Internal error in wrapper_complete_command: {ex}')
            # Complete function is probably not defined
            return []

    return settings.print_exceptions(wrapper_complete_command)
