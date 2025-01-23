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
		return '{}.{}'.format(
			str(self.model), # attribute's model name
			self.key,
		)

	def encode(self, o: any): return o

	@classmethod
	def ToString(cls): return cls.__typestr__
