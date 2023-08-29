import random


def game_menu() -> None:
    print("\nWelcome to card game. You have the following options:")
    print("1. start game\n2. pick a card\n3. shuffle deck\n4. show my cards\n5. check win or lose\n6. exit\n")


def create_deck(suits_list) -> list[str]:
    return [value + suit for suit in suits_list for value in VALUES]


def shuffle_deck(suits):
    pass


def pick_card(deck) -> tuple:
    """
    This function takes one argument, deck. It randomly selects one card from the deck and
    returns it. The picked card is then removed from the deck. Both the player and the robot will
    be picking cards from the same deck.
    """
    pass


def show_cards(player_cards) -> None:
    """
    This function takes in one argument, player_cards. Its main purpose is to display all the
    cards that the player holds. There is no return value for this function.
    """
    pass


def check_result(player_cards, robot_cards, suits) -> bool:
    pass


def play_game() -> None:
    pass


SUITS_1 = ["♥", "♦", "♣", "♠"]
SUITS_2 = ["😃", "😈", "😵", "🤢", "😨"]
SUITS_3 = ["🤡", "👹", "👺", "👻", "👽", "👾", "🤖"]
VALUES = ["2", "3", "4", "5", "6", "7", "8", "9", "10", "J", "Q", "K", "A"]
deck = create_deck(SUITS_1)

