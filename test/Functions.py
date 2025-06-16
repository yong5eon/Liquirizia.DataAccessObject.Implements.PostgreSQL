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
	value: int = INT(name='VALUE')
	description: str = VARCHAR(name='DESCRIPTION', null=True)
	atCreated: datetime = TIMESTAMP(name='AT_CREATED', timezone=True)


class TestFunctions(Case):
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
			)
		)
		con: Connection = Helper.Get('Sample')
		con.begin()
		con.run(Drop(SampleModel))
		con.run(Create(SampleModel))
		con.run(Insert(SampleModel).values(
			name='A',
			value=1,
			atCreated=datetime.now(),
		))
		con.run(Insert(SampleModel).values(
			name='A',
			value=1,
			description='This is A',
			atCreated=datetime.now(),
		))
		con.run(Insert(SampleModel).values(
			name='B',
			value=2,
			description='This is B',
			atCreated=datetime.now(),
		))
		con.run(Insert(SampleModel).values(
			name='C',
			value=3,
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
		_ = con.run(Get(SampleModel).values(
			Alias(AggregateToArray(SampleModel.name, distinct=True), 'vs')
		), filter=lambda _: _['vs'])
		ASSERT_IS_EQUAL(_, ['A', 'B', 'C'])
		con.commit()
		return

	@Order(2)
	def testToJSON(self):
		con: Connection = Helper.Get('Sample')
		con.begin()
		_ = con.run(Get(SampleModel).where(
			IsEqualTo(SampleModel.id, 1)
		).values(
			Alias(ToJSON({
				'id': SampleModel.id,
				'name': SampleModel.name,
				'1': 1,
				'2': Value(2),
			}), 'o')
		), filter=lambda _: _['o'])
		ASSERT_IS_EQUAL(_, {
			'id': 1,
			'name': 'A',
			'1': 1,
			'2': 2,
		})
		con.commit()
		return

	@Order(3)
	def testToJSONB(self):
		con: Connection = Helper.Get('Sample')
		con.begin()
		_ = con.run(Get(SampleModel).where(
			IsEqualTo(SampleModel.id, 1)
		).values(
			Alias(ToJSON({
				'id': SampleModel.id,
				'name': SampleModel.name,
				'1': 1,
				'2': Value(2),
			}), 'o')
		), filter=lambda _: _['o'])
		ASSERT_IS_EQUAL(_, {
			'id': 1,
			'name': 'A',
			'1': 1,
			'2': 2,
		})
		con.commit()
		return

	@Order(4)
	def testAggregateToJSON(self):
		con: Connection = Helper.Get('Sample')
		con.begin()
		_ = con.run(Get(SampleModel).values(
			Alias(AggregateToJSON({
				'name': SampleModel.name,
				'1': 1,
				'2': Value(2),
			}), 'vs')
		), filter=lambda _: _['vs'])
		ASSERT_IS_EQUAL(_, [
			{'name': 'A', '1': 1, '2': 2},
			{'name': 'A', '1': 1, '2': 2},
			{'name': 'B', '1': 1, '2': 2},
			{'name': 'C', '1': 1, '2': 2},
		])
		con.commit()
		return

	@Order(5)
	def testAggregateToJSONB(self):
		con: Connection = Helper.Get('Sample')
		con.begin()
		_ = con.run(Get(SampleModel).values(
			Alias(AggregateToJSONB({
				'name': SampleModel.name,
				'1': 1,
				'2': Value(2),
			}), 'vs')
		), filter=lambda _: _['vs'])
		ASSERT_IS_EQUAL(_, [
			{'name': 'A', '1': 1, '2': 2},
			{'name': 'A', '1': 1, '2': 2},
			{'name': 'B', '1': 1, '2': 2},
			{'name': 'C', '1': 1, '2': 2},
		])
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
	
	@Order(6)
	def testCount(self):
		con: Connection = Helper.Get('Sample')
		con.begin()
		_ = con.run(Get(SampleModel).values(
			Alias(Count(SampleModel.name), 'count')
		), filter=lambda _: _['count'])
		ASSERT_IS_EQUAL(_, 4)
		_ = con.run(Get(SampleModel).values(
			Alias(Count(SampleModel.name).where(
				NotIn(SampleModel.name, ['B', 'C'])
			), 'count')
		), filter=lambda _: _['count'])
		ASSERT_IS_EQUAL(_, 2)
		_ = con.run(Get(SampleModel).values(
			Alias(Count(SampleModel.name, distinct=True), 'count')
		), filter=lambda _: _['count'])
		ASSERT_IS_EQUAL(_, 3)
		_ = con.run(Get(SampleModel).values(
			Alias(Count(SampleModel.name, distinct=True).where(
				NotIn(SampleModel.name, ['B', 'C'])
			), 'count')
		), filter=lambda _: _['count'])
		ASSERT_IS_EQUAL(_, 1)
		con.commit()
		return
	
	@Order(7)
	def testSum(self):
		con: Connection = Helper.Get('Sample')
		con.begin()
		_ = con.run(Get(SampleModel).values(
			Alias(Sum(SampleModel.value), 'sum')
		), filter=lambda _: _['sum'])
		ASSERT_IS_EQUAL(_, 7)
		_ = con.run(Get(SampleModel).values(
			Alias(Sum(SampleModel.value).where(
				NotIn(SampleModel.name, ['B', 'C'])
			), 'sum')
		), filter=lambda _: _['sum'])
		ASSERT_IS_EQUAL(_, 2)
		_ = con.run(Get(SampleModel).values(
			Alias(Sum(SampleModel.value, distinct=True), 'sum')
		), filter=lambda _: _['sum'])
		ASSERT_IS_EQUAL(_, 6)
		_ = con.run(Get(SampleModel).values(
			Alias(Sum(SampleModel.value, distinct=True).where(
				NotIn(SampleModel.name, ['B', 'C'])
			), 'sum')
		), filter=lambda _: _['sum'])
		ASSERT_IS_EQUAL(_, 1)
		con.commit()
		return

	@Order(8)
	def testAverage(self):
		con: Connection = Helper.Get('Sample')
		con.begin()
		_ = con.run(Get(SampleModel).values(
			Alias(Average(SampleModel.value), 'avg')
		), filter=lambda _: _['avg'])
		ASSERT_IS_EQUAL(_, 1.75)
		_ = con.run(Get(SampleModel).values(
			Alias(Average(SampleModel.value).where(
				NotIn(SampleModel.name, ['B', 'C'])
			), 'avg')
		), filter=lambda _: _['avg'])
		ASSERT_IS_EQUAL(_, 1.0)
		_ = con.run(Get(SampleModel).values(
			Alias(Average(SampleModel.value, distinct=True), 'avg')
		), filter=lambda _: _['avg'])
		ASSERT_IS_EQUAL(_, 2.0)
		_ = con.run(Get(SampleModel).values(
			Alias(Average(SampleModel.value, distinct=True).where(
				NotIn(SampleModel.name, ['B', 'C'])
			), 'avg')
		), filter=lambda _: _['avg'])
		ASSERT_IS_EQUAL(_, 1.0)
		con.commit()
		return
	
	@Order(9)
	def testMin(self):
		con: Connection = Helper.Get('Sample')
		con.begin()
		_ = con.run(Get(SampleModel).values(
			Alias(Min(SampleModel.value), 'min')
		), filter=lambda _: _['min'])
		ASSERT_IS_EQUAL(_, 1)
		con.commit()
		return
	
	@Order(10)
	def testMax(self):
		con: Connection = Helper.Get('Sample')
		con.begin()
		_ = con.run(Get(SampleModel).values(
			Alias(Max(SampleModel.value), 'max')
		), filter=lambda _: _['max'])
		ASSERT_IS_EQUAL(_, 3)
		con.commit()
		return
	
	@Order(11)
	def testRowNumber(self):
		con: Connection = Helper.Get('Sample')
		con.begin()
		_ = con.run(Select(SampleModel).values(
			Alias(RowNumber(Ascend(SampleModel.value)), 'rn')
		), filter=lambda _: _['rn'])
		ASSERT_IS_EQUAL(_, [1, 2, 3, 4])
		con.commit()
		return
	
	@Order(12)
	def testRank(self):
		con: Connection = Helper.Get('Sample')
		con.begin()
		_ = con.run(Select(SampleModel).values(
			Alias(Rank(Ascend(SampleModel.value)), 'rank')
		), filter=lambda _: _['rank'])
		ASSERT_IS_EQUAL(_, [1, 1, 3, 4])
		con.commit()
		return

	@Order(13)
	def testDenseRank(self):
		con: Connection = Helper.Get('Sample')
		con.begin()
		_ = con.run(Select(SampleModel).values(
			Alias(DenseRank(Ascend(SampleModel.value)), 'rank')
		), filter=lambda _: _['rank'])
		ASSERT_IS_EQUAL(_, [1, 1, 2, 3])
		con.commit()
		return
	
	@Order(14)
	def testIfNull(self):
		con: Connection = Helper.Get('Sample')
		con.begin()
		_ = con.run(Select(SampleModel).values(
			Alias(IfNull(SampleModel.description, 'No Description'), 'desc')
		), filter=lambda _: _['desc'])
		ASSERT_IS_EQUAL(_, ['No Description', 'This is A', 'This is B', 'No Description'])
		con.commit()
		return
	
	@Order(15)
	def testNow(self):
		con: Connection = Helper.Get('Sample')
		con.begin()
		_ = con.run(Get(SampleModel).values(
			Alias(Now(), 'now')
		), filter=lambda _: _['now'])
		ASSERT_IS_NOT_NONE(_)
		con.commit()
		return
	
	@Order(16)
	def testYear(self):
		con: Connection = Helper.Get('Sample')
		con.begin()
		_ = con.run(Get(SampleModel).values(
			Alias(Year(SampleModel.atCreated), 'year')
		), filter=lambda _: _['year'])
		ASSERT_IS_NOT_NONE(_)
		con.commit()
		return
	
	@Order(17)
	def testMonth(self):
		con: Connection = Helper.Get('Sample')
		con.begin()
		_ = con.run(Get(SampleModel).values(
			Alias(Month(SampleModel.atCreated), 'month')
		), filter=lambda _: _['month'])
		ASSERT_IS_NOT_NONE(_)
		con.commit()
		return
	
	@Order(18)
	def testDay(self):
		con: Connection = Helper.Get('Sample')
		con.begin()
		_ = con.run(Get(SampleModel).values(
			Alias(Day(SampleModel.atCreated), 'day')
		), filter=lambda _: _['day'])
		ASSERT_IS_NOT_NONE(_)
		con.commit()
		return
	
	@Order(19)
	def testHour(self):
		con: Connection = Helper.Get('Sample')
		con.begin()
		_ = con.run(Get(SampleModel).values(
			Alias(Hour(SampleModel.atCreated), 'hour')
		), filter=lambda _: _['hour'])
		ASSERT_IS_NOT_NONE(_)
		con.commit()
		return
	
	@Order(20)
	def testMinute(self):
		con: Connection = Helper.Get('Sample')
		con.begin()
		_ = con.run(Get(SampleModel).values(
			Alias(Minute(SampleModel.atCreated), 'minute')
		), filter=lambda _: _['minute'])
		ASSERT_IS_NOT_NONE(_)
		con.commit()
		return
	
	@Order(21)
	def testSecond(self):
		con: Connection = Helper.Get('Sample')
		con.begin()
		_ = con.run(Get(SampleModel).values(
			Alias(Second(SampleModel.atCreated), 'second')
		), filter=lambda _: _['second'])
		ASSERT_IS_NOT_NONE(_)
		con.commit()
		return
	
	@Order(22)
	def testMilliSecond(self):
		con: Connection = Helper.Get('Sample')
		con.begin()
		_ = con.run(Get(SampleModel).values(
			Alias(MilliSecond(SampleModel.atCreated), 'millisecond')
		), filter=lambda _: _['millisecond'])
		ASSERT_IS_NOT_NONE(_)
		con.commit()
		return
	
	@Order(23)
	def testMicroSecond(self):
		con: Connection = Helper.Get('Sample')
		con.begin()
		_ = con.run(Get(SampleModel).values(
			Alias(MicroSecond(SampleModel.atCreated), 'microsecond')
		), filter=lambda _: _['microsecond'])
		ASSERT_IS_NOT_NONE(_)
		con.commit()
		return
	
	@Order(24)
	def testQuarter(self):
		con: Connection = Helper.Get('Sample')
		con.begin()
		_ = con.run(Get(SampleModel).values(
			Alias(Quarter(SampleModel.atCreated), 'quarter')
		), filter=lambda _: _['quarter'])
		ASSERT_IS_NOT_NONE(_)
		con.commit()
		return
	
	@Order(25)
	def testWeek(self):
		con: Connection = Helper.Get('Sample')
		con.begin()
		_ = con.run(Get(SampleModel).values(
			Alias(Week(SampleModel.atCreated), 'week')
		), filter=lambda _: _['week'])
		ASSERT_IS_NOT_NONE(_)
		con.commit()
		return
	
	@Order(26)
	def testDayOfWeek(self):
		con: Connection = Helper.Get('Sample')
		con.begin()
		_ = con.run(Get(SampleModel).values(
			Alias(DayOfWeek(SampleModel.atCreated), 'day_of_week')
		), filter=lambda _: _['day_of_week'])
		ASSERT_IS_NOT_NONE(_)
		con.commit()
		return
	
	@Order(27)
	def testDayOfWeekISO(self):
		con: Connection = Helper.Get('Sample')
		con.begin()
		_ = con.run(Get(SampleModel).values(
			Alias(DayOfWeekISO(SampleModel.atCreated), 'day_of_week_iso')
		), filter=lambda _: _['day_of_week_iso'])
		ASSERT_IS_NOT_NONE(_)
		con.commit()
		return
	
	@Order(28)
	def testTimezone(self):
		con: Connection = Helper.Get('Sample')
		con.begin()
		_ = con.run(Get(SampleModel).values(
			Alias(Timezone(SampleModel.atCreated), 'tz')
		), filter=lambda _: _['tz'])
		ASSERT_IS_NOT_NONE(_)
		con.commit()
		return
	
	@Order(29)
	def testTimezoneHour(self):
		con: Connection = Helper.Get('Sample')
		con.begin()
		_ = con.run(Get(SampleModel).values(
			Alias(TimezoneHour(SampleModel.atCreated), 'tz_hour')
		), filter=lambda _: _['tz_hour'])
		ASSERT_IS_NOT_NONE(_)
		con.commit()
		return

	@Order(30)
	def testTimezoneMinute(self):
		con: Connection = Helper.Get('Sample')
		con.begin()
		_ = con.run(Get(SampleModel).values(
			Alias(TimezoneMinute(SampleModel.atCreated), 'tz_minute')
		), filter=lambda _: _['tz_minute'])
		ASSERT_IS_NOT_NONE(_)
		con.commit()
		return

	@Order(31)
	def testTimezoneHourMinute(self):
		con: Connection = Helper.Get('Sample')
		con.begin()
		_ = con.run(Get(SampleModel).values(
			Alias(TimezoneHourMinute(SampleModel.atCreated), 'tz_second')
		), filter=lambda _: _['tz_second'])
		ASSERT_IS_NOT_NONE(_)
		con.commit()
		return
	
	@Order(32)
	def testMillennium(self):
		con: Connection = Helper.Get('Sample')
		con.begin()
		_ = con.run(Get(SampleModel).values(
			Alias(Millennium(SampleModel.atCreated), 'millennium')
		), filter=lambda _: _['millennium'])
		ASSERT_IS_NOT_NONE(_)
		con.commit()
		return
	
	@Order(33)
	def testCentury(self):
		con: Connection = Helper.Get('Sample')
		con.begin()
		_ = con.run(Get(SampleModel).values(
			Alias(Century(SampleModel.atCreated), 'century')
		), filter=lambda _: _['century'])
		ASSERT_IS_NOT_NONE(_)
		con.commit()
		return
	
	@Order(34)
	def testDecade(self):
		con: Connection = Helper.Get('Sample')
		con.begin()
		_ = con.run(Get(SampleModel).values(
			Alias(Decade(SampleModel.atCreated), 'decade')
		), filter=lambda _: _['decade'])
		ASSERT_IS_NOT_NONE(_)
		con.commit()
		return
	
	@Order(35)
	def testEpoch(self):
		con: Connection = Helper.Get('Sample')
		con.begin()
		_ = con.run(Get(SampleModel).values(
			Alias(Epoch(SampleModel.atCreated), 'epoch')
		), filter=lambda _: _['epoch'])
		ASSERT_IS_NOT_NONE(_)
		con.commit()
		return
	
	@Order(36)
	def testNextVal(self):
		con: Connection = Helper.Get('Sample')
		con.begin()
		_ = con.run(Get(SampleModel).values(
			Alias(NextVal('SEQ_SAMPLE'), 'next_val')
		), filter=lambda _: _['next_val'])
		ASSERT_IS_NOT_NONE(_)
		con.commit()
		return
