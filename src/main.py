from parser import KunaiParser
from lexer import KunaiLexer
from interpreter import KunaiExecute
import sys


file_name = sys.argv[1]
f = open(file_name)

parser = KunaiParser()
lexer  = KunaiLexer()

asString = f.read()
split = asString.split(';')
# print(split)
tree = parser.parse(lexer.tokenize(asString))
ID = {}
KunaiExecute(tree, ID)



