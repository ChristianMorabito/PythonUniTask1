import random as r

# TODO: see if you can minimise global variables used


def game_state_check(choice) -> bool:
    main_option = ("Welcome to card game. You have the following options\n" +
                   "1. start game (+ OPTIONS ALLOWED)\n" +
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
        return False
    return True


def deck_string() -> str:
    string = "\nYou selected the " + ("'default'" if suit == SUITS_1 else
                                      "'expressions'" if suit == SUITS_2 else
                                      "'wacky'") + " deck.\n\n"
    for i, card in enumerate(deck):
        if i == 0 or i % len(VALUES) != len(VALUES) - 1:
            string += card + "  \t"
        else:
            string += card + "\n"
    return string + "\nThe deck has now been shuffled. Game has begun!!"


def print_winner() -> None:
    print("\n" + ("You are the winner!!!" if winner["player"] else "You lose! Bot won...") +
          "\nThis is because " + win_string)


def game_menu(turn_count, choice=None) -> None:
    if choice:
        if choice[0] == 6:
            print("Exiting...")
            return
        elif choice[0] == 1 and not game_started:
            print(deck_string())
    if game_started:
        if choice[0] == 2:
            print("\nCard Selected:\tYou picked " + player_hand[-1] +
                  ("\nYou have 1 last turn!" if turn_count + 1 == TURN else ""))
        elif choice[0] == 3:
            print("\nCards sHuFfLeD")
        elif choice[0] == 4:
            print("\nYour current hand is " + show_cards(player_hand))
        elif choice[0] == 5:
            print_winner()

    if game_state_check(None if not choice else choice[0]):
        return


def create_deck(pick) -> None:
    global deck, suit
    suit.extend(SUITS_1 if pick == 1 else SUITS_2 if pick == 2 else SUITS_3)
    deck.extend([f"{value}{card}" for card in suit for value in VALUES])


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
        new_deck = deck[low + 1:high]
        r.shuffle(new_deck)
        new_deck = [deck[low]] + new_deck + [deck[high]]
        deck.clear()
        deck = new_deck
        q_card = deck.index(mid_card)
        deck[q_card], deck[mid] = deck[mid], deck[q_card]


def pick_card() -> int:
    global game_started
    if not game_started:
        return 0

    def avoid_mid_card():
        while True:
            random_int = r.randint(1, len(deck) - 2)
            card = deck[random_int]
            if card != mid_card:
                break
        return card, random_int

    player_card, player_rand = avoid_mid_card()
    player_hand.append(player_card)
    deck.remove(deck[player_rand])

    if r.randint(0, 9) != 5:  # 10% chance of bot not selecting a card
        bot_card, bot_rand = avoid_mid_card()
        bot_hand.append(bot_card)
        deck.remove(deck[bot_rand])
    return 1


def show_cards(hand) -> str:
    return " ".join(hand) if hand else "empty."


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
        win_string += ("you " if winner["player"] else "bot ") + reason + \
            f"\nYour hand was:\t {show_cards(player_hand)}\nBot's hand was:\t {show_cards(bot_hand)}"
    return TURN


def check_result() -> int:
    # Check if player hand or bot hand is empty
    if winner_check(not player_hand, "bot") or winner_check(not bot_hand, "player"):
        return win_reason(None)

    # Check if player/bot holds the same value card for all defined suits, or all defined suits - 1
    if len(player_hand) >= len(suit):
        player_suit_value_count = suit_value_check(player_hand)
        bot_suit_value_count = suit_value_check(bot_hand)

        if winner_check(player_suit_value_count == len(suit), "player") or \
           winner_check(bot_suit_value_count == len(suit), "bot"):
            return win_reason("held the same value card for all defined suits.")

        if winner_check(player_suit_value_count == len(suit)-1, "player") or \
           winner_check(bot_suit_value_count == len(suit)-1, "bot"):
            return win_reason(f"held the same value card for {len(suit)-1} consecutive suits.")

    # Check if player/bot holds more cards from the suit in position 2
    if len(player_hand) > 2:
        player_suit_count = len([item for item in player_hand[2:] if item[-1] == player_hand[1][-1]])
        bot_suit_count = len([item for item in bot_hand[2:] if item[-1] == bot_hand[1][-1]])
        if player_suit_count != bot_suit_count:
            winner_check(player_suit_count > bot_suit_count, "player") if True else winner_check(True, "bot")
            return win_reason("held more cards from the suit in position 2.")

    # Check if player/bot holds a higher average of the card’s value.
    player_score, bot_score = score_count(player_hand), score_count(bot_hand)
    winner_check(player_score >= bot_score, "player") if True else winner_check(True, "bot")
    return win_reason("had a higher score.\n"
                      f"Your score was {round(player_score, 2)}, & bot's score was {round(bot_score, 2)}.\n")


def reset() -> int:
    global suit, deck, mid_card, player_hand, bot_hand, winner, game_started, win_string
    suit.clear()
    deck.clear()
    mid_card = ""
    player_hand.clear()
    bot_hand.clear()
    winner["player"] = False
    winner["bot"] = False
    game_started = False
    win_string = ""
    return 0


def play_game(turn_count) -> int:
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
        turn_count += pick_card()
    elif pick[0] == 3:
        shuffle_deck()
    if turn_count == TURN or pick[0] == 5:
        turn_count = check_result()

    elif pick[0] == 6:
        main_loop = False

    game_menu(turn_count, [5] if turn_count == TURN else pick)
    if not game_started and pick[0] == 1:
        shuffle_deck()
        game_started = True
    return turn_count


def main():
    turn_count = 0
    game_menu(turn_count)
    while main_loop:
        print(turn_count)
        turn_count = play_game(turn_count)
        if turn_count == TURN:
            turn_count = reset()


SUITS_1 = ["♥", "♦", "♣", "♠"]
SUITS_2 = ["😃", "😈", "😵", "🤢", "😨"]
SUITS_3 = ["🤡", "👹", "👺", "👻", "👽", "👾", "🤖"]
VALUES = ["2", "3", "4", "5", "6", "7", "8", "9", "10", "J", "Q", "K", "A"]
TURN = 6
suit = []
deck = []
mid_card = ""
player_hand = []
bot_hand = []
win_string = ""
winner = {"player": False, "bot": False}
main_loop = True
game_started = False

if __name__ == '__main__':
    main()
