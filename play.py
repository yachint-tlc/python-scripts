from random import choice
from typing import Any
import math

YELLOW = '\033[93m'
BLUE = '\033[94m'
RESET = '\033[0m'
GREEN = '\033[92m'

def get_word_list(file_path: str) -> list[tuple[str, str]]:
    word_list: list[tuple[str, str]] = []

    with open(file_path, 'r') as file:
        for line in file:
            word, meaning = line.strip().split(':')
            word_list.append((word.strip(), meaning.strip()))

    return word_list

def shuffle(arr: list[Any], visited: set[int]):
    unvisited = [i for i in range(len(arr)) if i not in visited]

    if not unvisited:
        return -1

    chosen_index: int = choice(unvisited)
    visited.add(chosen_index)

    return chosen_index


file_path: str = 'words.txt'
words: list[tuple[str, str]] = get_word_list(file_path=file_path)

visited_set: set[int] = set()
score: int = 0

while True:
    print(f"✅ -- Progress: {math.ceil(len(visited_set)/len(words)*100)}% -- ✅")
    i: int = shuffle(arr = words, visited = visited_set)

    if i == -1:
        break;

    word, meaning = words[i]
    print(f"\n{YELLOW}Current word: {word}{RESET}")

    user_input: str = input("Enter: Show meaning, n: Next word, q: Quit\n").lower()

    if user_input == '':
              print(f"{BLUE}Meaning: {meaning}{RESET}")
    elif user_input == 'n':
        score = score + 1
    elif user_input == 'q':
        print("Thanks for playing! ... Bye :)")
        break;
    else:
        print("Invalid input. Please try again.")
        continue;

print(f"\n{GREEN}Your Score: {score}/{len(words)}{RESET}")
print(f"\n{GREEN}Thanks for playing! ... Bye :){RESET}")
