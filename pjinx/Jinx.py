import sys
from Scanner import Scanner
from Parser import Parser
from Interpreter import Interpreter
from Error import JinxException, JinxSyntaxError, JinxParseError, JinxRuntimeError

class Jinx:

    def __init__(self):

        self.args = sys.argv[1:]
        self.n = len(self.args)

        self.interpreter = Interpreter()
        
        self.hadError = False
        self.hadRuntimeError = False

    def main(self):

        if (self.n > 1):
            print("Usage : jinx [script]")
            sys.exit(64)
        
        elif (self.n == 1):
            self.runFile(self.args[0])
        
        else:
            self.runPrompt()
    
    def runFile(self, path):

        source = ""

        with open(path, "r") as f:
            source += f.read()
        
        self.run(source)

        if (self.hadError):
            sys.exit(65)

    def runPrompt(self):

        while (True):

            try:         
                line = input(">>> ")
                self.run(line)
                self.hadError = False

            except EOFError:
                sys.exit()

            except KeyboardInterrupt:
                sys.exit()

    def run(self, source):

        try:
            scanner = Scanner(source)
            tokens = scanner.scanTokens()

            parser = Parser(tokens)
            statements = parser.parse()

            if (self.hadError):
                return

            self.interpreter.interpret(statements)
        
        except (JinxSyntaxError, JinxParseError) as e:
            self.reportError(e)
        
        except JinxRuntimeError as e:
            self.reportRuntimeError(e)
        
    def reportError(self, err: JinxException) -> None:

        print(f"[Line {err.line}]: {err.message}")
        self.hadError = True
    
    def reportRuntimeError(self, err : JinxRuntimeError) -> None:

        print(f"[Line {err.line}]: {err.message}")
        self.hadError = True
        self.hadRuntimeError = True

if (__name__ == "__main__"):

    jinx = Jinx()
    jinx.main()


