from sly import Parser
from lexer import KunaiLexer

class KunaiTypeError(Exception):
    def __init__(self, message):
        self.message = message

class KunaiBinaryOperatorError(Exception):
    def __init__(self, message):
        self.message = message
        

class typeTOKEN:
    def __init__(self, theType, value):
        self.type = theType
        if (self.type == 'INT'):
            self.value = int(value)
        elif(self.type =='FLOAT'):
            self.value = float(value)
        elif(self.type =='STRING'):
            self.value = value
        else:
            self.value = value
    def setValue(self, newValue):
        if (self.type == 'INT'):
            self.value = int(newValue)
        elif(self.type =='FLOAT'):
            self.value = float(newValue)
        elif(self.type =='STRING'):
            self.value = newValue
        else:
             self.value = newValue
    
    def binaryoperator(self, operation, TOKEN2):
        if (self.type == TOKEN2.type):
            if operation == 'add':
                return typeTOKEN(self.type, self.value + TOKEN2.value)
            else:
                raise KunaiBinaryOperatorError("Operator {} not defined for type {}".format(operation, self.type))

        else:
            raise KunaiTypeError('''Cannot binary operate between objects 
            with two different types {} and {}. (operator {})
            '''.format(self.type, TOKEN2.type, operation))



class KunaiParser(Parser):
    debugfile = 'parser.out'

    def __init__(self):
        self.ID = {}
    tokens = KunaiLexer.tokens
    precedence = (
        ('left', PLUS, MINUS),
        ('left', TIMES, DIVIDE, DIVIDEFLOOR),
    )

    @_('statement')
    def statements(self, p):
        return ('statements', [p.statement])
    
    @_('statement statements')
    def statements(self, p):
        return ('statements', [p.statement] + p.statements[1])       

    @_('expr SEMICOLON')
    def statement(self, p):
        return ('statement', p.expr)

    @_('term')
    def expr(self, p):
        return ('term', p.term)

    @_('factor')
    def term(self, p):
        return ('factor', p.factor)

    @_('INT')
    def factor(self, p):
        return ('factor', typeTOKEN('INT', p.INT))
    
    @_('FLOAT')
    def factor(self, p):
        return ('factor', typeTOKEN('FLOAT', p.FLOAT))

    @_('ID ID ASSIGN expr')
    def factor(self, p):
        return ('var_assign', p.ID0, p.ID1, p.expr)           
        

    @_('PRINT LPAREN expr RPAREN')
    def expr(self, p):
        return ('print', p.expr)

# fix ones below



    @_('STRING')
    def factor(self, p):
        return ('string', typeTOKEN('STRING', p.STRING[1:-1]))

    
    
    @_('expr PLUS term')
    def expr(self, p): 
        return ('add', p.expr, p.term)

    
    @_('expr DIVIDE term')
    def expr(self, p):
        return ('divide', p.expr, p.term)
        
        
        '''if p.expr.type == p.term.type:
            if p.expr.type == 'STRING':
                raise KunaiTypeError("Cannot divide by string")
            elif p.expr.type == 'INT':
                return typeTOKEN('FLOAT', p.expr.value / p.term.value)
            elif p.expr.type == 'FLOAT':
                return typeTOKEN(p.expr.type, p.expr.value / p.term.value)
            else:
                return typeTOKEN(p.expr.type, p.expr.value / p.term.value)
        else:
            raise KunaiTypeError("Tried to add two variables of different types '{}' and '{}'".format(p.expr.type, p.term.type))
'''
    @_('expr DIVIDEFLOOR term')
    def expr(self, p):
        if p.expr.type == p.term.type:
            if p.expr.type == 'STRING':
                raise KunaiTypeError("Cannot divide by string")
            elif p.expr.type == 'INT':
                return typeTOKEN('INT', p.expr.value // p.term.value)
            elif p.expr.type == 'FLOAT':
                return typeTOKEN('INT', p.expr.value // p.term.value)
            else:
                return typeTOKEN(p.expr.type, p.expr.value / p.term.value)
        else:
            raise KunaiTypeError("Tried to add two variables of different types '{}' and '{}'".format(p.expr.type, p.term.type))

    
    #finish above

    @_('LBRACKET statements RBRACKET SEMICOLON')
    def statements(self, p):
        return p.statements

    @_('ID')
    def expr(self, p):
        return ('var', p.ID)       


    
if __name__ == '__main__':
    lexer = KunaiLexer()
    parser = KunaiParser()

    while True:
        try:
            text = input(':>')
            result = parser.parse(lexer.tokenize(text))
            try:
                print(result.value)
            except AttributeError:
                pass
        except EOFError:
            break
        except KunaiTypeError as error:
            print(error.message)
            pass