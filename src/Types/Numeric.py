# -*- coding: utf-8 -*-

from ..Type import Type
from ..Function import Function
from ..Value import Value

from Liquirizia.DataModel import Handler

from Liquirizia.Validator import Validator
from Liquirizia.Validator.Patterns import (
	IsToNone,
	IsNotToNone,
	IsInteger,
	IsFloat,
	IsDecimal,
	SetDefault,
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
			null: bool = False,
			default: Union[int, Value, Function]= None,
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
				vargs.append(IsToNone(IsInteger()))
			else:
				vargs.append(IsNotToNone(IsInteger()))
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
		super().__init__(
			key=name, 
			type='SMALLINT',
			typedefault=typedefault,
			null=null,
			default=default,
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
			default: Union[int, Value, Function]= None,
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
				vargs.append(IsToNone(IsInteger()))
			else:
				vargs.append(IsNotToNone(IsInteger()))
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
		super().__init__(
			key=name, 
			type='INTEGER',
			typedefault=typedefault,
			null=null,
			default=default,
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
			default: Union[int, Value, Function]= None,
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
				vargs.append(IsToNone(IsInteger()))
			else:
				vargs.append(IsNotToNone(IsInteger()))
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
		super().__init__(
			key=name, 
			type='BIGINT',
			typedefault=typedefault,
			null=null,
			default=default,
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
			default: Union[float, Value, Function] = None,
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
				vargs.append(IsToNone(IsFloat()))
			else:
				vargs.append(IsNotToNone(IsFloat()))
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
		super().__init__(
			key=name, 
			type='REAL',
			typedefault=typedefault,
			null=null,
			default=default,
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
			default: Union[float, Value, Function] = None,
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
				vargs.append(IsToNone(IsFloat()))
			else:
				vargs.append(IsNotToNone(IsFloat()))
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
		super().__init__(
			key=name, 
			type='DOUBLE PRECISION',
			typedefault=typedefault,
			null=null,
			default=default,
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
			default: Union[PyDecimal, Value, Function]= None,
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
				vargs.append(IsToNone(IsDecimal()))
			else:
				vargs.append(IsNotToNone(IsDecimal()))
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
		super().__init__(
			key=name, 
			type='{}({},{})'.format('NUMERIC', scale, precision),
			typedefault=typedefault,
			null=null,
			default=default,
			description=description,
			va=va,
			fn=fn,
		)
		return
