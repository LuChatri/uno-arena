# -*- coding: utf-8 -*-

import argparse
import cmd


class UnoInterface(cmd.Cmd):

    intro = 'Welcome to the Uno Arena shell.  Type help or ? for more info.  Type quit to exit the shell.\n''
    prompt = '>>>'

    def do_load(self, arg):
        """Add an engine instance for the next tournament."""
        pass


    def do_config(self, arg):
        """Change settings for a loaded engine instance."""
        pass


    def do_unload(self, arg):
        """Remove a loaded engine instance."""
        pass


    def do_tournament(self, arg):
        """Simulate a tournament between all loaded engine instances."""
        pass


    def do_quit(self, arg):
        """Stop all tournaments and exit the shell."""
        pass


if __name__ == '__main__':
    ui = UnoInterface()
    ui.cmdloop()
