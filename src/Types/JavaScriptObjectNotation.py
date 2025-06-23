# -*- coding: utf-8 -*-

from ..Type import Type
from ..Function import Function
from ..Value import Value

from Liquirizia.DataModel import Handler
from Liquirizia.Validator import Validator
from Liquirizia.Validator.Patterns import (
	IsObject,
	IsArray,
	Any,
)

from typing import Union, Dict

__all__ = (
	'JavaScriptObjectNotation',
	'JavaScriptObjectNotationByteArray',
)


class JavaScriptObjectNotation(Type, typestr='JSON'):
	def __init__(
		self, 
		name: str, 
		va: Validator = Validator(Any(IsObject(), IsArray())),
		fn: Handler = None,
		null: bool = False,
		default: Union[Dict, Value, Function]= None,
		description: str = None,
	):
		super().__init__(
			key=name,
			type=dict,
			va=va,
			fn=fn,
			typestr='JSON',
			null=null,
			default=default,
			description=description,
		)
		return


class JavaScriptObjectNotationByteArray(Type, typestr='JSONB'):
	def __init__(
		self, 
		name: str, 
		va: Validator = Validator(Any(IsObject(), IsArray())),
		fn: Handler = None,
		null: bool = False,
		default: Union[Dict, Value, Function]= None,
		description: str = None,
	):
		super().__init__(
			key=name, 
			type=dict,
			typestr='JSONB',
			null=null,
			default=default,
			description=description,
			va=va,
			fn=fn,
		)
		return
