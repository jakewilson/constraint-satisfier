class Token:
    ID        = 0
    NUM       = 1
    EQUAL     = 2
    NOT_EQUAL = 3
    STRING    = 4
    DOM_BEG   = 5
    DOM_END   = 6
    COMMA     = 7
    EOF       = 100
    ERROR     = 101

class Parser:

    TYPE  = 0
    VAL   = 1

    # for indexing the constraint tuple
    LEFT  = 0
    OP    = 1
    RIGHT = 2

    def __init__(self):
        self.lineno = 1
        self.token = ()

    def parse(self, prog):
        self.token = self.get_token(prog)
        self.prog = prog

        self.variables = set()
        self.constraints = []
        self.domain_set = set()

        self.domain()
        self.con_list()
        if self.token[self.TYPE] == Token.EOF:
            return (list(self.variables), self.constraints, self.domain_set)
        else:
            raise SyntaxError

    def con_list(self):
        while self.token[self.TYPE] == Token.ID:
            self.con()

    def con(self):
        self.constraint = ()
        self.match_id()
        self.op()
        self.right_side()
        self.add_constraint()

    def op(self):
        t = self.token[self.TYPE]
        self.constraint += (t,)
        if t == Token.EQUAL:
            self.match(Token.EQUAL)
        else: # t == Token.NOT_EQUAL
            self.match(Token.NOT_EQUAL)

    def right_side(self):
        t = self.token[self.TYPE]
        self.right_is_id = False
        if t == Token.ID:
            self.match_id()
            self.right_is_id = True
            return

        token = self.token
        self.literal()
        self.constraint += (token[self.VAL],)

    def literal(self):
        t = self.token[self.TYPE]
        if t == Token.STRING:
            self.match(t)
        elif t == Token.NUM:
            self.match(t)
        else:
            self.match(Token.ERROR)

    def domain_literal(self):
        token = self.token
        self.literal()
        self.domain_set.add(token[self.VAL])

    def domain(self):
        self.match(Token.DOM_BEG)
        self.domainlist()
        self.match(Token.DOM_END)

    def domainlist(self):
        while self.token[self.TYPE] == Token.STRING or self.token[self.TYPE] == Token.NUM:
            self.domain_literal()
            self.valuelist()

    def valuelist(self):
        while self.token[self.TYPE] == Token.COMMA:
            self.match(Token.COMMA)
            self.domain_literal()

    def match_id(self):
        # add the id to the variables if not already there
        iden = self.token[self.VAL]
        if iden not in self.variables:
            self.variables.add(iden)

        self.constraint += (iden,)
        self.match(Token.ID)
        
    
    def match(self, token_type=Token.ERROR):
        if token_type == self.token[self.TYPE]:
            # may have to do more here
            self.token = self.get_token()
        else:
            # TODO
            #print "[Parser] Line ", self.lineno, " saw ", self.token[self.VAL], " expected ", token_type
            raise SyntaxError()

    def add_constraint(self):
        op = self.constraint[self.OP] 
        constraint = self.constraint
        if op == Token.EQUAL:
            if self.right_is_id:
                self.constraints.append(lambda x: x[constraint[self.LEFT]] == x[constraint[self.RIGHT]])
            else:
                self.constraints.append(lambda x: x[constraint[self.LEFT]] == constraint[self.RIGHT])
        elif op == Token.NOT_EQUAL:
            if self.right_is_id:
                self.constraints.append(lambda x: x[constraint[self.LEFT]] != x[constraint[self.RIGHT]])
            else:
                self.constraints.append(lambda x: x[constraint[self.LEFT]] != constraint[self.RIGHT])
    
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
    
                if c!= '': prog.seek(-1, 1)
                return (Token.ID, iden)
            elif is_digit(c):
                num = c
            
                c = prog.read(1)
                while (is_digit(c)):
                    num += c
                    c = prog.read(1)
    
                if c != '': prog.seek(-1, 1)
                return (Token.NUM, int(num))
            elif c == '!':
                # a '=' must follow
                if prog.read(1) != '=':
                    return (Token.ERROR,)
                else:
                    return (Token.NOT_EQUAL,)
            elif c == '=':
                return (Token.EQUAL,)
            elif c == '\'' or c == '"': # string
                string = ''
                c = prog.read(1)
                while c != '\'' and c != '"':
                    if c == '':
                        return (Token.ERROR,)
                    string += c
                    c = prog.read(1)
    
                return (Token.STRING, string)
            elif c == '{':
                return (Token.DOM_BEG,)
            elif c == '}':
                return (Token.DOM_END,)
            elif c == ',':
                return (Token.COMMA,)
            elif c == '':
                return (Token.EOF,)
                break
            else:
                print '[Lexer] Illegal token on line ', self.lineno, ': \'', c, '\''
                return (Token.ERROR,)
                    
    
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
