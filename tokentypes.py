import enum

class Tokens(enum.Enum):
    #data values and identfier
    EOF = -1
    NEWLINE = 0
    NUMBER = 1
    STRING = 3
    IDENT = 4
    #keywords
    WRITE = 101
    READ  = 102
    IF  = 103
    ELSE = 104
    RETURN  = 105
    END  = 107
    MAIN = 108
    INT = 109
    REAL = 110
    THEN = 111
    REPEAT = 112
    UNTIL = 113
    TRUE = 114
    FALSE = 115
    #operations
    ASSIGN = 201
    GT  = 202
    GTEQ = 203
    LT = 204
    LTEQ = 205
    NOTEQ = 206
    COMAPRE = 207
    #symbols
    LEFTPRAN = 301
    RIGHTPRAN = 302
    PLUS = 303
    MINUS = 304
    ASTRIX = 306
    SLASH = 307
    LEPRAC = 308
    RIPRAC = 309
    SEMICOLON = 310
    MOD = 311
     
