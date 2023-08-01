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
    

functions_dict = {"clock": Clock()}