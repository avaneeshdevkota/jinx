from TokenType import TokenType
from Token import Token

class Scanner:

    def __init__(self, source):

        self.source = source
        self.tokens = []
        self.start = 0
        self.current = 0
        self.line = 1

        self.hadError = False

    def isAtEnd(self):

        return self.current >= len(self.source)

    def peek(self):

        if (self.isAtEnd()):
            return '/0'
        
        return self.source[self.current]

    def peekNext(self):

        if (self.current + 1 >= len(self.source)):
            return '\0'

        return self.source[self.current + 1]
    
    def advance(self):

        self.current += 1
        return self.source[self.current - 1]

    def match(self, ch):

        if (self.isAtEnd()):
            return False
    
        if (self.source[self.current] != ch):
            return False
        
        self.current += 1
        return True
    
    def error(self, line, message):

        self.report(line, "", message)
    
    def report(self, line, where, message):

        print(f"[Line {line}] Error {where} : {message}")
        self.hadError = True

    def add(self, type):

        self.addToken(type, None)
    
    def addToken(self, type, literal):

        text = self.source[self.start : self.current]
        self.tokens.append(Token(type, text, literal, self.line))
    
    def string(self):

        while (self.peek() != '"' and not self.isAtEnd()):

            if (self.peek() == '\n'):
                self.line += 1

            self.advance()
        
        if (self.isAtEnd()):

            self.error(self.line, "Unterminated string.")
            return
        
        self.advance()

        value = self.source[self.start + 1 : self.current - 1]
        self.addToken(TokenType('string'), value)
    
    def number(self):

        while (self.peek().isdigit()):
            self.advance()

        if (self.peek() == '.' and self.peekNext().isdigit()):

            self.advance()
            while (self.peek().isdigit()):
                self.advance()
        
        self.addToken(TokenType('number'), float(self.source[self.start : self.current]))
    
    def identifier(self):

        while (self.peek().isalnum()):
            self.advance()

        text = self.source[self.start : self.current]

        try:
            self.add(TokenType(text))

        except ValueError:
            self.add(TokenType('identifier'))
    
    def scanToken(self):

        ch = self.advance()

        ignore = [' ', '\r', '\t']
        singleCharTokens = ['(', ')', '{', '}', ',', '.', '-', '+', '*', '/', ';']

        if (ch in singleCharTokens):
            self.add(TokenType(ch))
        
        elif (ch == '!'):
            self.add(TokenType('!=') if self.match('=') else TokenType('!'))
        
        elif (ch == '='):
            self.add(TokenType('==') if self.match('=') else TokenType('='))
        
        elif (ch == '<'):
            self.add(TokenType('<=') if self.match('=') else TokenType('<'))

        elif (ch == '>'):
            self.add(TokenType('>=') if self.match('=') else TokenType('>'))
        
        elif (ch == '#'):
            while (self.peek() != '\n' and not self.isAtEnd()) :
                self.advance()
        
        elif (ch == '"'):
            self.string()
        
        elif (ch == '\n'):
            self.line += 1

        else:

            if (ch.isdigit()):
                self.number()

            elif (ch.isalpha()):
                self.identifier()
            
            elif (ch not in ignore):
                
                self.error(self.line, "Unexpected character")

    def scanTokens(self):

        while (not self.isAtEnd()):

            self.start = self.current
            self.scanToken()
        
        self.tokens.append(Token(TokenType.EOF, "", None, self.line))
        return self.tokens
    
