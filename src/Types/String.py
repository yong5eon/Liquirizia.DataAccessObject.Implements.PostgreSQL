# -*- coding: utf-8 -*-

from ..Type import Type
from ..Function import Function
from ..Value import Value

from Liquirizia.DataModel import Handler
from Liquirizia.Validator import Validator
from Liquirizia.Validator.Patterns import (
	Optional,
	IsString,
)

from typing import Union

__all__ = (
	'Char',
	'String',
	'Text',
)


class Char(Type, typestr='CHAR'):
	def __init__(
		self, 
		name: str,
		va: Validator = None,
		fn: Handler = None,
		size: int = None,
		null: bool = False,
		default: Union[str, Function] = None,
		description: str = None,
	):
		if va is None:
			if null:
				va = Validator(Optional(IsString()))
			else:
				va = Validator(IsString())
		super().__init__(
			key=name, 
			type=str,
			typestr='{}{}'.format(
				'CHAR',
				'({})'.format(size) if size else ''
			),
			va=va,
			fn=fn,
			null=null,
			default=default,
			description=description,
		)
		return


class String(Type, typestr='VARCHAR'):
	def __init__(
		self, 
		name: str, 
		va: Validator = None,
		fn: Handler = None,
		size: int = None,
		null: bool = False,
		default: Union[str, Value, Function] = None,
		description: str = None,
	):
		if va is None:
			if null:
				va = Validator(Optional(IsString()))
			else:
				va = Validator(IsString())
		super().__init__(
			key=name, 
			type=str,
			typestr='{}{}'.format(
				'VARCHAR',
				'({})'.format(size) if size else ''
			),
			va=va,
			fn=fn,
			null=null,
			default=default,
			description=description,
		)
		return


class Text(Type, typestr='TEXT'):
	def __init__(
		self, 
		name: str, 
		va: Validator = None,
		fn: Handler = None,
		null: bool = False,
		default: Union[str, Function] = None,
		description: str = None,
	):
		if va is None:
			if null:
				va = Validator(Optional(IsString()))
			else:
				va = Validator(IsString())
		super().__init__(
			key=name, 
			type=str,
			typestr='TEXT',
			va=va,
			fn=fn,
			null=null,
			default=default,
			description=description,
		)
		return
