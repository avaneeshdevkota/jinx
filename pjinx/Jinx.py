import sys
from Scanner import Scanner

class Jinx:

    def __init__(self):

        self.args = sys.argv[1:]
        self.n = len(self.args)
        self.hadError = False

    def main(self):

        if (self.n > 1):
            print("Usage : jinx [script]")
            sys.exit(64)
        
        elif (self.n == 1):
            self.runFile(sys.argv[0])
        
        else:
            self.runPrompt()
    
    def runFile(self, path):

        source = ""

        with open(path, "r") as f:
            source += f.read()
        
        self.run(source)

        if (self.getErrorState()):
            sys.exit(65)

    def runPrompt(self):

        while (True):

            try:
                line = input(">>> ")
                self.run(line)
                self.hadError = False

            except EOFError:
                sys.exit() 

    def run(self, source):

        scanner = Scanner(source)
        tokens = scanner.scanTokens()

        for token in tokens:
            print(token)
    
    def getErrorState(self):
        
        self.hadError = Scanner.hadError


if (__name__ == "__main__"):

    jinx = Jinx()
    jinx.main()


