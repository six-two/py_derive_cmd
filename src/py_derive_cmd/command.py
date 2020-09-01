from typing import List, Sequence, Tuple, Callable
from inspect import Parameter, signature
from collections import OrderedDict
# Local
from .settings import Settings
from .common import pluralize, remove_duplicates

def arg_counts(params: Sequence[Parameter]) -> Tuple[int, int]:
    max_args = len(params)
    min_args = 0
    for p in params:
        # Count how many arguments are required
        if p.default != Parameter.empty:
            break
        min_args += 1
    return (min_args, max_args)

class CommandInfo:
    def __init__(self, settings: Settings, fn: Callable, names: Sequence[str],
                 short_description: str, full_description: str = None, raw_arg: bool = False) -> None:
        # Check the names
        if len(names) < 1:
            raise Exception('Trying to create command with no name(s)')
        
        if len(set(names)) != len(names):
            settings.print_warning(f'Duplicate name in list: {names}')
            # Remove duplicate entries
            self.names = remove_duplicates(names)
        else:
            self.names = list(names)

        if full_description is None:
            if fn.__doc__:
                full_description = fn.__doc__
            else:
                settings.print_warning(f'Method {fn.__name__} has no doc string')

        # Store passed args
        self.settings = settings
        self.fn = fn
        self.short_description = short_description
        self.full_description = full_description
        self.use_raw_arg = raw_arg

        # Handle fn's parameters
        params = signature(fn).parameters.values()
        # Remove the self / my_shell / cmd parameter
        self.params = list(params)[1:]
        param_usage_list = [settings.param_to_help_text(p) for p in self.params]
        self.usage_params = ' '.join(param_usage_list)
        self.min_args, self.max_args = arg_counts(self.params)

        if self.min_args == self.max_args:
            error_arg_count = 'exactly ' + pluralize(self.min_args, 'argument')
        else:
            error_arg_count = f'between {self.min_args} and {self.max_args} arguments'
        self.err_arg_count = f'This command expects {error_arg_count}, but it got {{}}!'

    def aliases(self) -> List[str]:
        # TODO mark as readonly
        return self.names[1:]

    def register(self, create_do: bool = True, create_complete: bool = True, create_help: bool = True) -> None:
        # Prevent circular import
        from .create_methods import create_complete_command, create_do_command, create_help_method
        settings = self.settings

        if create_do:
            for name in self.names:
                # Add the do_ method, that executes the command
                do_command = create_do_command(self, name)
                settings.add_to_cmd(f'do_{name}', do_command)

        if create_complete and len(self.params) != 0:
            complete_command = create_complete_command(self)
            for name in self.names:
                # Add a method that handles tab-completion of the arguments
                settings.add_to_cmd(f'complete_{name}', complete_command)

        if create_help:
            help_command = create_help_method(self)
            for name in self.names:
                # Add a method that handels "?command" / "help command"
                settings.add_to_cmd(f'help_{name}', help_command)

