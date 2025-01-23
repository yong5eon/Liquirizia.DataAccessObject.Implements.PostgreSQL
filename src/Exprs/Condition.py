# -*- coding: utf-8 -*-

from ..Expr import Expr
from ..Function import Function
from ..Type import Type
from ..Column import Column

from typing import Union, Sequence, Any

__all__ = (
	'In',
	'IsNull',
	'IsNotNull',
)


class In(Expr):
	def __init__(
		self,
		col: Union[Column, Type],
		args: Sequence[Any],
	):
		self.col = col
		self.args = list(args) if isinstance(args, (list, tuple)) else [args]
		return
	def __str__(self):
		return '{} IN ({})'.format(
			str(self.col),
			', '.join([self.encode(arg) for arg in self.args])
		)
	def add(self, arg: Any):
		self.args.append(arg)
		return self


class IsNull(Expr):
	def __init__(
		self,
		col: Union[Column, Type, Function, Expr],
	):
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
		self.col = col
		return
	def __str__(self):
		return '{} IS NOT NULL'.format(
			str(self.col),
		)
