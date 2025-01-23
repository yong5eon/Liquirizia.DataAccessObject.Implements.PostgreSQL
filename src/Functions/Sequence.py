# -*- coding: utf-8 -*-

from ..Function import Function

from ..Sequence import Sequence
from ..Schema import Schema

__all__ = (
	'NextVal',
)


class NextVal(Function):
	def __init__(
		self,
		sequence: Sequence,
		schema: Schema = None,
	):
		self.seqence = sequence
		self.schema = schema
		return
	def __str__(self):
		return 'NEXTVAL(\'{}"{}"\')'.format(
			'"{}".'.format(str(self.schema)) if self.schema else '',
			str(self.seqence),
		)
