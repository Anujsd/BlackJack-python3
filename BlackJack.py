import random

playing = True

suits = ["Hearts", "Spades", "Diamonds" ,"Clubs"]
ranks = ["Two" , "Three" ,"Four", "Five", "Six", "Seven", "Eight", "Nine", "Ten", "Jack", "Queen", "King", "Ace"]
values = {"Two": 2 , "Three":3 ,"Four":4, "Five":5, "Six":6, "Seven":7, "Eight":8, "Nine":9, "Ten":10,
         "Jack":10, "Queen":10, "King":10, "Ace":11}

# class for creating card
class Card():
    def __init__(self, suit, rank):
        self.suit = suit
        self.rank = rank

    def __str__(self):
        return self.rank+" of "+self.suit


#class for creating deck, shuffling deck and giving random card
class Deck():
    def __init__(self):
        self.deck = []
        for suit in suits:
            for rank in ranks:
                self.deck.append(Card(suit, rank))
    def __str__(self):
        cards = " "
        for card in self.deck:
            cards +="\n"+card.__str__()
        return "We have deck as follows:" + cards

    def shuffle(self):
        random.shuffle(self.deck)

    def deal(self):
        return self.deck.pop()


# for managing cards of dealer and player
class Hand():
    def __init__(self):
        self.cards = []
        self.value = 0
        self.aces = 0

    def add_card(self, card):
        self.cards.append(card)
        self.value += values[card.rank]
        if card.rank == "Ace":
            self.aces +=1

    def adjust_for_ace(self):
        while self.aces and self.value > 21:
            self.value -= 10
            self.aces -= 1

# for managing chips of player
class Chips():
    def __init__(self):
        self.total = 100
        self.bet = 0
    def win_bet(self):
        self.total += self.bet
    def lose_bet(self):
        self.total -= self.bet

# for takeing bets
def take_bets(chips):
    while True:
        try:
            chips.bet = int(input("Please enter amount of bet : "))
        except ValueError:
            print("Please enter only integers")
        else:
            if chips.bet > chips.total:
                print("sorry your bet can't exceed {}".format(chips.total))
            else:
                break

# for taking one card from deck
def hit(deck, hand):
    hand.add_card(deck.deal())
    hand.adjust_for_ace()

# for asking player hit or stand
def hit_or_stand(deck ,hand):

    global playing
    while True:
        i = input("Please enter 'h' for hit and 's' for stand ")

        if i[0].lower() == 'h':
            hit(deck, hand)

        elif i[0].lower() == 's':
            print("player stands. Dealer is playing")
            playing  = False

        else:
            print("Sorry please Try again ")
            print("Enter only 'h' for hit and 's' for stand ")
            continue
        break

# for showing card's when dealer one card is hidden
def show_some(player, dealer):
    print("\n\nDealer's Hand : ")
    print("<card hidden>")
    print(dealer.cards[1])
    print("\nPlayer's Hand : ", *player.cards, sep="\n")
    print("\n")

# for showing card's when dealer card's are not hidden
def show_all(player, dealer):
    print("\nDealer's Hand : " , *dealer.cards, sep="\n")
    print("     Dealer's Hand = ",dealer.value)
    print("\nPlayer's Hand : " , *player.cards, sep="\n")
    print("     Player's Hand = ",player.value)
    print("\n")

# all conditions occuring in game of winning, losing and tie are managed by
# below functions

def player_bust(chips):
    print("Player Bust")
    chips.lose_bet()

def player_win(chips):
    print("Player win's")
    chips.win_bet()

def dealer_bust(chips):
    print("Dealer Bust")
    chips.win_bet()

def dealer_win(chips):
    print("Dealer Win's")
    chips.lose_bet()

def push():
    print("Dealer and Player tie! It's a push")

while True:
    print("\n\n\nWelcome to blackjack ! \n Get as close to 21 as you can without going over.\n\
 Dealer hits until he reaches 17. Aces count as 1 or 11\n")

    # create deck of cards
    deck = Deck()
    # shuffle cards randomly
    deck.shuffle()

    # add 2 card's to player
    player = Hand()
    player.add_card(deck.deal())
    player.add_card(deck.deal())

    # add 2 card's to dealer
    dealer = Hand()
    dealer.add_card(deck.deal())
    dealer.add_card(deck.deal())

    # set chips for player
    player_chips = Chips()

    # take bet from player
    take_bets(player_chips)

    # show cards keeping one dealer card hidden
    show_some(player, dealer)

    while playing:

        # ask player for his move
        hit_or_stand(deck, player)

        # show cards keeping one dealer card hidden
        show_some(player, dealer)

        # if player has more than 21 value then he bust and loses
        if player.value > 21:
            player_bust(player_chips)
            break

    # we will come here if player is bust or he stand . if he stands dealer will play
    # until he reches 17 . we will remove player bust codition from here
    if player.value <= 21:

        while dealer.value < 17:
            hit(deck, dealer)

        show_all(player , dealer)

        # all other cases

        if dealer.value > 21:
            dealer_bust(player_chips)
        elif dealer.value > player.value:
            dealer_win(player_chips)
        elif dealer.value < player.value:
            player_win(player_chips)
        else:
            push()

    print("Player has Total chips : ", player_chips.total)

    i = input("Do you want to play game again 'y' for Yes and 'n' for NO ")

    if i[0].lower() == 'y':
        playing = True
        continue
    else:
        print("Thank you for playing")
        break
