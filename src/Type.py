# -*- coding: utf-8 -*-

from Liquirizia.DataModel import Value, Handler
from Liquirizia.Validator.Validator import Validator

from abc import ABCMeta

from typing import Any

__all__ = (
	'Type'
)


class TypeCreateor(ABCMeta):
	def __repr__(cls): return cls.typestr


class Type(Value, metaclass=TypeCreateor):
	def __init__(
			self, 
			key: str,
			type: str,
			null: bool = False,
			default: Any = None,
			description: str = None,
			va: Validator = None,
			fn: Handler = None
		):
		super().__init__(
			va=va,
			default=None,
			description=description,
			fn=fn,
		)
		self.key = key
		self.type = type
		self.null = null
		self.default = default
		return

	def __init_subclass__(cls, typestr: str = None):
		cls.typestr = typestr
		return

	def __str__(self):
		return '{}.{}'.format(
			self.model.__model__, # attribute's model name
			self.key,
		)

	def encode(self, o: any): return o

	@classmethod
	def ToTypeString(cls): return cls.typestr
