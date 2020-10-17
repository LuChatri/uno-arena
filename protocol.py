"""
Constants for use in communciation with engines.

Messages must end in newlines.  Any unexpected messages should be ignored.
"""

# After boot, Uno Arena will send a PING to the engine.
# The engine must reply OK or it will be shut down.
PING = 'PING\n'
OK = 'OK\n'

# Tells the engine to shut down cleanly.  It has 5 seconds
# before a hard shutdown occurs.
SHUTDOWN = 'SHUTDOWN\n'
