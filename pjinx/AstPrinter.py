from typing import Any
from TokenType import TokenType
from Token import Token as T
from Expr import *

class AstPrinter(ExprVisitor):

    def visit_Binary_Expr(self, expr: Binary):
        return self.parenthesize(expr.operator.lexeme, expr.left, expr.right)
    
    def visit_Grouping_Expr(self, expr: Grouping):
        return self.parenthesize("group", expr.expr)
    
    def visit_Literal_Expr(self, expr: Literal):
        if (expr.value == None):
            return "nil"
        return str(expr.value)
    
    def visit_Unary_Expr(self, expr: Unary):
        return self.parenthesize(expr.operator.lexeme, expr.right)

    def main(self):

        expression = Binary(
            Unary(T(TokenType('-'), "-", None, 1), Literal(123)),
            T(TokenType('*'), "*", None, 1),
            Grouping(Literal(45.67))
        )
        
        print(self.print(expression))

    def print(self, expr: "Expr") -> str:
        return expr.accept(self)
    

    def parenthesize(self, name, *args):

        s = f"( {name}"

        for arg in args:
            s += " " + arg.accept(self)
        
        s += ")"
        return s

printer = AstPrinter()
printer.main()