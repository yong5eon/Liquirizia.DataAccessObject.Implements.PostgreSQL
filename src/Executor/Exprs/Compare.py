# -*- coding: utf-8 -*-

from ..Expr import Expr
from ...Type import Object

from typing import Union

__all__ = (
	'In'
)


class In(Expr):
	def __init__(self, attr: Union[Object,str], args):
		self.attr = attr
		self.args = args
		return
	def __str__(self):
		return '{} IN ({})'.format(
			str(self.attr),
			', '.join([self.encode(arg) for arg in self.args])
		)