# -*- coding: utf-8 -*-

from Liquirizia.Test import *

from Liquirizia.DataAccessObject import Helper
from Liquirizia.DataAccessObject.Properties.Database import Filter

from Liquirizia.DataAccessObject.Implements.PostgreSQL import *
from Liquirizia.DataAccessObject.Implements.PostgreSQL.Types import *
from Liquirizia.DataAccessObject.Implements.PostgreSQL.Values import *
from Liquirizia.DataAccessObject.Implements.PostgreSQL.Functions import *
from Liquirizia.DataAccessObject.Implements.PostgreSQL.Orders import *
from Liquirizia.DataAccessObject.Implements.PostgreSQL.Joins import *
from Liquirizia.DataAccessObject.Implements.PostgreSQL.Exprs import *

from Liquirizia.DataModel import Handler

from datetime import datetime, date
from decimal import Decimal


class SampleTableUpdated(Handler):
	def __call__(self, m, o, v, pv):
		changed = m.__cursor__.run(Update(SampleTable).set(
			**{o.name: v}
		).where(
			EqualTo(SampleTable.id, m.id)
		))
		return
class SampleTable(
	Table,
	name='SAMPLE',
	sequences=(
		Sequence('SEQ_SAMPLE', type=INT)
	),
	constraints=(
		PrimaryKey('PK_SAMPLE', cols=Column('ID')),
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
	colVector: list = VECTOR('COL_VECTOR', size=3, null=True)
	colGeography: Point = GEOGRAPHY('COL_GEOGRAPHY', null=True)


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
				pool=True,
				min=1,
				max=10,
			)
		)
		con: Connection = Helper.Get('Sample')
		con.begin()
		con.execute('CREATE EXTENSION IF NOT EXISTS VECTOR')
		con.execute('CREATE EXTENSION IF NOT EXISTS POSTGIS')
		con.commit()
		return super().setUpClass()
	
	def setUp(self):
		self.con: Connection = Helper.Get('Sample')
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

	@Parameterized(
		{'i': {
			'colBool': True,
			'colShort': 1,
			'colInteger': 2,
			'colLong': 3,
			'colFloat': 4.0,
			'colDecimal': Decimal(5.0),
			'colChar': 'C',
			'colString': 'String',
			'colText': 'Text',
			'colList': [1,2,3],
			'colDictionary': {'a': 1, 'b': 2},
			'colTimestamp': datetime.now(),
			'colDate': datetime.now().date(),
			'colTime': datetime.now().time(),
			'colVector': [1,2,3],
			'colGeography': Point(1, 2),
		}, 'status': True},
	)
	@Order(3)
	def testInsert(self, i, status):
		self.con.run(Create(SampleTable))
		try:
			_ = self.con.run(Insert(SampleTable).values(**i), fetch=SampleTable)
		finally:
			if status:
				ASSERT_IS_NOT_NONE(_)
			else:
				ASSERT_IS_NONE(_)
		return

	@Parameterized(
		{
			'i': {
				'colBool': True,
				'colShort': 1,
				'colInteger': 2,
				'colLong': 3,
				'colFloat': 4.0,
				'colDecimal': Decimal(5.0),
				'colChar': 'C',
				'colString': 'String',
				'colText': 'Text',
				'colList': [1,2,3],
				'colDictionary': {'a': 1, 'b': 2},
				'colTimestamp': datetime.now(),
				'colDate': datetime.now().date(),
				'colTime': datetime.now().time(),
				'colVector': [1,2,3],
				'colGeography': Point(1, 2),
			},
			'u': {
				'colBool': False,
				'colShort': 2,
				'colInteger': 3,
				'colLong': 4,
				'colFloat': 5.0,
				'colDecimal': Decimal(6.0),
				'colChar': 'c',
				'colString': 'string',
				'colText': 'text',
				'colList': [4,5,6],
				'colDictionary': {'a': 3, 'b': 4},
				'colTimestamp': datetime.now(),
				'colDate': datetime.now().date(),
				'colTime': datetime.now().time(),
				'colVector': [4,5,6],
				'colGeography': Point(3, 4),
			},
			'status': True
		},
	)
	@Order(4)
	def testUpdate(self, i, u, status):
		self.con.run(Create(SampleTable))
		try:
			_ = self.con.run(Insert(SampleTable).values(**i), fetch=SampleTable)
			_ = self.con.run(Update(SampleTable).where(EqualTo(SampleTable.id, _.id)).set(**u), fetch=SampleTable)
		finally:
			if status:
				ASSERT_IS_NOT_NONE(_)
			else:
				ASSERT_IS_NONE(_)
		return

	@Parameterized(
		{
			'i': {
				'colBool': True,
				'colShort': 1,
				'colInteger': 2,
				'colLong': 3,
				'colFloat': 4.0,
				'colDecimal': Decimal(5.0),
				'colChar': 'C',
				'colString': 'String',
				'colText': 'Text',
				'colList': [1,2,3],
				'colDictionary': {'a': 1, 'b': 2},
				'colTimestamp': datetime.now(),
				'colDate': datetime.now().date(),
				'colTime': datetime.now().time(),
				'colVector': [1,2,3],
				'colGeography': Point(1, 2),
			},
			'u': {
				'colBool': False,
				'colShort': 2,
				'colInteger': 3,
				'colLong': 4,
				'colFloat': 5.0,
				'colDecimal': Decimal(6.0),
				'colChar': 'c',
				'colString': 'string',
				'colText': 'text',
				'colList': [4,5,6],
				'colDictionary': {'a': 3, 'b': 4},
				'colTimestamp': datetime.now(),
				'colDate': datetime.now().date(),
				'colTime': datetime.now().time(),
				'colVector': [4,5,6],
				'colGeography': Point(3, 4),
			},
		},
	)
	@Order(5)
	def testUpdateWithHandler(self, i, u):
		self.con.run(Create(SampleTable))
		try:
			_ = self.con.run(Insert(SampleTable).values(**i), fetch=SampleTable)
			_.colBool=u['colBool']
			_.colShort=u['colShort']
			_.colInteger=u['colInteger']
			_.colLong=u['colLong']
			_.colFloat=u['colFloat']
			_.colDecimal=u['colDecimal']
			_.colChar=u['colChar']
			_.colString=u['colString']
			_.colText=u['colText']
			_.colList=u['colList']
			_.colDictionary=u['colDictionary']
			_.colTimestamp=u['colTimestamp']
			_.colDate=u['colDate']
			_.colTime=u['colTime']
			_.colVector=u['colVector']
			_.colGeography=u['colGeography']
			_ = self.con.run(Get(SampleTable).where(EqualTo(SampleTable.id, _.id)), fetch=SampleTable)
		finally:
			ASSERT_IS_NOT_NONE(_)
			ASSERT_IS_EQUAL(_.colBool, u['colBool'])
			ASSERT_IS_EQUAL(_.colShort, u['colShort'])
			ASSERT_IS_EQUAL(_.colInteger, u['colInteger'])
			ASSERT_IS_EQUAL(_.colLong, u['colLong'])
			ASSERT_IS_EQUAL(_.colFloat, u['colFloat'])
			ASSERT_IS_EQUAL(_.colDecimal, u['colDecimal'])
			ASSERT_IS_EQUAL(_.colChar, u['colChar'])
			ASSERT_IS_EQUAL(_.colString, u['colString'])
			ASSERT_IS_EQUAL(_.colText, u['colText'])
			ASSERT_IS_EQUAL(list(_.colList), u['colList'])
			ASSERT_IS_EQUAL(dict(_.colDictionary), u['colDictionary'])
			ASSERT_IS_EQUAL(_.colTimestamp, u['colTimestamp'])
			ASSERT_IS_EQUAL(_.colDate, u['colDate'])
			ASSERT_IS_EQUAL(_.colTime, u['colTime'])
			ASSERT_IS_EQUAL(list(_.colVector), u['colVector'])
			ASSERT_IS_EQUAL(_.colGeography, u['colGeography'])
		return

	@Order(6)
	def testDelete(self):
		self.con.run(Create(SampleTable))
		_ = self.con.run(Insert(SampleTable).values(
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
			colGeography=Point(1, 2),
		), fetch=SampleTable)
		ASSERT_IS_NOT_NONE(_)
		self.con.run(Delete(SampleTable).where(EqualTo(SampleTable.id, _.id)))
		_ = self.con.run(Get(SampleTable).where(EqualTo(SampleTable.id, _.id)), fetch=SampleTable)
		# ASSERT
		ASSERT_IS_NONE(_)
		return
	
	@Order(7)
	def testGet(self):
		self.con.run(Create(SampleTable))
		_ = self.con.run(Insert(SampleTable).values(
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
			colGeography=Point(1, 2),
		), fetch=SampleTable)
		# ASSERT
		ASSERT_IS_NOT_NONE(_)
		_ = self.con.run(Get(SampleTable).where(EqualTo(SampleTable.id, _.id)), fetch=SampleTable)
		ASSERT_IS_NOT_NONE(_)
		class RowFilter(Filter):
			def __call__(self, row):
				return {
					'id': row['ID'],
				}
		_ = self.con.run(Get(SampleTable).where(EqualTo(SampleTable.id, _.id)), filter=RowFilter())
		ASSERT_IS_NOT_NONE(_)
		return
