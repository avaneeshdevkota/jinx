import typing
from abc import ABC, abstractmethod
import Token
from Expr import *

class StmtVisitor(ABC):

	@abstractmethod
	def visit_Expression_Stmt(self, Stmt: "Expression") -> typing.Any:
		pass

	@abstractmethod
	def visit_Print_Stmt(self, Stmt: "Print") -> typing.Any:
		pass


class Stmt:

	def __init__(self): 
		pass

	@abstractmethod
	def accept(self, visitor: StmtVisitor) -> typing.Any:
		pass


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


