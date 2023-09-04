import random


def game_menu(arg_choice=None) -> None:
    if not arg_choice:
        print("\nWelcome to card game. You have the following options:")
    print("1. start game\n2. pick a card\n3. shuffle deck\n4. show my cards\n5. check win or lose\n6. exit\n")
    if arg_choice and arg_choice[0] == 1:
        if game_loop:
            print("Game ALREADY started!")
        else:
            print(deck)
            print("Game has now begun. Pick card or view cards.")




def create_deck(pick) -> None:
    global deck
    suits = SUITS_1 if pick == 1 else SUITS_2 if pick == 2 else SUITS_3
    deck = [value + suit for suit in suits for value in VALUES]


def shuffle_deck() -> None:
    random.shuffle(deck)


def pick_card() -> None:
    """
    This function takes one argument, deck. It randomly selects one card from the deck and
    returns it. The picked card is then removed from the deck. Both the player and the robot will
    be picking cards from the same deck.
    """
    global player_hand, bot_hand
    if not game_loop:
        return
    player_hand.append(deck.pop(random.randint(0, len(deck))))
    bot_hand.append(deck.pop(random.randint(0, len(deck))))



def show_cards(player_cards) -> None:
    """
    This function takes in one argument, player_cards. Its main purpose is to display all the
    cards that the player holds. There is no return value for this function.
    """
    pass


def check_result(player_cards, robot_cards, suits) -> bool:
    pass


def play_game() -> None:
    global deck, game_loop
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
        if not game_loop:
            create_deck(pick)
        game_menu(pick)
        game_loop = True

    elif pick[0] == 2:
        pass
    elif pick[0] == 3:
        shuffle_deck()




def main():
    game_menu()
    while main_loop:
        play_game()
        # while game_loop:
        #     pass



SUITS_1 = ["♥", "♦", "♣", "♠"]
SUITS_2 = ["😃", "😈", "😵", "🤢", "😨"]
SUITS_3 = ["🤡", "👹", "👺", "👻", "👽", "👾", "🤖"]
VALUES = ["2", "3", "4", "5", "6", "7", "8", "9", "10", "J", "Q", "K", "A"]
deck = []
player_hand = []
bot_hand = []
main_loop = True
game_loop = False

if __name__ == '__main__':
    main()
