# -*- coding: utf-8 -*-

from ..Type import Type

from Liquirizia.DataModel import Handler

from Liquirizia.Validator import Validator, Pattern
from Liquirizia.Validator.Patterns import (
	SetDefault,
	IsToNone,
	IsNotToNone,
	IsArray,
)

from ..Function import Function

from typing import Union, Sequence, Any, Type as T

__all__ = (
	'Array',
)


class Array(Type, typestr='ARRAY'):
	def __init__(
			self, 
			name: str,
			type: Union[str, T[Type]],
			size: Union[int, Sequence[int]] = None,
			null: bool = False,
			default: Union[Any, Function] = None,
			description: str = None,
			va: Validator = None,
			fn: Handler = None,
		):
		if not va:
			if null:
				va = Validator(IsToNone(IsArray()))
			else:
				va = Validator(IsNotToNone(IsArray()))
		args = None
		if size:
			args = []
			for s in size if isinstance(size, Sequence) else [size]:
				args.append('[{}]'.format(s))
		super().__init__(
			key=name, 
			type='{}{}'.format(
				type,
				''.join(args) if args else []
			),
			null=null,
			default=str(default) if isinstance(default, Function) else default,
			description=description,
			va=va,
			fn=fn,
		)
		return
