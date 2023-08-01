import os
import sys

if (len(sys.argv) != 2):

    print("Usage: python3 GenerateAst.py output_directory")
    sys.exit(64)

outputDir = sys.argv[1]

def defineAst(outputDir, baseName, types):

    path = os.path.join(outputDir, baseName + ".py")

    with open(path, "w") as file:

        file.write('import typing\n')
        file.write('from abc import ABC, abstractmethod\n')
        file.write('import Token\n')

        if (baseName == "Stmt"):
            file.write('from Expr import *\n')
        
        file.write('\n')

        defineVisitor(file, baseName, types)

        file.write(f'class {baseName}:\n\n')
        file.write(f"\tdef __init__(self): \n")
        file.write(f"\t\tpass\n\n")

        file.write(f"\t@abstractmethod\n")
        file.write(f"\tdef accept(self, visitor: {baseName}Visitor) -> typing.Any:\n")
        file.write(f"\t\tpass\n\n")

        for className, fields in types.items():

            file.write('\n')
            defineType(file, baseName, className, fields)
        
        file.write('\n')

def defineVisitor(file, baseName, types):

    visitor = f"{baseName}Visitor"
    file.write(f"class {visitor}(ABC):\n\n")

    for type in types:
        
        file.write('\t@abstractmethod\n')
        file.write(f'\tdef visit_{type}_{baseName}(self, {baseName}: "{type}") -> typing.Any:\n')
        file.write('\t\tpass\n\n')

    file.write("\n")

def defineType(file, baseName, className, fields):

    file.write(f"class {className}({baseName}):\n\n")
    file.write(f"\tdef __init__(self, {', '.join(fields)}):\n")
    file.write(f"\t\tsuper().__init__()\n\n")

    for field in fields:  
        file.write(f"\t\tself.{field.split(': ')[0]} = {field.split(': ')[0]}\n")
    
    file.write("\n")
    file.write(f"\tdef accept(self, visitor : {baseName}Visitor) -> typing.Any:\n")
    file.write(f"\t\treturn visitor.visit_{className}_{baseName}(self)\n\n")


expressions = {

    "Assign": ('name: Token', 'value: Expr'),
	"Binary": ('left: Expr', 'operator: Token', 'right: Expr'),
    "Call": ('callee: Expr', 'paren: Token', 'arguments: list'),  
	"Grouping": ('expr: Expr', ),
	"Literal": ('value: typing.Any', ),
    "Logical": ('left: Expr', 'operator: Token', 'right: Expr'),
	"Unary": ('operator: Token', 'right: Expr'),
    "Variable": ('name : Token', )
}

statements = {

    "Block": ('statements: list', ), 
	"Expression": ('expr: Expr', ), 
    "Function": ('name: Token', 'params: list', 'body: list'),
    "If": ('condition: Expr', 'thenBranch: Stmt', 'elseBranch: typing.Optional[Stmt]'),
	"Print": ('expr: Expr', ),
    "Var": ('name: Token', 'initializer: Expr'),
    "While": ('condition: Expr', 'body: Stmt')
}

defineAst(outputDir, "Expr", expressions)
defineAst(outputDir, "Stmt", statements)

# "Binary : Expr left, Token operator, Expr right",
# "Grouping : Expr expression",
# "Literal : Object value",
# "Unary : Token operator, Expr right"


