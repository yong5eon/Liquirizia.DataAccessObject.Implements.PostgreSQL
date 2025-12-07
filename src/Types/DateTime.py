# -*- coding: utf-8 -*-

from ..Type import Type
from ..Function import Function
from ..Value import Value

from Liquirizia.DataModel import Handler
from Liquirizia.Validator import Validator
from Liquirizia.Validator.Patterns import (
	Optional,
	IsDateTime,
	IsDate,
	IsTime,
)

from datetime import date, time, datetime

from typing import Union

__all__ = (
	'Timestamp',
	'Date',
	'Time',
)


class IfStrOrTimestampToDateTime(IsDateTime):
	def __call__(self, parameter):
		if isinstance(parameter, str):
			return datetime.fromisoformat(parameter)
		if isinstance(parameter, float):
			return datetime.fromtimestamp(parameter)
		return super().__call__(parameter)


class Timestamp(Type, typestr='TIMESTAMP'):
	def __init__(
		self, 
		name: str, 
		timezone: bool = False,
		va: Validator = None,
		fn: Handler = None,
		null: bool = False,
		default: Union[datetime, Value, Function] = None,
		description: str = None,
	):
		if va is None:
			if null:
				va = Validator(Optional(IfStrOrTimestampToDateTime()))
			else:
				va = Validator(IfStrOrTimestampToDateTime())
		super().__init__(
			name,
			type=datetime,
			typestr='TIMESTAMP{}'.format(' WITH TIME ZONE' if timezone else ''),
			va=va,
			fn=fn,
			null=null,
			default=default,
			description=description,
		)
		return


class IfStrToDate(IsDate):
	def __call__(self, parameter):
		if isinstance(parameter, str):
			return date.fromisoformat(parameter)
		return super().__call__(parameter)


class Date(Type, typestr='DATE'):
	def __init__(
		self, 
		name: str, 
		va: Validator = None,
		fn: Handler = None,
		null: bool = False,
		default: Union[date, Value, Function] = None,
		description: str = None,
	):
		if va is None:
			if null:
				va = Validator(Optional(IfStrToDate()))
			else:
				va = Validator(IfStrToDate())
		super().__init__(
			key=name, 
			type=date,
			typestr='DATE',
			null=null,
			default=default,
			description=description,
			va=va, 
			fn=fn,
		)
		return


class IfStrToTime(IsTime):
	def __call__(self, parameter):
		if isinstance(parameter, str):
			return time.fromisoformat(parameter)
		return super().__call__(parameter)


class Time(Type, typestr='TIME'):
	def __init__(
		self, 
		name: str, 
		va: Validator = None,
		fn: Handler = None,
		null: bool = False,
		default: Union[time, Value, Function] = None,
		description: str = None,
	):
		if va is None:
			if null:
				va = Validator(Optional(IfStrToTime()))
			else:
				va = Validator(IfStrToTime())
		super().__init__(
			key=name, 
			type=time,
			typestr='TIME',
			null=null,
			default=default,
			description=description,
			va=va, 
			fn=fn,
		)
		return
