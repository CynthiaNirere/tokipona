# ============================================================
#  main.py
#  Toki Pona Language Interpreter - Entry Point
#
#  How to run a program:
#    python main.py programs/helloworld.txt
#
#  This file just loads the source file and hands it off
#  to runner.py, which does the actual execution.
# ============================================================

import sys
import os

from runner import run_lines
from tokenizer import tokenize


def run_file(filepath):
    """Load a .txt source file and run it."""

    if not os.path.exists(filepath):
        print(f"Error: Could not find file '{filepath}'")
        sys.exit(1)

    with open(filepath, 'r') as f:
        source = f.read()

    lines = source.splitlines()

    variables = {}   # stores all global variables
    functions = {}   # stores all user-defined functions

    run_lines(lines, variables, functions)


def print_help():
    print("=" * 50)
    print("  Toki Pona Language Interpreter")
    print("=" * 50)
    print()
    print("Usage:")
    print("  python main.py <program.txt>")
    print()
    print("Available programs:")
    programs = [
        ("helloworld.txt",    "Prints Hello World"),
        ("cat.txt",           "Reads input and prints it back"),
        ("multiply.txt",      "Multiplies two numbers"),
        ("repeater.txt",      "Repeats a character N times"),
        ("reverse_string.txt","Reverses a string"),
        ("is_palindrome.txt", "Checks if a word is a palindrome"),
        ("is_even.txt",       "Checks if a number is even or odd"),
    ]
    for filename, description in programs:
        print(f"  programs/{filename:<22}  {description}")
    print()
    print("Quick keyword reference:")
    keywords = [
        ("toki",   "print"),
        ("kute",   "input"),
        ("nimi",   "declare variable"),
        ("ante",   "if"),
        ("sama",   "else"),
        ("sin",    "while loop"),
        ("musi",   "for loop"),
        ("pini",   "end block"),
        ("en",     "+  (add / concat)"),
        ("weka",   "-  (subtract)"),
        ("mute",   "*  (multiply)"),
        ("kipisi", "/  (divide)"),
        ("seme",   "== (equals)"),
        ("ala",    "!= (not equal)"),
        ("lili",   "<  (less than)"),
        ("suli",   ">  (greater than)"),
        ("lon",    "True"),
        ("ike",    "False"),
        ("awen",   "define function"),
        ("pana",   "return"),
    ]
    for kw, meaning in keywords:
        print(f"  {kw:<10}  {meaning}")
    print()


if __name__ == '__main__':
    if len(sys.argv) < 2:
        print_help()
        sys.exit(0)

    run_file(sys.argv[1])