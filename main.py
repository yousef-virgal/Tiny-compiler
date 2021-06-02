from scanner import *
from tokentypes import *
from emiter import *
from myparser import *
import sys
def main():
    with open(sys.argv[1],'r') as inputfile:
        source = inputfile.read()
    lexer = Lexer(source)

    lexer2 = Lexer(source)
    token = lexer2.getToken()
    while token.tokenKind != Tokens.EOF:
        token = lexer2.getToken()
    print("token list:")
    for i in lexer2.tokenList:print(i.tokenText)
    print("end")
    emiter = Emiter()
    parser = Parser(lexer,emiter)
    parser.program()
    print(emiter.getCode())
    print("parser completed")

if __name__ == "__main__":
    main()