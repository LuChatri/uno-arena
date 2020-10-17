# -*- coding: utf-8 -*-

import protocol
from engine import Engine
from argparse import ArgumentParser
from cmd import Cmd


class UnoInterface(Cmd):

    intro = 'Welcome to the Uno Arena shell.  Type help or ? for more info.  Type quit to exit the shell.\n'
    prompt = '>'


    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.engines = []
        
        self._load_parser = ArgumentParser(description=self.do_load.__doc__, prog='load')
        self._load_parser.add_argument('command', help='Command to instantiate the engine.')
        self._load_parser.add_argument('-n', '--name', help='Name for the engine instance.')
        self._load_parser.add_argument('-t', '--timeout', help='Max time to wait for boot up.', type=float, default=5)

        self._config_parser = ArgumentParser(description=self.do_config.__doc__, prog='config')

        self._unload_parser = ArgumentParser(description=self.do_unload.__doc__, prog='unload')
        self._unload_parser.add_argument('-n', '--name', help='Name for the instance to unload.')
        self._unload_parser.add_argument('-t', '--timeout', help='Max time to wait for shutdown', type=float, default=5)

        self._tournament_parser = ArgumentParser(description=self.do_tournament.__doc__, prog='tournament')


    def do_load(self, arg):
        """Add an engine instance for the next tournament.

        Command Line Example: load "python3 engine.py --no-gui" myengine
        """
        try:
            args = self._load_parser(arg.split())
        except SystemExit:
            return

        e = Engine(args.name, args.command)
        if e.ping(args.timeout):
            self.engines.append(e)
        else:
            print('Cannot start {}'.format(args.name))
            e.stop()
        

    def do_config(self, arg):
        """Change settings for a loaded engine instance.  WIP"""
        pass


    def do_unload(self, arg):
        """Shut down and remove a loaded engine instance.

        Command Line Example: unload myengine
        """
        try:
            args = self._unload_parser(arg.split())
        except SystemExit:
            return

        for e in self.engines:
            if e.name == args.name:
                print('Stopping {}'.format(e.name))
                e.stop()
                self.engines.remove(e)
                break
        else:
            print('Cannot find {}'.format(args.name))


    def do_tournament(self, arg):
        """Simulate a tournament between all loaded engine instances.  WIP"""
        pass


    def do_quit(self):
        """Stop engines and exit the shell."""
        for e in self.engines:
            print('Stopping {}'.format(e.name))
            e.stop()
        self.close()


    def help_load(self): self._load_parser.print_help()
    def help_config(self): self._config_parser.print_help()
    def help_unload(self): self._unload_parser.print_help()
    def help_tournament(self): self._tournament_parser.print_help()
    def help_quit(self): print(self.do_quit.__doc__)


if __name__ == '__main__':
    ui = UnoInterface()
    ui.cmdloop()
