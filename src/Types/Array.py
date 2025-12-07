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

from typing import Union, Sequence, Any, Type as T

__all__ = (
	'Array',
)


class Array(Type, typestr='ARRAY'):
	def __init__(
		self, 
		name: str,
		type: Union[str, T[Type]],
		typesize: int = None,
		size: Union[int, Sequence[int]] = None,
		va: Validator = None,
		fn: Handler = None,
		null: bool = False,
		default: Union[Any, Value, Function] = None,
		description: str = None,
	):
		args = None
		if size:
			args = []
			for s in size if isinstance(size, Sequence) else [size]:
				args.append('[{}]'.format(s))
		if va is None:
			if null:
				va = Validator(Optional(IsArray()))
			else:
				va = Validator(IsArray())
		super().__init__(
			key=name, 
			type=list,
			typestr='{}{}'.format(
				'{}{}'.format(
					type if isinstance(type, str) else type.__typestr__,
					'({})'.format(typesize) if typesize else ''
				),
				''.join(args) if args else []
			),
			va=va,
			fn=fn,
			null=null,
			default=default,
			description=description,
		)
		return
