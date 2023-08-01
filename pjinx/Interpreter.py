from typing import Optional, Callable
from Expr import *
from Stmt import *
from TokenType import TokenType
from Error import JinxRuntimeError
from Environment import Environment

class Interpreter(ExprVisitor, StmtVisitor):

    def __init__(self):

        self.environment = Environment(None)

    def interpret(self, statements):

        for statement in statements:

            if (statement == None):
                continue
            
            self.execute(statement)
        # try:

        # value = self.evaluate(expression)
        # print(self.toString(value))

        # except JinxRuntimeError:
        #     return None
    
    def toString(self, val):

        if (val == None):

            return 'nil'
        
        if (isinstance(val, float)):

            res = str(val)

            if (res.endswith('.0')):
                res = res[0 : len(res) - 2]
            
            return res
        
        return str(val)

    def visit_Binary_Expr(self, expr: Binary):

        left = self.evaluate(expr.left)
        right = self.evaluate(expr.right)

        if (expr.operator.type == TokenType('+')):

            if (isinstance(left, float) and isinstance(right, float)):

                return float(left) + float(right)
            
            if (isinstance(left, str) and isinstance(right, str)):
                return left + right
        
            raise JinxRuntimeError(expr.operator, "Operands must be both numbers or both strings.")

        if (expr.operator.type == TokenType('-')):

            if (isinstance(left, float) and isinstance(right, float)):
                return float(left) - float(right)
            
            else:
                raise JinxRuntimeError(expr.operator, "Operands must be numbers.")
        
        if (expr.operator.type == TokenType('*')):

            if (isinstance(left, float) and isinstance(right, float)):
                return float(left) * float(right)
            
            if (isinstance(left, str) and isinstance(right, float)):

                result = ""

                for i in range(int(right)):
                    result += left
                
                return result
            
            if (isinstance(left, float) and isinstance(right, str)):

                result = ""

                for i in range(int(left)):
                    result += right
                
                return result

            raise JinxRuntimeError(expr.operator, "Operands must be both numbers or one string and one number.")

        if (expr.operator.type == TokenType('/')):

            if (isinstance(left, float) and isinstance(right, float)):
                return left/right
            
            else:
                raise JinxRuntimeError(expr.operator, "Operands must be numbers.")
        
        if (expr.operator.type == TokenType('>')):

            if (isinstance(left, str) and isinstance(right, str)):
                return left > right
            
            if (isinstance(left, float) and isinstance(right, float)):
                return left > right
        
        if (expr.operator.type == TokenType('>=')):

            if (isinstance(left, str) and isinstance(right, str)):
                return left >= right
            
            if (isinstance(left, float) and isinstance(right, float)):
                return left >= right
        
        if (expr.operator.type == TokenType('<')):

            if (isinstance(left, str) and isinstance(right, str)):
                return left < right
            
            if (isinstance(left, float) and isinstance(right, float)):
                return left < right
        
        if (expr.operator.type == TokenType('<=')):

            if (isinstance(left, str) and isinstance(right, str)):
                return left <= right
            
            if (isinstance(left, float) and isinstance(right, float)):
                return left <= right
            
        if (expr.operator.type == TokenType('!=')):

            return not self.isEqual(left, right)
        
        if (expr.operator.type == TokenType('==')):

            return self.isEqual(left, right)
            
    def visit_Grouping_Expr(self, expr: Grouping):

        return self.evaluate(expr.expr)

    def visit_Literal_Expr(self, expr: Literal):

        return expr.value
    
    def visit_Logical_Expr(self, expr : Logical):

        left = self.evaluate(expr.left)
        
        if (expr.operator.type == TokenType('or')):

            if (self.isTrue(left)):
                return left

        else:
            if (not self.isTrue(left)):
                return left
        
        return self.evaluate(expr.right)
            

    def visit_Unary_Expr(self, expr: Unary):

        right = self.evaluate(expr.right)

        if (expr.operator.type == TokenType('!')):
            return not self.isTrue(right)
    
        if (expr.operator.type == TokenType('-')):

            if (isinstance(right, float)):
                return -float(expr.right.value)
            
            else:
                raise JinxRuntimeError(expr.operator, "Operand must be a number.")
    
        return None
    
    def visit_Variable_Expr(self, expr: Variable):

        return self.environment.get(expr.name)
    
    def visit_Expression_Stmt(self, stmt: Expression):

        self.evaluate(stmt.expr)
        return None
    
    def visit_If_Stmt(self, stmt : If):

        if (self.isTrue(self.evaluate(stmt.condition))):
            self.execute(stmt.thenBranch)

        elif (stmt.elseBranch != None):
            self.execute(stmt.elseBranch)
        
        return None
    
    def visit_Print_Stmt(self, stmt: Print):

        value = self.evaluate(stmt.expr)
        print(self.toString(value))
        return None
    
    def visit_Var_Stmt(self, stmt: Var):

        value = None

        if (stmt.initializer != None):
            value = self.evaluate(stmt.initializer)
        
        self.environment.define(stmt.name.lexeme, value)
        return None
    
    def visit_While_Stmt(self, stmt : While):

        while (self.isTrue(self.evaluate(stmt.condition))):
            self.execute(stmt.body)
        
        return None
    
    def visit_Assign_Expr(self, expr: Assign):

        value = self.evaluate(expr.value)
        self.environment.assign(expr.name, value)
        return value
    
    def visit_Block_Stmt(self, stmt: Block):

        self.executeBlock(stmt.statements, Environment(self.environment))
        return None
    
    def isTrue(self, expr):

        if (expr == None):
            return False
        
        if (isinstance(expr, bool)):
            return bool(expr)
        
        return True
    
    def isEqual(self, left, right):

        if (left == None and right == None):
            return True
        
        if (left == None or right == None):
            return False
        
        return left == right
        
    def evaluate(self, expr):

        return expr.accept(self)
    
    def execute(self, stmt):

        return stmt.accept(self)
    
    def executeBlock(self, statements, environment):

        previousEnvironment = self.environment

        try:
            self.environment = environment

            for statement in statements:
                self.execute(statement)

        finally:
            self.environment = previousEnvironment
    
    def error(self, token, message):

        err = JinxRuntimeError(token, message)
        return err
    

