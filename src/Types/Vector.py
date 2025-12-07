# -*- coding: utf-8 -*-

from ..Type import Type
from ..Function import Function
from ..Value import Value

from Liquirizia.DataModel import Handler
from Liquirizia.Validator import Validator
from Liquirizia.Validator.Patterns import (
	Optional,
	IsArray,
)

from typing import Union, Sequence

__all__ = (
	'Vector',
)


class IfStrToArray(IsArray):
	def __call__(self, parameter):
		if isinstance(parameter, str):
			parameter = eval(parameter)
		return super().__call__(parameter)


class Vector(Type, typestr='VECTOR'):
	def __init__(
			self, 
			name: str,
			size: Union[int, Sequence[int]],
			va: Validator = None,
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
		if va is None:
			if null:
				va = Validator(Optional(IfStrToArray()))
			else:
				va = Validator(IfStrToArray())
		super().__init__(
			key=name, 
			type=list,
			typestr='{}({})'.format('VECTOR', size),
			encoder=lambda o: str(o),
			null=null,
			default=default,
			description=description,
			va=va,
			fn=fn,
		)
		return
