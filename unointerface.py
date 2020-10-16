# -*- coding: utf-8 -*-

import argparse
import cmd


class UnoInterface(cmd.Cmd):

    intro = 'Welcome to the Uno Arena shell.  Type help or ? for more info.  Type quit to exit the shell.\n'
    prompt = '>'


    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.engines = {}
        
        self._load_parser = argparse.ArgumentParser(description=self.do_load.__doc__, prog='load')
        self._load_parser.add_argument('command', help='Command to instantiate the engine.')
        self._load_parser.add_argument(['-n', '--name'], help='Name for the engine instance.')

        self._config_parser = argparse.ArgumentParser(description=self.do_config.__doc__, prog='config')

        self_unload_parser = argparse.ArgumentParser(description=self.do_unload.__doc__, prog='unload')
        self_unload_parser.add_argument(['-n', '--name'], help='Name for the instance to unload.')

        self_tournament_parser = argparse.ArgumentParser(description=selfdo_tournament.__doc__, prog='tournament')


    def do_load(self, arg):
        """Add an engine instance for the next tournament.

        Command Line Example: load "python3 engine.py" myengine
        """
        pass


    def do_config(self, arg):
        """Change settings for a loaded engine instance.  WIP"""
        pass


    def do_unload(self, arg):
        """Shut down and remove a loaded engine instance.

        Command Line Example: unload myengine
        """
        pass


    def do_tournament(self, arg):
        """Simulate a tournament between all loaded engine instances.  WIP"""
        pass


    def do_quit(self):
        """Stop engines and exit the shell."""
        pass

    def help_load(self): self._load_parser.print_help()
    def help_config(self): self._config_parser.print_help()
    def help_unload(self): self._unload_parser.print_help()
    def help_tournament(self): self._tournament_parser.print_help()
    def help_quit(self): print(self.do_quit.__doc__)


if __name__ == '__main__':
    pass
    #ui = UnoInterface()
    #ui.cmdloop()
