# -*- coding: utf-8 -*-

from ..Expr import Expr
from ..Function import Function
from ..Column import Column
from ..Value import Value

from typing import Union, Sequence, Any

__all__ = (
	'In',
	'NotIn',
	'Is',
	'IsNull',
	'IsNotNull',
)


class In(Expr):
	def __init__(
		self,
		col: Union[Any, Value, Column, Function, Expr],
		args: Sequence[Union[Any, Value, Column, Function, Expr]] = None,
	):
		if not isinstance(col, (Value, Column, Function, Expr)): col = Value(col)
		self.col = col
		self.args = []
		if args:
			args = args if isinstance(args, (list, tuple)) else [args]
			for arg in args:
				if not isinstance(arg, (Value, Column, Function, Expr)):
					arg = Value(arg)
				self.args.append(arg)
		return
	def __str__(self):
		return '{} IN ({})'.format(
			str(self.col),
			', '.join([str(arg) for arg in self.args])
		)
	def where(self, arg: Union[Any, Value, Column, Function, Expr]):
		if not isinstance(arg, (Value, Column, Function, Expr)):
			arg = Value(arg)
		self.args.append(arg)
		return self


class NotIn(Expr):
	def __init__(
		self,
		col: Union[Any, Value, Column, Function, Expr],
		args: Sequence[Union[Any, Value, Column, Function, Expr]] = None,
	):
		if not isinstance(col, (Value, Column, Function, Expr)): col = Value(col)
		self.col = col
		self.args = []
		if args:
			args = args if isinstance(args, (list, tuple)) else [args]
			for arg in args:
				if not isinstance(arg, (Value, Column, Function, Expr)):
					arg = Value(arg)
				self.args.append(arg)
		return
	def __str__(self):
		return '{} NOT IN ({})'.format(
			str(self.col),
			', '.join([str(arg) for arg in self.args])
		)
	def where(self, arg: Union[Any, Value, Column, Function, Expr]):
		if not isinstance(arg, (Value, Column, Function, Expr)):
			arg = Value(arg)
		self.args.append(arg)
		return self


class Is(Expr):
	def __init__(
		self,
		col: Union[Any, Value, Column, Function, Expr],
		other: Union[Any, Value, Column, Function, Expr],
	):
		if not isinstance(col, (Value, Column, Function, Expr)): col = Value(col)
		if not isinstance(other, (Value, Column, Function, Expr)):
			other = Value(other)
		self.col = col
		self.other = other
		return
	def __str__(self):
		return '{} IS {}'.format(
			str(self.col),
			str(self.other),
		)


class IsNull(Expr):
	def __init__(
		self,
		col: Union[Any, Value, Column, Function, Expr],
	):
		if not isinstance(col, (Value, Column, Function, Expr)): col = Value(col)
		self.col = col
		return
	def __str__(self):
		return '{} IS NULL'.format(
			str(self.col),
		)


class IsNotNull(Expr):
	def __init__(
		self,
		col: Union[Any, Value, Column, Function, Expr],
	):
		if not isinstance(col, (Value, Column, Function, Expr)): col = Value(col)
		self.col = col
		return
	def __str__(self):
		return '{} IS NOT NULL'.format(
			str(self.col),
		)
