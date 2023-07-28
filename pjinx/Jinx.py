import sys
from Scanner import Scanner
from TokenType import TokenType

class Jinx:

    hadError = False

    def main(self):

        sys.argv = sys.argv[1:]
        n = len(sys.argv)

        if (n > 1):
            print("Usage : jinx [script]")
            sys.exit(64)
        
        elif (n == 1):
            self.runFile(sys.argv[0])
        
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

    def run(self, source):

        scanner = Scanner(source)
        tokens = scanner.scanTokens()

        for token in tokens:
            print(token)
    
    def error(self, line, message):

        self.report(line, "", message)
    
    def report(self, line, where, message):
        
        print(f"[Line {line}] Error {where}: {message}")
        self.hadError = True

if (__name__ == "__main__"):
    
    jinx = Jinx()
    jinx.main()


