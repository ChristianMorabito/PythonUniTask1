import random as r

# TODO: IF HAND IS EMPTY THEN HAVE IT NOT PRINT BOTH PLAYER AND BOTS CARDS
# TODO: MAKE IT SO THAT SYMBOLS OPTION IS SHOWN AT BEGINNING OF NEW GAME


def game_state_check(choice) -> bool:
    main_option = ("Welcome to card game. You have the following options\n"
                   "1. start game (+ OPTIONS ALLOWED)\n"
                   "2. pick a card\n"
                   "3. shuffle deck\n"
                   "4. show my cards\n"
                   "5. check win or lose\n"
                   "6. exit\n")


    suit_option = ("OPTIONS: select between 3 different suit types\n"
                   "Type: 1 1 for default:     ♥ ♦ ♣ ♠\n"
                   "      1 2 for expressions: 😃 😈 😵 🤢 😨\n"
                   "      1 3 for wacky:       🤡 👹 👺 👻 👽 👾 🤖\n")
    if not choice:
        print("\n" + main_option)
        print(suit_option)
    elif choice == 1 and game_started:
        print("\n_________________Game ALREADY started!_________________\n")
        print(main_option)
    elif 1 < choice < 6 and not game_started:
        print("\n___________________Game NOT started!___________________\n")
        print(main_option)
        print(suit_option)
    else:
        print("\n_______________________________________________________\n")
        print(main_option)


def deck_print() -> str:
    deck_string = "\nYou selected the " + ("'default'" if suits == SUITS_1 else
                                           "'expressions'" if suits == SUITS_2 else
                                           "'wacky'") + " deck.\n\n"
    for i, card in enumerate(deck):
        if i == 0 or i % len(VALUES) != len(VALUES) - 1:
            deck_string += card + "  \t"
        else:
            deck_string += card + "\n"
    return deck_string + "\nThe deck has now been shuffled. Game has begun!!"


def game_menu(choice=None) -> None:
    if choice:
        if choice[0] == 6:
            print("Exiting...")
            return
        elif choice[0] == 1 and not game_started:
            print(deck_print())
    if game_started:
        if choice[0] == 2:
            print("\nCard Selected:\tYou picked " + picked_card +
                  ("\nYou have 1 last turn!" if turn == 1 else ""))
        elif choice[0] == 3:
            print("\nCards sHuFfLeD")
        elif choice[0] == 4:
            print("\nYour current hand is ", end="")
            show_cards(player_hand)
        elif choice[0] == 5:
            print("\n" + ("You are the winner!!!" if winner["player"] else "You lose! Bot won...") +
                  "\nThis is because " + win_string)
            print(f"Your hand was:\t", end="")
            show_cards(player_hand)
            print(f"Bot's hand was:\t", end="")
            show_cards(bot_hand)
            input("\nPress ENTER")

    game_state_check(None if not choice else choice[0])



def create_deck(deck, suits, values) -> None:
    deck.extend([f"{value}{card}" for card in suits for value in values])


def shuffle_deck(deck, suits) -> None:
    global mid_card
    low, mid, high = 0, (len(deck) - 1) // 2, len(deck) - 1
    if suits and not game_started:
        low_suits, mid_suits, high_suits = 0, (len(suits) - 1) // 2, len(suits) - 1
        a_card = deck.index("A" + suits[low_suits])
        q_card = deck.index("Q" + suits[mid_suits])
        k_card = deck.index("K" + suits[high_suits])
        deck[low], deck[a_card] = deck[a_card], deck[low]
        deck[mid], deck[q_card] = deck[q_card], deck[mid]
        deck[high], deck[k_card] = deck[k_card], deck[high]
        mid_card = deck[mid]

    if game_started:
        new_deck = deck[low + 1:high]
        r.shuffle(new_deck)
        new_deck = [deck[low]] + new_deck + [deck[high]]
        deck.clear()
        deck.extend(new_deck)
        q_card = deck.index(mid_card)
        deck[q_card], deck[mid] = deck[mid], deck[q_card]


def pick_card(deck) -> str:
    global turn, game_started
    if not game_started:
        return ""

    def avoid_mid_card():
        while True:
            random_int = r.randint(1, len(deck) - 2)
            card = deck[random_int]
            if card != mid_card:
                break
        return card, random_int

    player_card, player_rand = avoid_mid_card()
    player_hand.append(player_card)
    popped_card = deck.pop(player_rand)

    if r.randint(0, 4) != 2:  # 20% chance of bot not selecting a card
        bot_card, bot_rand = avoid_mid_card()
        bot_hand.append(bot_card)
        deck.pop(bot_rand)
    turn -= 1

    return popped_card


def show_cards(player_cards) -> str:
    print(" ".join(player_cards) if player_cards else "empty.")


def suit_value_check(hand) -> int:
    hand_values = {card[:-1]: set() for card in hand}
    count = 0
    for i, value in enumerate(hand_values):
        for j in range(i, len(hand)):
            curr_value, curr_suit = hand[j][:-1], hand[j][-1]
            if value == curr_value:
                hand_values[value].add(curr_suit)
        count = max(count, len(hand_values[value]))
    return count


def score_count(hand):
    card_value = {"A": 1, "J": 11, "Q": 12, "K": 13}
    count = 0
    for card in hand:
        count += int(card[:-1] if card[:-1].isdigit() else card_value[card[:-1]])
    return count / len(hand)


def winner_check(condition, player) -> bool:
    winner[player] = condition
    return condition


def win_reason(reason):
    global win_string

    if not reason:
        win_string += "you had an empty hand." if winner["bot"] else "bot had an empty hand."

    else:
        win_string += ("you " if winner["player"] else "bot ") + reason



def check_result() -> None:
    if winner_check(not player_hand, "bot") or winner_check(not bot_hand, "player"):
        return win_reason(None)

    if len(player_hand) >= len(suits):
        player_suit_value_count = suit_value_check(player_hand)
        bot_suit_value_count = suit_value_check(bot_hand)

        if winner_check(player_suit_value_count == len(suits), "player") or \
           winner_check(bot_suit_value_count == len(suits), "bot"):
            return win_reason("held the same value card for all defined suits.")

        if winner_check(player_suit_value_count == len(suits)-1, "player") or \
           winner_check(bot_suit_value_count == len(suits)-1, "bot"):
            return win_reason(f"held the same value card for {len(suits)-1} consecutive suits.")

    if len(player_hand) > 2:
        player_suit_count = len([item for item in player_hand[2:] if item[-1] == player_hand[1][-1]])
        bot_suit_count = len([item for item in bot_hand[2:] if item[-1] == bot_hand[1][-1]])
        if player_suit_count != bot_suit_count:
            winner_check(player_suit_count > bot_suit_count, "player") if True else winner_check(True, "bot")
            return win_reason("held more cards from the suit in position 2.")

    player_score, bot_score = score_count(player_hand), score_count(bot_hand)
    winner_check(player_score >= bot_score, "player") if True else winner_check(True, "bot")
    return win_reason("held a higher average of the card values.")


def reset():
    global suits, deck, mid_card, player_hand, bot_hand, winner, \
           game_started, winner_chosen, turn, win_string, picked_card
    suits.clear()
    deck.clear()
    mid_card = ""
    player_hand.clear()
    bot_hand.clear()
    winner["player"] = False
    winner["bot"] = False
    game_started = False
    winner_chosen = False
    turn = 6
    win_string = ""
    picked_card = ""


def play_game() -> None:
    global game_started, main_loop, winner_chosen, picked_card
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
            suits.extend(SUITS_1 if pick[1] == 1 else SUITS_2 if pick[1] == 2 else SUITS_3)
            create_deck(deck, suits, VALUES)

    elif pick[0] == 2:
        picked_card = pick_card(deck)
    elif pick[0] == 3:
        shuffle_deck(deck, suits)
    if turn == 0 or pick[0] == 5:
        check_result()
        winner_chosen = True
    elif pick[0] == 6:
        main_loop = False

    game_menu([5] if turn == 0 else pick)
    if not game_started and pick[0] == 1:
        shuffle_deck(deck, suits)
        game_started = True


def main():
    game_menu()
    while main_loop:
        play_game()
        if winner_chosen:
            reset()



SUITS_1 = ["♥", "♦", "♣", "♠"]
SUITS_2 = ["😃", "😈", "😵", "🤢", "😨"]
SUITS_3 = ["🤡", "👹", "👺", "👻", "👽", "👾", "🤖"]
VALUES = ["2", "3", "4", "5", "6", "7", "8", "9", "10", "J", "Q", "K", "A"]
suits = []
deck = []
mid_card = ""
picked_card = ""
player_hand = []
bot_hand = []
win_string = ""
winner = {"player": False, "bot": False}
main_loop = True
game_started = False
winner_chosen = False
turn = 6


if __name__ == '__main__':
    main()
