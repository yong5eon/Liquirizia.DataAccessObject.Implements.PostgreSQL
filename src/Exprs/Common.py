# -*- coding: utf-8 -*-

from ..Expr import Expr
from ..Function import Function
from ..Type import Type
from ..Column import Column

from typing import Union, Type as T, Any

__all__ = (
	'Value',
	'Alias',
	'TypeTo',
	'If',
)


class Value(Expr):
	def __init__(self, value: Any):
		self.value = value
		return
	def __str__(self):
		fn ={
			str: lambda x: "'{}'".format(x),
		}.get(type(self.value), None)
		if fn: return fn(self.value)
		return str(self.value)


class Alias(Expr):
	def __init__(
		self,
		col: Union[Column, Type, Function, Expr],
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
		col: Union[Column, Type, Function, Expr],
		type: T[Type],
	):
		self.col = col
		self.type = type
		return
	def __str__(self):
		return '{}::{}'.format(str(self.col), str(self.type))


class If(Expr):
	def __init__(
		self,
		cond: Expr,
		thenexpr: Expr = None,
		elseexpr: Expr = None,
	):
		self.condexpr = cond
		self.thenexpr = thenexpr
		self.elseexpr = elseexpr
		return
	def then_(
		self,
		expr: Expr,
	):
		self.thenexpr = expr
		return self
	def else_(
		self,
		expr: Expr,
	):
		self.elseexpr = expr
		return self
	def __str__(self):
		return 'CASE WHEN {} THEN {}{} END'.format(
			str(self.condexpr),
			str(self.thenexpr),
			' ELSE {}'.format(str(self.elseexpr)) if self.elseexpr else '',
		)
