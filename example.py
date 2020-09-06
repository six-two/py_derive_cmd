#!/usr/bin/env python3
# pylint: disable=unused-wildcard-import
from py_derive_cmd import *
import cmd

class MyCmd(cmd.Cmd):
    pass

s = Settings(MyCmd, print_warnings=False)

@make_command(s, 'Test for the decorator', aliases=['d'])
def test_decorator(shell: MyCmd, req_arg: str, opt_arg: str = None):
    print('Decorator works')
    print(req_arg)
    print(opt_arg)

def test_register(shell: MyCmd, raw_arg: str):
    print('Register works')
    print(raw_arg)

@make_command(s, 'Exit the shell by pressing Ctrl-D')
def EOF(shell: MyCmd) -> bool:
    return True

CommandInfo(s, test_register, ['registered', 'r'], 'Test for register', raw_arg=True).register()

shell = MyCmd()
shell.cmdloop()