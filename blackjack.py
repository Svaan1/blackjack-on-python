from random import randint
from time import sleep
from os import system


clear = lambda: system('cls')

def skipline():
    print("\n" + "-" * 40)

class CardDeck:
    def __init__(self):
        self.deck = [["A","2","3","4","5","6","7","8","9","10","J","Q","K"],["A","2","3","4","5","6","7","8","9","10","J","Q","K"],["A","2","3","4","5","6","7","8","9","10","J","Q","K"],["A","2","3","4","5","6","7","8","9","10","J","Q","K"]]
        self.suits = {0: "Clubs", 1: "Diamonds", 2: "Hearts", 3: "Spades"}
    
    def define_default_deck(self):
        self.__init__()

    def draw_random_card(self):
        suit = randint(0,3)
        card = randint(0, (len(self.deck[suit]) - 1) )

        card_drawn = self.deck[suit][card], self.suits[suit]
        
        self.remove_card_with_index(suit,card)

        return card_drawn
    
    def remove_card_with_index(self, suit, value):
        self.deck[suit].pop(value)
    
    def print_deck(self):
        for index in range(0,4):
            suit_name = self.suits[index]
            suit_cards = self.deck[index]
            print(suit_name, suit_cards)

class BlackJack():
    def __init__(self,money=1000):
        self.cards = CardDeck()
        self.dealers_hand = []
        self.players_hand = []
        self.money = money
        self.wager = 0
        clear()
        self.switch()

    def switch(self):
        while True:
            operator = input('''\n
            Do you want to start a new game?\n
            [1] Yes
            [2] No\n
            ''')

            if operator == "2":
                break

            if operator == "1":
                clear()
                self.main()
            
            else:
                print("\nDigite uma opção válida.")
                sleep(1.5)
                clear()                
    def main(self):

        self.restart_cards()

        self.define_wager()
        clear()
        
        self.initial_draw()
        self.print_player_table()

        while True:
            if self.players_decision() == False:
                break
        
        self.print_table()
        sleep(3)

        while True:
            if self.dealers_decision() == False: break
            self.print_table()
            sleep(3)
        
        clear()
        self.print_table()
        print("\nDealer:",self.hand_value(self.dealers_hand))
        print("Player:",self.hand_value(self.players_hand))
        print("\nThe player", self.check_win() + "!")

    def players_decision(self):
        players_value = self.hand_value(self.players_hand)
        if players_value >= 21:
            clear()
            return False

        operator = int(input('''
        [1] Hit
        [2] Double Down
        [3] Stand\n
         '''))

        if operator == 1:
            self.hit_player()
            clear()
            self.print_player_table()
            return True
        elif operator == 2:
            self.double_down()
            clear()
            return False
        elif operator == 3:
            clear()
            return False
        else:
            print("Digite uma opção válida.")
            return True
    def dealers_decision(self):
        players_value = self.hand_value(self.players_hand)
        dealers_value = self.hand_value(self.dealers_hand)
        if dealers_value > 21:
            print("\nDealer Busts!")
            sleep(3)
            clear()
            return False
        if players_value > 21:
            print("\nPlayer Busts!")
            sleep(3)
            clear()
            return False
        if dealers_value == 21:
            print("\nDealer's Blackjack!\n")
            sleep(3)
            clear()
            return False
        if dealers_value > players_value and dealers_value <= 21 or dealers_value >= 17:
            print("\nDealer Stands!\n")
            sleep(3)
            clear()    
            return False   
        if dealers_value <= 16:
            self.hit_dealer()
            print("\nDealer Hits!")
            sleep(3)
            clear()
            return True

    def check_win(self):
        players_value = self.hand_value(self.players_hand)
        dealers_value = self.hand_value(self.dealers_hand)

        if dealers_value > 21:
            self.win()
            return "won"
        if players_value > 21:
            return "lost"

        if players_value == 21:
            if dealers_value == 21:
                return "tied"
            else:
                self.win()
                return "won"

        if players_value == dealers_value:
            return "tied"

        if players_value > dealers_value:
            self.win()
            return "won"
        
        if players_value < dealers_value:
            return "lost"
        self.money += self.wager * 2
    def restart_cards(self):
        self.dealers_hand = []
        self.players_hand = []
        self.cards.define_default_deck()
    def hand_value(self, hand):
        value = 0

        for index in range(0, len(hand)):
            card = hand[index][0]

            if card in "JQK":
                value += 10
                continue
            
            if card == "A":
                if value + 11 > 21:
                    value += 1
                    continue
                else:
                    value += 11
                    continue           
            else:
                value += int(card)
        
        return value
    
    def print_player_table(self):
        skipline()
        self.print_dealers_hand(value=False)
        self.print_players_hand()
        skipline()
    def print_table(self, value= True):
        skipline()
        self.print_dealers_hand()
        self.print_players_hand()
        skipline()

    def print_players_hand(self):
        print("Your hand:    ", end=' ')
        for card in self.players_hand:
            print(card[0],"of",card[1], end=' / ')
        print(f"Value = {self.hand_value(self.players_hand)}")    
    def print_dealers_hand(self, value=True):
        if value:
            print("\nDealers hand:  ", end='')
            for card in self.dealers_hand:
                print(card[0],"of",card[1], end=' / ')
            print(f"Value = {self.hand_value(self.dealers_hand)}")
        else:
            print("\nDealers hand:  ", end='')
            print(self.dealers_hand[0][0], self.dealers_hand[0][1], " / ", "??????? / ")

    def define_wager(self):
        while True:
            try:
                wager_value = float(input(f"\nDigite o valor da aposta (Saldo: {self.money}): "))
                if self.money > wager_value:
                    break
                else:
                    print("Dinheiro insuficiente.")
                    sleep(3)
                    clear()
                    continue
            except:
                continue
        
        if self.money < wager_value:
            return False

        self.wager = wager_value
        self.money -= wager_value
        return True
    def initial_draw(self):
        for i in range(0,2):
            self.hit_player()
            self.hit_dealer()

    def win(self):
        self.money += self.wager * 2
    def double_down(self):
        self.hit_player()
        if self.wager * 2 < self.money: self.wager *= 2        
    def hit_player(self):
        self.players_hand.append(self.cards.draw_random_card())
    def hit_dealer(self):
        self.dealers_hand.append(self.cards.draw_random_card())


