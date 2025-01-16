# -*- coding: utf-8 -*-

from ..Type import Type

from Liquirizia.DataModel import Handler

from Liquirizia.Validator import Validator, Pattern
from Liquirizia.Validator.Patterns import (
	IsToNone,
	IsNotToNone,
	IsString,
	IsSizeOf,
	IsSizeIn,
)

from ..Function import Function

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
			size: int = None,
			null: bool = False,
			default: Union[str, Function] = None,
			description: str = None,
			va: Validator = None,
			fn: Handler = None
		):
		if not va:
			if null:
				if size:
					va = Validator(IsToNone(IsString(IsSizeOf(size))))
				else:
					va = Validator(IsToNone(IsString()))
			else:
				if size:
					va = Validator(IsNotToNone(IsString(IsSizeOf(size))))
				else:
					va = Validator(IsNotToNone(IsString()))
		if isinstance(default, Function): default = str(default)
		if isinstance(default, str): default = '\'{}\''.format(default)
		super().__init__(
			key=name, 
			type='{}{}'.format(
				self.typestr,
				'({})'.format(size) if size else ''
			),
			null=null,
			default=default,
			description=description,
			va=va,
			fn=fn,
		)
		return


class String(Type, typestr='VARCHAR'):
	def __init__(
			self, 
			name: str, 
			size: int = None,
			null: bool = False,
			default: Union[str, Function] = None,
			description: str = None,
			va: Validator = None,
			fn: Handler = None,
		):
		if not va:
			if null:
				if size:
					va = Validator(IsToNone(IsString(IsSizeIn(size))))
				else:
					va = Validator(IsToNone(IsString()))
			else:
				if size:
					va = Validator(IsNotToNone(IsString(IsSizeIn(size))))
				else:
					va = Validator(IsNotToNone(IsString()))
		if isinstance(default, Function): default = str(default)
		if isinstance(default, str): default = '\'{}\''.format(default)
		super().__init__(
			key=name, 
			type='{}{}'.format(
				self.typestr,
				'({})'.format(size) if size else ''
			),
			null=null,
			default=default,
			description=description,
			va=va,
			fn=fn,
		)
		return


class Text(Type, typestr='TEXT'):
	def __init__(
			self, 
			name: str, 
			null: bool = False,
			default: Union[str, Function] = None,
			description: str = None,
			va: Validator = None,
			fn: Handler = None,
		):
		if not va:
			if null:
				va = Validator(IsToNone(IsString()))
			else:
				va = Validator(IsNotToNone(IsString()))
		if isinstance(default, Function): default = str(default)
		if isinstance(default, str): default = '\'{}\''.format(default)
		super().__init__(
			key=name, 
			type=self.typestr,
			null=null,
			default=default,
			description=description,
			va=va,
			fn=fn,
		)
		return
