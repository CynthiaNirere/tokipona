#  interpreter.py
# TOKENIZER

def tokenize(line):
  
    if '#' in line:
        line = line[:line.index('#')]

    line = line.strip()
    if not line:
        return []

    tokens = []
    i = 0

    while i < len(line):

        if line[i] == ' ':
            i += 1
            continue

        if line[i] == '"':
            j = i + 1
            while j < len(line) and line[j] != '"':
                j += 1
            tokens.append(('STRING', line[i + 1:j]))
            i = j + 1
            continue

        if line[i].isdigit():
            j = i
            while j < len(line) and (line[j].isdigit() or line[j] == '.'):
                j += 1
            tokens.append(('NUMBER', line[i:j]))
            i = j
            continue

        if line[i] == '-' and i + 1 < len(line) and line[i + 1].isdigit():
            prev = tokens[-1][1] if tokens else None
            operators = {'=', '(', ',', 'pana', 'kama', 'en', 'weka',
                         'mute', 'kipisi', 'lili', 'suli', 'seme', 'ala'}
            if prev is None or prev in operators:
                j = i + 1
                while j < len(line) and (line[j].isdigit() or line[j] == '.'):
                    j += 1
                tokens.append(('NUMBER', line[i:j]))
                i = j
                continue

        if line[i].isalpha() or line[i] == '_':
            j = i
            while j < len(line) and (line[j].isalnum() or line[j] == '_'):
                j += 1
            tokens.append(('WORD', line[i:j]))
            i = j
            continue

        tokens.append(('SYMBOL', line[i]))
        i += 1

    return tokens


# THE STACK

stack = []  

def push(value):
    stack.append(value)


def pop():
    if not stack:
        print("  [Stack error: tried to pop from an empty stack]")
        return 0
    return stack.pop()


def peek():
    """Look at the top value without removing it."""
    if not stack:
        print("  [Stack error: stack is empty]")
        return 0
    return stack[-1]


def clear_stack():
    stack.clear()

#  STACK OPERATIONS


def op_en():
    #en:  adding
    b = pop()
    a = pop()
    if isinstance(a, str) or isinstance(b, str):
        push(str(a) + str(b))
    else:
        push(a + b)


def op_weka():
    #weka: subtract
    b = pop()
    a = pop()
    push(a - b)


def op_mute():
    #mute: multiply
    b = pop()
    a = pop()
    push(a * b)


def op_kipisi():
    #kipisi: divide
    b = pop()
    a = pop()
    if b == 0:
        print("  [Math error: cannot divide by zero]")
        push(0)
    else:
        push(a / b)


def op_modulo():
    #%: remainder
    b = pop()
    a = pop()
    push(a % b)


def op_seme():
    #seme: equals
    b = pop()
    a = pop()
    push(a == b)


def op_ala():
    #ala: not equal
    b = pop()
    a = pop()
    push(a != b)


def op_lili():
   # lili: less than
    b = pop()
    a = pop()
    push(a < b)


def op_suli():
   # suli: greater than
    b = pop()
    a = pop()
    push(a > b)


def try_number(value):
   #Try to convert a string to int or float. Returns original if it can't
    try:
        if '.' in str(value):
            return float(value)
        return int(value)
    except (ValueError, TypeError):
        return value

#  BLOCK COLLECTORS

def collect_block(lines, start_i):
   
    block = []
    depth = 1
    i = start_i

    while i < len(lines):
        inner = lines[i].strip()
        tokens = tokenize(inner)

        if tokens:
            first = tokens[0][1]
            if first in ('ante', 'sin', 'awen', 'musi'):
                depth += 1
            elif first == 'pini':
                depth -= 1
                if depth == 0:
                    return block, i + 1

        block.append(inner)
        i += 1

    return block, i


def collect_if_block(lines, start_i):
    if_body   = []
    else_body = []
    in_else   = False
    depth     = 1
    i         = start_i

    while i < len(lines):
        inner  = lines[i].strip()
        tokens = tokenize(inner)

        if not tokens:
            (else_body if in_else else if_body).append(inner)
            i += 1
            continue

        first = tokens[0][1]

        if first in ('ante', 'sin', 'awen', 'musi'):
            depth += 1
        elif first == 'pini':
            depth -= 1
            if depth == 0:
                return if_body, else_body, i + 1
        elif first == 'sama' and depth == 1:
            in_else = True
            i += 1
            continue

        (else_body if in_else else if_body).append(inner)
        i += 1

    return if_body, else_body, i

#  THE RUNNER, executes

def run_lines(lines, variables, functions):
   
    i = 0

    while i < len(lines):
        line = lines[i].strip()

        if not line or line.startswith('#'):
            i += 1
            continue

        tokens = tokenize(line)
        if not tokens:
            i += 1
            continue

        first = tokens[0][1]   

        if first == 'pana' and len(tokens) > 1:
            ttype, tval = tokens[1]

            if ttype == 'NUMBER':
                push(try_number(tval))
            elif ttype == 'STRING':
                push(tval)
            elif ttype == 'WORD':
                if tval == 'lon':
                    push(True)
                elif tval == 'ike':
                    push(False)
                else:
                    push(variables.get(tval, 0))

            i += 1
        # Usage:  kama myVar
        elif first == 'kama':
            var_name = tokens[1][1]
            push(variables.get(var_name, 0))
            i += 1

        # Usage:  nimi result
        elif first == 'nimi':
            var_name = tokens[1][1]
            variables[var_name] = pop()
            i += 1

        # Usage:  toki
        elif first == 'toki':
            value = pop()
            print('' if value is None else value)
            i += 1

        # Usage:  kute myVar "Enter something: "
        elif first == 'kute':
            var_name = tokens[1][1]
            prompt = tokens[2][1] if len(tokens) > 2 and tokens[2][0] == 'STRING' else ''
            user_input = input(prompt)
            value = try_number(user_input)
            push(value)
            variables[var_name] = value
            i += 1

        # Arithmetic operators
        elif first == 'en':
            op_en()
            i += 1

        elif first == 'weka':
            op_weka()
            i += 1

        elif first == 'mute':
            op_mute()
            i += 1

        elif first == 'kipisi':
            op_kipisi()
            i += 1

        elif first == '%':
            op_modulo()
            i += 1

        #Comparison operators 
        elif first == 'seme':
            op_seme()
            i += 1

        elif first == 'ala':
            op_ala()
            i += 1

        elif first == 'lili':
            op_lili()
            i += 1

        elif first == 'suli':
            op_suli()
            i += 1

        elif first == 'len':
            push(len(str(pop())))
            i += 1

        elif first == 'index':
            idx    = int(pop())
            string = str(pop())
            try:
                push(string[idx])
            except IndexError:
                push('')
            i += 1

        elif first == 'dup':
            push(peek())
            i += 1

        elif first == 'ante':
            condition = pop()
            if_body, else_body, next_i = collect_if_block(lines, i + 1)
            chosen = if_body if condition else else_body
            result = run_lines(chosen, variables, functions)
            if result is not None:
                return result
            i = next_i

        elif first == 'sin':
            body, next_i = collect_block(lines, i + 1)
            loop_count = 0

            while pop():
                result = run_lines(body, variables, functions)
                if result is not None:
                    return result
                loop_count += 1
                if loop_count > 100_000:
                    print("  [Error: loop ran over 100,000 times, stopped]")
                    break

            i = next_i

        #  musi: for loop (counted range) 
        elif first == 'musi':
            var_name = tokens[1][1]

            raw_start = tokens[2][1]
            raw_end   = tokens[3][1]

            start_val = int(variables.get(raw_start, raw_start)
                            if tokens[2][0] == 'WORD' else raw_start)
            end_val   = int(variables.get(raw_end, raw_end)
                            if tokens[3][0] == 'WORD' else raw_end)

            body, next_i = collect_block(lines, i + 1)

            for val in range(start_val, end_val):
                variables[var_name] = val
                push(val)
                result = run_lines(body, variables, functions)
                if result is not None:
                    return result

            i = next_i

        #  awen: define a function
        elif first == 'awen':
            func_name = tokens[1][1]
            body, next_i = collect_block(lines, i + 1)
            functions[func_name] = body
            i = next_i

        elif first in functions:
            body = functions[first]
            result = run_lines(body, variables, functions)
            if result is not None:
                return result
            i += 1

        else:
            print(f"  [Warning: unknown instruction '{first}']")
            i += 1

    return None