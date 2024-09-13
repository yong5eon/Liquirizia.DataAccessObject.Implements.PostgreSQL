# -*- coding: utf-8 -*-

from ..Function import Function

__all__ = (
	'NextVal',
)


class NextVal(Function):
	def __init__(self, name:str):
		self.name = name
		return
	def __str__(self):
		return 'NEXTVAL(\'{}\')'.format(self.name)
