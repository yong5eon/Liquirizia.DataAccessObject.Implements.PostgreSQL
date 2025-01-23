# -*- coding: utf-8 -*-

from ..Expr import Expr
from ..Function import Function
from ..Type import Type
from ..Column import Column
from ..Value import Value

from typing import Union, Sequence, Any

__all__ = (
	'In',
	'IsNull',
	'IsNotNull',
)


class In(Expr):
	def __init__(
		self,
		col: Union[Column, Type, Function, Expr],
		args: Sequence[Union[Any, Value, Function, Expr]] = None,
	):
		if not isinstance(col, (Column, Type, Function, Expr)): col = Column(col)
		self.col = col
		self.args = []
		if args:
			args = args if isinstance(args, (list, tuple)) else [args]
			for arg in args:
				if not isinstance(arg, (Value, Function, Expr)):
					arg = Value(arg)
				self.args.append(arg)
		return
	def __str__(self):
		return '{} IN ({})'.format(
			str(self.col),
			', '.join([str(arg) for arg in self.args])
		)
	def where(self, arg: Union[Any, Value, Function, Expr]):
		if not isinstance(arg, (Value, Function, Expr)):
			arg = Value(arg)
		self.args.append(arg)
		return self


class IsNull(Expr):
	def __init__(
		self,
		col: Union[Column, Type, Function, Expr],
	):
		if not isinstance(col, (Column, Type, Function, Expr)): col = Column(col)
		self.col = col
		return
	def __str__(self):
		return '{} IS NULL'.format(
			str(self.col),
		)


class IsNotNull(Expr):
	def __init__(
		self,
		col: Union[Column, Type, Function, Expr],
	):
		if not isinstance(col, (Column, Type, Function, Expr)): col = Column(col)
		self.col = col
		return
	def __str__(self):
		return '{} IS NOT NULL'.format(
			str(self.col),
		)
