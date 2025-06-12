# -*- coding: utf-8 -*-

from Liquirizia.Test import *

from Liquirizia.DataAccessObject import Helper
from Liquirizia.DataAccessObject.Implements.PostgreSQL import *
from Liquirizia.DataAccessObject.Implements.PostgreSQL.Types import *
from Liquirizia.DataAccessObject.Implements.PostgreSQL.Constraints import *
from Liquirizia.DataAccessObject.Implements.PostgreSQL.Executors import *
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
	atCreated: datetime = TIMESTAMP(name='AT_CREATED')


class TestFunction(Case):
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
			atCreated=datetime.now(),
		))
		con.run(Insert(SampleModel).values(
			name='A',
			description='This is A',
			atCreated=datetime.now(),
		))
		con.run(Insert(SampleModel).values(
			name='B',
			description='This is B',
			atCreated=datetime.now(),
		))
		con.run(Insert(SampleModel).values(
			name='C',
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

	@Order(1)
	def testAggregateToArray(self):
		con: Connection = Helper.Get('Sample')
		con.begin()
		_ = con.run(Get(SampleModel).values(
			Alias(AggregateToArray(SampleModel.name), 'vs')
		), filter=lambda _: _['vs'])
		ASSERT_IS_EQUAL(_, ['A', 'A', 'B', 'C'])
		con.commit()
		return

	@Order(2)
	def testAggregateToArrayDistinct(self):
		con: Connection = Helper.Get('Sample')
		con.begin()
		_ = con.run(Get(SampleModel).values(
			Alias(AggregateToArray(SampleModel.name, distinct=True), 'vs')
		), filter=lambda _: _['vs'])
		ASSERT_IS_EQUAL(_, ['A', 'B', 'C'])
		con.commit()
		return

	@Order(3)
	def testAggregateToJSON(self):
		con: Connection = Helper.Get('Sample')
		con.begin()
		_ = con.run(Get(SampleModel).values(
			Alias(AggregateToJSON({
				'name': SampleModel.name,
			}), 'vs')
		), filter=lambda _: _['vs'])
		ASSERT_IS_EQUAL(_, [
			{'name': 'A'},
			{'name': 'A'},
			{'name': 'B'},
			{'name': 'C'},
		])
		con.commit()
		return

	@Order(5)
	def testAggregateToJSONDistinct(self):
		con: Connection = Helper.Get('Sample')
		con.begin()
		_ = con.run(Get(SampleModel).values(
			Alias(AggregateToJSON({
				'name': SampleModel.name,
			}, distinct=True), 'vs')
		), filter=lambda _: _['vs'])
		ASSERT_IS_EQUAL(_, [
			{'name': 'A'},
			{'name': 'B'},
			{'name': 'C'},
		])
		con.commit()
		return

	@Order(6)
	def testAggregateToJSONB(self):
		con: Connection = Helper.Get('Sample')
		con.begin()
		_ = con.run(Get(SampleModel).values(
			Alias(AggregateToJSONB({
				'name': SampleModel.name,
			}), 'vs')
		), filter=lambda _: _['vs'])
		ASSERT_IS_EQUAL(_, [
			{'name': 'A'},
			{'name': 'A'},
			{'name': 'B'},
			{'name': 'C'},
		])
		con.commit()
		return

	@Order(7)
	def testAggregateToJSONBDistinct(self):
		con: Connection = Helper.Get('Sample')
		con.begin()
		_ = con.run(Get(SampleModel).values(
			Alias(AggregateToJSONB({
				'name': SampleModel.name,
			}, distinct=True), 'vs')
		), filter=lambda _: _['vs'])
		ASSERT_IS_EQUAL(_, [
			{'name': 'A'},
			{'name': 'B'},
			{'name': 'C'},
		])
		con.commit()
		return
