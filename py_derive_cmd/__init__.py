from typing import List, Tuple, Callable, Sequence, Optional
import cmd
# Local
from .complete import GenericOption, OptionList, BoolOption, UsageException
from .arguments import ArgParser
from .settings import Settings
from .command import CommandInfo


# TODO add a list that stores all commands

def make_command(settings: Settings, short_description: str, aliases: Sequence[str] = [],
                 name: Optional[str] = None, raw_arg: bool = False) -> Callable:
    '''This decorator does not actually modify the function, it just adds it to the given "cls".'''
    def decorator_make_command(fn: Callable) -> Callable:
        _name = name if name else fn.__name__
        if _name in aliases:
            settings.print_warning(f'Command name "{_name}" is also in its alias list')
            names = list(aliases)
        else:
            names = [_name, *aliases]
        CommandInfo(settings, fn, names, short_description, raw_arg=raw_arg).register()
        return fn
    return decorator_make_command

__all__ = ['make_command', 'CommandInfo', 'Settings', 'ArgParser', 'GenericOption', 'OptionList',
 'BoolOption', 'UsageException']
