import time
import typing
from JinxCallable import JinxCallable

class Clock(JinxCallable):

    def call(self, interpreter, arguments):

        return time.time()
    
    def arity(self):

        return 0
    
    def __str__(self):

        return "<built-in function>"

class Print(JinxCallable):

    def call(self, interpreter, arguments):

        print(arguments[0])

    def arity(self):

        return 1
    
    def __str__(self):

        return "<built-in function>"

class Input(JinxCallable):
    
    def call(self, interpreter, arguments):

        return input()
    
    def arity(self):

        return 0
        
    def __str__(self):

        return "<built-in function>"

class Len(JinxCallable):

    def call(self, interpreter, arguments):

        return len(arguments[0])
    
    def arity(self):

        return 1
        
    def __str__(self):

        return "<built-in function>"
    

class toString(JinxCallable):

    def call(self, interpreter, arguments):

        return str(arguments[0])
    
    def arity(self):

        return 1
        
    def __str__(self):

        return "<built-in function>"

functions_dict = {"clock": Clock(), "print": Print(), "input": Input(), "len": Len(), "toString": toString()}