from JinxCallable import *
from Environment import Environment

class JinxFunction(JinxCallable):

    def __init__(self, declaration):

        self.declaration = declaration
    
    def call(self, interpreter, arguments):

        environment = Environment(interpreter.globals)

        for i in range(len(self.declaration.params)):
            environment.define(self.declaration.params[i].lexeme, arguments[i])
        
        interpreter.executeBlock(self.declaration.body, environment)
        return None
    
    def arity(self):

        return len(self.declaration.params)
    
    # def __str__(self):

    #     return f"<fn {self.declaration.name}>"