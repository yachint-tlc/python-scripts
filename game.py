from random import choice
from typing import Any
import math
from datetime import datetime
import os
import sys

YELLOW = '\033[93m'
BLUE = '\033[94m'
RESET = '\033[0m'
GREEN = '\033[92m'

def select_word_file() -> str:
    """Let user choose between existing result files or new game"""
    default_file = 'words.txt'
    
    # Get list of .txt files in results directory
    result_files = [f for f in os.listdir('results') 
                   if f.endswith('.txt')] if os.path.exists('results') else []
    
    if not result_files:
        print(f"No previous files found. Starting new game with {default_file}.")
        return default_file
    
    # Display file options
    print(f"Found {len(result_files)} previous file(s):")
    for i, f in enumerate(result_files, 1):
        print(f"  {i}. {f}")
    print(f"n. Start new game with {default_file}")
    
    # Get user choice
    while True:
        choice = input("Enter choice (number/n): ").lower()
        if choice == 'n':
            return default_file
        if choice.isdigit() and 1 <= int(choice) <= len(result_files):
            return os.path.join('results', result_files[int(choice)-1])
        print("Invalid choice. Please try again.")

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

def delete_file_prompt(new_game, file_path):
    if not new_game:
        delete_choice = input(f"Do you want to delete the file '{file_path}'? (y/n): ").lower()
        if delete_choice == 'y':
            if os.path.exists(file_path):
                try:
                    os.remove(file_path)
                    print(f"File '{file_path}' deleted successfully.")
                except Exception as e:
                    print(f"Error deleting file: {e}")
            else:
                print(f"File '{file_path}' does not exist.")

def main():
    file_path: str = select_word_file()
    new_game = True if file_path == 'words.txt' else False

    words: list[tuple[str, str]] = get_word_list(file_path=file_path)
    visited_set: set[int] = set()
    score: int = 0
    mistake: int = 0
    now = datetime.now()
    if os.name == 'nt':  # Windows
        day_format = "%#d"
    else:                # Unix/Linux/Mac
        day_format = "%-d"

    filename = now.strftime(f"{day_format}_%B_%I-%M-%S%p") # e.g., "5_May_03-45-00PM"
    directory = "results"
    mistake_filepath = os.path.join(directory, f"{filename}.txt")
    os.makedirs(directory, exist_ok=True)
    MISTAKE_LIMIT = 15
    print(f"--- {mistake_filepath}")
    file = None

    try:
        while True:
            print(f"✅ -- Progress: {math.ceil(len(visited_set)/len(words)*100)}% -- ✅")
            i: int = shuffle(arr = words, visited = visited_set)

            if i == -1:
                break;

            word, meaning = words[i]
            print(f"\n{YELLOW}Current word: {word}{RESET}")

            bypass = False

            while True:
                if not bypass:
                    user_input: str = input("Enter: Show meaning, n: Next word, q: Quit\n").lower()
                else:
                    user_input: str = input()
                    bypass = False

                if user_input == '':
                    print(f"{BLUE}Meaning: {meaning}{RESET}")
                    break;
                elif user_input == '.':
                    print('Revelaling ... ');
                    print(f"{BLUE}Meaning: {meaning}{RESET}")
                    bypass = True
                elif user_input == 'n':
                    score = score + 1
                    break;
                elif user_input == '/' and new_game:
                    mistake += 1
                    print(f"Mistake Recorded! Chances left: {MISTAKE_LIMIT - mistake}")
                    if file is None:
                        file = open(mistake_filepath, 'w')
                    file.write(f"{word}: {meaning}\n")
                    print(f"{BLUE}Meaning: {meaning}{RESET}")
                    if mistake == MISTAKE_LIMIT:
                        print(f"You have reached your mistake limit ({MISTAKE_LIMIT}), please revise them and come back later! - Filepath: {mistake_filepath}")
                        exit()
                    break;
                elif user_input == 'q':
                    print("Thanks for playing! ... Bye :)")
                    exit()
                else:
                    print("Invalid input. Please try again.")

    finally:
        if file is not None:
            file.close()

    delete_file_prompt(new_game, file_path)
    print(f"\n{GREEN}Your Score: {score}/{len(words)}{RESET}")
    print(f"\n{GREEN}Thanks for playing! ... Bye :){RESET}")

if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        print(f"\n{BLUE}Program interrupted by user (Ctrl+C). Exiting gracefully...{RESET}")
        sys.exit(0)