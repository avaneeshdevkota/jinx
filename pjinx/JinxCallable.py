from abc import ABC, abstractmethod

class JinxCallable(ABC):

    @abstractmethod
    def arity(self):
        self.arity = None

    @abstractmethod
    def call(self, interpreter, arguments):
        pass