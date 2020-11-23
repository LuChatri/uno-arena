# -*- coding: utf-8 -*-

import protocol
from argparse import ArgumentParser
from cmd import Cmd
from time import time


class UnoInterface(Cmd):

    intro = 'Welcome to the Uno Arena shell.  Type help or ? for more info.  Type quit to exit the shell.\n'
    prompt = '>'


    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.engines = []
        
        self._load_parser = ArgumentParser(description=self.do_load.__doc__, prog='load')
        self._load_parser.add_argument('command',
                                       help='Command to initialize the engine.')
        self._load_parser.add_argument('-n', '--name',
                                       help='Name for the engine instance.')
        self._load_parser.add_argument('-t', '--timeout',
                                       help='Max time to wait for boot up.',
                                       default=5,
                                       type=float)

        self._config_parser = ArgumentParser(description=self.do_config.__doc__, prog='config')

        self._unload_parser = ArgumentParser(description=self.do_unload.__doc__, prog='unload')
        self._unload_parser.add_argument('-n', '--name',
                                         help='Name for the instance to unload.')

        self._game_parser = ArgumentParser(description=self.do_game.__doc__, prog='game')


    def do_load(self, arg):
        """Add an engine instance for the next game.

        Command Line Example: load "python3 engine.py --no-gui" myengine
        """
        if len(self.engines) >= 15:
            print('There must fewer than 15 players')
            return
        
        try:
            args = self._load_parser(arg.split())
        except SystemExit:
            return

        e = Engine(args.name, args.command)
        t = time()

        while True:
            elapsed = time() - t
            timeout = args.timeout - elapsed

            if timeout < 0:
                print(f'Could not start {args.name}.  Shutting down...')
                e.stop()
                break

            msg = e.read(timeout)
            if msg[0] == protocol.BOOTING:
                print(f'{args.name} is booting...')
            elif msg[0] == protocol.ERROR:
                print(msg)
                print(f'Could not start {args.name}.  Shutting down...')
                e.force_stop()
                break
            elif msg[0] == protocol.READY:
                print(f'{args.name} booted successfully')
                self.engines.append(e)
                break
        

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

        name = args.name
        for e in self.engines:
            if e.name == name:
                print(f'Stopping {name}')
                e.stop()
                self.engines.remove(e)
                break
        else:
            print(f'Cannot find {name}')


    def do_game(self, arg):
        """Simulate a game between all loaded engine instances."""
        if not 2 <= len(self.engines) <= 15:
            print('There must be 2-15 players')
            return

        try:
            args = self._game_parser(arg.split())
        except SystemExit:
            return

        # Send New Game notification
        num_engines = len(self.engines)
        for e in self.engines:
            e.new_game(num_engines)

        # Start the game loop.
        simulate_game(self.engines)


    def do_quit(self):
        """Stop engines and exit the shell."""
        for e in self.engines:
            print(f'Stopping {e.name}')
            e.stop()
        self.close()


    def help_load(self): self._load_parser.print_help()
    def help_config(self): self._config_parser.print_help()
    def help_unload(self): self._unload_parser.print_help()
    def help_game(self): self._game_parser.print_help()
    def help_quit(self): print(self.do_quit.__doc__)


if __name__ == '__main__':
    ui = UnoInterface()
    ui.cmdloop()
