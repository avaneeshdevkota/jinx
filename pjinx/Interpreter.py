from typing import Optional, Callable
from Expr import *
from TokenType import TokenType
from Error import JinxRuntimeError

class Interpreter(ExprVisitor):

    def __init__(self):

        pass

    def interpret(self, expression):

        # try:

        value = self.evaluate(expression)
        print(self.toString(value))

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
    
    def error(self, token, message):

        err = JinxRuntimeError(token, message)
        return err
    

