from parser import KunaiParser
from parser import typeTOKEN
from parser import KunaiTypeError
from parser import KunaiBinaryOperatorError
from lexer import KunaiLexer


class KunaiExecute:
    def __init__(self, tree, ID):
        self.ID = ID
        result = self.runTree(tree)
        
    
    def runTree(self, node):
        if isinstance(node, typeTOKEN):
            return node
        if node is None:
            return None

        if node[0] == 'factor':
            return self.runTree(node[1])
        
        if node[0] == 'add':
            # print(node)
            return self.runTree(node[1]).binaryoperator('add', self.runTree(node[2]))
        
        if node[0] == 'print':
            print(self.runTree(node[1]).value)
            return self.runTree(node[1])

        if node[0] == 'var_assign':
            if node[1] == self.runTree(node[3]).type:
                self.ID[node[2]] = self.runTree(node[3])
                return node[1]
            else:
                raise KunaiTypeError("Tried to assign {} to {}".format(self.runTree(node[3]).type, node[1]))
        
        if node[0] == 'var':
            try:
                return self.ID[node[1]]        
            except LookupError:
                print(f'Undefined name {node[1]!r}')
                return 0
        
        if node[0] == 'statement':
            return self.runTree(node[1])
        
        if node[0] == 'term':
            return self.runTree(node[1])

        if node[0] == 'statements':
            for statement in node[1]:
                self.runTree(statement)
        
        
        


if __name__ == '__main__':
    lexer = KunaiLexer()
    parser = KunaiParser()
    ID = {}

    while True:
        try:
            text = input(":>")
        except EOFError:
            break
        if text:
            token = lexer.tokenize(text)
            tree = parser.parse(token)
            print(tree)
            try:
                KunaiExecute(tree, ID)
            except KunaiTypeError as Error:
                print(Error)
                continue
