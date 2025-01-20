# -*- coding: utf-8 -*-

from Liquirizia.Test import *

from Liquirizia.DataAccessObject import Helper

from Liquirizia.DataAccessObject.Implements.PostgreSQL import *
from Liquirizia.DataAccessObject.Implements.PostgreSQL.Types import *
from Liquirizia.DataAccessObject.Implements.PostgreSQL.Constraints import *
from Liquirizia.DataAccessObject.Implements.PostgreSQL.Functions import *
from Liquirizia.DataAccessObject.Implements.PostgreSQL.Executors import *
from Liquirizia.DataAccessObject.Implements.PostgreSQL.Executors.Filters import *
from Liquirizia.DataAccessObject.Implements.PostgreSQL.Executors.Orders import *
from Liquirizia.DataAccessObject.Implements.PostgreSQL.Executors.Joins import *
from Liquirizia.DataAccessObject.Implements.PostgreSQL.Executors.Exprs import *


from Liquirizia.DataModel import Model, Value, Handler
from Liquirizia.Validator import Validator, Pattern
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
	If,
	ToDecimal,
)

from datetime import datetime, date, time
from time import mktime
from decimal import Decimal
from copy import deepcopy


class StrToDateTime(Pattern):
	def __call__(self, parameter):
		return datetime.fromisoformat(parameter)

class StrToDate(Pattern):
	def __call__(self, parameter):
		return date.fromisoformat(parameter)
	
class StrToTime(Pattern):
	def __call__(self, parameter):
		return time.fromisoformat(parameter)


class SampleModel(Model):
	attrBool : bool = Value(Validator(IsToNone(IsBool())))
	attrInteger : int = Value(Validator(IsToNone(IsInteger())))
	attrFloat : float = Value(Validator(IsToNone(IsFloat())))
	attrDecimal : Decimal = Value(Validator(IsToNone(If(IsString(ToDecimal())),IsDecimal())))
	attrString : str = Value(Validator(IsToNone(IsString())))
	attrList : list = Value(Validator(IsToNone(IsList())))
	attrDictionary : dict = Value(Validator(IsToNone(IsDictionary())))
	attrDateTime : datetime = Value(Validator(IsToNone(If(IsString(StrToDateTime())),IsDateTime())))
	attrDate : date = Value(Validator(IsToNone(If(IsString(StrToDate())),IsDate())))
	attrTime : time = Value(Validator(IsToNone(If(IsString(StrToTime())),IsTime())))


class SampleTableUpdated(Handler):
	def __call__(self, m, o, v, pv):
		changed = m.__cursor__.run(Update(SampleTable).set(
			**{o.name: v}
		).where(
			IsEqualTo(SampleTable.id, m.id)
		))
		return
class SampleTable(
	Table,
	table='SAMPLE',
	sequences=(
		Sequence('SEQ_SAMPLE', type=INT)
	),
	constraints=(
		PrimaryKey('PK_SAMPLE', cols='ID'),
	),
	fn=SampleTableUpdated(),
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


class TestTable(Case):
	@classmethod
	def setUpClass(cls):
		Helper.Set(
			'Sample',
			Connection,
			Configuration(
				host='127.0.0.1',  # PostgreSQL Database Host Address
				port=5432,  # PostgreSQL Database Host Port
				database='postgres',  # Database Name
				username='postgres',  # Database User
				password='password',  # Database Password for User
				persistent=True,  # Is Persistent Connection, True/False
				min=1,
				max=10,
			)
		)
		con = Helper.Get('Sample')
		con.begin()
		con.execute('CREATE EXTENSION IF NOT EXISTS VECTOR')
		con.commit()
		return super().setUpClass()
	
	def setUp(self):
		self.con = Helper.Get('Sample')
		self.con.begin()
		return super().setUp()
	
	def tearDown(self):
		self.con.commit()
		return super().tearDown()

	@Order(1)
	def testCreate(self):
		self.con.run(Create(SampleTable))
		return

	@Order(2)
	def testDrop(self):
		self.con.run(Create(SampleTable))
		self.con.run(Drop(SampleTable))
		return

	@Order(3)
	def testInsert(self):
		self.con.run(Create(SampleTable))
		o = SampleModel(
			attrBool=True,
			attrInteger=0,
			attrFloat=0.0,
			attrDecimal=Decimal(0.0),
			attrString='String',
			attrList=[0,2,3],
			attrDictionary={
				'Bool': True,
				'Integer': 0,
				'Float': 0.0,
				'Decimal': Decimal(0.0),
				'String': 'String',
				'List': [0,2,3],
				'Dictionary': {
					'Bool': True,
					'Integer': 0,
					'Float': 0.0,
					'Decimal': Decimal(0.0),
					'String': 'String',
				}
			},
			attrDateTime=datetime.now(),
			attrDate=datetime.now().date(),
			attrTime=datetime.now().time(),
		)
		inserted = self.con.run(Insert(SampleTable).values(
			colBool=True,
			colShort=1,
			colInteger=2,
			colLong=3,
			colFloat=4.0,
			colDecimal=Decimal(5.0),
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
		))
		# ASSERT
		ASSERT_IS_NOT_NONE(inserted)
		ASSERT_IS_EQUAL(inserted.colBool, True)
		ASSERT_IS_EQUAL(inserted.colShort, 1)
		ASSERT_IS_EQUAL(inserted.colInteger, 2)
		ASSERT_IS_EQUAL(inserted.colLong, 3)
		ASSERT_IS_EQUAL(inserted.colFloat, 4.0)
		ASSERT_IS_EQUAL(inserted.colDecimal, Decimal(5.0))
		ASSERT_IS_EQUAL(inserted.colChar, 'C')
		ASSERT_IS_EQUAL(inserted.colString, 'String')
		ASSERT_IS_EQUAL(inserted.colText, 'Text')
		ASSERT_IS_EQUAL(list(inserted.colList), [1,2,3])
		ASSERT_IS_EQUAL(dict(inserted.colDictionary), {'a':1, 'b': 2})
		ASSERT_IS_EQUAL(list(inserted.colVector), [1,2,3])
		# ASSERT_IS_EQUAL(inserted.colDataModel, o)
		return

	@Order(4)
	def testUpdate(self):
		self.con.run(Create(SampleTable))
		o = SampleModel(
			attrBool=True,
			attrInteger=0,
			attrFloat=0.0,
			attrDecimal=Decimal(0.0),
			attrString='String',
			attrList=[0,2,3],
			attrDictionary={
				'Bool': True,
				'Integer': 0,
				'Float': 0.0,
				'Decimal': Decimal(0.0),
				'String': 'String',
				'List': [0,2,3],
				'Dictionary': {
					'Bool': True,
					'Integer': 0,
					'Float': 0.0,
					'Decimal': Decimal(0.0),
					'String': 'String',
				}
			},
			attrDateTime=datetime.now(),
			attrDate=datetime.now().date(),
			attrTime=datetime.now().time(),
		)
		inserted = self.con.run(Insert(SampleTable).values(
			colBool=True,
			colShort=1,
			colInteger=2,
			colLong=3,
			colFloat=4.0,
			colDecimal=Decimal(5.0),
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
		))
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
		updated = self.con.run(Update(SampleTable).where(IsEqualTo(SampleTable.id, inserted.id)).set(
			colBool=False,
			colShort=2,
			colInteger=3,
			colLong=4,
			colFloat=5.0,
			colDecimal=Decimal(6.0),
			colChar='c',
			colString='string',
			colText='text',
			colList=[4,5,6],
			colDictionary={'a': 3, 'b': 4},
			colTimestamp=datetime.now(),
			colDate=datetime.now().date(),
			colTime=datetime.now().time(),
			colVector=[4,5,6],
			colDataModel=o,
		))
		# ASSERT
		ASSERT_IS_NOT_NONE(inserted)
		ASSERT_IS_NOT_NONE(updated)
		ASSERT_IS_NOT_EQUAL(inserted.colBool, updated.colBool)
		ASSERT_IS_NOT_EQUAL(inserted.colShort, updated.colShort)
		ASSERT_IS_NOT_EQUAL(inserted.colInteger, updated.colInteger)
		ASSERT_IS_NOT_EQUAL(inserted.colLong, updated.colLong)
		ASSERT_IS_NOT_EQUAL(inserted.colFloat, updated.colFloat)
		ASSERT_IS_NOT_EQUAL(inserted.colDecimal, updated.colDecimal)
		ASSERT_IS_NOT_EQUAL(inserted.colChar, updated.colChar)
		ASSERT_IS_NOT_EQUAL(inserted.colString, updated.colString)
		ASSERT_IS_NOT_EQUAL(inserted.colText, updated.colText)
		ASSERT_IS_NOT_EQUAL(inserted.colList, updated.colList)
		ASSERT_IS_NOT_EQUAL(inserted.colDictionary, updated.colDictionary)
		ASSERT_IS_NOT_EQUAL(inserted.colVector, updated.colVector)
		ASSERT_IS_NOT_EQUAL(inserted.colDataModel, updated.colDataModel)
		return

	@Order(5)
	def testUpdateWithHandler(self):
		self.con.run(Create(SampleTable))
		o = SampleModel(
			attrBool=True,
			attrInteger=0,
			attrFloat=0.0,
			attrDecimal=Decimal(0.0),
			attrString='String',
			attrList=[0,2,3],
			attrDictionary={
				'Bool': True,
				'Integer': 0,
				'Float': 0.0,
				'Decimal': Decimal(0.0),
				'String': 'String',
				'List': [0,2,3],
				'Dictionary': {
					'Bool': True,
					'Integer': 0,
					'Float': 0.0,
					'Decimal': Decimal(0.0),
					'String': 'String',
				}
			},
			attrDateTime=datetime.now(),
			attrDate=datetime.now().date(),
			attrTime=datetime.now().time(),
		)
		inserted = self.con.run(Insert(SampleTable).values(
			colBool=True,
			colShort=1,
			colInteger=2,
			colLong=3,
			colFloat=4.0,
			colDecimal=Decimal(5.0),
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
		))
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
		inserted.colBool=False
		inserted.colShort=2
		inserted.colInteger=3
		inserted.colLong=4
		inserted.colFloat=5.0
		inserted.colDecimal=Decimal(6.0)
		inserted.colChar='c'
		inserted.colString='string'
		inserted.colText='text'
		inserted.colList=[4,5,6]
		inserted.colDictionary={'a': 3, 'b': 4}
		inserted.colTimestamp=datetime.now()
		inserted.colDate=datetime.now().date()
		inserted.colTime=datetime.now().time()
		inserted.colVector=[4,5,6]
		inserted.colDataModel=o
		# ASSERT
		updated = self.con.run(Get(SampleTable).where(IsEqualTo(SampleTable.id, inserted.id)).to(SampleTable))
		ASSERT_IS_NOT_NONE(inserted)
		ASSERT_IS_NOT_NONE(updated)
		ASSERT_IS_EQUAL(inserted.colBool, updated.colBool)
		ASSERT_IS_EQUAL(inserted.colShort, updated.colShort)
		ASSERT_IS_EQUAL(inserted.colInteger, updated.colInteger)
		ASSERT_IS_EQUAL(inserted.colLong, updated.colLong)
		ASSERT_IS_EQUAL(inserted.colFloat, updated.colFloat)
		ASSERT_IS_EQUAL(inserted.colDecimal, updated.colDecimal)
		ASSERT_IS_EQUAL(inserted.colChar, updated.colChar)
		ASSERT_IS_EQUAL(inserted.colString, updated.colString)
		ASSERT_IS_EQUAL(inserted.colText, updated.colText)
		ASSERT_IS_EQUAL(list(inserted.colList), list(updated.colList))
		ASSERT_IS_EQUAL(dict(inserted.colDictionary), dict(updated.colDictionary))
		ASSERT_IS_EQUAL(list(inserted.colVector), list(updated.colVector))
		# ASSERT_IS_EQUAL(inserted.colDataModel, updated.colDataModel)
		return

	@Order(6)
	def testDelete(self):
		self.con.run(Create(SampleTable))
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
		inserted = self.con.run(Insert(SampleTable).values(
			colBool=True,
			colShort=1,
			colInteger=2,
			colLong=3,
			colFloat=4.0,
			colDecimal=Decimal(5.0),
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
			colDataModelBool=o.attrBool,
			colDataModelInteger=o.attrInteger,
			colDataModelFloat=o.attrFloat,
			colDataModelDecimal=o.attrDecimal,
			colDataModelString=o.attrString,
			colDataModelList=o.attrList,
			colDataModelDictionary=dict(o.attrDictionary),
		))
		self.con.run(Delete(SampleTable).where(IsEqualTo(SampleTable.id, inserted.id)))
		_ = self.con.run(Get(SampleTable).where(IsEqualTo(SampleTable.id, inserted.id)).to(SampleTable))
		# ASSERT
		ASSERT_IS_NONE(_)
		return
	
