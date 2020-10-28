# UNO Arena
## What is this?
Have you ever heard of [UCI](https://en.wikipedia.org/wiki/Universal_Chess_Interface)?  It's the Universal Chess Interface, which allows communication between chess engines and GUIs. It enables games against and between chess engines, like so:

![Example Chess GUI](https://i.stack.imgur.com/ZceaT.gif)

I'm making something similar for UNO.

## Installation
To install, clone the repository from the command line.

    git clone https://github.com/LuChatri/uno-arena.git

UNO Arena is currently a command line tool only. A GUI version is on my todo list. Change into the installation directory and execute with [Python](https://www.python.org/downloads/).

    python main.py

You should see output like this:

    Welcome to the Uno Arena shell.  Type help or ? for more info.  Type quit to exit the shell.
    > 

## Usage

From the shell, typing `help` will show you how to use UNO Arena. Basically, you can set up games between engines that support the UNO Arena protocol, which is outlined in protocol.py.  The short version:

    # Add a new engine for the next game named "Alice"
    > load "java engine --no-gui" Alice
    
    # Add a new engine named "Bob"
    > load "python C:\Users\Bob\Bobsengine.py --ram 1 --other-options-here" Bob
    
    # Check their status
    > status
    Alice - Loaded
    Bob - Loaded
    
    # Start a three game tournamnet
    > game -g 3
    Results (3 Games):
    Alice - 40 Pts
    Bob - 125 Pts
    
    > quit

## Why?

1. Improving my coding skills
2. I want to pit self-made UNO engines against one another.  It's a good computer science/game theory project.
3. I want to make an UNO engine to beat my brother.

## To Do
- [ ] Finish implementing UNO logic
- [ ] Re-write protocol for sending moves
- [ ] Add networking abilities
- [ ] Add GUI
