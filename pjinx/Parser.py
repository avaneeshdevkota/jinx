from typing import Optional, Callable
from TokenType import TokenType
from Expr import *
from Stmt import *
from Error import JinxParseError

class Parser:

    def __init__(self, tokens : list):

        self.tokens = tokens
        self.current = 0

    def parse(self):

        statements = []

        while (not self.isAtEnd()):

            statement = self.declaration()
            statements.append(statement)

            # try:
            #     statement = self.declaration()
            #     statements.append(statement)
            
            # except:
            #     raise JinxParseError(self.tokens[self.current], "Something has gone very wrong.")

        
        return statements

        # try:
        #     return self.expression()

        # except JinxParseError:
        #     return None

    def expression(self):

        return self.assignment()
    
    def declaration(self):

        try:

            if (self.match(TokenType('var'))):
                return self.varDeclaration()
            
            if (self.match(TokenType('fun'))):
                return self.function("function")
            
            if (self.match(TokenType('class'))):
                return self.classDeclaration()
            
            return self.statement()
        
        except JinxParseError:

            self.synchronize()
            return None
        
    def classDeclaration(self):

        name = self.consume(TokenType('identifier'), "Expect class name.")
        self.consume(TokenType('{'), "Expect '{' before class body.")

        methods = []

        while (not self.check(TokenType('}')) and not self.isAtEnd()):
            methods.append(self.function("method"))
        
        self.consume(TokenType('}'), "Expect '}' after class body.")

        return Class(name, methods)
    
    def statement(self):

        if (self.match(TokenType('print'))):

            return self.printStatement()
        
        if (self.match(TokenType('{'))):

            return Block(self.block())
        
        if (self.match(TokenType('if'))):

            return self.ifStatement()
        
        if (self.match(TokenType('while'))):

            return self.whileStatement()
        
        if (self.match(TokenType('for'))):

            return self.forStatement()
        
        if (self.match(TokenType('return'))):

            return self.returnStatement()

        return self.expressionStatement()
    
    def ifStatement(self):

        self.consume(TokenType('('), "Expect '(' after if.")
        condition = self.expression()
        self.consume(TokenType(')'), "Expect ')' after '('.")

        thenBranch = self.statement()
        elseBranch = None

        if (self.match(TokenType('else'))):
            elseBranch = self.statement()
        
        return If(condition, thenBranch, elseBranch)

    def printStatement(self):

        value = self.expression()
        self.consume(TokenType(';'), "Expect ; after value.")
        return Print(value)
    
    def returnStatement(self):

        keyword = self.previous()
        value = None
        
        if (not self.check(TokenType(';'))):
            value = self.expression()
        
        self.consume(TokenType(';'), "Expect ';' after return value.")
        return Return(keyword, value)
    
    def varDeclaration(self):

        name = self.consume(TokenType('identifier'), "Expect variable name.")
        initializer = None

        if (self.match(TokenType('='))):
            initializer = self.expression()
        
        self.consume(TokenType(';'), "Expect ';' after variable declaration.")
        return Var(name, initializer)
    
    def whileStatement(self):
        
        self.consume(TokenType('('), "Expect '(' after 'while'.")
        condition = self.expression()
        self.consume(TokenType(')'), "Expect, ')' after '('.")
        body = self.statement()

        return While(condition, body)
    
    def forStatement(self):

        self.consume(TokenType('('), "Expect '(' after 'for'.")

        initializer = None

        if (self.match(TokenType(';'))):
            initializer = None
        
        elif (self.match(TokenType('var'))):
            initializer = self.varDeclaration()
        
        else:
            initializer = self.expressionStatement()
        
        condition = None

        if (not self.check(TokenType(';'))):
            condition = self.expression()
        
        self.consume(TokenType(';'), "Expect ';' after loop condition.")

        increment = None
        
        if (not self.check(TokenType(')'))):
            increment = self.expression()
        
        self.consume(TokenType(')'), "Expect ')' after clauses.")

        body = self.statement()

        if (increment != None):
            body = Block([body, Expression(increment)])

        if (condition == None):
            condition = Literal(True)
        
        body = While(condition, body)     

        if (initializer != None):
            body = Block([initializer, body])   

        return body

    def expressionStatement(self):

        expr = self.expression()
        self.consume(TokenType(';'), "Expect ; after value.")

        return Expression(expr)
    
    def function(self, kind):


        name = self.consume(TokenType('identifier'), f"Expect {kind} name.")
        self.consume(TokenType('('), f"Expect '(' after {kind} name.")
        parameters = []

        if (not self.check(TokenType(')'))):
            parameters.append(self.consume(TokenType('identifier'), "Expect parameter name."))
        

        while (self.match(TokenType(','))):

            if (len(parameters) >= 255):
                raise JinxParseError(self.peek(), "Can't have more than 255 parameters.")
        
            parameters.append(self.consume(TokenType('identifier'), "Expect parameter name."))
        
        
        self.consume(TokenType(')'), "Expect ')' after parameters.")

        self.consume(TokenType('{'), "Expect '{' before " + kind + "body.")

        body = self.block()

        return Function(name, parameters, body)


    def block(self):

        statements = []

        while (not self.check(TokenType('}')) and not self.isAtEnd()):
            statements.append(self.declaration())
        
        self.consume(TokenType('}'), "Expect '}' after block.")
        return statements

    def assignment(self):

        expr = self.logicalOr()

        if (self.match(TokenType('='))):

            equals = self.previous()
            value = self.assignment()
        
            if (isinstance(expr, Variable)):
                return Assign(expr.name, value)
            
            elif (isinstance(expr, Get)):
                return Set(expr.obj, expr.name, value)

            self.error(equals, "Invalid assignment target.")

        return expr
    
    def logicalOr(self):

        expr = self.logicalAnd()

        while (self.match(TokenType('or'))):

            operator = self.previous()
            right = self.logicalAnd()
            expr = Logical(expr, operator, right)
        
        return expr
    
    def logicalAnd(self):

        expr = self.equality()

        while (self.match(TokenType('and'))):

            operator = self.previous()
            right = self.equality()
            expr = Logical(expr, operator, right)
        
        return expr

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
        
        return self.call()
    
    def finishCall(self, callee):

        arguments = []

        if (not self.check(TokenType(')'))):

            arguments.append(self.expression())

        while (self.match(TokenType(','))):

            if (len(arguments) >= 255):
                raise JinxParseError(self.peek(), "Can't have more than 255 arguments.")
                
            arguments.append(self.expression())
        
        paren = self.consume(TokenType(')'), "Expect ')' after arguments.")

        return Call(callee, paren, arguments)

    def call(self):

        expr = self.primary()

        while (True):

            if (self.match(TokenType('('))):

                expr = self.finishCall(expr)

            elif (self.match(TokenType('.'))):

                name = self.consume(TokenType('identifier'), "Expect property name after '.'.")
                expr = Get(expr, name)
            
            else:
                break
        
        return expr            

    def primary(self):

        if (self.match(TokenType('false'))):
            return Literal(False)
        
        if (self.match(TokenType('true'))):
            return Literal(True)
    
        if (self.match(TokenType('nil'))):
            return Literal(None)
        
        if (self.match(TokenType('number'), TokenType('string'))):
            return Literal(self.previous().literal)

        if (self.match(TokenType('identifier'))):
            return Variable(self.previous())

        if (self.match(TokenType('('))):

            expr = self.expression()
            self.consume(TokenType(')'), "Expect ')' after '('")
            return Grouping(expr)
        
        if (self.match(TokenType('this'))):
            return This(self.previous())
    
        raise JinxParseError(self.peek(), "Expect expression.")
    
    def match(self, *args):

        for type in args:

            if (self.check(type)):
                self.advance()
                return True
        
        return False
    
    def consume(self, type, message):

        if (self.check(type)):
            return self.advance()
        
        raise JinxParseError(self.peek(), message)
    
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
    




    

