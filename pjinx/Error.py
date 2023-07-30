from Token import Token

class JinxException(BaseException):

    def __init__(self, line : int , message : str):
        self.line = line
        self.message = message
    
    def __str__(self):

        print(f"[Line {self.line}] Error : {self.message}")
    

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