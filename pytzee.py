"""
File:    pytzee.py
Author:  Bliss Phinehas
Date:    10/31/2024
Description:
The program makes it possible to play the game Yahtzee but through python.
 	"""

import random

# Special category scores for some of the Pytzee fun stuff
FULL_HOUSE = 25
SMALL_STRAIGHT = 30
LARGE_STRAIGHT = 40
YAHTZEE = 50
BONUS_YAHTZEE = 100
BONUS_THRESHOLD = 63
BONUS_POINTS = 35

# Types of scoring categories
CATEGORIES = [
    "count 1", "count 2", "count 3", "count 4", "count 5", "count 6",
    "three of a kind", "four of a kind", "full house", "small straight",
    "large straight", "pytzee", "chance"
]


def roll_dice():
    """Roll five dice and see what luck brings."""
    return [random.randint(1, 6) for _ in range(5)]


def calculate_sum(dice):
    """Sum up all dice for 'chance' or anything needing the total score."""
    return sum(dice)


def has_three_of_a_kind(dice):
    """Look for any number that shows up at least three times."""
    return any(dice.count(x) >= 3 for x in dice)


def has_four_of_a_kind(dice):
    """Check for four of a kind – it’s harder than it sounds!"""
    return any(dice.count(x) >= 4 for x in dice)


def has_full_house(dice):
    """Check if we've got a full house (a pair and a trio)."""
    unique_values = set(dice)
    return len(unique_values) == 2 and any(dice.count(x) == 3 for x in unique_values)


def has_small_straight(dice):
    """Look for four consecutive numbers for a small straight."""
    sorted_dice = sorted(set(dice))
    for i in range(len(sorted_dice) - 3):
        if sorted_dice[i:i + 4] == list(range(sorted_dice[i], sorted_dice[i] + 4)):
            return True
    return False


def has_large_straight(dice):
    """Large straight means five in a row – a rare treat."""
    return sorted(dice) in [list(range(1, 6)), list(range(2, 7))]


def has_yahtzee(dice):
    """Pytzee time! Do all five dice match up?"""
    return len(set(dice)) == 1


def show_scorecard(scorecard):
    """Display the scorecard nicely."""
    print("\nScorecard:")
    for category, score in scorecard.items():
        print(f"{category.ljust(20)}: {score}")


def play_pytzee(rounds):
    """Run through the main game loop for a given number of rounds."""
    scorecard = {category: 0 for category in CATEGORIES}
    used_categories = set()
    upper_section_score = 0

    for round_num in range(1, rounds + 1):
        print(f"\nRound {round_num} of {rounds}")
        dice = roll_dice()
        print(f"Rolled: {dice}")

        while True:
            choice = input("Enter category (or 'skip' to skip): ").strip().lower()
            if choice == "skip" or (choice in CATEGORIES and choice not in used_categories):
                break
            print("Oops! Invalid choice or already used. Try again.")

        if choice == "skip":
            print("Skipped this round.")
            continue

        used_categories.add(choice)
        score = 0

        # Score based on choice
        if choice.startswith("count"):
            num = int(choice.split()[1])
            score = dice.count(num) * num
            upper_section_score += score
        elif choice == "three of a kind" and has_three_of_a_kind(dice):
            score = calculate_sum(dice)
        elif choice == "four of a kind" and has_four_of_a_kind(dice):
            score = calculate_sum(dice)
        elif choice == "full house" and has_full_house(dice):
            score = FULL_HOUSE
        elif choice == "small straight" and has_small_straight(dice):
            score = SMALL_STRAIGHT
        elif choice == "large straight" and has_large_straight(dice):
            score = LARGE_STRAIGHT
        elif choice == "pytzee" and has_yahtzee(dice):
            score = YAHTZEE if scorecard["pytzee"] == 0 else BONUS_YAHTZEE
        elif choice == "chance":
            score = calculate_sum(dice)

        scorecard[choice] = score
        show_scorecard(scorecard)

    # Apply bonus if the upper section score is high enough
    if upper_section_score >= BONUS_THRESHOLD:
        print(f"Bonus achieved! +{BONUS_POINTS} points.")
        scorecard["bonus"] = BONUS_POINTS

    # Final score calculation
    final_score = sum(scorecard.values())
    print(f"\nFinal Score: {final_score}")


if __name__ == "__main__":
    # Set a random seed so we can see the same results if we want
    try:
        seed = int(input("Enter a random seed (or leave blank): ") or "0")
    except ValueError:
        seed = 0  # Default to 0 if input isn't a number
    random.seed(seed)

    # Start the game by asking for rounds
    try:
        rounds = int(input("How many rounds do you want to play? "))
        play_pytzee(rounds)
    except ValueError:
        print("Please enter a valid number of rounds.")
