"""
Constants for use in communciation with engines.
"""
# Messages must end in newlines.
# Any unexpected messages should be ignored.

# After boot, Uno Arena will send a PING to the engine.
# The engine must reply OK or it will be shut down.
PING = 'PING\n'
OK = 'OK\n'

# Tells the engine to shut down cleanly.  It has 5 seconds
# before a hard shutdown occurs.
SHUTDOWN = 'SHUTDOWN\n'

# Tells the engine to reset to an initial game state.
# Format: NEWGAME players {# of players}
NEWGAME = 'NEWGAME players {n_players}\n'

# Tells the engine the current position.
# Format: POSITION players {# of players} moves {moves...}
# Cards are strings formatted as follows:
#   "Normal" cards are two characters: a value 0-9 or S for skip, R
#   for reverse, or D for draw two, followed by a color in RGBY.
#   Wild cards are W.  After they are played, a color as appended to them.
#   Wild draw four cards are WD.  After they are played, a color is appended
#   to them.
# Moves are then given as follows:
#   At the start of the game or when the discard pile is reshuffled,
#   the move is written as SHUFFLE.
#   After the first SHUFFLE, the top card is turned over.  It is written in
#   the standard card format.
#   When a card is played, it is written in the standard card format.
#   When a player renegs, it is written as RENEG.
#   When a player draws but does not reneg, it is written as DRAW {n} where n
#   is the number of cards drawn.
#   When a WD is challenged, successful challenges are written as CS and
#   failed challenges are written as CF
#   There is no way to declare UNO because declaring UNO is trivial
#   with computers.
POSITION = 'POSITION players {n_players} moves {moves}\n'

# Tells the engine to start calculating.  It should not calculate without
# being sent this command.  It will always receive a position command prio
# to receiving the GO command.
GO = 'GO\n'

# Tells the engine to stop calculating.  It should not calculate after being
# sent this command.
STOP = 'STOP\n'

# Tells the engine to send what it thinks the best play is in the current
# position based only on prior calculation.
BEST = 'BEST\n'
