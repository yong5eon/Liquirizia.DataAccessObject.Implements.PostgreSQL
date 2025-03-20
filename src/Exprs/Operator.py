# -*- coding: utf-8 -*-

from ..Expr import Expr

from typing import Sequence

__all__ = (
	'And',
	'Or',
)


class And(Expr):
	def __init__(self, *args: Sequence[Expr]):
		self.args = args
		return
	def __str__(self):
		return '({})'.format(' AND '.join([str(arg) for arg in self.args]))


class Or(Expr):
	def __init__(self, *args: Sequence[Expr]):
		self.args = args
		return
	def __str__(self):
		return '({})'.format(' OR '.join([str(arg) for arg in self.args]))
