import typing
from abc import ABC, abstractmethod
import Token

class ExprVisitor(ABC):

	@abstractmethod
	def visit_Assign_Expr(self, Expr: "Assign") -> typing.Any:
		pass

	@abstractmethod
	def visit_Binary_Expr(self, Expr: "Binary") -> typing.Any:
		pass

	@abstractmethod
	def visit_Call_Expr(self, Expr: "Call") -> typing.Any:
		pass

	@abstractmethod
	def visit_Get_Expr(self, Expr: "Get") -> typing.Any:
		pass

	@abstractmethod
	def visit_Grouping_Expr(self, Expr: "Grouping") -> typing.Any:
		pass

	@abstractmethod
	def visit_Literal_Expr(self, Expr: "Literal") -> typing.Any:
		pass

	@abstractmethod
	def visit_Logical_Expr(self, Expr: "Logical") -> typing.Any:
		pass

	@abstractmethod
	def visit_Set_Expr(self, Expr: "Set") -> typing.Any:
		pass

	@abstractmethod
	def visit_Super_Expr(self, Expr: "Super") -> typing.Any:
		pass

	@abstractmethod
	def visit_This_Expr(self, Expr: "This") -> typing.Any:
		pass

	@abstractmethod
	def visit_Unary_Expr(self, Expr: "Unary") -> typing.Any:
		pass

	@abstractmethod
	def visit_Variable_Expr(self, Expr: "Variable") -> typing.Any:
		pass


class Expr:

	def __init__(self): 
		pass

	@abstractmethod
	def accept(self, visitor: ExprVisitor) -> typing.Any:
		pass


class Assign(Expr):

	def __init__(self, name: Token, value: Expr):
		super().__init__()

		self.name = name
		self.value = value

	def accept(self, visitor : ExprVisitor) -> typing.Any:
		return visitor.visit_Assign_Expr(self)


class Binary(Expr):

	def __init__(self, left: Expr, operator: Token, right: Expr):
		super().__init__()

		self.left = left
		self.operator = operator
		self.right = right

	def accept(self, visitor : ExprVisitor) -> typing.Any:
		return visitor.visit_Binary_Expr(self)


class Call(Expr):

	def __init__(self, callee: Expr, paren: Token, arguments: list):
		super().__init__()

		self.callee = callee
		self.paren = paren
		self.arguments = arguments

	def accept(self, visitor : ExprVisitor) -> typing.Any:
		return visitor.visit_Call_Expr(self)


class Get(Expr):

	def __init__(self, obj: Expr, name: Token):
		super().__init__()

		self.obj = obj
		self.name = name

	def accept(self, visitor : ExprVisitor) -> typing.Any:
		return visitor.visit_Get_Expr(self)


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


class Logical(Expr):

	def __init__(self, left: Expr, operator: Token, right: Expr):
		super().__init__()

		self.left = left
		self.operator = operator
		self.right = right

	def accept(self, visitor : ExprVisitor) -> typing.Any:
		return visitor.visit_Logical_Expr(self)


class Set(Expr):

	def __init__(self, obj: Expr, name: Token, value: Expr):
		super().__init__()

		self.obj = obj
		self.name = name
		self.value = value

	def accept(self, visitor : ExprVisitor) -> typing.Any:
		return visitor.visit_Set_Expr(self)


class Super(Expr):

	def __init__(self, keyword: Token, method: Token):
		super().__init__()

		self.keyword = keyword
		self.method = method

	def accept(self, visitor : ExprVisitor) -> typing.Any:
		return visitor.visit_Super_Expr(self)


class This(Expr):

	def __init__(self, keyword: Token):
		super().__init__()

		self.keyword = keyword

	def accept(self, visitor : ExprVisitor) -> typing.Any:
		return visitor.visit_This_Expr(self)


class Unary(Expr):

	def __init__(self, operator: Token, right: Expr):
		super().__init__()

		self.operator = operator
		self.right = right

	def accept(self, visitor : ExprVisitor) -> typing.Any:
		return visitor.visit_Unary_Expr(self)


class Variable(Expr):

	def __init__(self, name: Token):
		super().__init__()

		self.name = name

	def accept(self, visitor : ExprVisitor) -> typing.Any:
		return visitor.visit_Variable_Expr(self)


