# -*- coding: utf-8 -*-

from ..Type import Type

from Liquirizia.DataModel import Handler

from Liquirizia.Validator import Validator, Pattern
from Liquirizia.Validator.Patterns import (
	IsToNone,
	IsNotToNone,
	IsDateTime,
	IsDate,
	IsTime,
)

from ..Function import Function

from datetime import date, time, datetime

from typing import Union, Sequence

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
			default: Union[datetime, Function] = None,
			description: str = None,
			va: Validator = None,
			fn: Handler = None,
		):
		if not va:
			if null:
				va = Validator(IsToNone(IsDateTime()))
			else:
				va = Validator(IsNotToNone(IsDateTime()))
		super().__init__(
			name,
			type='{}{}'.format(self.typestr, ' WITH TIME ZONE' if timezone else ''),
			null=null,
			default=str(default) if isinstance(default, Function) else default,
			description=description,
			va=va,
			fn=fn,
		)
		return


class Date(Type, typestr='DATE'):
	def __init__(
			self, 
			name: str, 
			timezone: bool = False,
			null: bool = False,
			default: date = None,
			description: str = None,
			va: Validator = None,
			fn: Handler = None,
		):
		if not va:
			if null:
				va = Validator(IsToNone(IsDate()))
			else:
				va = Validator(IsNotToNone(IsDate()))
		super().__init__(
			key=name, 
			type='{}{}'.format(self.typestr, ' WITH TIME ZONE' if timezone else ''),
			null=null,
			default=str(default) if isinstance(default, Function) else default,
			description=description,
			va=va, 
			fn=fn,
		)
		return


class Time(Type, typestr='TIME'):
	def __init__(
			self, 
			name: str, 
			timezone: bool = False,
			null: bool = False,
			default: Union[time, Function] = None,
			description: str = None,
			va: Validator = None,
			fn: Handler = None,
		):
		if not va:
			if null:
				va = Validator(IsToNone(IsTime()))
			else:
				va = Validator(IsNotToNone(IsTime()))
		super().__init__(
			key=name, 
			type='{}{}'.format(self.typestr, ' WITH TIME ZONE' if timezone else ''),
			null=null,
			default=str(default) if isinstance(default, Function) else default,
			description=description,
			va=va, 
			fn=fn,
		)
		return
