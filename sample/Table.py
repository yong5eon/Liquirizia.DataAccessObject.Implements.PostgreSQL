# -*- coding: utf-8 -*-

from Liquirizia.DataAccessObject import Helper

from Liquirizia.DataAccessObject.Implements.PostgreSQL import *
from Liquirizia.DataAccessObject.Implements.PostgreSQL.Types import *
from Liquirizia.DataAccessObject.Implements.PostgreSQL.Constraints import *
from Liquirizia.DataAccessObject.Implements.PostgreSQL.Functions import *
from Liquirizia.DataAccessObject.Implements.PostgreSQL.Executors import *
from Liquirizia.DataAccessObject.Implements.PostgreSQL.Filters import *
from Liquirizia.DataAccessObject.Implements.PostgreSQL.Orders import *
from Liquirizia.DataAccessObject.Implements.PostgreSQL.Joins import *
from Liquirizia.DataAccessObject.Implements.PostgreSQL.Exprs import *

from Liquirizia.DataModel import Model, Value, Handler
from Liquirizia.Validator import Validator
from Liquirizia.Validator.Patterns import (
	IsToNone,
	IsBool,
	IsInteger,
	IsFloat,
	IsDecimal,
	IsString,
	IsList,
	IsDictionary,
	IsDateTime,
	IsDate,
	IsTime,
)

from Liquirizia.Util import PrettyPrint

from decimal import Decimal
from datetime import datetime, date, time


class SampleModel(Model):
	attrBool : bool = Value(Validator(IsToNone(IsBool())))
	attrInteger : int = Value(Validator(IsToNone(IsInteger())))
	attrFloat : float = Value(Validator(IsToNone(IsFloat())))
	attrDecimal : Decimal = Value(Validator(IsToNone(IsDecimal())))
	attrString : str = Value(Validator(IsToNone(IsString())))
	attrList : list = Value(Validator(IsToNone(IsList())))
	attrDictionary : dict = Value(Validator(IsToNone(IsDictionary())))
	attrDateTime : datetime = Value(Validator(IsToNone(IsDateTime())))
	attrDate : date = Value(Validator(IsToNone(IsDate())))
	attrTime : time = Value(Validator(IsToNone(IsTime())))


class SampleTableUpdated(Handler):
	def __call__(self, m, o, v, pv):
		print('{} of {} is changed {} to {}'.format(
			'{}({})'.format(o.name, o.key),
			'{}({})'.format(m.__class__.__name__, m.__model__),
			v,
			pv,
		))
		changed = m.__cursor__.run(Update(SampleTable).set(
			**{o.name: v}
		).where(
			IsEqualTo(SampleTable.id, m.id)
		))
		print(changed)
		return
class SampleTable(
	Table,
	name='SAMPLE',
	sequences=(
		Sequence('SEQ_SAMPLE', type=INT)
	),
	constraints=(
		PrimaryKey('PK_SAMPLE', cols='ID'),
	),
	fn=SampleTableUpdated()
):
	id : int = INT('ID', default=NextVal('SEQ_SAMPLE'))
	colBool : bool = BOOL('COL_BOOL', null=True)
	colShort : int = INT2('COL_INT2', null=True)
	colInteger : int = INT4('COL_INT', null=True)
	colLong : int = INT4('COL_INT8', null=True)
	colFloat : float = REAL('COL_FLOAT', null=True)
	colDecimal: Decimal = DECIMAL('COL_DECIMAL', scale=10, precision=1, null=True)
	colChar : str = CHAR('COL_CHAR', size=1, null=True)
	colString : str = VARCHAR('COL_VARCHAR', size=256, null=True)
	colText : str = TEXT('COL_TEXT', null=True)
	colList : list = ARRAY('COL_LIST', type='INTEGER', null=True)
	colDictionary : dict = JSON('COL_DICTIONARY', null=True)
	colTimestamp: datetime = TIMESTAMP('COL_TIMESTAMP', null=True)
	colDate: date = DATE('COL_DATE', null=True)
	colTime: date = TIME('COL_TIME', null=True)
	colVector : list = VECTOR('COL_VECTOR', size=3, null=True)
	colDataModel : Model = JSON('COL_DATAMODEL', null=True)


Helper.Set(
	'Sample',
	Connection,
	Configuration(
		host='127.0.0.1',  # PostgreSQL Database Host Address
		port=5432,  # PostgreSQL Database Host Port
		database='postgres',  # Database Name
		username='postgres',  # Database User
		password='password',  # Database Password for User
		persistent=True,  # Is Use Connection Pool, True/False
		min=1, # Minimum Connections in Pool
		max=1, # Maximum Connections in Pool
	)
)

con = Helper.Get('Sample')

con.begin()

# con.execute('CREATE EXTENSION VECTOR')
con.run(Drop(SampleTable))
con.run(Create(SampleTable))

o = SampleModel(
	attrBool=True,
	attrInteger=1,
	attrFloat=1.0,
	attrDecimal=Decimal(1.0),
	attrString='String',
	attrList=[1,2,3],
	attrDictionary={
		'Bool': True,
		'Integer': 1,
		'Float': 1.0,
		'Decimal': Decimal(1.0),
		'String': 'String',
		'List': [1,2,3],
		'Dictionary': {
			'Bool': True,
			'Integer': 1,
			'Float': 1.0,
			'Decimal': Decimal(1.0),
			'String': 'String',
		}
	},
	attrDateTime=datetime.now(),
	attrDate=datetime.now().date(),
	attrTime=datetime.now().time(),
)

# INSERT
_ = con.run(
	Insert(SampleTable).values(
		colBool=True,
		colShort=1,
		colInteger=1,
		colLong=1,
		colFloat=1.0,
		colDecimal=Decimal(1.0),
		colChar='C',
		colString='String',
		colText='Text',
		colList=[1,2,3],
		colDictionary={'a': 1, 'b': 2},
		colTimestamp=datetime.now(),
		colDate=datetime.now().date(),
		colTime=datetime.now().time(),
		colVector=[1,2,3],
		colDataModel=o,
	),
	fetch=SampleTable
)

PrettyPrint(_)

o = SampleModel(
	attrBool=False,
	attrInteger=2,
	attrFloat=2.0,
	attrDecimal=Decimal(2.0),
	attrString='string',
	attrList=[4,5,6],
	attrDictionary={
		'Bool': False,
		'Integer': 2,
		'Float': 2.0,
		'Decimal': Decimal(2.0),
		'String': 'string',
		'List': [4,5,6],
		'Dictionary': {
			'Bool': False,
			'Integer': 2,
			'Float': 2.0,
			'Decimal': Decimal(2.0),
			'String': 'string',
		}
	},
	attrDateTime=datetime.now(),
	attrDate=datetime.now().date(),
	attrTime=datetime.now().time(),
)


# HANDLER
_.colBool=False
_.colShort=2
_.colInteger=3
_.colLong=4
_.colFloat=5.0
_.colDecimal=Decimal(6.0)
_.colChar='S'
_.colString='ChangedString'
_.colText='ChangedText'
_.colList=[4,5,6]
_.colList.append(7)
_.colList.extend([8, 9])
_.colDictionary={'c': 3, 'd': 4}
_.colDictionary['e'] = 5
_.colTimestamp=datetime.now()
_.colDate=datetime.now().date()
_.colTime=datetime.now().time()
_.colVector=[4,5,6]
_.colDataModel=o

# SELECT
_ = con.run(Select(SampleTable), fetch=SampleTable)
PrettyPrint(_)

# GET
_ = con.run(Get(SampleTable), fetch=SampleTable)
PrettyPrint(_)

# DELETE
_ = con.run(Delete(SampleTable).where(IsEqualTo(SampleTable.id, 1)))
_ = con.run(Select(SampleTable), fetch=SampleTable)
PrettyPrint(_)

con.run(Drop(SampleTable))
con.commit()

