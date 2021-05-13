from tokentypes import *
from tokens import * 
import sys
class Lexer:
    #inillize soucrce code, number of chrachters in it, current charchter and postion
    def __init__(self,code) -> None:
        self.sourceCode = code +'\n'
        self.size = len(self.sourceCode)
        self.currentChar = ""
        self.currentPostion = -1
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
        sys.exit("scanner error :" + message)
    #skip comments until...
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
    
    def skipWhitSpaces(self):
        while self.currentChar == " " or self.currentChar == '\t' or self.currentChar == '\r':
            self.nxtChar()
    #return the next token that appears  
    def getToken(self):
        self.skipWhitSpaces()
        self.skipComments()
        token = None
        if self.currentChar == '\0':
            token = Token(Tokens.EOF,self.currentChar)
        elif self.currentChar == '\n':
            token = Token(Tokens.NEWLINE,self.currentChar)
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
        elif self.currentChar == '{':
            token = Token(Tokens.LEFTPRAN,self.currentChar)
        elif self.currentChar == '}':
            token = Token(Tokens.RIGHTPRAN,self.currentChar)
        elif self.currentChar == ';':
            token = Token(Tokens.SEMICOLON,self.currentChar)
        elif self.currentChar == '=':
            token = Token(Tokens.COMAPRE,"==") #token.tokenText might be  = or == dependes on implmentation of parser and emiter

        elif self.currentChar == '>':
            cur = self.currentChar
            if self.peak() == '=':
                self.nxtChar()
                token = Token(Tokens.GTEQ,cur+self.currentChar)
            else:
                token = Token(Tokens.GT,self.currentChar)
        elif self.currentChar == '<':
            cur  = self.currentChar
            if self.peak() == '=':
                self.nxtChar()
                token = Token(Tokens.LTEQ,cur+self.currentChar)
            else:
                token = Token(Tokens.LT,self.currentChar)
        elif self.currentChar == '!':
            cur  = self.currentChar
            if self.peak() == '=':
                self.nxtChar()
                token = Token(Tokens.NOTEQ,cur+self.currentChar)
            else:
                self.abort(self.currentChar)
        else:
            self.abort("unknown symbol - charchter "+ self.currentChar)
        self.nxtChar()
        return token
