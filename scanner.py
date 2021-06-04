from tokentypes import *
from tokens import * 
import sys
class Lexer:
    #inillize soucrce code, number of chrachters in it, current charchter and postion
    def __init__(self,code) -> None:
        self.error = False
        self.sourceCode = code +'\n'
        self.size = len(self.sourceCode)
        self.currentChar = ""
        self.currentPostion = -1
        self.tokenList = []
        self.nxtChar()

    #consume the next charcter of the source code untill you rach the end of the code
    def nxtChar(self):
        self.currentPostion+=1
        if self.currentPostion >= self.size:
            self.currentChar = '\0'
        else:
            self.currentChar = self.sourceCode[self.currentPostion]
    
    #return the next chrachter without consuming it
    def peak(self):
        if self.currentPostion+1>=self.size:
            return '\0'
        else:
            return self.sourceCode[self.currentPostion+1]
    
    #send an error with a message indicating the chracter that caused it
    def abort(self, message):
        print("SWITCHING ERROR!")
        self.error = True
        #sys.exit("scanner error :" + message)
    #skip comments ethier /**/ or //
    def skipComments(self):
        if self.currentChar == '/':
            if self.peak() == '*':
                self.nxtChar()
                self.nxtChar()
                while self.currentChar != '*' and self.peak() !='/':
                    self.nxtChar()
                self.nxtChar()
                self.nxtChar()
                return
            if self.peak() == '/':
                self.nxtChar()
                while self.currentChar != '\n':
                    self.nxtChar()
                return
        if self.currentChar == "{":
            self.nxtChar()
            while self.currentChar != "}":
                self.nxtChar()
            self.nxtChar()
            return
    # moves skips all whitespaces and tabs untill it reaches a chrachter or a number 
    def skipWhitSpaces(self):
        while self.currentChar == " " or self.currentChar == '\t' or self.currentChar == '\r':
            self.nxtChar()
    #return the next token that appears  
    def getToken(self):
        #skip white spaces and comments
        self.skipWhitSpaces()
        while self.currentChar == '{' or (self.currentChar == '/' and self.peak() == '*') or (self.currentChar == '/' and self.peak() == '/'):
            self.skipComments()
            self.skipWhitSpaces()

        token = None
        # single charcters
        if self.currentChar == '\0':
            token = Token(Tokens.EOF,self.currentChar)
        elif self.currentChar == '\n':
            token = Token(Tokens.NEWLINE,"NEW LINE")
        elif self.currentChar == '+':
            token = Token(Tokens.PLUS,self.currentChar)
        elif self.currentChar == '-':
            token = Token(Tokens.MINUS,self.currentChar)
        elif self.currentChar == '/':
            token = Token(Tokens.SLASH,self.currentChar)
        elif self.currentChar == '*':
            token = Token(Tokens.ASTRIX,self.currentChar)
        elif self.currentChar == '%':
            token = Token(Tokens.MOD,self.currentChar)
        elif self.currentChar == '(':
            token = Token(Tokens.LEPRAC,self.currentChar)
        elif self.currentChar == ')':
            token = Token(Tokens.RIPRAC,self.currentChar)
        #elif self.currentChar == '{':
        #    token = Token(Tokens.LEFTPRAN,self.currentChar)
        #elif self.currentChar == '}':
        #    token = Token(Tokens.RIGHTPRAN,self.currentChar)
        elif self.currentChar == ';':
            token = Token(Tokens.SEMICOLON,self.currentChar)
        elif self.currentChar == '=':
            token = Token(Tokens.COMAPRE,self.currentChar) #token.tokenText might be  = or == dependes on implmentation of parser and emiter

        # multiple charchters such as >= and <= ...

        #for charchter >=
        elif self.currentChar == '>':
            cur = self.currentChar
            if self.peak() == '=':
                self.nxtChar()
                token = Token(Tokens.GTEQ,cur+self.currentChar)
            else:
                # evaluates to >
                token = Token(Tokens.GT,self.currentChar)
        
        #for charchters <=
        elif self.currentChar == '<':
            cur  = self.currentChar
            if self.peak() == '=':
                self.nxtChar()
                token = Token(Tokens.LTEQ,cur+self.currentChar)
            else:
                #evalutes <
                token = Token(Tokens.LT,self.currentChar)
        #for charchter !=
        elif self.currentChar == '!':
            cur  = self.currentChar
            if self.peak() == '=':
                self.nxtChar()
                token = Token(Tokens.NOTEQ,cur+self.currentChar)
            else:
                # will abort as ! isnt supported
                self.abort(self.currentChar)
        
        #for charchter :=
        elif self.currentChar == ':':
            cur = self.currentChar
            if self.peak() == '=':
                self.nxtChar()
                token = Token(Tokens.ASSIGN,cur + self.currentChar) #again can be  = or := dependes on the implmentation of parser and emiter
            else:
                # abort as the charchter : isnt supported
                self.abort("unknown symbol - charchter "+ self.currentChar) 
        
        #for string ex: "this is a string"
        elif self.currentChar == '\"':
            self.nxtChar()
            start = self.currentPostion
            while self.currentChar != '\"':
                #dont allow special chatcters in the string
                if self.currentChar == '\t' or self.currentChar == '\n' or self.currentChar == '\\':
                    self.abort(self.currentChar + " is not suported in side of string")
                self.nxtChar()
            string = self.sourceCode[start:self.currentPostion]
            token = Token(Tokens.STRING,string)

        #for identfiers and special charchters
        elif self.currentChar.isalpha():
            start = self.currentPostion
            while self.peak().isalnum():
                self.nxtChar()
            text = self.sourceCode[start:self.currentPostion+1]
            kind = Token.checkIfKeyword(text.upper()) # returns none if the charchter isnt special else returns the charchter type
            if kind == None:
                token = Token(Tokens.IDENT,text)
            else:
                token = Token(kind,text)
        # for numbers could be intgers and floats
        elif self.currentChar.isdigit():
            start = self.currentPostion
            while self.peak().isdigit():
                self.nxtChar()
            if self.peak() == '.': # check if a . exists for float numbers
                self.nxtChar()
                while self.peak().isdigit(): # loop to find digits after the . charchter
                    self.nxtChar()
                token = Token(Tokens.NUMBER,self.sourceCode[start:self.currentPostion+1])
            else:
                token = Token(Tokens.NUMBER,self.sourceCode[start:self.currentPostion+1])
        
        #abort if chrachter doesnt match anything 
        else:
            self.abort("unknown symbol - charchter "+ self.currentChar) 
        self.nxtChar()
        self.tokenList.append(token)
        if(not self.error):
            print(token.tokenText)
            return token
        
