# -*- coding: utf-8 -*-

from ..Expr import Expr
from ...Function import Function
from ...Type import Type

from typing import Union, Type as T

__all__ = (
	'Alias',
	'TypeTo',
	'If',
)


class Alias(Expr):
	def __init__(
		self,
		col: Union[str, Type, Function, Expr],
		name: str
	):
		self.col = col
		self.name = name
		return
	def __str__(self):
		return '{} AS {}'.format(
			str(self.col),
			self.name,
		)
	

class TypeTo(Expr):
	def __init__(
		self,
		col: Union[str, Type, Function, Expr],
		type: Union[str, T[Type]]
	):
		self.col = col
		self.type = type
		return
	def __str__(self):
		return '{}::{}'.format(str(self.col), self.type)


class If(Expr):
	def __init__(
		self,
		expr: Union[str, Type, Function, Expr],
	):
		self.cond = expr
		self.then = None
		self.else = None
		return
	def then(
		self,
		expr: Union[str, Type, Function, Expr],
	):
		self.then = expr
		return self
	def else(
		self,
		expr: Union[str, Type, Function, Expr],
	):
		self.else = expr
		return self
	def __str__(self):
		return 'CASE WHEN {} THEN {}{} END'.format(
			str(self.cond),
			str(self.then),
			' ELSE {}'.format(str(self.else)) if self.else else '',
		)

