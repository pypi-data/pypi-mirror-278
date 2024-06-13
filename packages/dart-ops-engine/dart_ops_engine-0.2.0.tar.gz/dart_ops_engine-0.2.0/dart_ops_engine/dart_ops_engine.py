import argparse
from typing import List

from .action_command import ActionCommand
from .execute import Execute
import sys
from .define import request_argument

class DartOpsEngine:
    def __init__(self, description: str = None):
        self.description = description
        self.parser = argparse.ArgumentParser(description=description)
        self.subparsers = self.parser.add_subparsers(dest="command", help="子命令")
        self.commands = []
    def addAction(self, action_name, run, description=None):
        command_parser = self.subparsers.add_parser(action_name, description=description)
        command_parser.add_argument('--id', help='执行ID', default="")
        command_parser.add_argument('--index', help='执行的索引', default=0)
        command = ActionCommand(action_name, description, {},run)
        command_parser.set_defaults(func=command.run)
        self.commands.append(command)


    def run(self):
        cache_args = []
        for arg in sys.argv:
            prefixs = ['--args=', '--env=', '--res=']
            if any(arg.startswith(prefix) for prefix in prefixs):
                request_argument.append(arg)
            else:
                cache_args.append(arg)
        
        sys.argv = cache_args
        args = self.parser.parse_args()
        if hasattr(args, "func"):
            args.func(args)
    
    
    
    
