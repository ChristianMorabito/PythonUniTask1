import random as r


def game_menu(arg_choice=None) -> None:
    if not game_started:
        print("\nWelcome to card game. You have the following options:")
    print("1. start game\n2. pick a card\n3. shuffle deck\n4. show my cards\n5. check win or lose\n6. exit\n")
    if arg_choice and arg_choice[0] == 1:
        if game_started:
            print("Game ALREADY started!")
        else:
            print(deck)
            print("Game has now begun. Pick card or view cards.")
    elif arg_choice and arg_choice[0] == 2:
        print(f"You picked {player_hand[-1]}")


def create_deck(pick) -> list[str]:
    global deck
    suits = SUITS_1 if pick == 1 else SUITS_2 if pick == 2 else SUITS_3
    deck = [value + suit for suit in suits for value in VALUES]
    return suits


def shuffle_deck(suit_selection=None) -> None:
    global deck, mid_card
    low, mid, high = 0, (len(deck) - 1) // 2, len(deck) - 1
    if suit_selection:
        suit = SUITS_1 if suit_selection == 1 else SUITS_2 if suit_selection == 2 else SUITS_3
        low_suits, mid_suits, high_suits = 0, (len(suit) - 1) // 2, len(suit) - 1
        a_card = deck.index("A" + suit[low_suits])
        q_card = deck.index("Q" + suit[mid_suits])
        k_card = deck.index("K" + suit[high_suits])
        deck[low], deck[a_card] = deck[a_card], deck[low]
        deck[mid], deck[q_card] = deck[q_card], deck[mid]
        deck[high], deck[k_card] = deck[k_card], deck[high]
        mid_card = (deck[mid])

    shuffled_deck = deck[low+1:high]
    deck.clear()
    deck = shuffled_deck
    deck[mid], deck.index(mid_card) = deck.index(mid_card), deck[mid]



def pick_card() -> None:
    """
    This function takes one argument, deck. It randomly selects one card from the deck and
    returns it. The picked card is then removed from the deck. Both the player and the robot will
    be picking cards from the same deck.
    """
    if not game_started:
        return

    while True:
        player_rand = r.randint(1, len(deck)-2)
        player_card = deck[player_rand]
        if player_card != mid_card[0]:
            break
        print(f"player card was {player_card} hence next loop")

    player_hand.append(player_card)
    deck.remove(deck[player_rand])

    while True:
        bot_rand = r.randint(1, len(deck)-2)
        bot_card = deck[bot_rand]
        if bot_card != mid_card[0]:
            break
        print(f"bot card was {bot_card} hence next loop")

    bot_hand.append(bot_card)
    deck.remove(deck[bot_rand])

    print(deck)

def show_cards(player_cards) -> None:
    """
    This function takes in one argument, player_cards. Its main purpose is to display all the
    cards that the player holds. There is no return value for this function.
    """
    pass


def check_result(player_cards, robot_cards, suits) -> bool:
    pass


def play_game() -> None:
    global game_started
    pick = []
    while True:
        try:
            player_input = input("Please enter your selection: ").strip().split(" ", 1)
            first_input = int(player_input[0])
            if 0 < first_input < 7:
                pick.append(first_input)
                break
            else:
                print("Out of range! Try again...")
        except ValueError:
            print("Invalid input! Try again...")
    if pick[0] == 1:
        second_input = 1
        pick.append(second_input)
        if pick[0] == 1 and len(player_input) > 1:
            try:
                if 1 < int(player_input[1]) < 4:
                    second_input = int(player_input[1])
            except ValueError:
                pass
            finally:
                pick[1] = second_input
        if not game_started:
            create_deck(pick[1])
        game_menu(pick)
        shuffle_deck(pick[1])
        game_started = True

    elif pick[0] == 2:
        pick_card()
        game_menu(pick)
    elif pick[0] == 3:
        shuffle_deck()


def main():
    game_menu()
    while main_loop:
        play_game()


SUITS_1 = ["♥", "♦", "♣", "♠"]
SUITS_2 = ["😃", "😈", "😵", "🤢", "😨"]
SUITS_3 = ["🤡", "👹", "👺", "👻", "👽", "👾", "🤖"]
VALUES = ["2", "3", "4", "5", "6", "7", "8", "9", "10", "J", "Q", "K", "A"]
deck = []
mid_card = ""
player_hand = []
bot_hand = []
main_loop = True
game_started = False

if __name__ == '__main__':
    main()
