class Token:
    ID        = 0
    NUM       = 1
    EQUAL     = 2
    NOT_EQUAL = 3
    EOF       = 100

def get_token(prog):
    """ Retrieves the next token from prog, which is an open constraint file """
    while True:
        c = prog.read(1)

        if c == ' ' or c == '\t':
            continue
        elif c == '\n':
            get_token.lineno += 1
        elif is_letter(c):
            iden = c

            c = prog.read(1)
            while (is_letter(c)):
                iden += c
                c = prog.read(1)

            prog.seek(-1, 1)
            return (Token.ID, iden)
        elif is_digit(c):
            num = c
        
            c = prog.read(1)
            while (is_digit(c)):
                num += c
                c = prog.read(1)

            prog.seek(-1, 1)
            return (Token.NUM, iden)
        elif c == '!':
            # a '=' must follow
            if prog.read(1) != '=':
                raise SyntaxError()
            else:
                return (Token.NOT_EQUAL,)
        elif c == '=':
            return (Token.EQUAL,)
        elif c == '': # EOF?
            return (Token.EOF,)
            break
                
get_token.lineno = 1

def is_letter(c):
    if c == '': return False
    char = ord(c)
    return (char >= 65 and char <= 90) or (char >= 97 and char <= 122)

def is_digit(c):
    if c == '': return False
    char = ord(c)
    return (char >= 48 and char <= 57)


f = open('constraints', 'r')
token = get_token(f)
while token[0] != Token.EOF:
    print token
    token = get_token(f)
