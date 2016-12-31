class Token:
    ID        = 0
    NUM       = 1
    EQUAL     = 2
    NOT_EQUAL = 3
    STRING    = 4
    EOF       = 100
    ERROR     = 101

class Parser:

    TYPE = 0
    VAL  = 1

    def __init__(self):
        self.lineno = 1
        self.token = ()

    def parse(self, prog):
        self.token = self.get_token(prog)
        self.prog = prog
        self.con_list()
        return True

    def con_list(self):
        # TODO
        self.con()

    def con(self):
        self.match(Token.ID)
        self.op()
        self.right_side()

    def op(self):
        if self.token[self.TYPE] == Token.EQUAL:
            self.match(Token.EQUAL)
        else: # self.token[self.TYPE] == Token.NOT_EQUAL
            self.match(Token.NOT_EQUAL)

    def right_side(self):
        t = self.token[self.TYPE]
        if t == Token.ID:
            self.match(Token.ID)
        elif t == Token.STRING:
            self.match(Token.STRING)
        else: # t == Token.NUM
            self.match(Token.NUM)
    
    def match(self, token_type=Token.ERROR):
        if token_type == self.token[self.TYPE]:
            # may have to do more here
            self.token = self.get_token()
        else:
            # TODO
            #print "[Parser] Line ", self.lineno, " saw ", self.token[self.VAL], " expected ", token_type
            raise SyntaxError()
    
    def get_token(self, prog=None):
        """ Retrieves the next token from prog, which is an open constraint file """
        if not prog:
            prog = self.prog

        while True:
            c = prog.read(1)
    
            if c == ' ' or c == '\t':
                continue
            elif c == '\n':
                self.lineno += 1
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
                    
    
def is_letter(c):
    if c == '': return False
    char = ord(c)
    return (char >= 65 and char <= 90) or (char >= 97 and char <= 122)

def is_digit(c):
    if c == '': return False
    char = ord(c)
    return (char >= 48 and char <= 57)

if __name__ == '__main__':
    parser = Parser()
    with open('constraints') as f:
        parser.parse(f)
    print parser.token
