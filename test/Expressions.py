# -*- coding: utf-8 -*-

from Liquirizia.Test import *

from Liquirizia.DataAccessObject import Helper
from Liquirizia.DataAccessObject.Implements.PostgreSQL import *
from Liquirizia.DataAccessObject.Implements.PostgreSQL.Types import *
from Liquirizia.DataAccessObject.Implements.PostgreSQL.Functions import *
from Liquirizia.DataAccessObject.Implements.PostgreSQL.Orders import *
from Liquirizia.DataAccessObject.Implements.PostgreSQL.Joins import *
from Liquirizia.DataAccessObject.Implements.PostgreSQL.Exprs import *

from datetime import datetime


class SampleModel(
	Table,
	name='SAMPLE',
	sequences=(
		Sequence(name='SEQ_SAMPLE', type=INT),
	),
	constraints=(
		PrimaryKey(name='PK_SAMPLE', cols='ID'),
	),
	indexes=(),
):
	id: int = INT(name='ID', default=NextVal('SEQ_SAMPLE'))
	name: str = VARCHAR(name='NAME')
	description: str = VARCHAR(name='DESCRIPTION', null=True)
	data: dict = JSONB(name='DATA', null=True)
	atCreated: datetime = TIMESTAMP(name='AT_CREATED')


class TestExpressions(Case):
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
		con.run(Drop(SampleModel))
		con.run(Create(SampleModel))
		con.run(Insert(SampleModel).values(
			name='A',
			data={'1': 1, '2': 2.0, '3': 'abc'},
			atCreated=datetime.now(),
		))
		con.run(Insert(SampleModel).values(
			name='B',
			description='This is B',
			data={'1': 2, '2': 3.0, '3': 'def'},
			atCreated=datetime.now(),
		))
		con.run(Insert(SampleModel).values(
			name='C',
			data={'1': 3, '2': 4.0, '3': 'ghi'},
			atCreated=datetime.now(),
		))
		con.commit()
		return super().setUpClass()

	@classmethod
	def tearDownClass(cls):
		con: Connection = Helper.Get('Sample')
		con.begin()
		con.run(Drop(SampleModel))
		con.commit()
		return super().tearDownClass()

	# COMMON
	## ALIAS
	@Order(1)
	def testAlias(self):
		con: Connection = Helper.Get('Sample')
		con.begin()
		rows = con.run(Select(SampleModel).values(
			Alias(SampleModel.name, 'NM')
		))
		for row in rows:
			ASSERT_IS_EQUAL('NM' in row, True)
		con.commit()
		return

	## TYPE CAST
	@Order(2)
	def testTypeTo(self):
		con: Connection = Helper.Get('Sample')
		con.begin()
		rows = con.run(Select(SampleModel).values(
			TypeTo(SampleModel.id, FLOAT)
		))
		for row in rows:
			ASSERT_IS_EQUAL(isinstance(row['ID'], float), True)
		con.commit()
		return

	## IF
	@Order(3)
	def testIf(self):
		con: Connection = Helper.Get('Sample')
		con.begin()
		rows = con.run(Select(SampleModel).values(
			SampleModel.description,
			Alias(
				If(
					IsNotNull(
						SampleModel.description
					)
				).then_(Value('Y')).else_(Value('N')), 'STATUS'
			),
		))
		for row in rows:
			if row['DESCRIPTION']:
				ASSERT_IS_EQUAL(row['STATUS'], 'Y')
			else:
				ASSERT_IS_EQUAL(row['STATUS'], 'N')
		con.commit()
		return

	## IFNULL
	@Order(4)
	def testIfNull(self):
		con: Connection = Helper.Get('Sample')
		con.begin()
		_ = con.run(Select(SampleModel).values(
			Alias(
				IfNull(SampleModel.description, Value('No Description')),
				'_'
			),
		), filter=lambda row: row['_'])
		ASSERT_IS_EQUAL(_, [
			'No Description',
			'This is B',
			'No Description',
		])
		_ = con.run(Select(SampleModel).values(
			Alias(
				IfNull(SampleModel.description, 'No Description', 'Description'),
				'_'
			),
		), filter=lambda row: row['_'])
		ASSERT_IS_EQUAL(_, [
			'No Description',
			'Description',
			'No Description',
		])
		con.commit()
		return

	## IFNOTNULL
	@Order(5)
	def testIfNotNull(self):
		con: Connection = Helper.Get('Sample')
		con.begin()
		_ = con.run(Select(SampleModel).values(
			Alias(
				IfNotNull(SampleModel.description, Value('Description')),
				'_'
			),
		), filter=lambda row: row['_'])
		ASSERT_IS_EQUAL(_, [
			None,
			'Description',
			None,
		])
		_ = con.run(Select(SampleModel).values(
			Alias(
				IfNotNull(SampleModel.description, 'Description', 'No Description'),
				'_'
			),
		), filter=lambda row: row['_'])
		ASSERT_IS_EQUAL(_, [
			'No Description',
			'Description',
			'No Description',
		])
		con.commit()
		return

	## SWITCH(CASE WHEN THEN ELSE END)	
	@Order(6)
	def testSwitch(self):
		con: Connection = Helper.Get('Sample')
		con.begin()
		rows = con.run(Select(SampleModel).values(
			Alias(Switch().case(
				EqualTo(SampleModel.name, 'A'),
				1,
			).case(
				EqualTo(SampleModel.name, 'B'),
				2,
			).other(
				0
			), 'switch'),
		), filter=lambda row: row['switch'])
		ASSERT_IS_EQUAL(rows, [1,2,0])
		con.commit()
		return
	
	# CONDITION
	## IN
	@Order(7)
	def testIn(self):
		con: Connection = Helper.Get('Sample')
		con.begin()
		rows = con.run(Select(SampleModel).where(
			In(SampleModel.name, (Value('A'), Value('B')))
		))
		ASSERT_IS_EQUAL(len(rows), 2)
		con.commit()
		return

	## NOT IN
	@Order(8)
	def testNotIn(self):
		con: Connection = Helper.Get('Sample')
		con.begin()
		rows = con.run(Select(SampleModel).where(
			NotIn(SampleModel.name, (Value('A'), Value('B')))
		))
		ASSERT_IS_EQUAL(len(rows), 1)
		con.commit()
		return

	## IS
	@Order(9)
	def testIs(self):
		con: Connection = Helper.Get('Sample')
		con.begin()
		rows = con.run(Select(SampleModel).where(
			IsNull(SampleModel.description)
		))
		ASSERT_IS_EQUAL(len(rows), 2)
		con.commit()
		return

	## IS NULL
	@Order(10)
	def testIsNull(self):
		con: Connection = Helper.Get('Sample')
		con.begin()
		rows = con.run(Select(SampleModel).where(
			IsNull(SampleModel.description)
		))
		ASSERT_IS_EQUAL(len(rows), 2)
		con.commit()
		return

	## IS NOT NULL
	@Order(11)
	def testIsNotNull(self):
		con: Connection = Helper.Get('Sample')
		con.begin()
		rows = con.run(Select(SampleModel).where(
			IsNotNull(SampleModel.description)
		))
		ASSERT_IS_EQUAL(len(rows), 1)
		con.commit()
		return

	# CONDITION	
	## AND
	@Order(12)
	def testAnd(self):
		con: Connection = Helper.Get('Sample')
		con.begin()
		rows = con.run(Select(SampleModel).where(
			And(
				IsNotNull(SampleModel.description),
				Like(SampleModel.name, 'B')
			)
		))
		ASSERT_IS_EQUAL(len(rows), 1)
		con.commit()
		return

	## OR
	@Order(13)
	def testOr(self):
		con: Connection = Helper.Get('Sample')
		con.begin()
		rows = con.run(Select(SampleModel).where(
			Or(
				IsNotNull(SampleModel.description),
				Like(SampleModel.name, 'C')
			)
		))
		ASSERT_IS_EQUAL(len(rows), 2)
		con.commit()
		return

	# COMPARE
	## = EqualTo
	@Order(14)
	def testEqualTo(self):
		con: Connection = Helper.Get('Sample')
		con.begin()
		_ = con.run(Select(SampleModel).where(
			EqualTo(SampleModel.name, 'A')
		), filter=lambda row: row['NAME'])
		ASSERT_IS_EQUAL(_, ['A'])
		con.commit()
		return
	## != NotEqualTo
	@Order(15)
	def testNotEqualTo(self):
		con: Connection = Helper.Get('Sample')
		con.begin()
		_ = con.run(Select(SampleModel).where(
			NotEqualTo(SampleModel.name, 'A')
		), filter=lambda row: row['NAME'])
		ASSERT_IS_EQUAL(_, ['B', 'C'])
		con.commit()
		return
	## > GreaterThan
	@Order(16)
	def testGreaterThan(self):
		con: Connection = Helper.Get('Sample')
		con.begin()
		_ = con.run(Select(SampleModel).where(
			GreaterThan(SampleModel.id, 1)
		), filter=lambda row: row['ID'])
		ASSERT_IS_EQUAL(_, [2, 3])
		con.commit()
		return
	## >= GreaterEqualTo
	@Order(17)
	def testGreaterEqualTo(self):
		con: Connection = Helper.Get('Sample')
		con.begin()
		_ = con.run(Select(SampleModel).where(
			GreaterEqualTo(SampleModel.id, 1)
		), filter=lambda row: row['ID'])
		ASSERT_IS_EQUAL(_, [1, 2, 3])
		con.commit()
		return
	## < LessThan
	@Order(18)
	def testLessThan(self):
		con: Connection = Helper.Get('Sample')
		con.begin()
		_ = con.run(Select(SampleModel).where(
			LessThan(SampleModel.id, 3)
		), filter=lambda row: row['ID'])
		ASSERT_IS_EQUAL(_, [1, 2])
		con.commit()
		return
	## <= LessEqualTo
	@Order(19)
	def testLessEqualTo(self):
		con: Connection = Helper.Get('Sample')
		con.begin()
		_ = con.run(Select(SampleModel).where(
			LessEqualTo(SampleModel.id, 2)
		), filter=lambda row: row['ID'])
		ASSERT_IS_EQUAL(_, [1, 2])
		con.commit()
		return

	# STRING	
	## LIKE '%{}%'
	@Order(20)
	def testLike(self):
		con: Connection = Helper.Get('Sample')
		con.begin()
		_ = con.run(Select(SampleModel).where(
			Like(SampleModel.name, 'A')
		), filter=lambda row: row['NAME'])
		ASSERT_IS_EQUAL(_, ['A'])
		con.commit()
		return

	## LIKE '{}%'
	@Order(21)
	def testLikeStartWith(self):
		con: Connection = Helper.Get('Sample')
		con.begin()
		_ = con.run(Select(SampleModel).where(
			LikeStartWith(SampleModel.name, 'B')
		), filter=lambda row: row['NAME'])
		ASSERT_IS_EQUAL(_, ['B'])
		con.commit()
		return

	## LIKE '%{}'
	@Order(22)
	def testLikeEndWith(self):
		con: Connection = Helper.Get('Sample')
		con.begin()
		_ = con.run(Select(SampleModel).where(
			LikeEndWith(SampleModel.name, 'C')
		), filter=lambda row: row['NAME'])
		ASSERT_IS_EQUAL(_, ['C'])
		con.commit()
		return
	
	# JSON
	## OF
	@Order(23)
	def testOf(self):
		con: Connection = Helper.Get('Sample')
		con.begin()
		rows = con.run(Select(SampleModel).values(
			Alias(Of(
				SampleModel.data,
				'1',
			), '1'),
		), filter=lambda row: row['1'])
		ASSERT_IS_EQUAL(rows, [1, 2, 3])
		rows = con.run(Select(SampleModel).values(
			Alias(Of(
				SampleModel.data,
				'2',
				INTEGER,
			), '2'),
		), filter=lambda row: row['2'])
		ASSERT_IS_EQUAL(rows, [2, 3, 4])
		con.commit()
		return

	# SUBQUERY
	@Order(24)
	def testSubQuery(self):
		con: Connection = Helper.Get('Sample')
		con.begin()
		rows = con.run(Select(SampleModel).values(
			Alias(SampleModel.name, 'NAME'),
			Alias(Query(
				Get(SampleModel).where(
					EqualTo(SampleModel.id, 2)
				).values(
					SampleModel.description
				).limit(1)),
				'DESC'
			),
		))
		ASSERT_IS_EQUAL(rows, [
			{'NAME': 'A', 'DESC': 'This is B'},
			{'NAME': 'B', 'DESC': 'This is B'},
			{'NAME': 'C', 'DESC': 'This is B'},
		])
		con.commit()
		return
