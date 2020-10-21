# Copyright (c) UnlikeSuika
# See LICENSE for details
# I don't want to code Uno logic myself, so I'm using open source code released
# under the MIT license by UnlikeSuika.

from random import shuffle


def equal(c1: str, c2: str) -> bool:
    """Compare the color and value of two cards."""
    return c1 == c2


def equal_color(c1: str, c2: str) -> bool:
    """Compare the color of two cards."""
    return c1[1] == c2[1]


def equal_type(c1: str, c2: str) -> bool:
    """Compare the type of two cards."""
    if c1[0] == 'W' or c2[0] == 'W':
        return c1[:3] == c2[:3]
    return c1[0] == c2[0]


class Player(Engine):
    """Child class for adding Uno functionality to an engine.

    Args:
        hand (list): initial hand for the player
    """

    def __init__(self, *args, hand: list=[], **kwargs):
        super().__init__(*args, **kwargs)
        self.hand = hand


    def add_card(self, card: str):
        """Add `card` to the player's hand."""
        self.hand.append(card)


    def remove_card(self, card: str):
        """Remove exactly one of `card` from the player's hand."""
        self.hand.remove(card)


    def reset_hand(self):
        """Empty the player's hand."""
        self.hand = []


    def can_play_on(self, card: str) -> list:
        """Returns list of held cards playable on `card.`"""
        return [c for c in self.hand if (equal_color(c, card) or equal_type(c, card))]



class UnoGame:
    
    def __init__(self, players):
        self.players = players
        self.deck = []
        self.discard = []
        self.cycle = ReversibleCycle(players)


    def new_deck(self, randomize=True):
        """Makes a standard Uno deck.

        Args:
            shuffle (bool): Whether to randomize the deck (default: True)
        """
        deck = ['WD0', 'WD4']*4
        values = '0'+2*'123456789'+'SRD'
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
        
        if equal_type(c, 'S'):
            # Skip the next player
            next(self.cycle)
        elif equal_type(c, 'R'):
            # Flip the direction of play
            self.cycle.reverse()

        # Deal cards to each player
        for player in self.players:
            player.reset_hand()
            for i in range(7):
                player.add_card(self.draw_card())


    def play_turn(self):
        top_card = self.discard[-1]
        player = next(self.cycle)

        move = player.get_best_move()

        if move == protocol.RENEG:
            player.add_card(self.draw_card())
            return

        elif move == protocol.CHALLENGE:
            if not self.can_challenge:
                raise ValueError('Challenging is not allowed right now.')
            # Check if the challenge succeeded
            ind = self.players.index(player)-1
            last_p = self.players[ind]
            last_c = self.discard[-2]
            if last_p.can_play_on(last_c):
                # The last player could have played, so the challenge succeeds.
                pass
            else:
                # Otherise, it fails.
            return

        elif move == protocol.DRAW:
            pass

        elif move:
            # Playing a card.
            if player.can_play_on(top_card)

        # The discard list only ever has two cards:
        # the most recent discard and the second most recent discard.
        # No more is needed.
        if len(self.discard_list) >= 2:
            self.discard_list = [self.discard_list[-1], top_card]


    def draw_card(self, exclude_wild=False):
        if not self.deck:
            self.deck = self.new_deck(randomize=True)
            self.deck.remove(self.top_card)

        if exclude_wild:
            for count, card in enumerate(deck):
                if c[:2] != 'WD':
                    return self.deck.pop(count)
        else:
            return self.deck.pop(0)


    def end_game(self): pass




    def __can_be_played__(self, card):
        """
        Determines if the card can currently be played.
        Return:
        bool: True if the card can be played, False otherwise
        """
        if (self.wild_color != CardColor["BLACK"]
                and card.get_color() == self.wild_color):
            return True
        elif card.equals_color(self.discard[-1]):
            return True
        if card.equals_type(self.discard[-1]):
            return True
        if card.get_color() == CardColor["BLACK"]:
            return True
    
    def __play_card__(self, index):
        """
        Play the card of the given index, and move on to the next turn.
        Argument:
        index(int): Index of the card
        Return:
        bool: False if the current player wins the match, True otherwise
        """
        card = self.players[self.turn].get_cards()[index]
        self.__discard_player_card__(self.players[self.turn], index)
        turn_before = self.turn
        # Skip card
        if card.get_type() == CardType["SKIP"]:
            self.__next_turn__()
            print("Player " + str(self.turn+1) + " is skipped.")
            self.__next_turn__()
            self.wild_color == CardColor["BLACK"]
        # Draw Two card
        elif card.get_type() == CardType["DRAW_TWO"]:
            self.__next_turn__()
            self.__give_topdeck_to_player__(self.players[self.turn])
            self.__give_topdeck_to_player__(self.players[self.turn])
            print("Player "
                  +str(self.turn+1)
                  +" draws "
                  +str(self.players[self.turn].get_cards()[-2])
                  +", "
                  +str(self.players[self.turn].get_cards()[-1])
                  +" and is skipped.")
            self.players[self.turn].sort_cards()
            self.__next_turn__()
            self.wild_color == CardColor["BLACK"]
        # Reverse card
        elif card.get_type() == CardType["REVERSE"]:
            # Acts the same way as Skip card if there are only two players
            if len(self.players) == 2:
                self.__next_turn__()
                print("Player " + str(self.turn+1) + " is skipped.")
                self.__next_turn__()
            else:
                print("Order is reversed.")
                if self.clockwise:
                    self.clockwise = False
                else:
                    self.clockwise = True
                self.__next_turn__()
            self.wild_color == CardColor["BLACK"]
        # Wild card
        elif card.get_type() == CardType["WILD"]:
            print("Choose a color for wild card (\".r\", \".y\", \".g\", or \""
                  + ".b\")")
            color = input().split()[0]
            while color not in [".r", ".y", ".g", ".b"]:
                print("Invalid input.")
                color = input().split()[0]
            color_value = [".r", ".y", ".g", ".b"].index(color) + 1
            self.wild_color = CardColor(color_value)
            self.__next_turn__()
        # Wild Draw Four card
        elif card.get_type() == CardType["WILD_DRAW_FOUR"]:
            # Determine if Wild Draw Four card is legal
            is_legal_wd4 = True
            for card_it in self.players[self.turn].get_cards():
                if card_it.get_type() == CardType['WILD_DRAW_FOUR']:
                    continue
                elif (self.discard[-2].get_color() == CardColor['BLACK']
                      and card_it.get_color == self.wild_color):
                    is_legal_wd4 = False
                    break
                elif (self.discard[-2].get_color() != CardColor['BLACK']
                      and card_it.equals_color(self.discard[-2])):
                    is_legal_wd4 = False
                    break
            # Choose colour for wild
            print("Choose a color for wild card (\".r\", \".y\", \".g\", or \"."
                  + "b\")")
            color = input().split()[0]
            while color not in [".r", ".y", ".g", ".b"]:
                print("Invalid input.")
                color = input().split()[0]
            color_value = [".r", ".y", ".g", ".b"].index(color) + 1
            self.wild_color = CardColor(color_value)
            challenged_index = self.turn
            # Gives next player an opportunity to challenge
            self.__next_turn__()
            print("Will Player "
                  + str(self.turn + 1)
                  + " challenge the Wild Draw Four?")
            print("Answer by yes (\".y\") or no (\".n\").")
            answer = input().split()[0]
            while answer not in [".y", ".n"]:
                print("Invalid input.")
                answer = input().split()[0]
            # If challenged
            if answer == ".y":
                print("Player " + str(challenged_index + 1) + "'s cards are:")
                self.players[challenged_index].print_cards()
                # If challenge is not successful
                if is_legal_wd4:
                    print("The Wild Draw Four was legal.")            
                    print("Player " + str(self.turn+1) + " draws ", end="")
                    for i in range(6):
                        self.__give_topdeck_to_player__(self.players[self.turn])
                        print(str(self.players[self.turn].get_cards()[-1]),
                              end="")
                        if i < 5:
                            print(", ", end="")
                    print(" and is skipped.")
                    self.players[self.turn].sort_cards()
                # If challenge is successful
                else:
                    print("The Wild Draw Four was illegal.")
                    print("Player " + str(challenged_index + 1) + " draws ",
                          end="")
                    for i in range(4):
                        self.__give_topdeck_to_player__(
                            self.players[challenged_index])
                        print(
                            str(self.players[challenged_index].get_cards()[-1]),
                            end="")
                        if i < 3:
                            print(", ", end="")
                    print(".\nPlayer " + str(self.turn + 1) + " is skipped.")
                    self.players[challenged_index].sort_cards()
            # If not challenged
            else:
                print("Player " + str(self.turn + 1) + " draws ", end="")
                for i in range(4):
                    self.__give_topdeck_to_player__(self.players[self.turn])
                    print(str(self.players[self.turn].get_cards()[-1]), end="")
                    if i < 3:
                        print(", ", end="")
                print(" and is skipped.")
                self.players[self.turn].sort_cards()
            self.__next_turn__()
        # A non-action card
        else:
            self.__next_turn__()
        # If the player wins the match
        if not self.players[turn_before].get_cards():
            self.winner_index = turn_before
			self.wild_color = CardColor["BLACK"]
            return False
        return True

    def run(self):
        """Ask the current player what to do, and move on to the next turn.
        Return:
        bool: False if the game has ended this turn, True otherwise
        """
        print("----------")
        print("Player " + str(self.turn + 1) + "'s turn.")
        self.players[self.turn].print_cards()
        print("Top card: " + str(self.discard[-1]), end="")
        # Print the color called for Wild card (if applicable)
        if self.discard[-1].get_color() == CardColor["BLACK"]:
            if self.wild_color == CardColor["RED"]:
                print("[R]", end="")
            elif self.wild_color == CardColor["YELLOW"]:
                print("[Y]", end="")
            elif self.wild_color == CardColor["GREEN"]:
                print("[G]", end="")
            else:
                print("[B]", end="")
        print("\nPlay a card by \".p <card index>\" or draw by \".d\" (without "
              +"quotations).")
        # Loop continues until player makes a valid input.
        while True:
            move = input().split()
            if not move:
                print("Invalid input.")
            # Case of playing a card
            elif move[0] == ".p":
                if len(move) < 2:
                    print("Invalid input.")
                    continue
                try:
                    index = int(eval(move[1])) - 1
                except:
                    print("Invalid input.")
                    continue
                if index < 0 or index >= len(
                  self.players[self.turn].get_cards()):
                    print("Index out of range.")
                    continue
                player_card = self.players[self.turn].get_cards()[index]
                if self.__can_be_played__(player_card):
                    return self.__play_card__(index)
                else:
                    print("This card cannot be played.")
                    continue
            # Case of drawing a card
            elif move[0] == ".d":
                if not self.__give_topdeck_to_player__(self.players[self.turn]):
                    self.__next_turn__()
                    return True
                new_card = self.players[self.turn].get_cards()[-1]
                print("You have drawn card: " + str(new_card))
                print("Keep(\".k\") or play(\".p\")?")
                choice = input()
                while choice.split()[0] not in [".k", ".p"]:
                    print("Invalid input.")
                    choice = input()
                # Only play the card if the card can be played
                if choice.split()[0] == ".p":
                    if self.__can_be_played__(new_card):
                        return self.__play_card__(-1)
                    else:
                        print("This card cannot be played.")
                self.players[self.turn].sort_cards()
                self.__next_turn__()
                return True
            else:
                print("Invalid input.")

    def game_end(self):
        """
        Add the score to the winner
        Return:
        int: Index of the player who wins the game
        """
        score = 0
        winner = self.players[self.winner_index]
        for player in self.players:
            if player == winner:
                continue
            for card in player.get_cards():
                if card.get_type() == CardType["ONE"]:
                    score += 1
                elif card.get_type() == CardType["TWO"]:
                    score += 2
                elif card.get_type() == CardType["THREE"]:
                    score += 3
                elif card.get_type() == CardType["FOUR"]:
                    score += 4
                elif card.get_type() == CardType["FIVE"]:
                    score += 5
                elif card.get_type() == CardType["SIX"]:
                    score += 6
                elif card.get_type() == CardType["SEVEN"]:
                    score += 7
                elif card.get_type() == CardType["EIGHT"]:
                    score += 8
                elif card.get_type() == CardType["NINE"]:
                    score += 9
                elif card.get_type() in [CardType["SKIP"],
                                         CardType["DRAW_TWO"],
                                         CardType["REVERSE"]]:
                    score += 20
                elif card.get_type() in [CardType["WILD"],
                                         CardType["WILD_DRAW_FOUR"]]:
                    score += 50
        self.players[self.winner_index].add_score(score)
        print("Player "
              + str(self.winner_index+1)
              + " earns "
              + str(score)
              + " points!")
        return self.winner_index


def main():
    print("How many players? (2-10)")
    while True:
        try:
            num_player = int(eval(input()))
            if num_player >= 2 and num_player <= 10:
                break
            else:
                print("There must be two to ten players.")
        except KeyboardInterrupt:
            return
        except:
            print("Invalid input.")
    players = []
    for i in range(num_player):
        players.append(Player())
    game = Game(players)
    while True:
        if not game.run():
            winner_index = game.game_end()
            print("===== Current scoreboard =====")
            for i in range(len(players)):
                if i == winner_index:
                    print("*", end="")
                print("Player "+str(i+1)+": "+str(players[i].get_score()))
            print("==============================")
            winner = players[winner_index]
            if winner.get_score() >= 500:
                print("Player "
                      +str(winner_index+1)
                      +" wins with total score of "
                      +str(winner.get_score())
                      +"!")
                return
            else:
                print("Starting next game...")
                game = Game(players)

main()
