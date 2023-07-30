from TokenType import TokenType
from Expr import *
from Error import JinxParseError

class Parser:

    def __init__(self, tokens : list):

        self.tokens = tokens
        self.current = 0
        self.hadError = False
    

    def parse(self):

        try:
            return self.expression()

        except JinxParseError:
            return None

    def expression(self):

        return self.equality()

    def equality(self):

        expr = self.comparison()

        while (self.match(TokenType('!='), TokenType('=='))):

            operator = self.previous()
            right = self.comparison()
            expr = Binary(expr, operator, right)
        
        return expr
    
    def comparison(self):

        expr = self.term()

        while (self.match(TokenType('>'), TokenType('>='), TokenType('<'), TokenType('<='),)):

            operator = self.previous()
            right = self.term()
            expr = Binary(expr, operator, right)
        
        return expr

    def term(self):

        expr = self.factor()

        while (self.match(TokenType('-'), TokenType('+'))):

            operator = self.previous()
            right = self.factor()
            expr = Binary(expr, operator, right)
        
        return expr
    
    def factor(self):

        expr = self.unary()

        while (self.match(TokenType('*'), TokenType('/'))):

            operator = self.previous()
            right = self.unary()
            expr = Binary(expr, operator, right)

        return expr


    def unary(self):
        
        if (self.match(TokenType('!'), TokenType('-'))):

            operator = self.previous()
            right = self.unary()

            return Unary(operator, right)

        return self.primary()

    def primary(self):

        if (self.match(TokenType('false'))):
            return Literal(False)
        
        if (self.match(TokenType('true'))):
            return Literal(True)
    
        if (self.match(TokenType('nil'))):
            return Literal(None)
        
        if (self.match(TokenType('number'), TokenType('string'))):
            return Literal(self.previous().literal)

        if (self.match(TokenType('('))):

            expr = self.expression()
            self.consume(TokenType(')'), "Expect ')' after '('")
            return Grouping(expr)
    
        raise self.error(self.peek(), "Expect expression.")

    
    def match(self, *args):

        for type in args:

            if (self.check(type)):
                self.advance()
                return True
        
        return False
    
    def consume(self, type, message):
        
        if (self.check(type)):
            return self.advance()
        
        raise self.error(self.peek(), message)

    def error(self, token, message):

        err = JinxParseError(token, message)
        return err
    
    def synchronize(self):

        self.advance()
        
        while (not self.isAtEnd()):

            if (self.previous().type == TokenType(';')):
                return
            
            if (self.peek().type == TokenType('class')):
                return
            
            if (self.previous().type == TokenType('fun')):
                return
            
            if (self.peek().type == TokenType('var')):
                return

            if (self.previous().type == TokenType('for')):
                return
            
            if (self.peek().type == TokenType('if')):
                return
            
            if (self.previous().type == TokenType('while')):
                return
            
            if (self.peek().type == TokenType('print')):
                return
            
            if (self.previous().type == TokenType('return')):
                return
        
            self.advance()

            

            

    def check(self, type):

        if (self.isAtEnd()):
            return False
    
        return self.peek().type == type
    
    def advance(self):

        if (not self.isAtEnd()):
            self.current += 1
        
        return self.previous()

    def isAtEnd(self):

        return self.peek().type == TokenType('eof')
    
    def peek(self):

        return self.tokens[self.current]
    
    def previous(self):

        return self.tokens[self.current - 1]
    




    

