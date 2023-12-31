from JinxCallable import *
from Environment import Environment
from Return import Return

class JinxFunction(JinxCallable):

    def __init__(self, declaration, closure, isInitializer):

        self.declaration = declaration
        self.closure = closure
        self.isInitializer = isInitializer
    
    def bind(self, instance):

        env = Environment(self.closure)
        env.define("this", instance)

        return JinxFunction(self.declaration, env, self.isInitializer)
    
    def call(self, interpreter, arguments):

        environment = Environment(self.closure)

        for i in range(len(self.declaration.params)):
            environment.define(self.declaration.params[i].lexeme, arguments[i])

        try:
            interpreter.executeBlock(self.declaration.body, environment)
        
        except Return as return_value:

            if (self.isInitializer):
                return self.closure.getAt(0, "this")
            
            return return_value.value
        
        if (self.isInitializer):
            return self.closure.getAt(0, "this")

        return None
    
    def arity(self):

        return len(self.declaration.params)