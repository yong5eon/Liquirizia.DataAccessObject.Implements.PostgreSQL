# -*- coding: utf-8 -*-

from ..Type import Type

from Liquirizia.DataModel import Model, Handler
from Liquirizia.DataModel.Util import ToDict

from Liquirizia.Validator import Validator, Pattern
from Liquirizia.Validator.Patterns import (
	IsToNone,
	IsNotToNone,
	IsDictionary,
	If,
	IsTypeOf,
)

from ..Function import Function

from typing import Union, Dict

__all__ = (
	'JavaScriptObjectNotation',
	'JavaScriptObjectNotationByteArray',
)


class IsModel(Pattern):
	def __init__(
		self,
		*args,
		error: BaseException = None
	):
		self.patterns = args
		self.error = error
		return

	def __call__(self, parameter):
		if not isinstance(parameter, Model):
			if self.error:
				raise self.error
			raise TypeError('{} must be based {}'.format(
				'\'{}\''.format(parameter) if isinstance(parameter, str) else parameter, 
				self.type.__name__,
			))
		for pattern in self.patterns:
			parameter = pattern(parameter)
		return parameter


class ModelToDict(Pattern):
	def __call__(self, parameter):
		return ToDict(parameter)


class JavaScriptObjectNotation(Type, typestr='JSON'):
	def __init__(
			self, 
			name: str, 
			null: bool = False,
			default: Union[Dict, Function]= None,
			description: str = None,
			va: Validator = None,
			fn: Handler = None,
		):
		if not va:
			if null:
				va = Validator(IsToNone(If(IsModel(ModelToDict())), IsDictionary()))
			else:
				va = Validator(IsNotToNone(If(IsModel(ModelToDict())), IsDictionary()))
		super().__init__(
			key=name, 
			type='JSON',
			null=null,
			default=str(default) if isinstance(default, Function) else default,
			description=description,
			va=va,
			fn=fn,
		)
		return


class JavaScriptObjectNotationByteArray(Type, typestr='JSONB'):
	def __init__(
			self, 
			name: str, 
			null: bool = False,
			default: Union[Dict, Function]= None,
			description: str = None,
			va: Validator = None,
			fn: Handler = None,
		):
		if not va:
			if null:
				va = Validator(IsToNone(If(IsTypeOf(Model, ModelToDict())), IsDictionary()))
			else:
				va = Validator(IsNotToNone(If(IsTypeOf(Model, ModelToDict())), IsDictionary()))
		super().__init__(
			key=name, 
			type='JSONB',
			null=null,
			default=str(default) if isinstance(default, Function) else default,
			description=description,
			va=va,
			fn=fn,
		)
		return
