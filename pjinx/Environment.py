from Error import JinxRuntimeError
from Token import Token

class Environment:

    def __init__(self, enclosing):
        
        self.enclosing = enclosing
        self.var_map = {}

    def define(self, name, value):

        self.var_map[name] = value

    def get(self, name : Token):

        if (name.lexeme in self.var_map.keys()):

            return self.var_map[name.lexeme]
        
        if (self.enclosing != None):

            return self.enclosing.get(name)
        
        raise JinxRuntimeError(name, f"Undefined variable {name.lexeme}.")

    def assign(self, name : Token, value):

        if (name.lexeme in self.var_map.keys()):

            self.var_map[name.lexeme] = value
            return 
        
        if (self.enclosing != None):

            self.enclosing.assign(name, value)
            return
        
        raise JinxRuntimeError(name, f"Undefined variable {name.lexeme}.")
        


        
    


    
