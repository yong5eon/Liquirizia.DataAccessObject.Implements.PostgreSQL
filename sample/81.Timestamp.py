# -*- coding: utf-8 -*-

from Liquirizia.DataAccessObject import Helper

from Liquirizia.DataAccessObject.Implements.PostgreSQL import *
from Liquirizia.DataAccessObject.Implements.PostgreSQL.Types import *
from Liquirizia.DataAccessObject.Implements.PostgreSQL.Values import *
from Liquirizia.DataAccessObject.Implements.PostgreSQL.Constraints import *
from Liquirizia.DataAccessObject.Implements.PostgreSQL.Functions import *
from Liquirizia.DataAccessObject.Implements.PostgreSQL.Executors import *
from Liquirizia.DataAccessObject.Implements.PostgreSQL.Orders import *
from Liquirizia.DataAccessObject.Implements.PostgreSQL.Joins import *
from Liquirizia.DataAccessObject.Implements.PostgreSQL.Exprs import *

from Liquirizia.Utils import PrettyPrint

from datetime import datetime, timezone, timedelta, date, time


class SampleTable(
	Table,
	name='SAMPLE',
	sequences=(
		Sequence('SEQ_SAMPLE', type=INT)
	),
	constraints=(
		PrimaryKey('PK_SAMPLE', cols=Column('ID')),
	),
):
	id : int = INT('ID', default=NextVal('SEQ_SAMPLE'))
	colTimestamp: datetime = TIMESTAMP('COL_TIMESTAMP', null=True)
	colTimestampTZ: datetime = TIMESTAMP('COL_TIMESTAMP_WITH_TIMEZONE', timezone=True, null=True)
	colTimestampTZD: datetime = TIMESTAMP('COL_TIMESTAMP_WITH_TIMEZONE_HAS_DEFAULT', timezone=True, default=Now())
	colDate: date = DATE('COL_DATE', default=Now())
	colTime: time = TIME('COL_TIME', default=Now())


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

con.execute('SET TIME ZONE "Asia/Seoul"') # Asia/Seoul

con.run(Drop(SampleTable))
con.run(Create(SampleTable))

# INSERT
ROK = timezone(timedelta(hours=9)) # Asia/Seoul
THA = timezone(timedelta(hours=7)) # Asia/Bangkok

dt = datetime.now()
dtz = dt.astimezone(tz=ROK)
_: SampleTable = con.run(
	Insert(SampleTable).values(
		colTimestamp=dt,
		colTimestampTZ=dtz,
		colTimestampTZD=dtz,
	),
	fetch=SampleTable
)

PrettyPrint(_)
print(_.colTimestampTZ.astimezone(THA))
print(_.colTimestampTZD.astimezone(THA))

_ = con.run(Get(SampleTable).values(
	Alias(SampleTable.colTimestamp, 'ts'),
	Alias(Year(SampleTable.colTimestamp), 'year'),
	Alias(Month(SampleTable.colTimestamp), 'month'),
	Alias(Day(SampleTable.colTimestamp), 'day'),
	Alias(Hour(SampleTable.colTimestamp), 'hour'),
	Alias(Minute(SampleTable.colTimestamp), 'minute'),
	Alias(Second(SampleTable.colTimestamp), 'second'),
	Alias(MilliSecond(SampleTable.colTimestamp), 'millisecond'),
	Alias(MicroSecond(SampleTable.colTimestamp), 'microsecond'),
	Alias(Quarter(SampleTable.colTimestamp), 'quarter'),
	Alias(Week(SampleTable.colTimestamp), 'week'),
	Alias(DayOfWeek(SampleTable.colTimestamp), 'dayofweek'),
	Alias(DayOfWeekISO(SampleTable.colTimestamp), 'dayofweekiso'),
	Alias(DayOfYear(SampleTable.colTimestamp), 'dayofyear'),
	Alias(Millennium(SampleTable.colTimestamp), 'millennium'),
	Alias(Century(SampleTable.colTimestamp), 'century'),
	Alias(Decade(SampleTable.colTimestamp), 'decade'),
	Alias(Epoch(SampleTable.colTimestamp), 'epoch'),
))
PrettyPrint(_)

_ = con.run(Get(SampleTable).values(
	Alias(SampleTable.colTimestampTZ, 'ts'),
	Alias(Year(SampleTable.colTimestampTZ), 'year'),
	Alias(Month(SampleTable.colTimestampTZ), 'month'),
	Alias(Day(SampleTable.colTimestampTZ), 'day'),
	Alias(Hour(SampleTable.colTimestampTZ), 'hour'),
	Alias(Minute(SampleTable.colTimestampTZ), 'minute'),
	Alias(Second(SampleTable.colTimestampTZ), 'second'),
	Alias(MilliSecond(SampleTable.colTimestampTZ), 'millisecond'),
	Alias(MicroSecond(SampleTable.colTimestampTZ), 'microsecond'),
	Alias(Quarter(SampleTable.colTimestampTZ), 'quarter'),
	Alias(Week(SampleTable.colTimestampTZ), 'week'),
	Alias(DayOfWeek(SampleTable.colTimestampTZ), 'dayofweek'),
	Alias(DayOfWeekISO(SampleTable.colTimestampTZ), 'dayofweekiso'),
	Alias(DayOfYear(SampleTable.colTimestampTZ), 'dayofyear'),
	Alias(Timezone(SampleTable.colTimestampTZ), 'timezone'),
	Alias(TimezoneHour(SampleTable.colTimestampTZ), 'timezonehour'),
	Alias(TimezoneMinute(SampleTable.colTimestampTZ), 'timezoneminute'),
	Alias(TimezoneHourMinute(SampleTable.colTimestampTZ), 'timezonehourminute'),
	Alias(Millennium(SampleTable.colTimestampTZ), 'millennium'),
	Alias(Century(SampleTable.colTimestampTZ), 'century'),
	Alias(Decade(SampleTable.colTimestampTZ), 'decade'),
	Alias(Epoch(SampleTable.colTimestampTZ), 'epoch'),
))
PrettyPrint(_)

_ = con.run(Get(SampleTable).values(
	Alias(SampleTable.colDate, 'dt'),
	Alias(Year(SampleTable.colDate), 'year'),
	Alias(Month(SampleTable.colDate), 'month'),
	Alias(Day(SampleTable.colDate), 'day'),
	Alias(Quarter(SampleTable.colDate), 'quarter'),
	Alias(Week(SampleTable.colDate), 'week'),
	Alias(DayOfWeek(SampleTable.colDate), 'dayofweek'),
	Alias(DayOfWeekISO(SampleTable.colDate), 'dayofweekiso'),
	Alias(DayOfYear(SampleTable.colDate), 'dayofyear'),
	Alias(Millennium(SampleTable.colDate), 'millennium'),
	Alias(Century(SampleTable.colDate), 'century'),
	Alias(Decade(SampleTable.colDate), 'decade'),
	Alias(Epoch(SampleTable.colDate), 'epoch'),
))
PrettyPrint(_)

_ = con.run(Get(SampleTable).values(
	Alias(SampleTable.colTime, 'ts'),
	Alias(Hour(SampleTable.colTime), 'hour'),
	Alias(Minute(SampleTable.colTime), 'minute'),
	Alias(Second(SampleTable.colTime), 'second'),
	Alias(MilliSecond(SampleTable.colTime), 'millisecond'),
	Alias(MicroSecond(SampleTable.colTime), 'microsecond'),
	Alias(Epoch(SampleTable.colTime), 'epoch'),
))
PrettyPrint(_)


con.commit()