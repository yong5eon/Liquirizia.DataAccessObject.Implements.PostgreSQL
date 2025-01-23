# -*- coding: utf-8 -*-

from ..Type import Type
from ..Function import Function
from ..Value import Value

from Liquirizia.DataModel import Handler

from Liquirizia.Validator import Validator
from Liquirizia.Validator.Patterns import (
	IsToNone,
	IsNotToNone,
	IsString,
	IsSizeOf,
	IsSizeIn,
	SetDefault,
)

from typing import Union

__all__ = (
	'Char',
	'String',
	'Text',
)


class Char(Type, typestr='CHAR'):
	def __init__(
			self, 
			name: str,
			size: int = None,
			null: bool = False,
			default: Union[str, Function] = None,
			description: str = None,
			va: Validator = None,
			fn: Handler = None
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
				if size:
					vargs.append(IsToNone(IsString(IsSizeOf(size))))
				else:
					vargs.append(IsToNone(IsString()))
			else:
				if size:
					vargs.append(IsNotToNone(IsString(IsSizeOf(size))))
				else:
					vargs.append(IsNotToNone(IsString()))
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
			type='{}{}'.format(
				'CHAR',
				'({})'.format(size) if size else ''
			),
			typedefault=typedefault,
			null=null,
			default=default,
			description=description,
			va=va,
			fn=fn,
		)
		return


class String(Type, typestr='VARCHAR'):
	def __init__(
			self, 
			name: str, 
			size: int = None,
			null: bool = False,
			default: Union[str, Value, Function] = None,
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
				if size:
					vargs.append(IsToNone(IsString(IsSizeIn(size))))
				else:
					vargs.append(IsToNone(IsString()))
			else:
				if size:
					vargs.append(IsNotToNone(IsString(IsSizeIn(size))))
				else:
					vargs.append(IsNotToNone(IsString()))
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
			type='{}{}'.format(
				'VARCHAR',
				'({})'.format(size) if size else ''
			),
			typedefault=typedefault,
			null=null,
			default=default,
			description=description,
			va=va,
			fn=fn,
		)
		return


class Text(Type, typestr='TEXT'):
	def __init__(
			self, 
			name: str, 
			null: bool = False,
			default: Union[str, Function] = None,
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
				vargs.append(IsToNone(IsString()))
			else:
				vargs.append(IsNotToNone(IsString()))
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
			type='TEXT',
			typedefault=typedefault,
			null=null,
			default=default,
			description=description,
			va=va,
			fn=fn,
		)
		return
