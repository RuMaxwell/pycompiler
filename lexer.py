"""
    A lexer of Cool.
"""

def otherwise(_):
    return True


def is_alpha(c):
    return 'A' <= c <= 'Z' or 'a' <= c <= 'z'


def is_number(c):
    return '0' <= c <= '9'


def isAlphaNum(c):
    return is_number(c) or is_alpha(c)


def is_id_head(c):
    return is_alpha(c) or c == '_'


def is_id_body(c):
    return isAlphaNum(c) or c == '_'


state_trans = {
    "Normal": [
        [is_number, "Integer"],
        [is_id_head, "Identifier"],
        [lambda x: x == '"', "String?"],
        [lambda x: x == '-', "Dash"],
        [lambda x: x == '.', "Dispatch"],
        [lambda x: x == '@', "BasePointer"],
        [lambda x: x == '~', "Tilde"],
        [lambda x: x == '*', "Multiplication"],
        [lambda x: x == '/', "Division"],
        [lambda x: x == '+', "Addition"],
        [lambda x: x == '<', "Lower"],
        [lambda x: x == '=', "Equal"],
        [lambda x: x == '(', "LParen"],
        [lambda x: x == ')', "RParen"],
        [lambda x: x == '{', "LBrace"],
        [lambda x: x == '}', "RBrace"],
        [lambda x: x == ';', "Semicolon"],
        [otherwise, "Normal"]
    ],
    "Addition": [
        [otherwise, "EndOfToken"]
    ],
    "Assignment": [
        [otherwise, "EndOfToken"]
    ],
    "BasePointer": [
        [otherwise, "EndOfToken"]
    ],
    "BlockCmtEnd?": [
        [lambda x: x == ')', "BlockComment"],
        [otherwise, "BlockComment?"]
    ],
    "BlockComment": [
        [otherwise, "EndOfToken"]
    ],
    "BlockComment?": [
        [lambda x: x == '*', "BlockCmtEnd?"],
        [otherwise, "BlockComment?"]
    ],
    "CaseArrow": [
        [otherwise, "EndOfToken"]
    ],
    "Dash": [
        [lambda x: x == '-', "LineComment"],
        [is_id_body, "Normal"],
        [otherwise, "Error"]
    ],
    "Dispatch": [
        [otherwise, "EndOfToken"]
    ],
    "Division": [
        [otherwise, "EndOfToken"]
    ],
    "Equal": [
        [lambda x: x == '>', "CaseArrow"],
        [otherwise, "EndOfToken"]
    ],
    "Escape?": [
        [lambda x: x in ['b', 't', 'n', 'f', '\\', '\n'], "String?"],
        [otherwise, "Error"]
    ],
    "Floating": [
        [is_number, "Floating"],
        [otherwise, "EndOfToken"]
    ],
    "Identifier": [
        [is_id_body, "Identifier"],
        [otherwise, "EndOfToken"]
    ],
    "Integer": [
        [is_number, "Integer"],
        [lambda x: x == '.', "Floating"],
        [otherwise, "EndOfToken"]
    ],
    "LBrace": [
        [otherwise, "EndOfToken"]
    ],
    "LessEqual": [
        [otherwise, "EndOfToken"]
    ],
    "LineComment": [
        [lambda x: x == '\n', "EndOfToken"],
        [otherwise, "LineComment"]
    ],
    "Lower": [
        [lambda x: x == '-', "Assignment"],
        [lambda x: x == '=', "LessEqual"],
        [otherwise, "EndOfToken"]
    ],
    "LParen": [
        [lambda x: x == '*', "BlockComment?"],
        [otherwise, "EndOfToken"]
    ],
    "Multiplication": [
        [otherwise, "EndOfToken"]
    ],
    "RBrace": [
        [otherwise, "EndOfToken"]
    ],
    "RParen": [
        [otherwise, "EndOfToken"]
    ],
    "Semicolon": [
        [otherwise, "EndOfToken"]
    ],
    "String": [
        [otherwise, "EndOfToken"]
    ],
    "String?": [
        [lambda x: x == '"', "String"],
        [lambda x: x == '\\', "Escape?"],
        [otherwise, "String?"]
    ],
    "Tilde": [
        [otherwise, "EndOfToken"]
    ],
    "Error": [
        [otherwise, "Error"]
    ]
}


def update_state(state, x):
    global state_trans

    guard = state_trans[state]

    for item in guard:
        if item[0](x):
            return item[1]

    raise Exception("Unknown problem")


charbuff = ' '
tokenbuff = ""


def read_token(state, s):
    global charbuff, tokenbuff
    if s == "":
        if state != "Normal":
            return ("Error", ("Error", "Unexpected EOF"), False)
        else:
            return ("EOF", "", False)

    x = s[0]

    charbuff = x
    tokenbuff += x
    newstate = update_state(state, x)

    token = None
    endoftok = False

    """if newstate == "Normal":
        if state != "Normal":
            token = (state, tokenbuff[:-1])
            tokenbuff = charbuff
            newstate = refreshState(newstate, charbuff)
        else:
            tokenbuff = ""
    elif newstate == "EndOfToken":"""
    if newstate == "Normal":
        tokenbuff = ""
    elif newstate == "EndOfToken":
        endoftok = True
        newstate = "Normal"
        token = (state, tokenbuff[:-1])
        tokenbuff = ""
    else:
        token = None

    return (newstate, token, endoftok)


keywords = [
    "case",
    "class",
    "else",
    "esac",
    "fi",
    "if",
    "in",
    "inherits",
    "isvoid",
    "let",
    "loop",
    "new",
    "not",
    "of",
    "pool",
    "then",
    "while"
]


def check_keyword(tok):
    if tok:
        if tok[0] == "Identifier":
            if tok[1] in keywords:
                return ("Keyword", tok[1])
    return tok


def lexer(s):
    global charbuff

    lexes = []

    if s == "":
        return []
        
    #state = "Normal"
    #states = readToken(state, s)
    state = "Normal"

    linenum = 1
    columnnum = 1

    while state not in ("Error", "EOF"):
        states = read_token(state, s)
        state = states[0]
        tok = states[1]
        tok = check_keyword(tok)
        moveon = not states[2]
        if tok:
            lexes.append((linenum, columnnum) + tok)
        if moveon:
            s = s[1:]
            if charbuff == '\n':
                columnnum = 1
                linenum += 1
            else:
                columnnum += 1
    
    if state == "Error":
        print("Lexical error:", states[1])

    return lexes


def main():
    from sys import argv
    if len(argv) > 1:
        fn = argv[1]
        with open(fn, 'r') as f:
            ls = f.readlines()
            ls = ''.join(ls)
        list(map(print, lexer(ls)))

if __name__ == '__main__':
    main()
