# Universal Uno Interface Protocol
This document outlines the Universal Uno Interface protocol, which is used by this project to facilitate communication between Uno Arena and Uno engines.

# Communication Rules
- Uno Arena will send messages to an engine by writing to the engine's standard input.
- Engines will send messsages to Uno Arena by writing their own standard outputs.
- Messages that are unexpected or malformed should be ignored when received.

# Message Format
- Every message is begins with a key word that signals what type of message it is followed by the parameters that accompany the key word.
- Every message ends with a newline character `\n`.
- Every message will be lowercased.

# Key Words / Commands
In alphabetical order.
- `booting` - The engine should send this to Uno Arena immediately upon initialization to signal that it is starting up.
- `error` -  The engine send this to Uno Arena after encountering a fatal error. Uno Arena will no longer communicate with the engine or respond to its communications.  Full syntax:
  - `<error> := error <error-message>`
- `go` - Uno Arena should send this to the engine to signal the engine to start calculating from its internal game state.
- `move` - The engine should send this to Uno Arena after receiving a `stop` command to signal the move it would play based on the game state.  In the event that an illegal move is sent, Uno Arena will ignore it. Full syntax:
  - `<move> := move <move-info>`
  - `<move-info> := challenge | draw | renege | <card>`
  - `<card> := W<color> | WD4<color> | <type><color>`
  - `<color> := R | G | B | Y`
  - `<type> := [0-9] | R | S | D2`
  - Ex: `move WR` means play a wild and change the color to red.  `move 5R` means play a red five.  `move draw` means draw one card from the deck.
- `newgame` - Uno Arena should send this to the engine to signal the engine to reset its internal game sttate.  Full syntax:
  - `<newgame> := newgame <number-players> <top-card> ``
  - `<number-players> := [0-9]+
  - `<top-card> := <card>`
  - `<card> := W<color> | WD4<color> | <type><color>`
  - `<color> := R | G | B | Y`
  - `<type> := [0-9] | R | S | D2`
- `newmoves` - Uno Arena should send this to the engine to alter the engine's internal game state from a pre-existing state.  In other words, the engine should play out the specified moves in its internal game.  Full syntax:
  - `<newmoves> := newmoves <move>*`
  - `<move> := challenge | draw (<card>* | <number>) | renege | <card>`
  - `<number> := [0-9]+`
  - `<card> := W<color> | WD4<color> | <type><color>`
  - `<color> := R | G | B | Y`
  - `<type> := [0-9] | R | S | D2`
- `ready` - The engine should send this to Uno Arena to signal that the engine has booted and can receive information about the game state.
- `shutdown` - Uno Arena should send this to the engine to signal the engine to shut down immediately.  No further communication should be expected from Uno Arena.
- `shuttingdown` - The engine should send this to Uno Arena after receiving a `shutdown` command to signal that it has shut down and that its process can be terminated.  If the engine has not shut down thirty seconds after the `shutdown` command, it will be force stopped.
- `stop` - Uno Arena should send this to the engine to signal the engine to stop calculating.
