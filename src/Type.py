# -*- coding: utf-8 -*-

from Liquirizia.DataModel import Value, Handler
from Liquirizia.Validator.Validator import Validator

from abc import ABCMeta

from typing import Any

__all__ = (
	'Type'
)


class TypeCreator(ABCMeta):
	def __repr__(cls): return cls.__typestr__


class Type(Value, metaclass=TypeCreator):
	def __init__(
			self, 
			key: str,
			type: str,
			typedefault: str = None,
			null: bool = False,
			default: Any = None,
			description: str = None,
			va: Validator = None,
			fn: Handler = None
		):
		super().__init__(
			va=va,
			default=default,
			description=description,
			fn=fn,
		)
		self.key = key
		self.type = type
		self.typedefault = typedefault
		self.null = null
		return

	def __init_subclass__(cls, typestr: str = None):
		cls.__typestr__ = typestr
		return

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

	def encode(self, o: any): return o

	@classmethod
	def ToString(cls): return cls.__typestr__
