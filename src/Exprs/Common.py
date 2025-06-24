# -*- coding: utf-8 -*-

from ..Expr import Expr
from ..Function import Function
from ..Type import Type
from ..Column import Column
from ..Value import Value
from ..Executors import Select

from typing import Union, Type as T, Any, List, Tuple

__all__ = (
	'Alias',
	'TypeTo',
	'If',
	'IfNull',
	'IfNotNull',
	'Switch',
	'Query',
)


class Alias(Expr):
	def __init__(
		self,
		col: Union[Any, Value, Column, Function, Expr],
		name: str
	):
		if not isinstance(col, (Value, Column, Function, Expr)): col = Value(col)
		self.col = col
		self.name = name
		return
	def __str__(self):
		return '{} AS "{}"'.format(
			str(self.col),
			self.name,
		)
	

class TypeTo(Expr):
	def __init__(
		self,
		col: Union[Any, Value, Column, Function, Expr],
		type: Union[str, T[Type]],
	):
		if not isinstance(col, (Value, Column, Function, Expr)): col = Value(col)
		self.col = col
		self.type = type
		return
	def __str__(self):
		return '{}::{}'.format(
			str(self.col), 
			self.type if isinstance(self.type, str) else self.type.__typestr__
		)


class If(Expr):
	def __init__(
		self,
		cond: Union[Any, Value, Column, Function, Expr],
		thenexpr: Union[Any, Value, Expr, Function, Column] = None,
		elseexpr: Union[Any, Value, Expr, Function, Column] = None,
	):
		self.condexpr = cond
		if not isinstance(self.condexpr, (Value, Column, Function, Expr)): self.condexpr = Value(self.condexpr)
		self.thenexpr = thenexpr
		if not isinstance(self.thenexpr, (Value, Column, Function, Expr)): self.thenexpr = Value(self.thenexpr)
		self.elseexpr = elseexpr
		if self.elseexpr and not isinstance(self.elseexpr, (Value, Column, Function, Expr)): self.elseexpr = Value(self.elseexpr)
		return
	def then_(
		self,
		expr: Union[Any, Value, Column, Function, Expr],
	):
		self.thenexpr = expr
		if not isinstance(self.thenexpr, (Value, Column, Function, Expr)): self.thenexpr = Value(self.thenexpr)
		return self
	def else_(
		self,
		expr: Union[Any, Value, Column, Function, Expr],
	):
		self.elseexpr = expr
		if not isinstance(self.elseexpr, (Value, Column, Function, Expr)): self.elseexpr = Value(self.elseexpr)
		return self
	def __str__(self):
		return 'CASE WHEN {} THEN {}{} END'.format(
			str(self.condexpr),
			str(self.thenexpr),
			' ELSE {}'.format(str(self.elseexpr)) if self.elseexpr else '',
		)


class IfNull(Expr):
	def __init__(
		self,
		cond: Union[Any, Value, Column, Function, Expr],
		thenexpr: Union[Any, Value, Expr, Function, Column],
		elseexpr: Union[Any, Value, Expr, Function, Column] = None,
	):
		self.cond = cond
		if not isinstance(self.cond, (Value, Column, Function, Expr)): self.cond = Value(self.cond)
		self.thenexpr = thenexpr
		if not isinstance(self.thenexpr, (Value, Column, Function, Expr)): self.thenexpr = Value(self.thenexpr)
		self.elseexpr = elseexpr
		if self.elseexpr and not isinstance(self.elseexpr, (Value, Column, Function, Expr)): self.elseexpr = Value(self.elseexpr)
		return
	def then_(
		self,
		expr: Union[Any, Value, Column, Function, Expr],
	):
		self.thenexpr = expr
		if not isinstance(self.thenexpr, (Value, Column, Function, Expr)): self.thenexpr = Value(self.thenexpr)
		return self
	def else_(
		self,
		expr: Union[Any, Value, Column, Function, Expr],
	):
		self.elseexpr = expr
		if not isinstance(self.elseexpr, (Value, Column, Function, Expr)): self.elseexpr = Value(self.elseexpr)
		return self
	def __str__(self):
		return 'CASE WHEN {} IS NULL THEN {} ELSE {} END'.format(
			str(self.cond),
			str(self.thenexpr),
			str(self.elseexpr) if self.elseexpr else str(self.cond),
		)


class IfNotNull(Expr):
	def __init__(
		self,
		cond: Union[Any, Value, Column, Function, Expr],
		thenexpr: Union[Any, Value, Expr, Function, Column],
		elseexpr: Union[Any, Value, Expr, Function, Column] = None,
	):
		self.cond = cond
		if not isinstance(self.cond, (Value, Column, Function, Expr)): self.cond = Value(self.cond)
		self.thenexpr = thenexpr
		if not isinstance(self.thenexpr, (Value, Column, Function, Expr)): self.thenexpr = Value(self.thenexpr)
		self.elseexpr = elseexpr
		if self.elseexpr and not isinstance(self.elseexpr, (Value, Column, Function, Expr)): self.elseexpr = Value(self.elseexpr)
		return
	def then_(
		self,
		expr: Union[Any, Value, Column, Function, Expr],
	):
		self.thenexpr = expr
		if not isinstance(self.thenexpr, (Value, Column, Function, Expr)): self.thenexpr = Value(self.thenexpr)
		return self
	def else_(
		self,
		expr: Union[Any, Value, Column, Function, Expr],
	):
		self.elseexpr = expr
		if not isinstance(self.elseexpr, (Value, Column, Function, Expr)): self.elseexpr = Value(self.elseexpr)
		return self
	def __str__(self):
		return 'CASE WHEN {} IS NOT NULL THEN {} ELSE {} END'.format(
			str(self.cond),
			str(self.thenexpr),
			str(self.elseexpr) if self.elseexpr else str(self.cond),
		)


class Switch(Expr):
	def __init__(
		self,
		*args: List[Tuple[
			Union[Any, Value, Column, Function, Expr],
			Union[Any, Value, Column, Function, Expr],
		]]
	):
		self.args: List[Tuple[
			Union[Any, Value, Column, Function, Expr],
			Union[Any, Value, Column, Function, Expr],
		]] = list(args)
		self.elseexpr = None
		return
	def case(
		self,
		cond: Union[Any, Value, Column, Function, Expr],
		thenexpr: Union[Any, Value, Column, Function, Expr] = None,
	):
		if not isinstance(thenexpr, (Value, Column, Function, Expr)): thenexpr = Value(thenexpr)
		self.args.append(
			'WHEN {} THEN {}'.format(
				str(cond),
				str(thenexpr),
			)
		)
		return self
	def other(
		self,
		elseexpr: Union[Any, Value, Column, Function, Expr] = None,
	):
		if not isinstance(elseexpr, (Value, Column, Function, Expr)): elseexpr = Value(elseexpr)
		self.elseexpr = elseexpr
		return self
	def __str__(self):
		if not self.args:
			return 'NULL'
		expr = 'CASE {}'.format(' '.join(self.args))
		if self.elseexpr:
			expr += ' ELSE {}'.format(str(self.elseexpr))
		expr += ' END'
		return expr


class Query(Expr):
	def __init__(
		self,
		executor : Select,
	):
		self.executor = executor
		return
	def __str__(self):
		return '({})'.format(self.executor.query)
