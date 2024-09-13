# -*- coding: utf-8 -*-

from Liquirizia.DataModel import Model, Handler
from Liquirizia.DataAccessObject.Model import Properties

from .Type import Type

from ..Type import Object
from ..Constraint import Constraint
from .Index import Index

from typing import Sequence

__all__ = (
	'Table'
)


class Table(Properties):
	def __init__(
		self, 
		name: str, 
		constraints: Sequence[Constraint] = None,
		indexes: Sequence[Index] = None,
		fn: Handler = None,
	):
		self.name = name
		self.constraints = constraints
		for constraint in self.constraints if self.constraints else []: constraint.table = name
		self.indexes = indexes
		for index in self.indexes if self.indexes else []: index.table = name
		self.fn = fn
		return
	
	def __call__(self, obj: Model):
		obj.__properties__ = {
			'type': Type.Table,
			'name': self.name,
			'constraints': self.constraints,
			'indexes': self.indexes,
		}
		def __new__(cls, **kwargs):
			o = object.__new__(cls)
			o.__object__ = dict()
			o.__cursor__ = None
			for k, v in cls.__dict__.items():
				if not isinstance(v, Object): continue
				if self.fn and not v.callback: v.callback = self.fn
				v.__init_object__(o, kwargs[v.key.lower()] if v.key.lower() in kwargs.keys() else None)
			return o
		obj.__new__ = __new__
		return obj
