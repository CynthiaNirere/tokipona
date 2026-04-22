# tokipona
A programming language based on Toki Pona, interpreted with Python.


## How to Run
`python3 main.py programs/helloworld.txt`

## Project Structure

tokipona/
main.py\
interpreter.py\
 programs/\
    ├── helloworld.txt\
    ├── cat.txt\
    ├── multiply.txt\
    ├── repeater.txt\
    ├── reverse_string.txt\
    ├── is_palindrome.txt\
    └── is_even.txt


`main.py` is the entry point. `interpreter.py` holds everything — the tokenizer, stack, and runner.


## How the Stack Works
 You push values on top and pop them off the top. Every value in this language goes through the stack.

```
pana 3     push 3        stack: [3]
pana 4     push 4        stack: [3, 4]
mute       multiply      stack: [12]
toki       print         stack: []     prints: 12
```

## Keywords

*Input and Output

`toki` — pop the top of the stack and print it

`kute name "prompt"` — ask the user for input, push it onto the stack, and store it in a variable

**Pushing and Storing Values**

`pana value` — push a number, string, or variable onto the stack

`kama name` — push a variable's value onto the stack

`nimi name` — pop the top and store it in a variable

*Math*

`en` — pop two values, push their sum (also works for joining strings)

`weka` — pop two values, push the difference

`mute` — pop two values, push the product

`kipisi` — pop two values, push the quotient

`%` — pop two values, push the remainder

*Comparisons*

`seme` — pop two values, push True if they are equal

`ala` — pop two values, push True if they are not equal

`lili` — pop two values, push True if the first is less than the second

`suli` — pop two values, push True if the first is greater than the second

*String Operations

`len` — pop a string, push its length

`index` — pop an index and a string, push the character at that position

*Control Flow*

`ante` — if statement. Pops the top; if True runs the block, otherwise runs the `sama` block

`sama` — the else branch inside an `ante` block

`sin` — while loop. Pops the top each time; keeps running while True. The loop body must push a new condition at the end

`musi i 0 5` — for loop. Runs the block with i going from 0 up to 4

`pini` — ends any block (ante, sin, musi, or awen)

*Functions*

`awen name` — define a function, ended with `pini`

To call a function just write its name on its own line.

*Booleans*

`lon` means True, `ike` means False.


## Example

```
# multiply two numbers
kute a "First number: "
kute b "Second number: "
mute
toki
```

```
# check if a number is even
kute num "Enter a number: "
pana 2
%
pana 0
seme
ante
    pana "even!"
    toki
sama
    pana "odd."
    toki
pini
```

## Requirements
Python 3 or higher. No extra libraries needed.
