# -*- coding: utf-8 -*-

from ..Function import Function

from ..Sequence import Sequence

from typing import Union

__all__ = (
	'NextVal',
)


class NextVal(Function):
	def __init__(
		self,
		sequence: Union[str, Sequence]
	):
		self.seqence = sequence.name if isinstance(sequence, Sequence) else sequence
		return
	def __str__(self):
		return 'NEXTVAL(\'{}\')'.format(self.seqence)
