# -*- coding: utf-8 -*-

from .Bool import Bool
from .Numeric import (
	Short,
	Integer,
	Long,
	Float,
	Double,
	Decimal,
)
from .String import (
	Char,
	String,
	Text,
)
from .DateTime import (
	Timestamp,
	Date,
	Time,
)
from .Binary import Binary
from .JavaScriptObjectNotation import (
	JavaScriptObjectNotation,
	JavaScriptObjectNotationByteArray,
)
from .Array import Array
from .Vector import Vector
from .Geography import Geography

__all__ = (
	'Bool', 'BOOL', 'BOOLEAN',
	'Short', 'INT2', 'SMALLINT',
	'Integer', 'INT', 'INT4', 'INTEGER',
	'Long', 'INT8', 'BIGINT',
	'Float', 'FLOAT', 'REAL',
	'Double', 'DOUBLE',
	'Decimal', 'DECIMAL', 'NUMERIC',
	'Char', 'CHAR',
	'String', 'VARCHAR', 'STRING',
	'Text', 'TEXT',
	'Date', 'DATE',
	'Time', 'TIME',
	'Timestamp', 'TIMESTAMP',
	'Binary', 'BLOB', 'BYTES', 'BYTEARRAY', 'BYTESTREAM',
	'JavaScriptObjectNotation', 'JSON',
	'JavaScriptObjectNotationByteArray', 'JSONB',
	'Array', 'ARRAY',
	'Vector', 'VECTOR',
	'Geography', 'GEOGRAPHY',
)

# PRE-DEFINED TYPE
## BOOL
BOOL = Bool
BOOLEAN = Bool
## INTEGER
INT2 = Short
SMALLINT = Short
INT = Integer
INTEGER = Integer
INT4 = Integer
INT8 = Long
BIGINT = Long
## FLOAT
FLOAT = Float
REAL = Float
## DOUBLE
DOUBLE = Double
## DECIMAL
DECIMAL = Decimal
NUMERIC = Decimal
## STRING
CHAR = Char
VARCHAR = String
STRING = String
TEXT = Text
## DATETIME
DATE = Date
TIME = Time
TIMESTAMP = Timestamp
## BYTE ARRAY
BLOB = Binary
BYTES = Binary
BYTEARRAY = Binary
BYTESTREAM = Binary
## JSON
JSON = JavaScriptObjectNotation
JSONB = JavaScriptObjectNotationByteArray
## ARRAY
ARRAY = Array
## VECTOR
VECTOR = Vector
## GEOGRAPHY
GEOGRAPHY = Geography
