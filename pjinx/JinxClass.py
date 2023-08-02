from JinxCallable import JinxCallable
from JinxInstance import JinxInstance

class JinxClass(JinxCallable):

    def __init__(self, name, superclass, methods):

        self.name = name
        self.superclass = superclass
        self.methods = methods

    def findMethod(self, name):

        if (name in self.methods.keys()):
            return self.methods[name]
        
        if (self.superclass != None):
            return self.superclass.findMethod(name)
        
        return None

    def arity(self):

        initializer = self.findMethod("init")

        if (initializer == None):
            return 0
        
        return initializer.arity()

    def call(self, interpreter, arguments):

        instance = JinxInstance(self)
        initializer = self.findMethod("init")

        if (initializer != None):
            initializer.bind(instance).call(interpreter, arguments)

        return instance
    
    def __str__(self):
        return self.name