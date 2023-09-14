import random as r

# TODO: MAKE IT SO THAT SYMBOLS OPTION IS SHOWN AT BEGINNING OF NEW GAME
# TODO: HAVE HAPPY/SAD EMOJI AT END WITH WIN/LOSS MSG
# TODO: PUT BORDER / EMOJIS AROUND OUTPUT BEFORE THE MENU TO DRAW ATTN THERE


def game_state_check(choice_arg) -> None:
    main_option = ("Welcome to card game. You have the following options\n"
                   "1. start game (+ OPTIONS ALLOWED)\n"
                   "2. pick a card\n"
                   "3. shuffle deck\n"
                   "4. show my cards\n"
                   "5. check win/lose\n"
                   "6. exit\n")


    suit_option = ("OPTIONS: select between 3 different suit types\n"
                   "Type: 1 1 for default:     ♥ ♦ ♣ ♠\n"
                   "      1 2 for expressions: 😃 😈 😵 🤢 😨\n"
                   "      1 3 for wacky:       🤡 👹 👺 👻 👽 👾 🤖\n")

    game_running = "\n_____________🟢Game Currently Running🟢____________\n"
    game_already_started = "\n_____________🚨Game ALREADY started!🚨______________\n"
    game_not_started = "\n_______________🚨Game NOT started!🚨________________\n"
    line = "\n___________________________________________________________\n"
    if not choice_arg:
        print(line + main_option)
        print(suit_option)
    elif choice_arg == 1 and game_started:
        print(game_already_started + main_option)
    elif 1 < choice_arg < 6 and not game_started:
        print(game_not_started + main_option + suit_option)
    else:
        print(game_running + main_option)


def deck_print() -> str:
    deck_string = "\nYou selected the " + ("'default'" if suits == SUITS_1 else
                                           "'expressions'" if suits == SUITS_2 else
                                           "'wacky'") + " deck.\n\n"
    for i, card in enumerate(deck):
        deck_string += (card + "  \t") if i == 0 or i % len(VALUES) != len(VALUES) - 1 else (card + "\n")

    return deck_string + ("\nThe deck has now been shuffled. Game has begun!!\n"
                          "You may pick a card up to 6 times, "
                          "or 'check win/lose' to end the game earlier.")


def game_menu() -> None:
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
            print("\n~^~Cards sHuFfLeD~^~")
        elif choice[0] == 4:
            print("\nYour current hand is ", end="")
            show_cards(player_hand)
        elif choice[0] == 5:
            print(win_string)
            if player_hand and bot_hand:
                print(f"➕ PLAYER hand:\t", end="")
            show_cards(player_hand)
            print(f"➕ BOT hand:\t", end="")
            show_cards(bot_hand)

        if choice[0] != 1:
            input("\nPress ENTER\t")

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


def show_cards(player_cards) -> None:
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

    win_string += ("\n" + ("😊 You are the winner!!! 😊" if winner["player"] else "☹️ You lose! Bot won... ☹️") +
                   "\nBecause ")

    if not reason:
        win_string += "you had an empty hand." if winner["bot"] else "bot had an empty hand."
    else:
        win_string += ("you " if winner["player"] else "bot ") + reason


def check_result(player_cards, robot_cards, suits) -> bool:

    def sequence():
        if winner_check(not player_cards, "bot") or winner_check(not robot_cards, "player"):
            return win_reason(None)

        if len(player_cards) >= len(suits):
            player_suit_value_count = suit_value_check(player_cards)
            bot_suit_value_count = suit_value_check(robot_cards)

            if (winner_check(player_suit_value_count == len(suits), "player") or
                    winner_check(bot_suit_value_count == len(suits), "bot")):
                return win_reason("held the same value card for all defined suits.")


            if (winner_check(player_suit_value_count == len(suits)-1, "player") or
                    winner_check(bot_suit_value_count == len(suits)-1, "bot")):
                return win_reason(f"held the same value card for {len(suits)-1} consecutive suits.")


        if len(player_cards) > 2:
            player_suit_count = len([item for item in player_cards[2:] if item[-1] == player_cards[1][-1]])
            bot_suit_count = len([item for item in robot_cards[2:] if item[-1] == robot_cards[1][-1]])
            if player_suit_count != bot_suit_count:
                (winner_check(player_suit_count > bot_suit_count, "player") if True else
                 winner_check(True, "bot"))
                return win_reason("held more cards from the suit in position 2.")

        player_score, bot_score = score_count(player_cards), score_count(robot_cards)
        winner_check(player_score >= bot_score, "player") if True else winner_check(True, "bot")
        reason = ""
        if player_score != bot_score:
            higher_score, lower_score = max(player_score, bot_score), min(player_score, bot_score)
            reason += (f"held a higher score of {round(higher_score, 2)},\n"
                       f"whilst " + ("you " if player_score < bot_score else "bot ") +
                       f"held a lower score of {round(lower_score, 2)}.")
        else:
            reason += ('drew with the bot,\nso you are "technically" still the "winner".\n'
                       f'You both scored {round(player_score, 2)}.')
        win_reason(reason)

    sequence()
    return winner["player"]


def reset():
    global suits, deck, mid_card, player_hand, bot_hand, winner, \
           game_started, turn, win_string, picked_card, choice
    suits.clear()
    deck.clear()
    mid_card = ""
    player_hand.clear()
    bot_hand.clear()
    winner["player"] = False
    winner["bot"] = False
    game_started = False
    turn = 6
    win_string = ""
    picked_card = ""



def play_game() -> None:
    global turn, game_started, main_loop, picked_card, choice
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
    elif pick[0] == 6:
        main_loop = False

    if turn == 0 or pick[0] == 5:
        check_result(player_hand, bot_hand, suits)
        turn = 0  # force turn variable to 0 to end game.
    choice = [5] if turn == 0 else pick
    game_menu()
    if not game_started and pick[0] == 1:
        shuffle_deck(deck, suits)
        game_started = True


def main():
    game_menu()
    while main_loop:
        play_game()
        if turn == 0:
            reset()


SUITS_1 = ["♥", "♦", "♣", "♠"]
SUITS_2 = ["😃", "😈", "😵", "🤢", "😨"]
SUITS_3 = ["🤡", "👹", "👺", "👻", "👽", "👾", "🤖"]
VALUES = ["2", "3", "4", "5", "6", "7", "8", "9", "10", "J", "Q", "K", "A"]
suits = []
deck = []
player_hand = []
bot_hand = []
choice = []
mid_card = ""
picked_card = ""
win_string = ""
winner = {"player": False, "bot": False}
main_loop = True
game_started = False
turn = 6


if __name__ == '__main__':
    main()
