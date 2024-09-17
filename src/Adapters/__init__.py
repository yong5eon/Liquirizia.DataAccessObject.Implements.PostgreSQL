# -*- coding: utf-8 -*-

from .Model import (
	ModelDumper,
	ListDumper,
	TupleDumper,
	DictionaryDumper,
	InitAdapterForModel,
)
from .JavaScriptObjectNotation import (
	JavaScriptObjectNotationDumper,
	InitAdapterForJavaScriptObjectNotation,
)

from psycopg import Connection

__all__ = (
	'InitAdpaters',
	# JSON
	'JavaScriptObjectNotationDumper',
	# MODEL
	'ModelDumper',
	'ListDumper',
	'TupleDumper',
	'DictionaryDumper',
)


def InitAdapters(connection: Connection):
	InitAdapterForModel(connection)
	InitAdapterForJavaScriptObjectNotation(connection)
	return
