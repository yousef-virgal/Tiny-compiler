from scanner import *
from tokentypes import *
import sys
def main():
    with open(sys.argv[1],'r') as inputfile:
        source = inputfile.read()
    lexer = Lexer(source)

    token = lexer.getToken()
    while token.tokenKind != Tokens.EOF:
        print("token : {} , kind : {}".format(token.tokenText,token.tokenKind))
        token = lexer.getToken()

if __name__ == "__main__":
    main()