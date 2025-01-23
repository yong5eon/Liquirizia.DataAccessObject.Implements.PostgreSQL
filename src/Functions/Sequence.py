# -*- coding: utf-8 -*-

from ..Function import Function

from ..Sequence import Sequence

__all__ = (
	'NextVal',
)


class NextVal(Function):
	def __init__(
		self,
		sequence: Sequence
	):
		self.seqence = str(sequence)
		return
	def __str__(self):
		return 'NEXTVAL(\'"{}"\')'.format(self.seqence)
