# -*- coding: utf-8 -*-

from ..Type import Type
from ..Function import Function
from ..Value import Value
from ..Patterns import IsModel, ModelToDict

from Liquirizia.DataModel import Model, Handler
from Liquirizia.DataModel.Utils import ToDict

from Liquirizia.Validator import Validator
from Liquirizia.Validator.Patterns import (
	IsToNone,
	IsNotToNone,
	IsDictionary,
	IsArray,
	Any,
	If,
	IsTypeOf,
	SetDefault,
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
			null: bool = False,
			default: Union[Dict, Value, Function]= None,
			description: str = None,
			va: Validator = None,
			fn: Handler = None,
		):
		if not va:
			vargs = []
			if default:
				if not isinstance(default, Function):
					if isinstance(default, Value):
						vargs.append(SetDefault(default.value))
					else:
						vargs.append(SetDefault(default))
			if null:
				vargs.append(IsToNone(If(IsModel(ModelToDict())), Any(IsDictionary(), IsArray())))
			else:
				vargs.append(IsNotToNone(IsNotToNone(If(IsModel(ModelToDict())), Any(IsDictionary(), IsArray()))))
			va = Validator(*vargs)
		typedefault = None
		if default is not None:
			if isinstance(default, Value):
				typedefault = str(default)
				default = default.value
			elif isinstance(default, Function):
				typedefault = str(default)
				default = None
			else:
				typedefault = str(Value(default))
		super().__init__(
			key=name, 
			type='JSON',
			typedefault=typedefault,
			null=null,
			default=default,
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
			default: Union[Dict, Value, Function]= None,
			description: str = None,
			va: Validator = None,
			fn: Handler = None,
		):
		if not va:
			vargs = []
			if default:
				if not isinstance(default, Function):
					if isinstance(default, Value):
						vargs.append(SetDefault(default.value))
					else:
						vargs.append(SetDefault(default))
			if null:
				vargs.append(IsToNone(If(IsTypeOf(Model, ModelToDict())), Any(IsDictionary(), IsArray())))
			else:
				vargs.append(IsNotToNone(If(IsTypeOf(Model, ModelToDict())), Any(IsDictionary(), IsArray())))
			va = Validator(*vargs)
		typedefault = None
		if default is not None:
			if isinstance(default, Value):
				typedefault = str(default)
				default = default.value
			elif isinstance(default, Function):
				typedefault = str(default)
				default = None
			else:
				typedefault = str(Value(default))
		super().__init__(
			key=name, 
			type='JSONB',
			typedefault=typedefault,
			null=null,
			default=default,
			description=description,
			va=va,
			fn=fn,
		)
		return
