import typing
from abc import ABC, abstractmethod
import Token

class ExprVisitor(ABC):

	@abstractmethod
	def visit_Binary_Expr(self, Expr: "Binary") -> typing.Any:
		pass

	@abstractmethod
	def visit_Grouping_Expr(self, Expr: "Grouping") -> typing.Any:
		pass

	@abstractmethod
	def visit_Literal_Expr(self, Expr: "Literal") -> typing.Any:
		pass

	@abstractmethod
	def visit_Unary_Expr(self, Expr: "Unary") -> typing.Any:
		pass


class Expr:

	def __init__(self): 
		pass

	@abstractmethod
	def accept(self, visitor: ExprVisitor) -> typing.Any:
		pass


class Binary(Expr):

	def __init__(self, left: Expr, operator: Token, right: Expr):
		super().__init__()

		self.left = left
		self.operator = operator
		self.right = right

	def accept(self, visitor : ExprVisitor) -> typing.Any:
		return visitor.visit_Binary_Expr(self)


class Grouping(Expr):

	def __init__(self, expr: Expr):
		super().__init__()

		self.expr = expr

	def accept(self, visitor : ExprVisitor) -> typing.Any:
		return visitor.visit_Grouping_Expr(self)


class Literal(Expr):

	def __init__(self, value: typing.Any):
		super().__init__()

		self.value = value

	def accept(self, visitor : ExprVisitor) -> typing.Any:
		return visitor.visit_Literal_Expr(self)


class Unary(Expr):

	def __init__(self, operator: Token, right: Expr):
		super().__init__()

		self.operator = operator
		self.right = right

	def accept(self, visitor : ExprVisitor) -> typing.Any:
		return visitor.visit_Unary_Expr(self)


