import random as r


def invalid_game_state(choice) -> bool:
    if choice == 1 and game_started:
        print("Game ALREADY started!")
    elif 1 < choice < 6 and not game_started:
        print("Game has NOT started")
    else:
        return False
    return True


def game_menu(choice=None) -> None:
    # TODO: DON'T LET THE GAME_MENU FUNCTION
    if choice and choice[0] == 6:
        print("Exiting...")
        return
    print("\nWelcome to card game. You have the following options\n"
          "1. start game\n2. pick a card\n3. shuffle deck\n4. show my cards\n5. check win or lose\n6. exit\n")
    if not choice or invalid_game_state(choice[0]):
        return
    if choice[0] == 1:  # TODO: PRINT OUT DIFFERENT CARD OPTIONS TO BEGIN THE GAME WITH
        print(deck)
        print("Game has now begun. Pick card or view cards.")
    elif choice[0] == 2:
        print(f"You picked {player_hand[-1]}")
        if turn == 1:
            print("You have 1 last turn!!")
    elif choice[0] == 3:
        print("Cards shuffled")
    elif choice[0] == 4:
        print(f"Your current hand is {show_cards()}")


def create_deck(pick) -> None:
    global deck, suit
    suit = SUITS_1 if pick == 1 else SUITS_2 if pick == 2 else SUITS_3
    deck = [f"{value} of {card}" for card in suit for value in VALUES]


def shuffle_deck() -> None:
    global deck, mid_card
    low, mid, high = 0, (len(deck) - 1) // 2, len(deck) - 1
    if suit and not game_started:
        low_suits, mid_suits, high_suits = 0, (len(suit) - 1) // 2, len(suit) - 1
        a_card = deck.index("A" + suit[low_suits])
        q_card = deck.index("Q" + suit[mid_suits])
        k_card = deck.index("K" + suit[high_suits])
        deck[low], deck[a_card] = deck[a_card], deck[low]
        deck[mid], deck[q_card] = deck[q_card], deck[mid]
        deck[high], deck[k_card] = deck[k_card], deck[high]
        mid_card = deck[mid]

    if game_started:
        new_deck = deck[low+1:high]
        r.shuffle(new_deck)
        new_deck = [deck[low]] + new_deck + [deck[high]]
        deck.clear()
        deck = new_deck
        q_card = deck.index(mid_card)
        deck[q_card], deck[mid] = deck[mid], deck[q_card]


def pick_card() -> None:
    global turn, game_started
    if not game_started:
        return

    def avoid_mid_card():
        while True:
            random_int = r.randint(1, len(deck)-2)
            card = deck[random_int]
            if card != mid_card:
                break
        return card, random_int

    player_card, player_rand = avoid_mid_card()
    player_hand.append(player_card)
    deck.remove(deck[player_rand])

    if r.randint(0, 4) != 2:  # 20% chance of bot not selecting a card
        bot_card, bot_rand = avoid_mid_card()
        bot_hand.append(bot_card)
        deck.remove(deck[bot_rand])
    turn -= 1
    if turn == 0:
        game_started = False


def show_cards() -> str:
    return ' '.join(player_hand) if player_hand else "empty."


def same_value_check(cards_list) -> bool:
    if len(cards_list) < len(suit):
        return False
    card_set = set()
    for card in cards_list:



def check_result() -> None:
    if same_value_check(player_hand):
        winner["player"] = True
    if same_value_check(bot_hand):
        winner["bot"] = True




def play_game() -> None:
    global game_started, main_loop
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

    elif pick[0] == 2:
        pick_card()
    elif pick[0] == 3:
        shuffle_deck()
    elif pick[0] == 5:
        check_result()
    elif pick[0] == 6:
        main_loop = False

    game_menu(pick)
    if not game_started and pick[0] == 1:
        shuffle_deck()
        game_started = True


def main():
    game_menu()
    while main_loop:
        play_game()


SUITS_1 = ["♥", "♦", "♣", "♠"]
SUITS_2 = ["😃", "😈", "😵", "🤢", "😨"]
SUITS_3 = ["🤡", "👹", "👺", "👻", "👽", "👾", "🤖"]
VALUES = ["2", "3", "4", "5", "6", "7", "8", "9", "10", "J", "Q", "K", "A"]
suit = []
deck = []
mid_card = ""
player_hand = []
winner = {"player": False, "bot": False}
bot_hand = []
main_loop = True
game_started = False
turn = 6

if __name__ == '__main__':
    main()
