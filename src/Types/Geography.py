# -*- coding: utf-8 -*-

from ..Type import Type
from ..Function import Function
from ..Value import Value

from Liquirizia.DataModel import Handler
from Liquirizia.Validator import Validator

from typing import Union, Tuple

__all__ = (
	'Geography',
)


class Geography(Type, typestr='GEOGRAPHY'):
	def __init__(
			self, 
			name: str,
			subtype: str = 'POINT',
			srid: int = 4326,
			null: bool = False,
			default: Union[Tuple[float, float], Function] = None,
			description: str = None,
			va: Validator = None,
			fn: Handler = None,
		):
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
			type='{}({}, {})'.format('GEOGRAPHY', subtype, srid),
			typedefault=typedefault,
			null=null,
			default=default,
			description=description,
			va=va,
			fn=fn,
		)
		return
