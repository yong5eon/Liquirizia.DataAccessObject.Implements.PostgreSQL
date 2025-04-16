# -*- coding: utf-8 -*-

from ..Type import Type
from ..Function import Function
from ..Value import Value

from Liquirizia.DataModel import Handler

from Liquirizia.Validator import Validator
from Liquirizia.Validator.Patterns import (
	IsToNone,
	IsNotToNone,
	IsDateTime,
	IsDate,
	IsTime,
	SetDefault,
)

from datetime import date, time, datetime

from typing import Union

__all__ = (
	'Timestamp',
	'Date',
	'Time',
)


class Timestamp(Type, typestr='TIMESTAMP'):
	def __init__(
			self, 
			name: str, 
			timezone: bool = False,
			null: bool = False,
			default: Union[datetime, Value, Function] = None,
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
				vargs.append(IsToNone(IsDateTime()))
			else:
				vargs.append(IsNotToNone(IsDateTime()))
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
			name,
			type='{}{}'.format(str(self.__class__), ' WITH TIME ZONE' if timezone else ''),
			typedefault=typedefault,
			null=null,
			default=default,
			description=description,
			va=va,
			fn=fn,
		)
		return


class Date(Type, typestr='DATE'):
	def __init__(
			self, 
			name: str, 
			null: bool = False,
			default: Union[date, Value, Function] = None,
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
				vargs.append(IsToNone(IsDate()))
			else:
				vargs.append(IsNotToNone(IsDate()))
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
			type=str(self.__class__),
			typedefault=typedefault,
			null=null,
			default=default,
			description=description,
			va=va, 
			fn=fn,
		)
		return


class Time(Type, typestr='TIME'):
	def __init__(
			self, 
			name: str, 
			null: bool = False,
			default: Union[time, Value, Function] = None,
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
				vargs.append(IsToNone(IsTime()))
			else:
				vargs.append(IsNotToNone(IsTime()))
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
			type=str(self.__class__),
			typedefault=typedefault,
			null=null,
			default=default,
			description=description,
			va=va, 
			fn=fn,
		)
		return
