import random
import os
from bext import fg

GARBAGE_CHARS = '~!@#$%^&*()_+-={}[]|;:,.<>?/\\'
MAX_WORDS = 12

with open('sevenletterwords.txt') as dictionaryFile:
    WORDS = dictionaryFile.readlines()
for i in range(len(WORDS)):
    WORDS[i] = WORDS[i].strip().upper()

WORDS = random.sample(WORDS, len(WORDS))


def calculate_common_letters(string1, string2):
    # sum(c1 == c2 for c1, c2 in zip(string1, string2)) ### 1 liner
    count = 0
    for c1, c2 in zip(string1, string2):
        if c1 == c2:
            count += 1
    return count


def get_words():
    counts = [2, 7, 2]
    secretPassword = random.choice(WORDS)
    words = [secretPassword]
    for word in WORDS:
        difference = calculate_common_letters(secretPassword, word)
        if difference == 0 and counts[0] != 0:
            counts[0] -= 1
            words.append(word)
        elif difference == 3 and counts[2] != 0:
            counts[2] -= 1
            words.append(word)
        elif difference >= 1 and counts[1] != 0:
            counts[1] -= 1
            words.append(word)
        if counts == [0, 0, 0]:
            break
    return words


def overwrite_string(string, string_to_insert, index):
    string = string[:index] + string_to_insert + \
        string[index + len(string_to_insert):]
    return string


def get_terminal(words):
    board = []
    LINES = 16
    LINE_LEN = 16
    WORD_LEN = 7
    memoryAddress = LINE_LEN * random.randint(0, 4000)
    lines_with_words = random.sample(range(LINES * 2), MAX_WORDS)

    current_word = 0
    for i in range(LINES):
        left_col = ""
        right_col = ""
        for j in range(LINE_LEN):
            left_col += random.choice(GARBAGE_CHARS)
            right_col += random.choice(GARBAGE_CHARS)

        if i in lines_with_words:
            index = random.randint(0, LINE_LEN - WORD_LEN)
            left_col = overwrite_string(left_col, words[current_word], index)
            current_word += 1

        if i + LINES in lines_with_words:
            index = random.randint(0, LINE_LEN - WORD_LEN)
            right_col = overwrite_string(right_col, words[current_word], index)
            current_word += 1

        board.append(hex(memoryAddress) + '  ' + left_col + '    ' +
                     hex(memoryAddress + LINE_LEN * LINES) + '  ' + right_col)

        memoryAddress += LINE_LEN

    return '\n'.join(board)


def get_guess(words, remaining):
    while True:
        move = input(
            f'Enter password: ({remaining} tries remaining): ').upper()
        if move in words:
            return move


def runGame():
    guess = ""
    game_words = get_words()
    secret_password = game_words[0]
    game_words = random.sample(game_words, len(game_words))  # shuffle again
    game_terminal = get_terminal(game_words)

    for remaining in range(4, 0, -1):
        os.system('cls')
        fg('white')
        print('Enter the correct word to hack this system:')
        fg('green')
        print(game_terminal)
        fg('white')
        print(
            f'Last Guess - {guess} {calculate_common_letters(guess, secret_password)} / 7 correct')
        guess = get_guess(game_words, remaining)
        if guess == secret_password:
            print('A C C E S S   G R A N T E D')
            return
        else:
            game_terminal = game_terminal.replace(guess, ".......")
        print(f'Locked out of system. Password was {secret_password}.')


if __name__ == '__main__':
    runGame()
