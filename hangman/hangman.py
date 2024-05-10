import random

# The Hangman ASCII art
HANGMAN_ASCII_ART = """
Welcome to the game Hangman
  _    _                                         
 | |  | |                                        
 | |__| | __ _ _ __   __ _ _ __ ___   __ _ _ __  
 |  __  |/ _` | '_ \ / _` | '_ ` _ \ / _` | '_ \ 
 | |  | | (_| | | | | (_| | | | | | | (_| | | | |
 |_|  |_|\__,_|_| |_|\__, |_| |_| |_|\__,_|_| |_|
                      __/ |                      
                     |___/ """

MAX_TRIES = 6  # Maximum number of tries allowed

# Hangman ASCII art for different stages of the hangman
HANGMAN_PHOTOS = {
    0: """
 x-------x
""",
    1: """
 x-------x
 |
 |
 |
 |
 |
""",
    2: """
 x-------x
 |       |
 |       0
 |
 |
 |
""",
    3: """
 x-------x
 |       |
 |       0
 |       |
 |
 |
""",
    4: """
 x-------x
 |       |
 |       0
 |      /|\\
 |
 |
""",
    5: """
 x-------x
 |       |
 |       0
 |      /|\\
 |      /
 |
""",
    6: """
 x-------x
 |       |
 |       0
 |      /|\\
 |      / \\
 |
""",
}


def is_valid_input(letter_guessed):
    """
    Checks if the input is a valid single letter.
    """
    return len(letter_guessed) == 1 and letter_guessed.isalpha()


def check_valid_input(letter_guessed, old_letters_guessed):
    """
    Checks if the input is a valid single letter that hasn't been guessed before.
    """
    return is_valid_input(letter_guessed) and letter_guessed.lower() not in [
        l.lower() for l in old_letters_guessed
    ]


def try_update_letter_guessed(letter_guessed, old_letters_guessed):
    """
    Updates the list of guessed letters if the input is valid.
    """
    if check_valid_input(letter_guessed, old_letters_guessed):
        old_letters_guessed.append(letter_guessed.lower())
        return True
    else:
        print("X")
        sorted_letters = sorted([l.lower() for l in old_letters_guessed])
        for i, letter in enumerate(sorted_letters):
            print(letter, end="->") if i != len(sorted_letters) - 1 else print(letter)
        print("\n wrong input", "enter another letter")
        return False


def check_win(secret_word, old_letters_guessed):
    """
    Checks if the player has guessed all the letters in the secret word.
    """
    for letter in list_hidden_word(secret_word, old_letters_guessed):
        if letter == "_":
            return False
    return True


def show_hidden_word(secret_word, old_letters_guessed):
    """
    Displays the current state of the secret word with guessed letters revealed.
    """
    print(" ".join(list_hidden_word(secret_word, old_letters_guessed)))


def list_hidden_word(secret_word, old_letters_guessed):
    """
    Creates a list of the secret word with guessed letters revealed.
    """
    hidden_word = ["_"] * len(secret_word)
    for i, letter in enumerate(secret_word):
        if letter.lower() in [l.lower() for l in old_letters_guessed]:
            hidden_word[i] = letter
    return hidden_word


def print_hangman(num_of_tries):
    """
    Prints the Hangman ASCII art that matches the number of incorrect tries.
    """
    print(HANGMAN_PHOTOS[num_of_tries])


def choose_word(file_path, index):
    """
    Picks a word from a file based on a given index.
    """

    if type(index) != int or index < 0:
        index = 0
    while True:
        try:
            with open(file_path, "r") as file:
                words = list(file.read().split())
                num_unique_words = len(set(words))
                secret_word = words[(index - 1) % len(words)]
            return num_unique_words, secret_word
        except FileNotFoundError:
            print("File not found")
            file_path = input("Enter file path for words file: ")
            choose_word(file_path, index)


def main():
    """
    Main function to run the Hangman game.
    """
    file_path_words = input("Enter file path for words file: ")
    word_index = int(input("Enter the index of the word you want to choose: "))
    secret_word = choose_word(file_path_words, word_index)[1]

    print(HANGMAN_ASCII_ART)
    print("You have", MAX_TRIES, "tries to guess the word.")
    old_letters_guessed = []
    num_of_tries = 0
    while num_of_tries < MAX_TRIES:
        if check_win(secret_word, old_letters_guessed):
            print("WIN")
            print(
                "Good job! You found the word",
                secret_word,
                "in",
                num_of_tries,
                "tries",
            )
            break

        print_hangman(num_of_tries)
        show_hidden_word(secret_word, old_letters_guessed)

        letter_guessed = input("Guess a letter: ").lower()
        if try_update_letter_guessed(letter_guessed, old_letters_guessed):
            if letter_guessed not in secret_word:
                num_of_tries += 1

    if num_of_tries == MAX_TRIES:
        print("YOU LOST")
        print("The word was", secret_word)


if __name__ == "__main__":
    main()
