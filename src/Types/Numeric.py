# -*- coding: utf-8 -*-

from ..Type import Type

from Liquirizia.DataModel import Handler

from Liquirizia.Validator import Validator, Pattern
from Liquirizia.Validator.Patterns import (
	IsToNone,
	IsNotToNone,
	IsInteger,
	IsFloat,
	IsDecimal,
)

from ..Function import Function
from decimal import Decimal as PyDecimal
from typing import Union, Sequence

__all__ = (
	'Short',
	'Integer',
	'Long',
	'Float',
	'Double',
	'Decimal',
)


class Short(Type, typestr='SMALLINT'):
	def __init__(
			self, 
			name: str, 
			null: bool = False,
			default: Union[int, Function]= None,
			description: str = None,
			va: Validator = None,
			fn: Handler = None,
		):
		if not va:
			if null:
				va = Validator(IsToNone(IsInteger()))
			else:
				va = Validator(IsNotToNone(IsInteger()))
		super().__init__(
			key=name, 
			type=self.typestr,
			null=null,
			default=str(default) if isinstance(default, Function) else default,
			description=description,
			va=va,
			fn=fn,
		)
		return


class Integer(Type, typestr='INTEGER'):
	def __init__(
			self, 
			name: str, 
			null: bool = False,
			default: Union[int, Function]= None,
			description: str = None,
			va: Validator = None,
			fn: Handler = None,
		):
		if not va:
			if null:
				va = Validator(IsToNone(IsInteger()))
			else:
				va = Validator(IsNotToNone(IsInteger()))
		super().__init__(
			key=name, 
			type=self.typestr,
			null=null,
			default=str(default) if isinstance(default, Function) else default,
			description=description,
			va=va,
			fn=fn,
		)
		return


class Long(Type, typestr='BIGINT'):
	def __init__(
			self, 
			name: str, 
			null: bool = False,
			default: Union[int, Function]= None,
			description: str = None,
			va: Validator = None,
			fn: Handler = None,
		):
		if not va:
			if null:
				va = Validator(IsToNone(IsInteger()))
			else:
				va = Validator(IsNotToNone(IsInteger()))
		super().__init__(
			key=name, 
			type=self.typestr,
			null=null,
			default=str(default) if isinstance(default, Function) else default,
			description=description,
			va=va,
			fn=fn,
		)
		return


class Float(Type, typestr='REAL'):
	def __init__(
			self, 
			name: str, 
			null: bool = False,
			default: Union[float, Function] = None,
			description: str = None,
			va: Validator = None,
			fn: Handler = None,
		):
		if not va:
			if null:
				va = Validator(IsToNone(IsFloat()))
			else:
				va = Validator(IsNotToNone(IsFloat()))
		super().__init__(
			key=name, 
			type=self.typestr,
			null=null,
			default=str(default) if isinstance(default, Function) else default,
			description=description,
			va=va,
			fn=fn,
		)
		return


class Double(Type, typestr='DOUBLE PRECISION'):
	def __init__(
			self, 
			name: str, 
			null: bool = False,
			default: Union[float, Function] = None,
			description: str = None,
			va: Validator = None,
			fn: Handler = None,
		):
		if not va:
			if null:
				va = Validator(IsToNone(IsFloat()))
			else:
				va = Validator(IsNotToNone(IsFloat()))
		super().__init__(
			key=name, 
			type=self.typestr,
			null=null,
			default=str(default) if isinstance(default, Function) else default,
			description=description,
			va=va,
			fn=fn,
		)
		return


class Decimal(Type, typestr='NUMERIC'):
	def __init__(
			self, 
			name: str, 
			scale: int,
			precision: int,
			null: bool = False,
			default: Union[PyDecimal, Function]= None,
			description: str = None,
			va: Validator = None,
			fn: Handler = None,
		):
		if not va:
			if null:
				va = Validator(IsToNone(IsDecimal()))
			else:
				va = Validator(IsNotToNone(IsDecimal()))
		super().__init__(
			key=name, 
			type='{}({},{})'.format(self.typestr, scale, precision),
			null=null,
			default=str(default) if isinstance(default, Function) else default,
			description=description,
			va=va,
			fn=fn,
		)
		return
