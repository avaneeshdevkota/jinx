import typing
from Token import Token
from Expr import *
from Stmt import *
from Error import *
from FunctionType import FunctionType, ClassType

class Resolver(ExprVisitor, StmtVisitor):

    def __init__(self, interpreter):

        self.interpreter = interpreter
        self.scopes = []
        self.currentFunction = FunctionType('none')
        self.currentClass = ClassType('none')

    def visit_Block_Stmt(self, stmt: Block):

        self.beginScope()
        self.resolve(stmt.statements)
        self.endScope()
        
        return None
    
    def visit_Class_Stmt(self, stmt: Class):

        enclosingClass = self.currentClass
        self.currentClass = ClassType('class')

        self.declare(stmt.name)
        self.define(stmt.name)

        self.beginScope()
        self.scopes[-1]["this"] = True

        for method in stmt.methods:

            declaration = FunctionType('method')

            if (method.name.lexeme == "init"):
                declaration = FunctionType('method')

            self.resolveFunction(method, declaration)

        self.endScope()

        self.currentClass = enclosingClass
        return None
    
    def visit_Expression_Stmt(self, stmt: Expression):

        self.resolve(stmt.expr)
        return None
    
    def visit_Function_Stmt(self, stmt: Function):

        self.declare(stmt.name)
        self.define(stmt.name)

        self.resolveFunction(stmt, FunctionType('function'))
        return None
    
    def visit_If_Stmt(self, stmt: If):

        self.resolve(stmt.condition)
        self.resolve(stmt.thenBranch)

        if (stmt.elseBranch != None):
            self.resolve(stmt.elseBranch)
        
        return None
    
    def visit_Print_Stmt(self, stmt: Print):

        self.resolve(stmt.expr)
        return None
    
    def visit_Return_Stmt(self, stmt: Return):

        if (self.currentFunction == FunctionType('none')):
            raise JinxException(stmt.keyword.line, "Can't return from top-level code.")

        if (stmt.value != None):
            
            if (self.currentFunction == FunctionType('initializer')):
                raise JinxException(stmt.keyword.line, "Can't return a value from an initializer.")
            
            self.resolve(stmt.value)
        
        return None
    
    def visit_Var_Stmt(self, stmt: Var):

        self.declare(stmt.name)

        if (stmt.initializer != None):
            self.resolve(stmt.initializer)
        
        self.define(stmt.name)
        return None
    
    def visit_While_Stmt(self, stmt: While):

        self.resolve(stmt.condition)
        self.resolve(stmt.body)

        return None
    
    def visit_Assign_Expr(self, expr: Assign):

        self.resolve(expr.value)
        self.resolveLocal(expr, expr.name)
        return None
    
    def visit_Binary_Expr(self, expr: Binary):

        self.resolve(expr.left)
        self.resolve(expr.right)
        return None
    
    def visit_Call_Expr(self, expr: Call):

        self.resolve(expr.callee)

        for arg in expr.arguments:
            self.resolve(arg)
        
        return None
    
    def visit_Get_Expr(self, expr: Get):

        self.resolve(expr.obj)
        return None
    
    def visit_Grouping_Expr(self, expr: Grouping):

        self.resolve(expr.expr)
        return None
    
    def visit_Literal_Expr(self, expr: Literal):

        return None
    
    def visit_Logical_Expr(self, expr: Logical):

        self.resolve(expr.left)
        self.resolve(expr.right)

        return None
    
    def visit_Set_Expr(self, expr: Set):

        self.resolve(expr.value)
        self.resolve(expr.obj)
        return None
    
    def visit_This_Expr(self, expr: This):

        if (self.currentClass == ClassType('none')):
            raise JinxException(expr.keyword.line, "Can't use 'this' outside of a class.")

        self.resolveLocal(expr, expr.keyword)
        return None
    
    def visit_Unary_Expr(self, expr: Unary):

        self.resolve(expr.right)
        return None


    def visit_Variable_Expr(self, expr: Variable):

        if (self.scopes and self.scopes[-1].get(expr.name.lexeme, None) == False):
            raise JinxException(expr.name.line, "Can't read local variable in its own initializer.")
        
        self.resolveLocal(expr, expr.name)
        return None
        
    def resolve(self, se):

        if (isinstance(se, list)):

            for stmt in se:
                self.resolve(stmt)
        
        else:
            se.accept(self)

    def resolveFunction(self, function : Function, type):


        enclosingFunction = self.currentFunction
        self.currentFunction = type

        self.beginScope()

        for param in function.params:

            self.declare(param)
            self.define(param)
        
        self.resolve(function.body)

        self.endScope()
        self.currentFunction = enclosingFunction
    
    def beginScope(self):

        self.scopes.append({})

    def endScope(self):

        self.scopes.pop()

    def declare(self, name : Token):

        if (not self.scopes):
            return
        
        scope = self.scopes[-1]

        if (name.lexeme in scope.keys()):
            raise JinxException(name.line, "Already a variable with this name in scope.")
        
        scope[name.lexeme] = False

    def define(self, name : Token):

        if (not self.scopes):
            return 
        
        self.scopes[-1][name.lexeme] = True
    
    def resolveLocal(self, expr : Expr, name : Token):

        for i in range(len(self.scopes)-1, -1, -1):
            if (name.lexeme in self.scopes[i].keys()):
                self.interpreter.resolve(expr, len(self.scopes) - 1 - i)
                return
