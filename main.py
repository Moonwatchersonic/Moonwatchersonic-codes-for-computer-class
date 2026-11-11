
import random

# ============================================================
# FUNCTION 1: get_choices
# ============================================================
def get_choices():
    """
    Return the choices that are allowed in the game.
    """
    choices = ["rock", "paper", "scissors"]
    return choices


# ============================================================
# FUNCTION 2: show_separator
# ============================================================
def show_separator():
    """
    Print a line that makes the program easier to read.
    """
    print("=" * 35)


# ============================================================
# FUNCTION 3: show_welcome
# ============================================================
def show_welcome():
    """
    Display the welcome message.
    """
    show_separator()
    print(" Welcome to Rock, Paper, Scissors! ")
    show_separator()
    print("Type 'rock', 'paper', or 'scissors' to play.")
    print("Type 'quit' or 'q' at any time to exit.")
    print()


# ============================================================
# FUNCTION 4: get_player_input
# ============================================================
def get_player_input():
    """
    Ask the player to type something.
    strip() removes spaces from the beginning and end.
    lower() converts the input to lowercase.
    """
    user_choice = input("Enter your choice: ").strip().lower()
    return user_choice


# ============================================================
# FUNCTION 5: is_quit_command
# ============================================================
def is_quit_command(user_choice):
    """
    Return True if the player wants to quit.
    Return False otherwise.
    """
    if user_choice == "quit" or user_choice == "q":
        return True
    else:
        return False


# ============================================================
# FUNCTION 6: is_valid_choice
# ============================================================
def is_valid_choice(user_choice, choices):
    """
    Check whether the player's choice is in the choices list.
    """
    if user_choice in choices:
        return True
    else:
        return False


# ============================================================
# FUNCTION 7: show_invalid_choice_message
# ============================================================
def show_invalid_choice_message():
    """
    Tell the player that the input was not valid.
    """
    print("Invalid choice!")
    print("Please type rock, paper, or scissors.")
    print()


# ============================================================
# FUNCTION 8: get_computer_choice
# ============================================================
def get_computer_choice(choices):
    """
    Randomly choose one item from the choices list.
    """
    computer_choice = random.choice(choices)
    return computer_choice


# ============================================================
# FUNCTION 9: show_computer_choice
# ============================================================
def show_computer_choice(computer_choice):
    """
    Display the computer's choice.
    """
    print(f"Computer chose: {computer_choice}")


# ============================================================
# FUNCTION 10: is_tie
# ============================================================
def is_tie(player_choice, computer_choice):
    """
    Return True when both players chose the same thing.
    """
    if player_choice == computer_choice:
        return True
    else:
        return False


# ============================================================
# FUNCTION 11: player_wins
# ============================================================
def player_wins(player_choice, computer_choice):
    """
    Determine whether the player won the round.

    The player wins when:
    rock beats scissors
    paper beats rock
    scissors beats paper
    """
    if player_choice == "rock" and computer_choice == "scissors":
        return True

    elif player_choice == "paper" and computer_choice == "rock":
        return True

    elif player_choice == "scissors" and computer_choice == "paper":
        return True

    else:
        return False


# ============================================================
# FUNCTION 12: determine_round_winner
# ============================================================
def determine_round_winner(player_choice, computer_choice):
    """
    Return a word describing the winner of the round.

    Possible results are:
    "tie"
    "player"
    "computer"
    """
    if is_tie(player_choice, computer_choice):
        return "tie"

    elif player_wins(player_choice, computer_choice):
        return "player"

    else:
        return "computer"


# ============================================================
# FUNCTION 13: show_round_result
# ============================================================
def show_round_result(round_winner):
    """
    Display the result of the round.
    """
    if round_winner == "tie":
        print("It is a tie!")

    elif round_winner == "player":
        print("You win this round!")

    else:
        print("The computer wins this round!")


# ============================================================
# FUNCTION 14: update_scores
# ============================================================
def update_scores(player_score, computer_score, ties, round_winner):
    """
    Update the correct score.
    The function returns all three updated scores.
    """
    if round_winner == "player":
        player_score += 1

    elif round_winner == "computer":
        computer_score += 1

    elif round_winner == "tie":
        ties += 1

    return player_score, computer_score, ties


# ============================================================
# FUNCTION 15: show_score
# ============================================================
def show_score(player_score, computer_score, ties):
    """
    Display the current scores.
    """
    print()
    print(
        f"Score -> You: {player_score} | "
        f"Computer: {computer_score} | "
        f"Ties: {ties}"
    )
    print("-" * 35)
    print()


# ============================================================
# FUNCTION 16: create_scoreboard
# ============================================================
def create_scoreboard():
    """
    Create the starting scores.

    The function returns three values:
    player_score
    computer_score
    ties
    """
    player_score = 0
    computer_score = 0
    ties = 0

    return player_score, computer_score, ties


# ============================================================
# FUNCTION 17: show_game_over
# ============================================================
def show_game_over(player_score, computer_score, ties):
    """
    Display the final scores when the game ends.
    """
    print()
    show_separator()
    print("GAME OVER")
    show_separator()

    print("Final Score:")
    print(f"You: {player_score}")
    print(f"Computer: {computer_score}")
    print(f"Ties: {ties}")


# ============================================================
# FUNCTION 18: determine_overall_winner
# ============================================================
def determine_overall_winner(player_score, computer_score):
    """
    Compare the final player and computer scores.
    Return the overall result.
    """
    if player_score > computer_score:
        return "player"

    elif player_score < computer_score:
        return "computer"

    else:
        return "tie"


# ============================================================
# FUNCTION 19: show_overall_winner
# ============================================================
def show_overall_winner(overall_winner):
    """
    Display the final winner message.
    """
    print()

    if overall_winner == "player":
        print("Congratulations, you beat the computer!")

    elif overall_winner == "computer":
        print("The computer wins this time. Better luck next time!")

    else:
        print("The entire game was a tie!")


# ============================================================
# FUNCTION 20: show_goodbye
# ============================================================
def show_goodbye():
    """
    Display the goodbye message.
    """
    print()
    print("Thanks for playing!")


# ============================================================
# FUNCTION 21: play_one_round
# ============================================================
def play_one_round(choices, player_score, computer_score, ties):
    """
    Play one complete round.

    This function:
    1. Gets the player's choice.
    2. Gets the computer's choice.
    3. Displays the computer's choice.
    4. Determines the round winner.
    5. Displays the round result.
    6. Updates the scores.
    7. Displays the updated scores.
    8. Returns the updated scores.
    """
    player_choice = get_player_input()

    # Check for invalid input
    if not is_valid_choice(player_choice, choices):
        show_invalid_choice_message()
        return player_score, computer_score, ties

    computer_choice = get_computer_choice(choices)

    show_computer_choice(computer_choice)

    round_winner = determine_round_winner(
        player_choice,
        computer_choice
    )

    show_round_result(round_winner)

    player_score, computer_score, ties = update_scores(
        player_score,
        computer_score,
        ties,
        round_winner
    )

    show_score(player_score, computer_score, ties)

    return player_score, computer_score, ties


# ============================================================
# FUNCTION 22: play_game
# ============================================================
def play_game():
    """
    Run the complete Rock, Paper, Scissors game.
    """
    choices = get_choices()

    player_score, computer_score, ties = create_scoreboard()

    show_welcome()

    want_to_play = True

    while want_to_play:

        user_choice = get_player_input()

        # Check whether the player wants to quit
        if is_quit_command(user_choice):
            want_to_play = False

        # Check whether the player's choice is valid
        elif not is_valid_choice(user_choice, choices):
            show_invalid_choice_message()

        else:
            # Get the computer's choice
            computer_choice = get_computer_choice(choices)

            show_computer_choice(computer_choice)

            # Determine the round winner
            round_winner = determine_round_winner(
                user_choice,
                computer_choice
            )

            # Display the result
            show_round_result(round_winner)

            # Update the scores
            player_score, computer_score, ties = update_scores(
                player_score,
                computer_score,
                ties,
                round_winner
            )

            # Display updated scores
            show_score(player_score, computer_score, ties)

    # Display final results after the player quits
    show_game_over(player_score, computer_score, ties)

    overall_winner = determine_overall_winner(
        player_score,
        computer_score
    )

    show_overall_winner(overall_winner)

    show_goodbye()


# ============================================================
# PROGRAM START
# ============================================================

play_game()
