from scanner import *
from emiter import *
from tokentypes import *
import sys
class Parser:
    
    # constructor
    def __init__(self,scanner,emiter) -> None:
        self.scanner = scanner
        self.emiter = emiter
        self.curToken = None
        self.peekToken =None
        self.symbols = set()
        self.labelsDeclared = set()
        #self.labelsgotoed = set()
        self.nextToken()
        self.nextToken()

    # abort case of an error
    def abort(self,message):
        sys.exit("Parser error "+ message)


    #checks with kind  == curtoken kind
    def checkToken(self,kind):
        return kind == self.curToken.tokenKind
    #checks with kind  == peak kind
    def checkPeak(self,kind):
        return kind == self.peekToken.tokenKind

    #force a token to match a type --if not abort else get next token 
    def match(self, kind):
        if not self.checkToken(kind):
            self.abort("Expected " + kind.name + ", got " + self.curToken.tokenKind.name)
        self.nextToken()   

    def nextToken(self):
        self.curToken = self.peekToken
        self.peekToken = self.scanner.getToken()


    def program(self):
        #headers for any program
        self.emiter.headerLine("#include<stdio.h>")
        self.emiter.headerLine("int main(void){")

        #exsaust all the new lines 
        while self.checkToken(Tokens.NEWLINE):
            self.nextToken()

        #main loop for checking staments
        while not self.checkToken(Tokens.EOF):
            self.statment()
        #needed for any c program    
        self.emiter.emitLine("return 0 ;")
        self.emiter.emitLine("}")

        #for label in self.labelsgotoed:
        #    if label not in self.labelsDeclared:
        #        self.abort("Attempting to GOTO to undeclared label: " + label)

    def statment(self):
        #print stament 
        if self.checkToken(Tokens.WRITE):
            self.nextToken()
            #string
            if self.checkToken(Tokens.STRING):
                self.emiter.emitLine("printf(\""+self.curToken.tokenText+"\\n\");")
                self.nextToken()
            # number or identfier
            else:
                self.emiter.emit("printf(\"%" + ".2f\\n\", (float)(")
                self.expersion()
                self.emiter.emitLine("));")
            self.match(Tokens.SEMICOLON)
            
        # if conditions
        elif self.checkToken(Tokens.IF):
            self.nextToken()
            self.emiter.emit("if(")
            self.comaprison()
            self.match(Tokens.THEN)
            self.nlPlus()
            self.emiter.emitLine("){")
            while not self.checkToken(Tokens.END):
                self.statment()
            self.match(Tokens.END)
            self.emiter.emitLine("}")
            self.nlPlus()

        #loops repeat - until #not sure
        elif self.checkToken(Tokens.REPEAT):
            self.nextToken()
            self.emiter.emitLine("do\n{")
            self.nl()
            while not self.checkToken(Tokens.UNTIL):
                self.statment()
            self.emiter.emitLine("}")
            self.match(Tokens.UNTIL)
            self.emiter.emit("while(!(")
            self.comaprison()
            self.emiter.emitLine("));")
            self.nlPlus()
            


        #loops repeat - until    
        #elif self.checkToken(Tokens.REPEAT):
        #   self.nextToken()
        #    self.emiter.emit("while(")
        #    self.comaprison()
        #    self.match(TokenTypes.REPEAT)
        #    self.nl()
        #    self.emiter.emitLine("){")
        #    while not self.checkToken(TokenTypes.ENDWHILE):
        #        self.statment()
        #    self.match(TokenTypes.ENDWHILE)
        #    self.emiter.emitLine("}")

        #elif self.checkToken(TokenTypes.LABEL):
        #    self.nextToken()
        #    if self.curToken.tokenText in self.labelsDeclared:
        #        self.abort("Label already exists: " + self.curToken.text)
        #    self.labelsDeclared.add(self.curToken.tokenText)
        #    self.emiter.emitLine(self.curToken.tokenText+":")
        #    self.match(TokenTypes.IDENT)


        #elif self.checkToken(TokenTypes.GOTO):
        #    self.nextToken()
        #    self.labelsgotoed.add(self.curToken.tokenText)
        #    self.emiter.emitLine("goto:"+self.curToken.tokenText+";")
        #    self.match(TokenTypes.IDENT)

        #assining variables
        elif self.checkToken(Tokens.IDENT):
            if self.curToken.tokenText not in self.symbols:
                self.symbols.add(self.curToken.tokenText)
                self.emiter.headerLine("float "+self.curToken.tokenText+";")
            self.emiter.emit(self.curToken.tokenText+"=")
            self.nextToken()
            self.match(Tokens.ASSIGN)
            self.expersion()
            self.match(Tokens.SEMICOLON)
            self.emiter.emitLine(";")
        
        elif self.checkToken(Tokens.READ):
            self.nextToken()
            if self.curToken not in self.symbols:
                self.symbols.add(self.curToken.tokenText)
                self.emiter.headerLine("float "+ self.curToken.tokenText+";")
            self.emiter.emitLine("if(0 == scanf(\"%" + "f\", &" + self.curToken.tokenText + ")) {")
            self.emiter.emitLine(self.curToken.tokenText + " = 0;")
            self.emiter.emit("scanf(\"%")
            self.emiter.emitLine("*s\");")
            self.emiter.emitLine("}")
            self.match(Tokens.IDENT)
            self.match(Tokens.SEMICOLON)
        else :
            self.abort("Invalid statement at " + self.curToken.tokenText + " (" + self.curToken.tokenKind.name + ")")
        self.nl()


    def comaprison(self):
        self.expersion()
        if self.checkComparison():
            if self.checkToken(Tokens.COMAPRE):
                self.emiter.emit(" == ")
            else:
                self.emiter.emit(self.curToken.tokenText)
            self.nextToken()
            self.expersion()
        else:
            self.abort("Expected comparison operator at: " + self.curToken.text)
        while self.checkComparison():
            if self.checkToken(Tokens.COMAPRE):
                self.emiter.emit(" == ")
            else:
                self.emiter.emit(self.curToken.tokenText)
            self.nextToken()
            self.expersion()
    def checkComparison(self):
        if self.checkToken(Tokens.COMAPRE) or self.checkToken(Tokens.NOTEQ) or self.checkToken(Tokens.GT) or self.checkToken(Tokens.GTEQ) or self.checkToken(Tokens.LT) or self.checkToken(Tokens.LTEQ):
            return True
        else:
            return False


    def expersion(self):
        self.term()
        while self.checkToken(Tokens.PLUS) or self.checkToken(Tokens.MINUS):
            self.emiter.emit(self.curToken.tokenText)
            self.nextToken()
            self.term()


    def term(self):
        self.uniry()

        while self.checkToken(Tokens.SLASH) or self.checkToken(Tokens.ASTRIX):
            self.emiter.emit(self.curToken.tokenText)
            self.nextToken()
            self.uniry()

    def uniry(self):
        if self.checkToken(Tokens.PLUS) or self.checkToken(Tokens.MINUS):
            self.emiter.emit(self.curToken.tokenText)
            self.nextToken()
        self.primary()

    def primary(self):
        if self.checkToken(Tokens.NUMBER):
            self.emiter.emit(self.curToken.tokenText)
            self.nextToken()
        elif self.checkToken(Tokens.IDENT):
            if self.curToken.tokenText not in self.symbols:
                self.abort("Referencing variable before assignment: " + self.curToken.tokenText)
            self.emiter.emit(self.curToken.tokenText)
            self.nextToken()
        else:
            self.abort("Unexpected token at " + self.curToken.tokenText)
    
    def nlPlus(self):
        self.match(Tokens.NEWLINE)
        while self.checkToken(Tokens.NEWLINE):
            self.nextToken()
    def nl(self):
        #self.match(TokenTypes.NEWLINE)
        while self.checkToken(Tokens.NEWLINE):
            self.nextToken()