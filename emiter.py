#code generator
class Emiter:
    def __init__(self) -> None:
        self.header = ""
        self.code = ""
    #write a code in the same line
    def emit(self,code):
        self.code += code
    #write code and add new line
    def emitLine(self,code):
        self.code += code + "\n"
    #write header code and add new line
    def headerLine(self,code):
        self.header += code + "\n"
    #returns the final code combined should be called after parssing 
    def getCode(self):
        return self.header+self.code