from sly import Lexer

class KunaiLexer(Lexer):
    
    tokens = {ID, FLOAT, INT, STRING, PLUS, MINUS, TIMES, 
              DIVIDE, ASSIGN, LBRACKET, RBRACKET, SEMICOLON, 
              RETURN,FUNCTION,LPAREN, RPAREN, DIVIDEFLOOR, PRINT
              
              }

    ignore = ' \t\n'
    PRINT    = r'print'
    RETURN   = r'return'
    FUNCTION = r'function'
    ID       = r'[a-zA-Z_][a-zA-Z0-9_]*'
    STRING   = r'"[a-zA-Z0-9_]*"'
    FLOAT    = r'[-+]?[0-9]+(\.([0-9]+)?([eE][-+]?[0-9]+)?|[eE][-+]?[0-9]+)'
    # regex from https://stackoverflow.com/a/19821296/6888722
    INT      = r'[0-9]+'
    PLUS     = r'\+'
    MINUS    = r'-'
    TIMES    = r'\*'
    DIVIDEFLOOR=r'/_'
    DIVIDE   = r'/'
    ASSIGN   = r':'
    LBRACKET = r'{'
    RBRACKET = r'}'
    LPAREN   = r'\('
    RPAREN   = r'\)'

    @_(r';')
    def SEMICOLON(self, t):
        self.lineno += 1
        return t
    
    def error(self, t):
        print("Illegal character {}".format(t.value[0]))
        self.index += 1


if __name__ == '__main__':
    data = """
    function hello(x):{return x};
    """
    lexer = KunaiLexer()
    for tok in lexer.tokenize(data):
        print(('type=%r, value=%r, %r' % (tok.type, tok.value, tok)))