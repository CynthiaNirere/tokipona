# ============================================================
#  tokenizer.py
#  Toki Pona Language - Tokenizer
#
#  Job: Take one line of source code (a string) and break it
#  into a list of tokens. A token is a small named piece,
#  like a number, a word, or a symbol.
#
#  Each token is a tuple:  ('TYPE', 'value')
#  Types used:
#    'NUMBER'  -> a numeric value like 42 or 3.14
#    'STRING'  -> text inside double quotes like "hello"
#    'WORD'    -> a keyword or variable name like toki or x
#    'SYMBOL'  -> a punctuation character like = ( ) [ ]
# ============================================================


def tokenize(line):
    """
    Split one line of source code into a list of tokens.
    Returns an empty list if the line is blank or a comment.
    """

    # Remove everything after a '#' comment marker
    if '#' in line:
        line = line[:line.index('#')]

    line = line.strip()

    # Nothing left to tokenize
    if not line:
        return []

    tokens = []
    i = 0

    while i < len(line):

        # -- Skip spaces --
        if line[i] == ' ':
            i += 1
            continue

        # -- String literal: "hello world" --
        if line[i] == '"':
            j = i + 1
            while j < len(line) and line[j] != '"':
                j += 1
            tokens.append(('STRING', line[i + 1:j]))
            i = j + 1
            continue

        # -- Regular number: 42 or 3.14 --
        if line[i].isdigit():
            j = i
            while j < len(line) and (line[j].isdigit() or line[j] == '.'):
                j += 1
            tokens.append(('NUMBER', line[i:j]))
            i = j
            continue

        # -- Negative number: -5  (only right after an operator or '=') --
        if line[i] == '-' and i + 1 < len(line) and line[i + 1].isdigit():
            # Only treat as negative if the previous token was an operator
            prev = tokens[-1][1] if tokens else None
            operators = {'=', '(', ',', 'en', 'weka', 'mute', 'kipisi',
                         'lili', 'suli', 'seme', 'ala'}
            if prev is None or prev in operators:
                j = i + 1
                while j < len(line) and (line[j].isdigit() or line[j] == '.'):
                    j += 1
                tokens.append(('NUMBER', line[i:j]))
                i = j
                continue

        # -- Word / keyword / variable name --
        if line[i].isalpha() or line[i] == '_':
            j = i
            while j < len(line) and (line[j].isalnum() or line[j] == '_'):
                j += 1
            tokens.append(('WORD', line[i:j]))
            i = j
            continue

        # -- Two-character symbols: == != <= >= --
        if i + 1 < len(line) and line[i:i + 2] in ('==', '!=', '<=', '>='):
            tokens.append(('SYMBOL', line[i:i + 2]))
            i += 2
            continue

        # -- Single-character symbol --
        tokens.append(('SYMBOL', line[i]))
        i += 1

    return tokens