from Token import Token

class JinxException(BaseException):

    def __init__(self, line : int , message : str):
        
        self.line = line
        self.message = message

class JinxSyntaxError(JinxException):

    ...

class JinxParseError(JinxException):

    def __init__(self, token : Token, message : str):

        self.line = token.line
        self.message = message

class JinxRuntimeError(JinxException):

    def __init__(self, token : Token, message : str):

        self.line = token.line
        self.message = message