# -*- coding: utf-8 -*-
"""
Created on Thu Nov 10 14:05:45 2016

@author: LeviZ
"""

# Mini-project #6 - Blackjack

import simplegui
import random

# load card sprite - 936x384 - source: jfitz.com
CARD_SIZE = (72, 96)
CARD_CENTER = (36, 48)
card_images = simplegui.load_image("http://storage.googleapis.com/codeskulptor-assets/cards_jfitz.png")

CARD_BACK_SIZE = (72, 96)
CARD_BACK_CENTER = (36, 48)
card_back = simplegui.load_image("http://storage.googleapis.com/codeskulptor-assets/card_jfitz_back.png")    

# initialize some useful global variables
in_play = False
deck = []
outcome = ""
score = 0

# define globals for cards
SUITS = ('C', 'S', 'H', 'D')
RANKS = ('A', '2', '3', '4', '5', '6', '7', '8', '9', 'T', 'J', 'Q', 'K')
VALUES = {'A':1, '2':2, '3':3, '4':4, '5':5, '6':6, '7':7, '8':8, '9':9, 'T':10, 'J':10, 'Q':10, 'K':10}


# define card class
class Card:
    def __init__(self, suit, rank):
        if (suit in SUITS) and (rank in RANKS):
            self.suit = suit
            self.rank = rank
        else:
            self.suit = None
            self.rank = None
            print "Invalid card: ", suit, rank

    def __str__(self):
        return self.suit + self.rank

    def get_suit(self):
        return self.suit

    def get_rank(self):
        return self.rank

    def draw(self, canvas, pos):
        card_loc = (CARD_CENTER[0] + CARD_SIZE[0] * RANKS.index(self.rank), 
                    CARD_CENTER[1] + CARD_SIZE[1] * SUITS.index(self.suit))
        canvas.draw_image(card_images, card_loc, CARD_SIZE, [pos[0] + CARD_CENTER[0], pos[1] + CARD_CENTER[1]], CARD_SIZE)
        
# define hand class
class Hand:
    def __init__(self):
        # create Hand object
        self.cards = []

    def __str__(self):
        # return a string representation of a hand
        ans = ""
        for c in range(0, len(self.cards)):
            ans += str(self.cards[c]) + " "
        return "Hand contains " + ans
    def add_card(self, card):
        # add a card object to a hand
        self.cards.append(card)
    def get_value(self):
        # count aces as 1, if the hand has an ace, then add 10 to hand value if it doesn't bust
#        self.get_value(card) = card_value
#        card_value = self.cards[card].rank
        hand_value = 0
        ace = False
        for c in self.cards:
            if c.get_rank() == 'A':
                ace = True
            hand_value += VALUES[c.get_rank()]
            
        if ace and hand_value + 10 <= 21:
            hand_value += 10
        # compute the value of the hand, see Blackjack video
        return hand_value
    def draw(self, canvas, pos):
        # draw a hand on the canvas, use the draw method for cards
        buffer = 75
        for c in self.cards:
            c.draw(canvas, [pos[0] + buffer, pos[1]])
            buffer += CARD_SIZE[0] + 25

     
# define deck class 
class Deck:
    def __init__(self):
        # create a Deck object
        self.deck = []
        for s in SUITS:
            for r in RANKS:
                self.deck.append(Card(s, r))

    def shuffle(self):
        # shuffle the deck 
        random.shuffle(self.deck)

    def deal_card(self):
        # deal a card object from the deck
        return self.deck.pop()
    def __str__(self):
        # return a string representing the deck
        cards_in_deck = ""
        for cid in range(0, len(self.deck)):
            cards_in_deck += str(self.deck[cid]) + " "
        return "Deck contains " + str(cards_in_deck)


#define event handlers for buttons
def deal():
    global outcome, in_play, deck, score, my_hand, dealer_hand, outcome
    # your code goes here
    deck = Deck()                  
    deck.shuffle()   
    outcome = " "
    my_hand = Hand()
    my_hand.add_card(deck.deal_card())
    my_hand.add_card(deck.deal_card())
                      
    dealer_hand = Hand()
    dealer_hand.add_card(deck.deal_card())
    dealer_hand.add_card(deck.deal_card())
    if in_play:
        outcome = " "
        score -= 1
    in_play = True
    if my_hand.get_value() == 21 and len(my_hand.cards) == 2:
        if dealer_hand.get_value() == 21 and len(dealer_hand.cards) == 2:
            in_play = False
            score +=0
            outcome = "Push - Double Blackjack"
        else:
            in_play = False
            score +=1
            outcome = "Blackjack! You Win!"                  
    # tells if the hand is over or not to diplay dealer hole card
        
def hit():
    # replace with your code below
    global my_hand, in_play, outcome, score
    # if the hand is in play, hit the player
    if in_play:
        my_hand.add_card(deck.deal_card())
    # if busted, assign a message to outcome, update in_play and score
        if my_hand.get_value() > 21:
            in_play = False
            score -= 1
            outcome = "You Busted. Dealer Wins"
        if my_hand.get_value() <= 21 and len(my_hand.cards) == 5:
            in_play = False
            score += 1        
            outcome = "5 cards, You Win!"

def stand():
    # replace with your code below
    global dealer_hand, my_hand, score, outcome, in_play
    # if hand is in play, repeatedly hit dealer until his hand has value 17 or more
    if in_play:
        while dealer_hand.get_value() < 17:
            dealer_hand.add_card(deck.deal_card())
        if (len(dealer_hand.cards) == 5) and (dealer_hand.get_value <=21) and (dealer_hand.get_value > my_hand.get_value):
            in_play = False
            score -= 1
            outcome = "Dealer Wins - 5 Cards"
        elif dealer_hand.get_value() > 21:
            in_play = False
            score += 1
            outcome = "Dealer Has Busted. You Win!"
        elif dealer_hand.get_value() < my_hand.get_value():
            outcome = "You Win!"
            score +=1
            in_play = False

        else:
            outcome = "Dealer Wins. You Lose"
            score -= 1
            in_play = False
    
    # assign a message to outcome, update in_play and score

# draw handler    
def draw(canvas):
    # test to make sure that card.draw works, replace with your code below
    global in_play 
    canvas.draw_text("Blackjack", (75, 50), 40, "White")
    canvas.draw_text("Score: " + str(score), (400, 50), 30, "White")
    canvas.draw_text("Dealer", (75, 150), 30, "Black")
    canvas.draw_text("Player", (75, 325), 30, "Black")
    canvas.draw_text(outcome, [225, 150], 30, "White")
    my_hand.draw(canvas,  (0, 350))
    dealer_hand.draw(canvas, (0, 175))
            
    if in_play:
        canvas.draw_text("Hit or Stand?", (250, 325), 30, "White")
        canvas.draw_image(card_back, CARD_BACK_CENTER, CARD_BACK_SIZE, (75 + CARD_SIZE[0]/2, 175+CARD_SIZE[1]/2), 
                          CARD_SIZE)
    else:
        canvas.draw_text("New Deal?", (225, 325), 30, "White")
#        for c in dealer_hand.cards:
#            c.draw(canvas, (75, 175))
#    card = Card("S", "A")
#    card.draw(canvas, [300, 300])


# initialization frame
frame = simplegui.create_frame("Blackjack", 800, 600)
frame.set_canvas_background("Green")

#create buttons and canvas callback
frame.add_button("Deal", deal, 200)
label1 = frame.add_label(" ")
frame.add_button("Hit",  hit, 200)
label1 = frame.add_label(" ")
frame.add_button("Stand", stand, 200)
frame.set_draw_handler(draw)


# get things rolling
deal()
frame.start()


# remember to review the gradic rubric