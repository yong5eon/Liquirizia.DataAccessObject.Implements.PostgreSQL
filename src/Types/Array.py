# -*- coding: utf-8 -*-

from ..Type import Type
from ..Function import Function
from ..Value import Value

from Liquirizia.DataModel import Handler
from Liquirizia.Validator import Validator
from Liquirizia.Validator.Patterns import (
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
		type: T[Type],
		typesize: int = None,
		size: Union[int, Sequence[int]] = None,
		va: Validator = Validator(IsArray()),
		fn: Handler = None,
		null: bool = False,
		default: Union[Any, Value, Function] = None,
		description: str = None,
	):
		SCALAR_TYPES = [
			'BOOLEAN',
			'SMALLINT',
			'INTEGER',
			'BIGINT',
			'REAL',
			'DOUBLE PRECISION',
			'NUMERIC',
			'DECIMAL',
			# TODO : add other scalar types
		]
		if type.__typestr__ not in SCALAR_TYPES:
			raise TypeError(
				'Type {} is not a scalar type for array'.format(type.__typestr__)
			)
		args = None
		if size:
			args = []
			for s in size if isinstance(size, Sequence) else [size]:
				args.append('[{}]'.format(s))
		super().__init__(
			key=name, 
			type=list,
			typestr='{}{}'.format(
				'{}{}'.format(
					type.__typestr__,
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
