# -*- coding: utf-8 -*-

from ..Type import Type
from ..Function import Function
from ..Value import Value

from Liquirizia.DataModel import Handler
from Liquirizia.Validator import Validator
from Liquirizia.Validator.Patterns import (
	IsArray,
)

from typing import Union, Sequence

__all__ = (
	'Vector',
)


class Vector(Type, typestr='VECTOR'):
	def __init__(
			self, 
			name: str,
			size: Union[int, Sequence[int]],
			va: Validator = Validator(IsArray()),
			fn: Handler = None,
			null: bool = False,
			default: Union[Sequence[float], Function] = None,
			description: str = None,
		):
		args = None
		if size:
			args = []
			for s in size if isinstance(size, Sequence) else [size]:
				args.append('[{}]'.format(s))
		super().__init__(
			key=name, 
			type=list,
			typestr='{}({})'.format('VECTOR', size),
			null=null,
			default=default,
			description=description,
			va=va,
			fn=fn,
		)
		return
