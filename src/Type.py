# -*- coding: utf-8 -*-

from Liquirizia.DataModel import Value as BaseType, Handler, MISSING
from Liquirizia.Validator.Validator import Validator

from .Value import Value
from .Function import Function

from typing import Any, Union

__all__ = (
	'Type'
)


class Type(BaseType):
	def __init__(
			self, 
			key: str,
			type: str,
			typestr: str,
			va: Validator = None,
			fn: Handler = None,
			null: bool = False,
			default: Union[Any, Value, Function] = None,
			description: str = None,
		):
		super().__init__(
			type=type,
			va=va,
			fn=fn,
			default=None if null else MISSING,
			description=description,
		)
		self.key = key
		self.null = null
		self.typestr = typestr
		if default is not None:
			if isinstance(default, Value):
				self.typedef = str(default)
			elif isinstance(default, Function):
				self.typedef = str(default)
			else:
				self.typedef = str(Value(default))
		else:
			self.typedef = None
		return
	
	def __init_subclass__(cls, typestr: str):
		cls.__typestr__ = typestr
		return super().__init_subclass__()

	def __str__(self):
		from .Table import Table
		from .View import View
		if issubclass(self.model, Table):
			return '{}"{}"."{}"'.format(
				'"{}".'.format(self.model.__schema__) if self.model.__schema__ else '',
				self.model.__table__, # attribute's model name
				self.key,
			)
		if issubclass(self.model, View):
			return '{}"{}"."{}"'.format(
				'"{}".'.format(self.model.__schema__) if self.model.__schema__ else '',
				self.model.__view__, # attribute's model name
				self.key,
			)
