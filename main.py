from scanner import *
from tokentypes import *

def main():
    sourc = ""
    lexer = Lexer(sourc)

    token = lexer.getToken()
    while token.tokenKind != Tokens.EOF:
        print(token.tokenKind)
        token = lexer.getToken()

if __name__ == "__main__":
    main()