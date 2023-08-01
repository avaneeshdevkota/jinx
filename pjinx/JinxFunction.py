from JinxCallable import *
from Environment import Environment
from Return import Return

class JinxFunction(JinxCallable):

    def __init__(self, declaration):

        self.declaration = declaration
    
    def call(self, interpreter, arguments):

        environment = Environment(interpreter.globals)

        for i in range(len(self.declaration.params)):
            environment.define(self.declaration.params[i].lexeme, arguments[i])

        try:
            interpreter.executeBlock(self.declaration.body, environment)
        
        except Return as return_value:
            return return_value.value
        
        return None
    
    def arity(self):

        return len(self.declaration.params)