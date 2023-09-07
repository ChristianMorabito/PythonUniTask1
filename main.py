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
    elif choice[0] == 5:
        print("You are the winner!!!" if winner["player"] else "You lose! Bot won...\nTry again!")


def create_deck(pick) -> None:
    global deck, suit
    suit = SUITS_1 if pick == 1 else SUITS_2 if pick == 2 else SUITS_3
    deck = [f"{value}{card}" for card in suit for value in VALUES]


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


def pick_card() -> None:
    global turn, game_started
    if not game_started:
        return

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

    if r.randint(0, 4) != 2:  # 20% chance of bot not selecting a card
        bot_card, bot_rand = avoid_mid_card()
        bot_hand.append(bot_card)
        deck.remove(deck[bot_rand])
    turn -= 1


def show_cards() -> str:
    return ''.join(player_hand) if player_hand else "empty."


def suit_value_check(hand) -> int:
    hand_values = {card[:-1]: set() for card in hand}
    count = 0
    for i, value in enumerate(hand_values):
        for j in range(i, len(hand)):
            curr_value, curr_suit = hand[j][:-1], hand[j][-1]
            if value == curr_value:
                hand_values[value].add(curr_suit)
        count = max(count, len(hand_values[value]))
    print(hand_values)
    return count


def score_count(hand):
    card_value = {"A": 1, "J": 11, "Q": 12, "K": 13}
    count = 0
    for card in hand:
        count += int(card[:-1] if card[:-1].isdigit() else card_value[card[:-1]])
    return count / len(hand)


def win_check(player_condition, bot_condition) -> bool:
    if player_condition:
        winner["player"] = True
    if bot_condition:
        winner["bot"] = True
    if winner["player"] or winner["bot"]:
        return True
    return False


def win_pick(condition) -> None:
    if condition:
        winner["player"] = True
    else:
        winner["bot"] = True


def check_result() -> None:
    if not player_hand or not bot_hand:
        win_pick(player_hand)
        return

    if len(player_hand) >= len(suit):
        player_suit_value_count = suit_value_check(player_hand)
        bot_suit_value_count = suit_value_check(bot_hand)

        if win_check(player_suit_value_count == len(suit), bot_suit_value_count == len(suit)) or \
           win_check(player_suit_value_count == len(suit)-1, bot_suit_value_count == len(suit)-1):
            return

    if len(player_hand) > 2:
        player_count = len([item for item in player_hand[2:] if item[-1] == player_hand[1][-1]])
        bot_count = len([item for item in bot_hand[2:] if item[-1] == bot_hand[1][-1]])
        if player_count != bot_count:
            win_pick(player_count > bot_count)
            return

    player_score, bot_score = score_count(player_hand), score_count(bot_hand)
    win_pick(player_score > bot_score)


def reset():
    global suit, deck, mid_card, player_hand, bot_hand, winner, game_started, winner_chosen, turn
    suit.clear()
    deck.clear()
    mid_card = ""
    player_hand.clear()
    bot_hand.clear()
    winner["player"] = False
    winner["bot"] = False
    game_started = False
    winner_chosen = False
    turn = 6




def play_game() -> None:
    global game_started, main_loop, winner_chosen
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
    if turn == 0 or pick[0] == 5:  # TODO: FIX IF PLAYER TYPES 2, what it prints in game_menu()
        check_result()
        winner_chosen = True
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
        if winner_chosen:
            reset()



SUITS_1 = ["♥", "♦", "♣", "♠"]
SUITS_2 = ["😃", "😈", "😵", "🤢", "😨"]
SUITS_3 = ["🤡", "👹", "👺", "👻", "👽", "👾", "🤖"]
VALUES = ["2", "3", "4", "5", "6", "7", "8", "9", "10", "J", "Q", "K", "A"]
suit = []
deck = []
mid_card = ""
player_hand = []
bot_hand = []
winner = {"player": False, "bot": False}
main_loop = True
game_started = False
winner_chosen = False
turn = 6

if __name__ == '__main__':
    main()
