# -*- coding: utf-8 -*-

from ..Type import Type
from ..Function import Function
from ..Value import Value

from Liquirizia.DataModel import Handler

from Liquirizia.Validator import Validator
from Liquirizia.Validator.Patterns import (
	IsToNone,
	IsNotToNone,
	IsArray,
	SetDefault,
)

from typing import Union, Sequence, Any, Type as T

__all__ = (
	'Array',
)


class Array(Type, typestr='ARRAY'):
	def __init__(
			self, 
			name: str,
			type: T[Type],
			typesize: int = None,
			size: Union[int, Sequence[int]] = None,
			null: bool = False,
			default: Union[Any, Value, Function] = None,
			description: str = None,
			va: Validator = None,
			fn: Handler = None,
		):
		if not va:
			vargs = []
			if default:
				if not isinstance(default, Function):
					if isinstance(default, Value):
						vargs.append(SetDefault(default.value))
					else:
						vargs.append(SetDefault(default))
			if null:
				vargs.append(IsToNone(IsArray()))
			else:
				vargs.append(IsNotToNone(IsArray()))
			va = Validator(*vargs)
		typedefault = None
		if default is not None:
			if isinstance(default, Value):
				typedefault = str(default)
				default = default.value
			elif isinstance(default, Function):
				typedefault = str(default)
				default = None
			else:
				typedefault = str(Value(default))
		args = None
		if size:
			args = []
			for s in size if isinstance(size, Sequence) else [size]:
				args.append('[{}]'.format(s))
		super().__init__(
			key=name, 
			type='{}{}'.format(
				'{}{}'.format(
					str(type),
					'({})'.format(typesize) if typesize else ''
				),
				''.join(args) if args else []
			),
			typedefault=typedefault,
			null=null,
			default=default,
			description=description,
			va=va,
			fn=fn,
		)
		return
