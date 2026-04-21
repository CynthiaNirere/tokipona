# ============================================================
#  runner.py
#  Toki Pona Language - Statement Runner
#    toki   -> print
#    kute   -> input
#    nimi   -> variable assignment
#    ante   -> if / else
#    sin    -> while loop
#    musi   -> for loop
#    awen   -> function definition
#    pana   -> return
#
# ============================================================

from tokenizer import tokenize
from evaluator import evaluate_expr


# -------------------------------------------------------
# Helper: collect lines inside a block until 'pini'
# -------------------------------------------------------

def collect_block(lines, start_i):
    """
    Collect all lines from start_i until the matching 'pini'.
    Handles nested blocks by tracking depth.

    Returns:
        block  - the list of lines inside the block
        next_i - the index of the line after 'pini'
    """
    block = []
    depth = 1
    i = start_i

    while i < len(lines):
        inner_line = lines[i].strip()
        inner_tokens = tokenize(inner_line)

        if inner_tokens:
            first = inner_tokens[0][1]
            if first in ('ante', 'sin', 'awen', 'musi'):
                depth += 1          # nested block opened
            elif first == 'pini':
                depth -= 1
                if depth == 0:
                    return block, i + 1   # found the matching pini

        block.append(inner_line)
        i += 1

    return block, i  # reached end of lines (missing pini)


def collect_if_block(lines, start_i):
    """
    Collect the if-body and optional else-body for an 'ante' block.

    Returns:
        if_body   - lines inside the 'ante' block
        else_body - lines inside the 'sama' block (may be empty)
        next_i    - line index after the closing 'pini'
    """
    if_body = []
    else_body = []
    in_else = False
    depth = 1
    i = start_i

    while i < len(lines):
        inner_line = lines[i].strip()
        inner_tokens = tokenize(inner_line)

        if not inner_tokens:
            (else_body if in_else else if_body).append(inner_line)
            i += 1
            continue

        first = inner_tokens[0][1]

        if first in ('ante', 'sin', 'awen', 'musi'):
            depth += 1
        elif first == 'pini':
            depth -= 1
            if depth == 0:
                return if_body, else_body, i + 1
        elif first == 'sama' and depth == 1:
            in_else = True
            i += 1
            continue  # don't add 'sama' itself to any body

        (else_body if in_else else if_body).append(inner_line)
        i += 1

    return if_body, else_body, i


# -------------------------------------------------------
# Main runner
# -------------------------------------------------------

def run_lines(lines, variables, functions):
    """
    Execute a list of source code lines.

    variables : dict of current variable names -> values
    functions : dict of user-defined function names -> (params, body)

    Returns a value only when a 'pana' (return) statement is hit.
    Otherwise returns None.
    """
    i = 0

    while i < len(lines):
        line = lines[i].strip()

        # Skip blank lines and comment-only lines
        if not line or line.startswith('#'):
            i += 1
            continue

        tokens = tokenize(line)
        if not tokens:
            i += 1
            continue

        first = tokens[0][1]  # the first word on this line

        # --------------------------------------------------------
        # toki  ->  print
        # Usage:  toki "Hello"
        #         toki myVar
        #         toki "Value: " en x
        # --------------------------------------------------------
        if first == 'toki':
            value = evaluate_expr(tokens[1:], variables, functions)
            print('' if value is None else value)
            i += 1

        # --------------------------------------------------------
        # kute  ->  input
        # Usage:  kute varName "Enter something: "
        # --------------------------------------------------------
        elif first == 'kute':
            var_name = tokens[1][1]
            prompt = ''
            if len(tokens) > 2:
                p = evaluate_expr(tokens[2:], variables, functions)
                prompt = '' if p is None else str(p)

            user_input = input(prompt)

            # Try to store as a number, fall back to string
            try:
                if '.' in user_input:
                    variables[var_name] = float(user_input)
                else:
                    variables[var_name] = int(user_input)
            except ValueError:
                variables[var_name] = user_input

            i += 1

        # --------------------------------------------------------
        # nimi  ->  declare / assign variable
        # Usage:  nimi x = 10
        #         nimi greeting = "hello"
        #         nimi result = a mute b
        # --------------------------------------------------------
        elif first == 'nimi':
            var_name = tokens[1][1]
            # tokens[2] is the '=' sign, expression starts at index 3
            value = evaluate_expr(tokens[3:], variables, functions)
            variables[var_name] = value
            i += 1

        # --------------------------------------------------------
        # ante  ->  if statement
        # Usage:  ante x suli 5
        #             toki "big"
        #         sama
        #             toki "small"
        #         pini
        # --------------------------------------------------------
        elif first == 'ante':
            condition = evaluate_expr(tokens[1:], variables, functions)
            if_body, else_body, next_i = collect_if_block(lines, i + 1)

            chosen_body = if_body if condition else else_body
            result = run_lines(chosen_body, variables, functions)

            if result is not None:
                return result   # bubble up a return value

            i = next_i

        # --------------------------------------------------------
        # sin  ->  while loop
        # Usage:  sin x lili 10
        #             x = x en 1
        #         pini
        # --------------------------------------------------------
        elif first == 'sin':
            condition_tokens = tokens[1:]
            body, next_i = collect_block(lines, i + 1)

            loop_count = 0
            while evaluate_expr(condition_tokens, variables, functions):
                result = run_lines(body, variables, functions)
                if result is not None:
                    return result
                loop_count += 1
                if loop_count > 100_000:
                    print("  [Error: Loop stopped — ran over 100,000 times]")
                    break

            i = next_i

        # --------------------------------------------------------
        # musi  ->  for loop (counted range)
        # Usage:  musi i = 0 lili 5
        #             toki i
        #         pini
        # Means:  for i in range(0, 5)
        # --------------------------------------------------------
        elif first == 'musi':
            var_name  = tokens[1][1]    # loop variable
            # tokens[2] = '='
            start_val = int(evaluate_expr([tokens[3]], variables, functions))
            # tokens[4] = 'lili'
            end_val   = int(evaluate_expr([tokens[5]], variables, functions))

            body, next_i = collect_block(lines, i + 1)

            for val in range(start_val, end_val):
                variables[var_name] = val
                result = run_lines(body, variables, functions)
                if result is not None:
                    return result

            i = next_i

        # --------------------------------------------------------
        # awen  ->  define a function
        # Usage:  awen add a b
        #             pana a en b
        #         pini
        # --------------------------------------------------------
        elif first == 'awen':
            func_name = tokens[1][1]
            params    = [t[1] for t in tokens[2:] if t[0] == 'WORD']
            body, next_i = collect_block(lines, i + 1)
            functions[func_name] = (params, body)
            i = next_i

        # --------------------------------------------------------
        # pana  ->  return a value from a function
        # Usage:  pana x en 1
        # --------------------------------------------------------
        elif first == 'pana':
            value = evaluate_expr(tokens[1:], variables, functions)
            return value

        # --------------------------------------------------------
        # Assignment without 'nimi':  varName = expr
        # Usage:  x = x en 1
        #         reversed = reversed en ch
        # --------------------------------------------------------
        elif len(tokens) >= 3 and tokens[1][1] == '=':
            var_name = tokens[0][1]
            value = evaluate_expr(tokens[2:], variables, functions)
            variables[var_name] = value
            i += 1

        # --------------------------------------------------------
        # Anything else: treat as a standalone expression
        # (e.g., a function call whose return value we ignore)
        # --------------------------------------------------------
        else:
            evaluate_expr(tokens, variables, functions)
            i += 1

    return None  # no return statement was hit