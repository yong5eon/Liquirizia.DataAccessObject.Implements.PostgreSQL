# -*- coding: utf-8 -*-

from ..Expr import Expr
from ..Function import Function
from ..Type import Type

from typing import Union

__all__ = (
	'In',
	'IsNull',
	'IsNotNull',
)


class In(Expr):
	def __init__(
		self,
		col: Union[str, Type, Function, Expr],
		args
	):
		self.col = col
		self.args = args
		return
	def __str__(self):
		return '{} IN ({})'.format(
			str(self.col),
			', '.join([self.encode(arg) for arg in self.args])
		)


class IsNull(Expr):
	def __init__(
		self,
		col: Union[str, Type, Function, Expr],
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
		col: Union[str, Type, Function, Expr],
	):
		self.col = col
		return
	def __str__(self):
		return '{} IS NOT NULL'.format(
			str(self.col),
		)
