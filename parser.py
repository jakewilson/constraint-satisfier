class Token:
    ID        = 0
    NUM       = 1
    EQUAL     = 2
    NOT_EQUAL = 3
    STRING    = 4
    EOF       = 100
    ERROR     = 101

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
            # id's must start with a letter, but can contain both letters and digits
            while (is_letter(c) or is_digit(c)):
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
            return (Token.NUM, int(num))
        elif c == '!':
            # a '=' must follow
            if prog.read(1) != '=':
                return (Token.ERROR,)
            else:
                return (Token.NOT_EQUAL,)
        elif c == '=':
            return (Token.EQUAL,)
        elif c == '\'': # string
            string = ''
            c = prog.read(1)
            while c != '\'':
                if c == '':
                    return (Token.ERROR,)
                string += c
                c = prog.read(1)

            return (Token.STRING, string)
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
