
import protocol
from engine import Engine
from random import shuffle
from re import match
from time import sleep


class UnoGame:


    ILLEGAL_MOVE = 0
    TIMED_OUT = 1
    CALC_TIME = 1
    
    
    def __init__(self, engines):
        self.players = [Player(e) for e in engines]
        self.deck = []
        self.discard = []
        self.cycle = ReversibleCycle(self.players)


    def new_deck(self, randomize=True) -> list:
        """Makes a standard Uno deck.

        Args:
            shuffle (bool): Whether to randomize the deck (default: True)
        """
        deck = 4*['W', 'WD4']
        values = list('0'+2*'123456789RS') + 2*['D2']
        for color in 'RGBY':
            deck.extend([v+color for v in vals])

        if randomize:
            shuffle(deck)
        return deck


    def start(self):
        self.deck = self.new_deck(randomize=True)

        # Turn over the top card
        c = self.draw_card(exclude_wild=True)
        self.discard.append(c)
        
        if c.startswith('S'):
            # Skip the next player
            next(self.cycle)
        elif c.startswith('R'):
            # Flip the direction of play
            self.cycle.reverse()

        # Reset engine internal states
        msg = f'{protocol.NEWGAME} {len(self.players)} {c}'
        for player in self.players:
            player.write(msg)

        # Deal cards
        for player in self.players:
            for i in range(7):
                player.add_card(self.draw_card())


    def play_turn(self):
        top_card = self.discard[-1]
        player = next(self.cycle)

        while True:
            player.write(protocol.GO)
            time.sleep(self.CALC_TIME)

            while (msg := player.read()):
                if msg[0] == protocol.MOVE:
                    break
                elif msg[0] == protocol.ERROR:
                    return (self.TIMED_OUT, player)
            else:
                return (self.TIMED_OUT, player)

            
            if msg[1] == protocol.RENEGE:
                player.add_card(self.draw_card())
                break

            elif msg[1] == protocol.CHALLENGE:
                if not self.can_challenge:
                    return (self.ILLEGAL_MOVE, player)

                self.can_challenge = False
                last_p = self.players[self.players.index(player)-1]
                last_top_c = self.discard[-2]

                if last_p.can_play_on(last_top_c):
                    # The last player could have played, so the challenge succeeds.
                    # The player can then do another action.
                    for i in range(4):
                        last_p.add_card(self.draw_card())
                    continue
                else:
                    # The challenge fails, so they draw and their turn ends.
                    for i in range(6):
                        player.add_card(self.draw_card())
                    break

            elif msg[1] == protocol.DRAW:
                # Draw while true, play first good card
            
            else:
                # A card is being played.
                card = self.parse_card(msg[1])
                if card is False:
                    return (self.ILLEGAL_MOVE, player)

                c_type, color = card
                if c_type == 'WD4':
                    pass
                elif c_type == 'W':
                    pass
                else:
                    last_c_type, last_color = self.parse_card(self.discard[-1])
                    if c_type != last_c_type and color != last_color:
                        return (self.ILLEGAL_MOVE, player)

                    if c_type == 'R':
                        self.cycle.reverse()
                    elif c_type == 'S':
                        next(self.cycle)
                    elif c_type == 'D2':
                        pass
                    else:
                        pass


    def parse_card(self, card: str) -> tuple:
        card = card.upper()
        try:
            if card.startswith('WD4'):
                c_type = 'WD4'
                color = card[3]
            elif card.startswith('D2'):
                c_type = 'D2'
                color = card[2]
            else:
                c_type = card[0]
                if c_type not in '0123456789RSW':
                    return False
                color = card[1]
        except IndexError:
            return False

        if color not in 'RGBY':
            return False

        return (c_type, color)


    def draw_card(self, exclude_wild=False) -> str:
        if not self.deck:
            self.deck = self.new_deck(randomize=True)
            self.deck.remove(self.top_card)

        if exclude_wild:
            for count, card in enumerate(deck):
                if 'W' not in card:
                    return self.deck.pop(count)
        else:
            return self.deck.pop(0)
