# -*- coding: utf-8 -*-

from collections.abc import MutableSequence, MutableMapping, MutableSet
from datetime import datetime, date
from decimal import Decimal
from json import JSONEncoder

__all__ = (
	'Encoder'
)


class Encoder(JSONEncoder):
	"""Type Encoder for JSON"""

	def default(self, obj):
		if isinstance(obj, Decimal):
			return float(obj)
		if isinstance(obj, MutableSequence):
			return list(obj)
		if isinstance(obj, MutableMapping):
			return dict(obj)
		if isinstance(obj, MutableSet):
			return set(obj)
		if isinstance(obj, (date, datetime)):
			return obj.isoformat()
		return None
