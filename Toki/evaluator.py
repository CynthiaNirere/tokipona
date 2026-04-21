# ============================================================
#  evaluator.py
#  Toki Pona Language - Expression Evaluator
#
#  Job: Take a list of tokens that represent an expression
#  (like  a mute b  or  x en 1  or  "hi" en name)
#  and compute the result — a number, string, or boolean.
#
#  This file also handles:
#    - Built-in functions: len(), str(), int()
#    - User-defined function calls
#    - String indexing: word[0]
# ============================================================

from tokenizer import tokenize


# Toki Pona operator keywords mapped to Python operators
OPERATOR_MAP = {
    'en':     '+',
    'weka':   '-',
    'mute':   '*',
    'kipisi': '/',
    'seme':   '==',
    'ala':    '!=',
    'lili':   '<',
    'suli':   '>',
    'lon':    'True',
    'ike':    'False',
}


def evaluate_expr(tokens, variables, functions):
    """
    Turn a list of tokens into a single Python value.
    Handles numbers, strings, variables, operators, and function calls.
    """

    expr_parts = []  # We'll build a Python expression string here
    i = 0

    while i < len(tokens):
        ttype, tval = tokens[i]

        # --- Number literal ---
        if ttype == 'NUMBER':
            expr_parts.append(tval)

        # --- String literal ---
        elif ttype == 'STRING':
            expr_parts.append(repr(tval))  # repr() adds quotes safely

        # --- Word: keyword, operator, variable, or function name ---
        elif ttype == 'WORD':

            # Operator keywords (en, weka, mute, etc.)
            if tval in OPERATOR_MAP:
                expr_parts.append(OPERATOR_MAP[tval])

            # Function call:  funcName(arg1, arg2)
            elif i + 1 < len(tokens) and tokens[i + 1][1] == '(':
                result = _handle_function_call(tval, tokens, i + 2, variables, functions)
                value, i = result
                expr_parts.append(repr(value))
                continue  # i already advanced inside helper

            # String / list indexing:  word[0]
            elif i + 1 < len(tokens) and tokens[i + 1][1] == '[':
                var_name = tval
                i += 2  # skip variable name and '['
                idx_tokens = []
                while i < len(tokens) and tokens[i][1] != ']':
                    idx_tokens.append(tokens[i])
                    i += 1
                # i is now on ']'
                idx_val = evaluate_expr(idx_tokens, variables, functions)
                base_str = str(variables.get(var_name, ''))
                try:
                    char = base_str[int(idx_val)]
                except IndexError:
                    char = ''
                expr_parts.append(repr(char))

            # Regular variable
            else:
                val = variables.get(tval, 0)
                expr_parts.append(repr(val))

        # --- Symbol: +, -, (, ), [, ], ==, etc. ---
        elif ttype == 'SYMBOL':
            sym = tval
            if sym in ('+', '-', '*', '/', '%', '(', ')', '[', ']'):
                expr_parts.append(sym)
            elif sym in ('==', '!=', '<', '>', '<=', '>='):
                expr_parts.append(sym)

        i += 1

    expr_str = ' '.join(expr_parts)

    if not expr_str.strip():
        return None

    try:
        return eval(expr_str)
    except Exception as e:
        print(f"  [Expression error: '{expr_str}'] -> {e}")
        return 0


def _handle_function_call(func_name, tokens, start_i, variables, functions):
    """
    Parse and call a function.  Returns (result_value, new_index).
    start_i should point to the token AFTER the opening '('.
    """
    args = []
    current_arg = []
    depth = 1
    i = start_i

    while i < len(tokens):
        tok_type, tok_val = tokens[i]

        if tok_val == '(':
            depth += 1
            current_arg.append(tokens[i])
        elif tok_val == ')':
            depth -= 1
            if depth == 0:
                if current_arg:
                    args.append(evaluate_expr(current_arg, variables, functions))
                    current_arg = []
                i += 1  # move past the closing ')'
                break
            else:
                current_arg.append(tokens[i])
        elif tok_val == ',' and depth == 1:
            args.append(evaluate_expr(current_arg, variables, functions))
            current_arg = []
        else:
            current_arg.append(tokens[i])

        i += 1

    result = call_function(func_name, args, variables, functions)
    return result, i


def call_function(name, args, variables, functions):
    """
    Call a built-in function or a user-defined function.
    Returns the function's result value.
    """

    # --- Built-in: len(x) ---
    if name == 'len':
        return len(str(args[0])) if args else 0

    # --- Built-in: str(x) ---
    if name == 'str':
        return str(args[0]) if args else ''

    # --- Built-in: int(x) ---
    if name == 'int':
        try:
            return int(args[0]) if args else 0
        except (ValueError, TypeError):
            return 0

    # --- User-defined function ---
    if name in functions:
        # Import here to avoid circular imports
        from runner import run_lines

        param_names, body_lines = functions[name]

        # Copy global variables into a local scope
        local_vars = dict(variables)

        # Bind each argument to its parameter name
        for idx, param in enumerate(param_names):
            if idx < len(args):
                local_vars[param] = args[idx]

        return run_lines(body_lines, local_vars, functions)

    print(f"  [Error: Unknown function '{name}']")
    return None