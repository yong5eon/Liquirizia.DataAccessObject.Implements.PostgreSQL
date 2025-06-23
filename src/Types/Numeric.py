# -*- coding: utf-8 -*-

from ..Type import Type
from ..Function import Function
from ..Value import Value

from Liquirizia.DataModel import Handler
from Liquirizia.Validator import Validator
from Liquirizia.Validator.Patterns import (
	IsInteger,
	IsFloat,
	IsDecimal,
)

from decimal import Decimal as PyDecimal
from typing import Union

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
		va: Validator = Validator(IsInteger()),
		fn: Handler = None,
		null: bool = False,
		default: Union[int, Value, Function]= None,
		description: str = None,
	):
		super().__init__(
			key=name, 
			type=int,
			typestr='SMALLINT',
			va=va,
			fn=fn,
			null=null,
			default=default,
			description=description,
		)
		return


class Integer(Type, typestr='INTEGER'):
	def __init__(
		self, 
		name: str, 
		va: Validator = Validator(IsInteger()),
		fn: Handler = None,
		null: bool = False,
		default: Union[int, Value, Function]= None,
		description: str = None,
	):
		super().__init__(
			key=name, 
			type=int,
			typestr='INTEGER',
			va=va,
			fn=fn,
			null=null,
			default=default,
			description=description,
		)
		return


class Long(Type, typestr='BIGINT'):
	def __init__(
		self, 
		name: str, 
		va: Validator = Validator(IsInteger()),
		fn: Handler = None,
		null: bool = False,
		default: Union[int, Value, Function]= None,
		description: str = None,
	):
		super().__init__(
			key=name, 
			type=int,
			typestr='BIGINT',
			va=va,
			fn=fn,
			null=null,
			default=default,
			description=description,
		)
		return


class Float(Type, typestr='REAL'):
	def __init__(
		self, 
		name: str, 
		va: Validator = Validator(IsFloat()),
		fn: Handler = None,
		null: bool = False,
		default: Union[float, Value, Function] = None,
		description: str = None,
	):
		super().__init__(
			key=name, 
			type=float,
			typestr='REAL',
			va=va,
			fn=fn,
			null=null,
			default=default,
			description=description,
		)
		return


class Double(Type, typestr='DOUBLE PRECISION'):
	def __init__(
		self, 
		name: str, 
		va: Validator = Validator(IsFloat()),
		fn: Handler = None,
		null: bool = False,
		default: Union[float, Value, Function] = None,
		description: str = None,
	):
		super().__init__(
			key=name, 
			type=float,
			typestr='DOUBLE PRECISION',
			va=va,
			fn=fn,
			null=null,
			default=default,
			description=description,
		)
		return


class Decimal(Type, typestr='NUMERIC'):
	def __init__(
		self, 
		name: str, 
		scale: int,
		precision: int,
		va: Validator = Validator(IsDecimal()),
		fn: Handler = None,
		null: bool = False,
		default: Union[PyDecimal, Value, Function]= None,
		description: str = None,
	):
		super().__init__(
			key=name, 
			type=PyDecimal,
			typestr='NUMERIC({},{})'.format(scale, precision),
			va=va,
			fn=fn,
			null=null,
			default=default,
			description=description,
		)
		return
