import random
# from IPython.display import clear_output # Available in the jupyter notebook system with .ipynb filetype

suits = ('Hearts', 'Diamonds', 'Spades', 'Clubs')
ranks = ('Two', 'Three', 'Four', 'Five', 'Six', 'Seven', 'Eight', 'Nine', 'Ten', 'Jack', 'Queen', 'King', 'Ace')
values = {'Two': 2, 'Three': 3, 'Four': 4, 'Five': 5, 'Six': 6, 'Seven': 7, 'Eight': 8, 'Nine': 9, 'Ten': 10,
          'Jack': 10,
          'Queen': 10, 'King': 10, 'Ace': 11}

class Card:
    def __init__(self, suit, rank):
        self.rank = rank
        self.suit = suit

    def __str__(self):
        return self.suit + ' of ' + self.rank


class Deck:
    def __init__(self):
        self.deck = []
        for suit in suits:
            for rank in ranks:
                self.deck.append(Card(suit, rank))

    def __str__(self):
        for card in self.deck:
            print(card)
        return ''


    def deck_shuffle(self):
        """Randomizes cards in the deck object"""
        random.shuffle(self.deck)

    def test_deck(self):
        """Prints out deck values for debugging"""
        print(self.deck)

    def deal(self):
        """Removes card from the deck and returns the card object that was removed from the deck"""
        dealt_card = self.deck.pop()
        return dealt_card


class Hand:
    def __init__(self):
        self.cards = []
        self.value = 0
        self.aces = 0

    def add_card(self, card):
        """
        Adds a card object to the hand
        :param card: A passed card object to be stored in self.cards
        """
        self.cards.append(card)
        self.value += values[card.rank]
        if card.rank == 'Ace':
            self.aces += 1

    def check_aces(self):
        """Checks and adjusts value for aces when appropriate"""
        if self.aces and self.value > 21:
            self.value -= 10
            self.aces -= 1


class Chips:
    def __init__(self, total=0, bet=0):
        self.total = total
        self.bet = bet

    def starting_amount(self):
        """Allows player to initialize their chip count"""
        while True:
            try:
                self.total = int(input('How many chips are you starting with?'))
                break
            except ValueError:
                print('Please enter a valid amount.')
                continue

    def win_bet(self):
        """Called if the player wins the hand. Because the player loses the chips when the bet is placed they win 2*bet"""
        self.total += self.bet * 2

    def place_bet(self):
        """Player inputs their bet amount. Checks to see if they have enough remaining chips"""
        while True:

            try:
                self.bet = int(input('What bet amount would you like to place?  '))
            except ValueError:
                print('Please try an integer value only.')

            else:
                if self.bet > self.total:
                    print(f'You must use a value lower than the amount of chips you have. You have {self.total} chips to bet with.')
                else:
                    break

        self.total -= self.bet


def take_hit(deck, hand):
    """
    Adds an additional card to the hand passed. Calls check_aces for value check.
    :param deck: The game deck.
    :param hand: Whose hand is receiving the card.
    :return:
    """
    hand.add_card(deck.deal())
    hand.check_aces()


def hit_or_stand(deck, player_hand):
    """
    Asks the player after card deal if they would like to receive additional cards or stick with their current hand.
    :param deck: The game deck.
    :param player_hand: The player's hand that could receive a card.
    """
    global playing

    while True:
        decision = input('Would you like to hit or stand? ')

        if decision[0].lower() == 'h':
            take_hit(deck, player_hand)

        elif decision[0].lower() == 's':
            playing = False

        else:
            print('Please respond with hit or stand')
            continue
        break


def show_some(player, dealer):
    """
    Shows player's cards to the player and shows the top dealer's card.
    :param player: player's hand
    :param dealer: dealer's hand
    """
    # clear_output() # Available call for .ipynb in Jupyter Notebook System

    # Dealer's hand output
    print('\nDealers Hand:')
    print('<hidden card>')
    print('', dealer.cards[1])

    # Player's hand output
    print('\nPlayer\'s Hand:')
    for card in player.cards:
        print('', card)
    print(f'The Player\'s hand is {player.value}.')


def show_all(player, dealer):
    """
    Shows all cards the dealer and player have.
    :param player: player's hand
    :param dealer: dealer's hand
    """

    # Dealer's hand output
    # clear_output() # Available call for .ipynb in Jupyter Notebook System
    print('\nDealers Hand:')
    for card in dealer.cards:
        print('', card)
    print(f'The Dealer\'s hand is {dealer.value}.')

    # Player's hand output
    print('\nPlayer\'s Hand:')
    for card in player.cards:
        print('', card)
    print(f'The Player\'s hand is {player.value}. \n')


def player_busts():
    """Print Statement if the player busts"""
    print('Player Busted. Never lucky.')


def dealer_busts(chips):
    """Print statement if dealer busts. Additionally the player receives 2 * bet amount"""
    chips.win_bet()
    print('Dealer Busted. Everyone wins.')


def push(chips):
    """Push occurs when dealer and player's hands are tied. At this point the player's chips (bet amount) are returned"""
    chips.total += chips.bet
    print('Dealer and player tied. Guess its a push.')


def player_wins(chips):
    """Called when player wins their hand. Player receives 2 * bet amount"""
    chips.win_bet()
    print('Player had the better hand. Enjoy that money.')


def dealer_wins():
    """Dealer wins print statement"""
    print('Dealer wins. The house always wins.')


def keep_playing():
    """Loops game and allows for continuous play"""
    global playing
    while True:
        try:
            new_game = input('Would you like to play another hand? y/n?')
        except ValueError:
            print('Please answer Y/N')
        else:
            if new_game[0].lower() == 'y':
                playing = True
                return playing

            elif new_game[0].lower() == 'n':
                print(f'Thanks for playing. Your final chip value is {player_chips.total}')
                break
            else:
                print('Please enter either Yes or No')
                continue


# Game Loop

print('Welcome to Blackjack. The goal of the game is to beat the dealer by being closer to 21. If you go over you lose! Dealer hits on 17 cause he is a crazy man.')

player_chips = Chips()
player_chips.starting_amount()
playing = True

while playing:

    dealer_busted = False
    player_busted = False

    # Create and shuffle the deck
    deck = Deck()
    deck.deck_shuffle()

    player_chips.place_bet()

    player = Hand()
    dealer = Hand()

    # Deal the cards
    player.add_card(deck.deal())
    dealer.add_card(deck.deal())
    player.add_card(deck.deal())
    dealer.add_card(deck.deal())
    player.check_aces()
    dealer.check_aces()

    show_some(player, dealer)

    # Hit or stand
    while playing:
        hit_or_stand(deck, player)
        show_some(player, dealer)

        if player.value > 21:
            player_busted = True
            playing = False

    if player.value <= 21:
        while dealer.value < 17:
            take_hit(deck, dealer)

    if dealer.value > 21:
        dealer_busted = True

    show_all(player, dealer)

    if player_busted:
        player_busts()
    elif dealer_busted:
        dealer_busts(player_chips)
    elif player.value > dealer.value and (player_busted is not True):
        player_wins(player_chips)
    elif player.value == dealer.value:
        push(player_chips)
    elif player.value < dealer.value and (dealer_busted is not True):
        dealer_wins()

    print(f'You have {player_chips.total} chips left.')

    keep_playing()

    if playing:
        continue
    else:
        break
