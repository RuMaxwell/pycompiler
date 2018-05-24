states = [
    "Normal",
    "Identifier",
    "Integer",
    "Floating",
    "String",
    "Dash",
    "LineComment",
    "LParen",
    "BlockComment",
    "BlockCmtEnd?",
    "Error"
]

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
        [lambda x: x == '"', "String"],
        [lambda x: x == '-', "Dash"],
        [lambda x: x == '(', "LParen"],
        [otherwise, "Normal"]
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
    "String": [
        [lambda x: x == '"', "StringEnd"],
        [otherwise, "String"]
    ],
    "StringEnd": [
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
        [lambda x: x == '*', "BlockComment"],
        [otherwise, "EndOfToken"]
    ],
    "BlockComment": [
        [lambda x: x == '*', "BlockCmtEnd?"],
        [otherwise, "BlockComment"]
    ],
    "BlockCmtEnd?": [
        [lambda x: x == ')', "BlockCmtEnd"],
        [otherwise, "BlockComment"]
    ],
    "BlockCmtEnd": [
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
        return ("EOF", "")

    x = s[0]

    charbuff = x
    tokenbuff += x
    newstate = refreshState(state, x)

    token = None

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
        newstate = "Normal"
        token = (state, tokenbuff[:-1])
        tokenbuff = ""
    else:
        token = None

    return (newstate, token)

def lexer(s):
    lexes = []

    if s == "":
        return []
        
    state = "Normal"
    states = readToken(state, s)

    while state != "EOF":
        s = s[1:]
        states = readToken(state, s)
        state = states[0]
        tok = states[1]
        if tok:
            lexes.append(tok)

    return lexes

def main():
    from sys import argv
    if len(argv) > 1:
        fn = argv[1]
        with open(fn, 'r') as f:
            ls = f.readlines()
            ls = '\n'.join(ls)
        print(lexer(ls))

if __name__ == '__main__':
    main()
