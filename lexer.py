"""
    A lexer of Cool.
"""

def otherwise(_):
    return True


def isAlpha(c):
    return 'A' <= c <= 'Z' or 'a' <= c <= 'z'


def isNumber(c):
    return '0' <= c <= '9'


def isAlphaNum(c):
    return isNumber(c) or isAlpha(c)


def isIdHead(c):
    return isAlpha(c) or c == '_'


def isIdBody(c):
    return isAlphaNum(c) or c == '_'


stateTrans = {
    "Normal": [
        [isNumber, "Integer"],
        [isIdHead, "Identifier"],
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
        [otherwise, "Normal"]
    ],
    "LBrace": [
        [otherwise, "EndOfToken"]
    ],
    "Dispatch": [
        [otherwise, "EndOfToken"]
    ],
    "BasePointer": [
        [otherwise, "EndOfToken"]
    ],
    "Tilde": [
        [otherwise, "EndOfToken"]
    ],
    "Multiplication": [
        [otherwise, "EndOfToken"]
    ],
    "Division": [
        [otherwise, "EndOfToken"]
    ],
    "Addition": [
        [otherwise, "EndOfToken"]
    ],
    "Lower": [
        [lambda x: x == '-', "Assignment"],
        [lambda x: x == '=', "LessEqual"],
        [otherwise, "EndOfToken"]
    ],
    "Equal": [
        [lambda x: x == '>', "CaseArrow"],
        [otherwise, "EndOfToken"]
    ],
    "Assignment": [
        [otherwise, "EndOfToken"]
    ],
    "LessEqual": [
        [otherwise, "EndOfToken"]
    ],
    "CaseArrow": [
        [otherwise, "EndOfToken"]
    ],
    "Identifier": [
        [isIdBody, "Identifier"],
        [otherwise, "EndOfToken"]
    ],
    "Integer": [
        [isNumber, "Integer"],
        [lambda x: x == '.', "Floating"],
        [otherwise, "EndOfToken"]
    ],
    "Floating": [
        [isNumber, "Floating"],
        [otherwise, "EndOfToken"]
    ],
    "String?": [
        [lambda x: x == '"', "String"],
        [otherwise, "String?"]
    ],
    "String": [
        [otherwise, "EndOfToken"]
    ],
    "Dash": [
        [lambda x: x == '-', "LineComment"],
        [isIdBody, "Normal"],
        [otherwise, "Error"]
    ],
    "LineComment": [
        [lambda x: x == '\n', "EndOfToken"],
        [otherwise, "LineComment"]
    ],
    "LParen": [
        [lambda x: x == '*', "BlockComment?"],
        [otherwise, "EndOfToken"]
    ],
    "BlockComment?": [
        [lambda x: x == '*', "BlockCmtEnd?"],
        [otherwise, "BlockComment?"]
    ],
    "BlockCmtEnd?": [
        [lambda x: x == ')', "BlockComment"],
        [otherwise, "BlockComment?"]
    ],
    "BlockComment": [
        [otherwise, "EndOfToken"]
    ],
    "RParen": [
        [otherwise, "EndOfToken"]
    ],
    "Error": [
        [otherwise, "Error"]
    ]
}


def refreshState(state, x):
    global stateTrans

    guard = stateTrans[state]

    for item in guard:
        if item[0](x):
            return item[1]

    raise Exception("Unknown problem")


charbuff = ' '
tokenbuff = ""


def readToken(state, s):
    global charbuff, tokenbuff
    if s == "":
        return ("EOF", "", False)

    x = s[0]

    charbuff = x
    tokenbuff += x
    newstate = refreshState(state, x)

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


def checkKeyword(tok):
    if tok:
        if tok[0] == "Identifier":
            if tok[1] in keywords:
                return ("Keyword", tok[1])
    return tok


def lexer(s):
    lexes = []

    if s == "":
        return []
        
    #state = "Normal"
    #states = readToken(state, s)
    state = "Normal"

    while state != "EOF":
        states = readToken(state, s)
        state = states[0]
        tok = states[1]
        tok = checkKeyword(tok)
        moveon = not states[2]
        if tok:
            lexes.append(tok)
        if moveon:
            s = s[1:]

    return lexes


def main():
    from sys import argv
    if len(argv) > 1:
        fn = argv[1]
        with open(fn, 'r') as f:
            ls = f.readlines()
            ls = '\n'.join(ls)
        list(map(print, lexer(ls)))

if __name__ == '__main__':
    main()
