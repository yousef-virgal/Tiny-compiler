from scanner import *
from tokentypes import *
from emiter import *
from myparser import *
import sys
def main():
    with open(sys.argv[1],'r') as inputfile:
        source = inputfile.read()
    lexer = Lexer(source)

    emiter = Emiter()
    parser = Parser(lexer,emiter)
    parser.program()
    print(emiter.getCode())
    print("parser completed")

if __name__ == "__main__":
    main()