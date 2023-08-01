import typing
from abc import ABC, abstractmethod
import Token
from Expr import *

class StmtVisitor(ABC):

	@abstractmethod
	def visit_Block_Stmt(self, Stmt: "Block") -> typing.Any:
		pass

	@abstractmethod
	def visit_Expression_Stmt(self, Stmt: "Expression") -> typing.Any:
		pass

	@abstractmethod
	def visit_Print_Stmt(self, Stmt: "Print") -> typing.Any:
		pass

	@abstractmethod
	def visit_Var_Stmt(self, Stmt: "Var") -> typing.Any:
		pass


class Stmt:

	def __init__(self): 
		pass

	@abstractmethod
	def accept(self, visitor: StmtVisitor) -> typing.Any:
		pass


class Block(Stmt):

	def __init__(self, statements: list):
		super().__init__()

		self.statements = statements

	def accept(self, visitor : StmtVisitor) -> typing.Any:
		return visitor.visit_Block_Stmt(self)


class Expression(Stmt):

	def __init__(self, expr: Expr):
		super().__init__()

		self.expr = expr

	def accept(self, visitor : StmtVisitor) -> typing.Any:
		return visitor.visit_Expression_Stmt(self)


class Print(Stmt):

	def __init__(self, expr: Expr):
		super().__init__()

		self.expr = expr

	def accept(self, visitor : StmtVisitor) -> typing.Any:
		return visitor.visit_Print_Stmt(self)


class Var(Stmt):

	def __init__(self, name: Token, initializer: Expr):
		super().__init__()

		self.name = name
		self.initializer = initializer

	def accept(self, visitor : StmtVisitor) -> typing.Any:
		return visitor.visit_Var_Stmt(self)


