# -*- coding: utf-8 -*-

from Liquirizia.DataModel import Attribute, Handler
from Liquirizia.Validator.Validator import Validator

__all__ = (
	'Object'
)


class Object(Attribute):
	def __init__(
			self, 
			key: str,
			type: str,
			null: bool = False,
			default: str = None,
			va: Validator = Validator(),
			fn: Handler = None
		):
		super().__init__(va, fn=fn)
		self.key = key
		self.type = type
		self.null = null
		self.default = default
		self.reference = None
		self.referenceTable = None
		self.referenceKey = None
		return
	
	def __str__(self):
		return '{}.{}'.format(
			self.model.__properties__['name'], # attribute's model name
			self.key
		)
	
	def encode(self, o: any):
		return o
	