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

con.commit()