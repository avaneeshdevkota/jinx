from Error import *

class JinxInstance:

    def __init__(self, jclass):

        self.jclass = jclass
        self.fields = {}

    def get(self, name):

        if name.lexeme in self.fields.keys():
            return self.fields[name.lexeme]
        
        method = self.jclass.findMethod(name.lexeme)

        if (method != None):
            return method.bind(self)
        
        raise JinxRuntimeError(name, f"Undefined property {name.lexeme}. ")
    
    def set(self, name, value):
        
        self.fields[name.lexeme] = value
    
    def __str__(self):

        return f"<{self.jclass.name} instance>"