#  Toki Pona Language 
#  How to run a program:
#    python3 main.py programs/helloworld.txt

import sys
import os
from interpreter import tokenize, run_lines, clear_stack

def run_file(filepath):
    if not os.path.exists(filepath):
        print(f"Error: File '{filepath}' not found.")
        sys.exit(1)

    with open(filepath, 'r') as f:
        lines = f.read().splitlines()

    clear_stack()      
    variables = {}      
    functions = {}      

    run_lines(lines, variables, functions)


def print_help():
    print("  Toki Pona Stack-Based Language Interpreter")
    print()
    print("Programs:")
    programs = [
        ("helloworld.txt",     "Prints Hello World"),
        ("cat.txt",            "Reads input and prints it back"),
        ("multiply.txt",       "Multiplies two numbers"),
        ("repeater.txt",       "Repeats a character N times"),
        ("reverse_string.txt", "Reverses a string"),
        ("is_palindrome.txt",  "Checks if a word is a palindrome"),
        ("is_even.txt",        "Checks if a number is even or odd"),
    ]
    for name, desc in programs:
        print(f"  programs/{name:<22} {desc}")
    print()
    print("Stack keyword reference:")
    keywords = [
        ("pana value",  "push a value onto the stack"),
        ("kama name",   "push a variable's value"),
        ("nimi name",   "pop top and store in variable"),
        ("toki",        "pop top and print it"),
        ("kute name",   "get input, push it, store it"),
        ("en",          "pop two, push sum or concat"),
        ("weka",        "pop two, push difference"),
        ("mute",        "pop two, push product"),
        ("kipisi",      "pop two, push quotient"),
        ("%",           "pop two, push remainder"),
        ("seme",        "pop two, push True if equal"),
        ("ala",         "pop two, push True if not equal"),
        ("lili",        "pop two, push True if a < b"),
        ("suli",        "pop two, push True if a > b"),
        ("len",         "pop string, push its length"),
        ("index",       "pop index + string, push char"),
        ("dup",         "duplicate the top value"),
        ("ante",        "if: pop condition, run block"),
        ("sama",        "else branch inside ante"),
        ("sin",         "while: pop condition each loop"),
        ("musi i 0 5",  "for loop: i from 0 to 4"),
        ("awen name",   "define a function"),
        ("pini",        "end a block"),
        ("lon / ike",   "True / False"),
    ]
    for kw, meaning in keywords:
        print(f"  {kw:<16} {meaning}")
    print()


if __name__ == '__main__':
    if len(sys.argv) < 2:
        print_help()
        sys.exit(0)

    run_file(sys.argv[1])