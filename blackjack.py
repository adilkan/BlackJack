import random

# Constants
DECK_COUNT = 5
DECK_START = 2
DECK_END = 11
BLACKJACK = 21
BET = 1000
MAX_GAMES = 1000000
HIT = 'HIT'
DOUBLE = 'DOUBLE'
STAND = 'STAND'


class Bot:
    def game_tactic(self, my_cards, dealer_card):
        '''
        Decide the action based on the player's hand and the dealer's visible card.
        Returns 'HIT' for Hit, 'DOUBLE' for Double Down, 'STAND' for Stand.
        '''
        value = sum(my_cards)

        # Bot's strategy based on player's hand and dealer's visible card
        if value <= 8:
            return HIT
        if value == 9:
            if 2 < dealer_card < 7:
                return DOUBLE
            return HIT
        if value == 10:
            if dealer_card < 10:
                return DOUBLE
            return HIT
        if value == 11:
            if dealer_card < 11:
                return DOUBLE
            return HIT
        if value == 12:
            if 3 < dealer_card < 7:
                return STAND
            return HIT
        if 12 < value < 17:
            if dealer_card < 7:
                return STAND
            return HIT
        return STAND


class DeckManager:
    def __init__(self):
        self.create_new_deck()

    def create_new_deck(self):
        # Create a new deck with shuffled cards
        self.current_deck = []
        for i in range(DECK_START, DECK_END + 1):
            quantity = DECK_COUNT * 4 if i != 10 else DECK_COUNT * 4 * 4
            self.current_deck.extend([i] * quantity)
        random.shuffle(self.current_deck)

    def draw_card(self):
        # Draw a card from the deck
        return self.current_deck.pop()

    def refresh_deck(self):
        # Refresh the deck if there are not enough cards left
        if len(self.current_deck) < 70:
            self.create_new_deck()


class Dealer:
    def __init__(self):
        self.deck = DeckManager()
        self.bet = BET
        self.player_wins = 0
        self.player_money = 0
        self.game_count = 0
        self.draw_count = 0

    def print_info(self):
        percentage_wins = round((self.player_wins / self.game_count) * 100, 2)
        percentage_losses = round(
            ((self.game_count - self.player_wins - self.draw_count) / self.game_count) * 100, 2)
        percentage_draws = round((self.draw_count / self.game_count) * 100, 2)

        print(
            f'Count of Player Win: {self.player_wins}\nCount of Draws: {self.draw_count}\nCount of all Games: {self.game_count}\nPlayer Money: {self.player_money}\n  Win   Draw   Lose\n{percentage_wins}%/{percentage_draws}%/{percentage_losses}%\n\n\n')

    def check_win(self, dealers, players):
        # Check the result of the game based on the hands
        over_dealer = self.check_over_21(dealers)
        over_players = self.check_over_21(players)
        if over_dealer:
            if over_players:
                return 'Draw'
            return 'Player'
        if over_players:
            return 'Dealer'
        if sum(dealers) > sum(players):
            return 'Dealer'
        if sum(dealers) < sum(players):
            return 'Player'
        return 'Draw'

    def dealer_play(self, dealer_cards):
        # Dealer plays based on a rule to stand at 17 or higher
        while sum(dealer_cards) < 17:
            card = self.deck.draw_card()
            dealer_cards.append(card)
            check = self.check_over_21(dealer_cards)
            if type(check) == list:
                dealer_cards = check
        return dealer_cards

    def check_over_21(self, deck):
        # Check if the hand is over 21 and handle the case of an Ace being used as 1
        if sum(deck) > BLACKJACK:
            if 11 in deck:
                deck.remove(11)
                deck.append(1)
                return deck
            return True
        return False

    def play(self, dealer_cards, players_cards):
        # The main logic for playing a round of the game
        response = bot.game_tactic(players_cards, dealer_cards[0])
        while response == HIT:
            card = self.deck.draw_card()
            players_cards.append(card)
            check = self.check_over_21(players_cards)
            if check is True:
                break
            if type(check) == list:
                players_cards = check

            response = bot.game_tactic(players_cards, dealer_cards[0])
            if response == DOUBLE:
                response = HIT

        if response == DOUBLE:
            card = self.deck.draw_card()
            players_cards.append(card)
            check = self.check_over_21(players_cards)
            if type(check) == list:
                players_cards = check
            self.bet *= 2

        dealer_cards = self.dealer_play(dealer_cards)
        return self.check_win(dealer_cards, players_cards)

    def check_black_jack(self, dealer_cards, players_cards):
        # Check for a blackjack in the initial hands and update results accordingly
        dealer_black_jack = sum(dealer_cards) == BLACKJACK
        player_black_jack = sum(players_cards) == BLACKJACK
        if player_black_jack:
            if dealer_black_jack:
                self.draw_count += 1
            else:
                self.player_wins += 1
                self.player_money += self.bet * 1.5
            return True
        elif dealer_black_jack:
            self.player_money -= self.bet
            return True

    def get_cards(self):
        # Deal initial hands for dealer and player
        dealers_hand = [self.deck.draw_card() for _ in range(2)]
        players_hand = [self.deck.draw_card() for _ in range(2)]
        return dealers_hand, players_hand

    def main(self):
        # Main game loop to play multiple rounds
        for i in range(MAX_GAMES):
            self.deck.refresh_deck()
            self.bet = BET
            dealer_cards, players_cards = self.get_cards()
            self.game_count += 1
            if self.check_black_jack(dealer_cards, players_cards):
                continue
            result = self.play(dealer_cards, players_cards)
            if result == 'Draw':
                self.draw_count += 1
            elif result == 'Dealer':
                self.player_money -= self.bet
            else:
                self.player_money += self.bet
                self.player_wins += 1
            self.print_info()


if __name__ == '__main__':
    # Create instances and start the game
    bot = Bot()
    dealer = Dealer()
    dealer.main()
