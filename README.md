# Liquirizia.DataAccessObject.Implements.PostgreSQL
PostgreSQL Data Access Object for Liquirizia

## 사용 방법
```python
# -*- coding: utf-8 -*-

from Liquirizia.DataAccessObject import DataAccessObjectHelper, DataAccessObjectError
from Liquirizia.DataAccessObject.Errors import *
from Liquirizia.DataAccessObject.Properties.Database.Errors import *

from Liquirizia.DataAccessObject.Implements.PostgreSQL import DataAccessObject, DataAccessObjectConfiguration

import sys

if __name__ == '__main__':

	con = None

	try:
		# Set connection
		DataAccessObjectHelper.Set(
			'Sample',
			DataAccessObject,
			DataAccessObjectConfiguration(
				host='YOUR_POSTGRESQL_HOST',  # PostgreSQL Database Host Address
				port=YOUR_POSTGRESQL_PORT,  # PostgreSQL Database Host Port
				database='YOUR_DATABASE',  # Database Name
				username='YOUR_USER',  # Database User
				password='YOUR_PASSWORD',  # Database Password for User
				persistent=True,  # Is Persistent Connection, True/False
			)
		)

		# Get Connection
		con = DataAccessObjectHelper.Get('Sample')
	except DataAccessObjectConnectionError as e:
		print(str(e), file=sys.stderr)
		exit(-1)
	except Exception as e:
		print(str(e), file=sys.stderr)
		exit(-1)

	try:
		con.begin()

		con.execute('DROP TABLE IF EXISTS LOG')
		con.execute(
			'''
			CREATE TABLE IF NOT EXISTS LOG (
				ID SERIAL NOT NULL,
				TEXT TEXT NOT NULL,
				CREATED TIMESTAMP NOT NULL DEFAULT NOW(),
				CONSTRAINT PK_LOG PRIMARY KEY(ID)
			)
			'''
		)
		con.execute("INSERT INTO LOG(TEXT) VALUES('TEST1')")
		con.execute("INSERT INTO LOG(TEXT) VALUES('TEST2')")
		con.execute("INSERT INTO LOG(TEXT) VALUES('TEST3')")

		con.commit()
	except DataAccessObjectExecuteError as e:
		con.rollback()
		print(str(e), file=sys.stderr)
	except DataAccessObjectCursorError as e:
		con.rollback()
		print(str(e), file=sys.stderr)
	except DataAccessObjectCommitError as e:
		print(str(e), file=sys.stderr)
	except DataAccessObjectRollBackError as e:
		print(str(e), file=sys.stderr)
	except DataAccessObjectConnectionClosedError as e:
		print('Connection is closed, {}'.format(str(e)), file=sys.stderr)
	except DataAccessObjectError as e:
		print('Error, {}'.format(str(e)), file=sys.stderr)
	except Exception as e:
		print(str(e), file=sys.stderr)

	try:
		con.execute('SELECT * FROM LOG')

		rows = con.rows()

		for i, row in enumerate(rows):
			print('{} : {}'.format(i, row), file=sys.stdout)

		con.execute('DROP TABLE IF EXISTS LOG')
	except DataAccessObjectExecuteError as e:
		con.rollback()
		print(str(e), file=sys.stderr)
	except DataAccessObjectCursorError as e:
		con.rollback()
		print(str(e), file=sys.stderr)
	except DataAccessObjectConnectionClosedError as e:
		print('Connection is closed, {}'.format(str(e)), file=sys.stderr)
	except DataAccessObjectError as e:
		print('Error, {}'.format(str(e)), file=sys.stderr)
	except Exception as e:
		print(str(e), file=sys.stderr)
```
