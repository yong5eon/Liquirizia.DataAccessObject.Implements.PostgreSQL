# -*- coding: utf-8 -*-

from ..Expr import Expr
from ..Column import Column
from ..Type import Type

from typing import Union, Type as T

__all__ = (
	'Of',
)


class Of(Expr):
	def __init__(
		self,
		col: Union[str, Column, Expr],
		arg: str,
		type: Union[str, T[Type]] = None,
	):
		self.col = col
		if isinstance(col, str):
			self.col = Column(col)
		self.arg = arg
		self.type = type
		return
	def __str__(self):
		return '({}->{}){}'.format(
			str(self.col),
			'\'{}\''.format(self.arg) if isinstance(self.arg, str) else str(self.arg),
			'::{}'.format(
				self.type if isinstance(self.type, str) else self.type.__typestr__
			) if self.type else '',
		)
	def cast(
		self,
		type: Union[str, T[Type]],
	):
		self.type = type if isinstance(type, str) else type.__typestr__
		return self
