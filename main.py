"""
Name:          Christian Morabito
Student ID:    22298827
Last modified: 18/09/23

This program is a simple card where the user has to select a winning
combination of cards against the computer. This program was created
as a student assessment at Monash University, ITO4133: Intro. to Python
"""


import random as r

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


def game_state_string(choice_arg) -> str:
    """
    Func to return a string of: title, suit options & game msgs, based on input & game state.
    :param choice_arg: accepts int that represents the choice input from game_menu() function
    :return returns string to print
    """

    title = """
    ▒█▀▀█ ░█▀▀█ ▒█▀▀█ ▒█▀▀▄ 　 ▒█▀▀█ ░█▀▀█ ▒█▀▄▀█ ▒█▀▀▀ 
    ▒█░░░ ▒█▄▄█ ▒█▄▄▀ ▒█░▒█ 　 ▒█░▄▄ ▒█▄▄█ ▒█▒█▒█ ▒█▀▀▀ 
    ▒█▄▄█ ▒█░▒█ ▒█░▒█ ▒█▄▄▀ 　 ▒█▄▄█ ▒█░▒█ ▒█░░▒█ ▒█▄▄▄
                      ...verse against the computer...\n"""
    # reference: https://fsymbols.com/generators/carty/

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
    line = "___________________________________________________________\n"

    if choice_arg == 1 and game_started:  # if player presses '1' to start game when game has already started
        return game_already_started + main_option
    elif not choice_arg or turn == 0:  # if game hasn't started, so title & suit options are presented
        return line + title + line + main_option + "\n" + suit_option
    elif 1 < choice_arg < 6 and not game_started:  # if player is attempting to make a choice when game hasn't started
        return game_not_started + main_option + suit_option
    else:
        return game_running + main_option  # if player makes valid choice whilst game is running


def deck_string() -> str:
    """
    Function return a string which elegantly presents the deck.
    :return returns string to print
    """

    text_and_deck = ""

    for i, card in enumerate(deck):  # loop to elegantly present the deck of cards.
        text_and_deck += (card + "  \t") if i == 0 or i % len(VALUES) != len(VALUES) - 1 else (card + "\n")

    return text_and_deck


def game_menu() -> None:
    """ Func to print the game menu & all other game based notifications, depending on input & game state """

    if choice:  # if choice[] is not empty
        if choice[0] == 6:  # if true, then exit game & end function
            print("Exiting...")
            return
        elif choice[0] == 1 and not game_started:  # if game hasn't started & player presses 1 to start the game,
            print("\n_______________🟢GAME HAS NOW BEGUN🟢______________")
            print("\nYou selected the " + ("'default'" if suits == SUITS_1 else
                                           "'expressions'" if suits == SUITS_2 else
                                           "'wacky'") + " deck.\n")
            print(deck_string())  # then print deck
            print("The deck has now been shuffled. Game has begun!!\nYou may pick a card up to 6 times, "
                  "or 'check win/lose' to end the game earlier.")

    if game_started:
        if 1 < choice[0] < 5:
            print("\n_____________🟢Game Currently Running🟢____________")
        if choice[0] == 2:  # card picked from deck
            print("\nCard Selected:\tYou picked " + picked_card)
        elif choice[0] == 3:  # deck shuffled
            print("\n" + deck_string())
            print("\n~^~Cards sHuFfLeD~^~", end="")
        elif choice[0] == 4:  # print player's hand of cards
            print("\nYour current hand is ", end="")
            show_cards(player_hand)
        elif choice[0] == 5:  # game has ended, win/loss is checked
            print("\n___________________🔵GAME OVER🔵__________________")
            print(win_string)  # print the string of info declaring the winner, reason & score
            if player_hand and bot_hand:  # only print player's & bot's cards, if neither were empty
                print(f"🔷 PLAYER hand:\t", end="")
                show_cards(player_hand)
                print(f"🔷 BOT hand:\t", end="")
                show_cards(bot_hand)

        if 1 < choice[0] < 5:  # only show turn count if input is between 2 & 4 (inclusive)
            print("\n♥ " + (f"You have {turn} turns left" if turn > 1 else "You have 1 last turn!") + " ♥")

    if choice:
        if game_started and choice[0] > 1 or (not game_started and choice[0] == 1):
            input("\nPress ENTER ⏎ \n")  # prevent 'next turn' screen from printing

    # print title, suit options &/or game state msgs pertaining to the next turn
    print(game_state_string(None if not choice else choice[0]))


def create_deck(deck, suits, values) -> None:
    """
    Func to create deck[] based on suits[] selected & values.
    Note: deck, suits & values are references to global variables
    :param deck: empty list to hold the deck of cards
    :param suits: list of suits that player chose
    :param values: list of default values to merge with suits
    """

    deck.extend([f"{value}{card}" for card in suits for value in values])


def shuffle_deck(deck, suits) -> None:
    """
    Func to place 'A_1st_suit, Q_mid_suit, & K_last_suit in the
    1st, mid & last positions of the deck. Once done, then all cards
    but those 3 are shuffled.
    :param deck: accepts deck list (str)
    :param suits: accepts suits list (str)
    """

    global mid_card
    low, mid, high = 0, (len(deck) + 1) // 2, len(deck) - 1  # establish L/M/H points in the deck
    if suits and not game_started:  # this condition is only true once deck is 1st created
        low_suits, mid_suits, high_suits = 0, (len(suits) - 1) // 2, len(suits) - 1  # establish L/M/H points in suits
        a_card = deck.index("A" + suits[low_suits])  # declare variables to hold these 3 cards
        q_card = deck.index("Q" + suits[mid_suits])
        k_card = deck.index("K" + suits[high_suits])
        deck[low], deck[a_card] = deck[a_card], deck[low]  # place the 3 cards in appropriate positions within the deck
        deck[mid], deck[q_card] = deck[q_card], deck[mid]
        deck[high], deck[k_card] = deck[k_card], deck[high]
        mid_card = deck[mid]  # establish mid_card to make sure it's avoided when pick_card() function is called

    if game_started:  # this condition is only true when player has started the game & wants to manually shuffle
        temp_deck = deck[low + 1:high]  # create temp deck which is a copy of deck, but avoiding 1st & last cards
        r.shuffle(temp_deck)  # shuffle the temp deck
        temp_deck = [deck[low]] + temp_deck + [deck[high]]  # place the 1st & last cards from deck into temp deck
        deck.clear()  # erase contents of deck
        deck.extend(temp_deck)  # fill deck with temp deck contents
        q_card = deck.index(mid_card)  # find the new index of the original middle card
        deck[q_card], deck[mid] = deck[mid], deck[q_card]  # swap it back into the middle


def pick_card(deck) -> str:
    """
    Func to remove card from the deck & return it
    :param deck: accepts deck list
    :return: returns string of removed card
    """

    global turn, game_started
    if not game_started:
        return ""

    def avoid_mid_card():
        """This function ensures that the middle card is not collected"""

        while True:
            # random_int is an index from 2nd card to 2nd last card (inc.)
            # this is to avoid the special 1st & last cards
            random_int = r.randint(1, len(deck) - 2)
            card = deck[random_int]
            if card != mid_card:  # loop is only exited if selected card is not the special middle card.
                break
        return card, random_int

    player_card, player_rand = avoid_mid_card()  # call function & receive outputted card string & card index
    player_hand.append(player_card)  # use card string to add to player cards
    popped_card = deck.pop(player_rand)  # remove card from deck

    if r.randint(0, 4) != 2:  # 20% chance of bot not selecting a card
        bot_card, bot_rand = avoid_mid_card()
        bot_hand.append(bot_card)
        deck.pop(bot_rand)
    turn -= 1

    return popped_card


def show_cards(player_cards) -> None:
    """
    Func to print the list 'player_cards' as a formatted string
    @param player_cards: accepts list of player cards
    """

    # prints cards as a string, 1 space between each card. If list is empty, then prints 'empty'.
    print(" ".join(player_cards) if player_cards else "empty.")


def suit_value_check(hand) -> int:
    """
    Func to count the no. of times a player holds
    the same value card for all the defined suits
    @param hand: accepts a list of cards (str) to check
    @return: returns a count as an int
    """

    # 1) dict. comprehension below creates a dictionary that holds each card value & and pairs it with set()
    # e.g. hand = ['A♥', '5♦', '8♣', '10♠']; hand_values = {'A': set(), '5': set(), '8': set(), '10': set()}
    hand_values = {card[:-1]: set() for card in hand}
    count = 0
    for i, value in enumerate(hand_values):
        for j in range(i, len(hand)):
            curr_value, curr_suit = hand[j][:-1], hand[j][-1]  # eg. in ['A♥'], curr_value == 'A'; curr_suit == '♥'
            if value == curr_value:
                # add the curr_suit into the set() of the dict. key -> curr_value
                hand_values[value].add(curr_suit)
        # record if this is the largest count thus far.
        count = max(count, len(hand_values[value]))
    return count


def score_count(hand):
    """
    Func to return the score of the inputted hand.
    The score is the average
    @param hand: accepts a list of cards (str) to check
    @return: returns the average as an int
    """

    # dict. below is used to assign a number with the card value, if the card value is a letter (not digit).
    face = {"A": 1, "J": 11, "Q": 12, "K": 13}
    count = 0
    for card in hand:
        value = card[:-1]  # e.g. if card == 'A♥', then card[:-1] == 'A'; therefore value == 'A'
        # if value is digit, e.g. '5', then convert to str; if not digit ('face value'), then refer to dict face value
        count += int(value) if value.isdigit() else face[value]
    return count / len(hand)  # returns average


def winner_check(condition, player) -> bool:
    """
    Func to return simple boolean based on player's win state.
    @param condition: condition is a boolean expression
    @param player: player refers to either 'player' or 'bot'
    @return: returns True or False depending on win state.
    """

    winner[player] = condition  # returns True or False, depending on condition expression.
    return condition


def win_reason(reason):
    """
    Func to create a string message, based on the win/loss state of the game.
    @param reason: accepts string which gives reason for win/loss
    """

    global win_string

    win_string += ("\n" + ("😊___YOU ARE THE WINNER___😊" if winner["player"] else "☹️_____YOU LOST_____☹️") +
                   "\n")

    if not reason:
        win_string += "You had an empty hand." if winner["bot"] else "Bot had an empty hand."
    else:
        win_string += ("You " if winner["player"] else "Bot ") + reason


def check_result(player_cards, robot_cards, suits) -> bool:
    """
    Func to return boolean based on player's win-state.
    @param player_cards: accepts list (str) of player's held card
    @param robot_cards: accepts list (str) of bot's held card
    @param suits: accepts list (str) of the selected suits
    @return: returns boolean based on player's win-state
    """

    def priority_order():
        """
        Nested function to sequentially compare the combination
        of cards held by the player and the robot to determine if
        the player has won the game order of priority:
        Rule 1 > Rule 2 > Rule 3 > Rule 4
        @return: returns None
        """

        # First check if player/bot have empty hands.
        if winner_check(not player_cards, "bot") or winner_check(not robot_cards, "player"):
            return win_reason(None)

        # RULE 1 & RULE 2 check:
        if len(player_cards) >= len(suits):  # rule can only be checked if this is true
            player_suit_value_count = suit_value_check(player_cards)  # returns int
            bot_suit_value_count = suit_value_check(robot_cards)  # returns int

            # RULE 1: player holds the same value card for all the defined suits
            if (winner_check(player_suit_value_count == len(suits), "player") or
                    winner_check(bot_suit_value_count == len(suits), "bot")):  # if either are True, func ends
                return win_reason("held the same value card for all defined suits.")

            # RULE 2: player holds the same value card for all the defined suits, minus 1
            if (winner_check(player_suit_value_count == len(suits) - 1, "player") or
                    winner_check(bot_suit_value_count == len(suits) - 1, "bot")):  # if either are True, func ends
                return win_reason(f"held the same value card for {len(suits) - 1} consecutive suits.")

        # RULE 3: check
        if len(player_cards) > 2:  # rule can only be checked if this is true
            # RULE 3: player holds more cards from the suit in position 2.
            player_suit_count = len([item for item in player_cards[2:] if item[-1] == player_cards[1][-1]])
            bot_suit_count = len([item for item in robot_cards[2:] if item[-1] == robot_cards[1][-1]])
            if player_suit_count != bot_suit_count:  # if True, func ends
                (winner_check(player_suit_count > bot_suit_count, "player") if True else
                 winner_check(True, "bot"))
                return win_reason("held more '2nd position suit' cards.")

        player_score, bot_score = score_count(player_cards), score_count(robot_cards)
        winner_check(player_score >= bot_score, "player") if True else winner_check(True, "bot")

        # RULE 4: player holds a higher average of the card’s value
        reason = ""
        if player_score != bot_score:
            higher_score, lower_score = max(player_score, bot_score), min(player_score, bot_score)
            reason += (f"held a higher score of {round(higher_score, 2)};\n" +
                       (f"you " if player_score < bot_score else "bot ") +
                       f"held a lower score of {round(lower_score, 2)}.")
        else:
            reason += ('drew with the bot,\nso you are "technically" still the "winner".\n'
                       f'You both scored {round(player_score, 2)}.')
        return win_reason(reason)

    priority_order()  # call the nested function
    return winner["player"]


def reset():
    """ Func to reset all global variables so player can play another round. """

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
    """
    Function to control player input & manage all aspects of the game play.
    This function calls the subsequent functions pertaining to player input.
    """

    global turn, game_started, main_loop, picked_card, choice
    pick = []  # this list holds player input

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

    if pick[0] == 1:  # player opts to start the game
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

        if not game_started:  # deck is created once when player enters '1' to start the game
            suits.extend(SUITS_1 if pick[1] == 1 else SUITS_2 if pick[1] == 2 else SUITS_3)
            create_deck(deck, suits, VALUES)

    elif pick[0] == 2:  # player opts to pick a card
        picked_card = pick_card(deck)
    elif pick[0] == 3:  # player opts to shuffle deck
        shuffle_deck(deck, suits)
    elif pick[0] == 6:  # player opts to exit program
        main_loop = False

    # player opts to end current game to check if winner or loser
    if game_started and (turn == 0 or pick[0] == 5):
        check_result(player_hand, bot_hand, suits)
        turn = 0  # force turn variable to 0 to end game.

    choice = [5] if turn == 0 else pick  # sets global variable of player choice, based on game state
    game_menu()  # calls the game menu function to print messages & gfx onto the screen

    if not game_started and pick[0] == 1:  # deck is shuffled implicitly only once, when game has begun.
        shuffle_deck(deck, suits)
        game_started = True  # global variable is updated


def main():
    """ Main function acts as execution point for the program """

    game_menu()
    while main_loop:
        play_game()
        if turn == 0:
            reset()


if __name__ == '__main__':
    main()
