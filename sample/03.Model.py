# -*- coding: utf-8 -*-

from Liquirizia.DataAccessObject import Helper

from Liquirizia.DataAccessObject.Properties.Database import Filter

from Liquirizia.DataAccessObject.Implements.PostgreSQL import *
from Liquirizia.DataAccessObject.Implements.PostgreSQL.Types import *
from Liquirizia.DataAccessObject.Implements.PostgreSQL.Functions import *
from Liquirizia.DataAccessObject.Implements.PostgreSQL.Orders import *
from Liquirizia.DataAccessObject.Implements.PostgreSQL.Joins import *
from Liquirizia.DataAccessObject.Implements.PostgreSQL.Exprs import *

from Liquirizia.Validator import Validator
from Liquirizia.Validator.Patterns import (
	IsString,
	IsSizeOf,
	IsIn,
)

from Liquirizia.DataModel import Handler
from Liquirizia.Utils import *

from random import randrange, sample
from datetime import datetime
from decimal import Decimal as decimal, Context as context

from typing import Dict

# table
class StudentUpdated(Handler):
	def __call__(self, m, o, v, pv):
		print('{} of {} is changed {} to {} in {}'.format(
			o.key,
			m.__model__,
			pv,
			v,
			m,
		))
		changed = m.__cursor__.run(Update(Student).set(
			**{o.name: v}
		).where(
			EqualTo(Student.id, m.id)
		))
		PrettyPrint(changed)
		return
class Student(
	Table,
	name='STUDENT',
	sequences=(
		Sequence(name='SEQ_STUDENT', type=INT),
	),
	constraints=(
		PrimaryKey(name='PK_STUDENT', cols=Column('ID')),
		Check(name='CHK_STUDENT_IS_DELETED', expr=In(Column('IS_DELETED'), (Value('Y'), Value('N')))),
	),
	indexes=(
		IndexUnique(name='UK_STUDENT_CODE', exprs=Ascend(Column('CODE'))),
		Index(name='IDX_STUDENT_IS_DELETED', exprs=Ascend(Column('IS_DELETED'))),
		Index(name='IDX_STUDENT_AT_CREATED', exprs=Descend(Column('AT_CREATED'))),
		Index(name='IDX_STUDENT_AT_UPDATED', exprs=Descend(Column('AT_UPDATED'))),
	),
	fn=StudentUpdated(),
):
	id = INT(name='ID', default=NextVal('SEQ_STUDENT'))
	code = TEXT('CODE')
	name = TEXT(name='NAME')
	metadata = BYTEARRAY(name='METADATA')
	atCreated = TIMESTAMP(name='AT_CREATED', default=Now())
	atUpdated = TIMESTAMP(name='AT_UPDATED', null=True)
	isDeleted = CHAR(name='IS_DELETED', size=1, default=Value('N'), va=Validator(IsString(IsSizeOf(1), IsIn('Y', 'N'))))
	isUpdated = BOOL(name='IS_UPDATED', default=Value(False))


class ClassUpdated(Handler):
	def __call__(self, m, o, v, pv):
		print('{} of {} is changed {} to {} in {}'.format(
			o.key,
			m.__model__,
			pv,
			v,
			m,
		))
		changed = m.__cursor__.run(Update(Class).set(
			**{o.name: v}
		).where(
			EqualTo(Class.id, m.id)
		))
		PrettyPrint(changed)
		return
class Class(
	Table,
	name='CLASS',
	sequences=(
		Sequence('SEQ_CLASS', type=INT),
	),
	constraints=(
		PrimaryKey(name='PK_CLASS', cols=Column('ID')),
		Check(name='CHK_CLASS_IS_DELETED', expr=In(Column('IS_DELETED'), (Value('Y'), Value('N')))),
	),
	indexes=(
		IndexUnique(name='UK_CLASS_CODE', exprs=Ascend(Column('CODE'))),
		Index(name='IDX_CLASS_IS_DELETED', exprs=Ascend(Column('IS_DELETED'))),
		Index(name='IDX_CLASS_AT_CREATED', exprs=Descend(Column('AT_CREATED'))),
		Index(name='IDX_CLASS_AT_UPDATED', exprs=Descend(Column('AT_UPDATED'))),
	),
	fn=ClassUpdated(),
):
	id = INT(name='ID', default=NextVal('SEQ_CLASS'))
	code = TEXT(name='CODE')
	name = TEXT(name='NAME')
	atCreated = TIMESTAMP(name='AT_CREATED', default=Now())
	atUpdated = TIMESTAMP(name='AT_UPDATED', null=True)
	isDeleted = CHAR(name='IS_DELETED', size=1, default=Value('N'), va=Validator(IsIn('Y', 'N')))
	isUpdated = BOOL(name='IS_UPDATED', default=Value(False))


class StudentClassUpdated(Handler):
	def __call__(self, m, o, v, pv):
		print('{} of {} is changed {} to {} in {}'.format(
			o.key,
			m.__model__,
			pv,
			v,
			m,
		))
		changed = m.__cursor__.run(Update(StudentOfClass).set(
			**{o.name: v}
		).where(
			EqualTo(StudentOfClass.studentId, m.studentId),
			EqualTo(StudentOfClass.classId, m.classId),
		))
		PrettyPrint(changed)
		return
class StudentOfClass(
	Table,
	name='STUDENT_CLASS',
	constraints=(
		PrimaryKey(name='PK_STUDENT_CLASS', cols=(Column('STUDENT'), Column('CLASS'))),
		ForeignKey(name='FK_STUDENT_CLASS_STUDENT', cols=Column('STUDENT'), reference=Student, referenceCols=Student.id),
		ForeignKey(name='FK_STUDENT_CLASS_CLASS', cols=Column('STUDENT'), reference=Class, referenceCols=Class.id),
	),
	indexes=(
		Index(name='IDX_STUDENT_CLASS_SCORE', exprs=Ascend(Column('SCORE'))),
		Index(name='IDX_STUDENT_CLASS_AT_CREATED', exprs=Descend('AT_CREATED')),
		Index(name='IDX_STUDENT_CLASS_AT_UPDATED', exprs=Descend('AT_UPDATED')),
	),
	fn=StudentClassUpdated(),
):
	studentId = INT(name='STUDENT')
	studentName = TEXT(name='STUDENT_NAME')
	classId = INT(name='CLASS')
	className = TEXT(name='CLASS_NAME')
	score = FLOAT(name='SCORE', null=True)
	rate = DECIMAL(name='RATE', precision=1, scale=3, null=True)
	tests = ARRAY(name='TESTS', type='INTEGER', null=True)
	vector = VECTOR(name='POSISTION', size=3, null=True)
	metadata = JSON(name='METADATA', null=True)
	atCreated = TIMESTAMP(name='AT_CREATED', timezone=True, default=Now())
	atCreatedDate = DATE(name='AT_CREATED_DATE', default=Now())
	atCreatedTime = TIME(name='AT_CREATED_TIME', default=Now())
	atUpdated = TIMESTAMP(name='AT_UPDATED', null=True)
	atUpdatedDate = DATE(name='AT_UPDATED_DATE', null=True)
	atUpdatedTime = TIME(name='AT_UPDATED_TIME', null=True)
	isUpdated = BOOL(name='IS_UPDATED', default=Value(False))


# View 
class StatOfStudent(
	View,
	name='STAT_STUDENT',
	executor=Select(Student).join(
		LeftOuter(StudentOfClass, EqualTo(Student.id, StudentOfClass.studentId)),
		LeftOuter(Class, EqualTo(StudentOfClass.classId, Class.id)),
	).where(
		EqualTo(Student.isDeleted, 'N')
	).group(
		Student.id
	).values(
		Student.id,
		Student.name,
		Alias(Count(Class.id), 'COUNT'),
		Alias(Sum(StudentOfClass.score), 'SUM'),
		Alias(Average(StudentOfClass.score), 'AVG'),
		Student.atCreated,
		Student.atUpdated,
	).order(
		Ascend(Student.id)
	)
):
	id = INT(name='ID')
	name = TEXT(name='NAME')
	count = INT(name='COUNT')
	sum = FLOAT(name='SUM', null=True)
	average = FLOAT(name='AVG', null=True)
	atCreated = TIMESTAMP(name='AT_CREATED')
	atUpdated = TIMESTAMP(name='AT_UPDATED', null=True)


class StatOfClass(
	View,
	name='STAT_CLASS',
	executor=Select(Class).join(
		LeftOuter(StudentOfClass, EqualTo(Class.id, StudentOfClass.classId)),
		LeftOuter(Student), EqualTo(StudentOfClass.studentId, Student.id)
	).where(
		EqualTo(Class.isDeleted, 'N')
	).group(
		Class.id
	).values(
		Class.id,
		Class.name,
		Alias(Count(Student.id), 'COUNT'),
		Alias(Sum(StudentOfClass.score), 'SUM'),
		Alias(Average(StudentOfClass.score), 'AVG'),
		Class.atCreated,
		Class.atUpdated,
	).order(
		Ascend(Class.id)
	)
):
	id = INT(name='ID')
	name = TEXT(name='NAME')
	count = INT(name='COUNT')
	sum = FLOAT(name='SUM', null=True)
	average = FLOAT(name='AVG', null=True)
	atCreated = TIMESTAMP(name='AT_CREATED')
	atUpdated = TIMESTAMP(name='AT_UPDATED', null=True)


if __name__ == '__main__':

	# Set connection
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

	# Get Connection
	con: Connection = Helper.Get('Sample')
	con.begin()
	
	con.run(Drop(StatOfClass))
	con.run(Drop(StatOfStudent))
	con.run(Drop(StudentOfClass))
	con.run(Drop(Class))
	con.run(Drop(Student))
	con.run(Create(Student))
	con.run(Create(Class))
	con.run(Create(StudentOfClass))
	con.run(Create(StatOfStudent))
	con.run(Create(StatOfClass))

	STUDENT = [
		['SU970001', 'Koo Hayoon', 'README.md'],
		['SU970002', 'Ma Youngin', 'README.md'],
		['SU970003', 'Kang Miran', 'README.md'],
		['SU970004', 'Song Hahee', 'README.md'],
	]

	CLASS = [
		['CS000', 'What is Computer Science'],
		['CS100', 'Programming Language'],
		['CS101', 'C'],
		['CS102', 'C++'],
		['CS103', 'Java'],
		['CS104', 'JavaScript'],
		['CS105', 'Python'],
		['CS120', 'Operating System'],
		['CS130', 'Network'],
		['CS131', 'TCP/IP'],
		['CS132', 'HTTP'],
		['CS140', 'Database'],
		['CS141', 'Practice of RDBMS with MySQL'],
		['CS142', 'Practice of RDBMS with PostgreSQL'],
		['CS150', 'Distributed System'],
		['CS160', 'AI(Artificial Intelligence)'],
	]

	STUDENT_OF_CLASS = [
		['SU970001', 'CS000'],
		['SU970001', 'CS100'],
		['SU970001', 'CS120'],
		['SU970001', 'CS130'],
		['SU970002', 'CS000'],
		['SU970002', 'CS100'],
		['SU970002', 'CS101'],
		['SU970002', 'CS102'],
		['SU970003', 'CS000'],
		['SU970003', 'CS120'],
		['SU970003', 'CS130'],
		['SU970003', 'CS140'],
		['SU970003', 'CS150'],
		['SU970004', 'CS000'],
		['SU970004', 'CS130'],
		['SU970004', 'CS132'],
		['SU970004', 'CS140'],
		['SU970004', 'CS142'],
		['SU970004', 'CS150'],
	]

	students = []
	for _ in STUDENT:
		s = con.run(
			Insert(Student).values(
				code=_[0],
				name=_[1],
				metadata=open(_[2], mode='rb').read(),
			),
			fetch=Student,
		)
		PrettyPrint(s)
		students.append(s)
	
	for _ in students:
		PrettyPrint(_)
		_.atUpdated = datetime.now()
		_.isUpdated = True
		PrettyPrint(_)
	
	students = con.run(Select(Student), fetch=Student)
	PrettyPrint(students)

	classes = []
	for _ in CLASS:
		classes.append(con.run(
			Insert(Class).values(
				code=_[0],
				name=_[1],
			),
			fetch=Class,
		))
	
	for _ in classes:
		PrettyPrint(_)
		_.atUpdated = datetime.now()
		_.isUpdated = True
		PrettyPrint(_)
	
	classes = con.run(Select(Class), fetch=Class)
	PrettyPrint(classes)
	
	for scode, ccode in STUDENT_OF_CLASS:
		s = con.run(Get(Student).where(EqualTo(Student.code, scode)), fetch=Student)
		c = con.run(Get(Class).where(EqualTo(Class.code, ccode)), fetch=Class)
		costs = []
		for i in range(0, randrange(5, 10)):
			costs.append(randrange(0, 100))
		exec = Insert(StudentOfClass).values(
			studentId=s.id,
			studentName=s.name,
			classId=c.id,
			className=c.name,
			score=sum(costs)/len(costs),
			rate=decimal(sum(costs)/len(costs), context=context(prec=1)),
			tests=costs,
			vector=[randrange(-10, 10), randrange(-10, 10), randrange(-10, 10)],
			metadata={},
		).on(
			StudentOfClass.studentId,
			StudentOfClass.classId,
		).set(
			studentName=s.name,
			className=c.name,
			score=sum(costs)/len(costs),
			rate=decimal(sum(costs)/len(costs), context=context(prec=1)),
			tests=costs,
			vector=[randrange(-10, 10), randrange(-10, 10), randrange(-10, 10)],
			metadata={},
			atUpdated=datetime.now(),
			isUpdated=True,
		)
		sc = con.run(exec)
		PrettyPrint(sc)
	
	studentsOfClasses = con.run(Select(StudentOfClass), fetch=StudentOfClass)
	PrettyPrint(studentsOfClasses)

	for _ in studentsOfClasses if studentsOfClasses else []:
		PrettyPrint(_)
		costs = []
		for i in range(0, randrange(5, 10)):
			costs.append(randrange(0, 100))
		_.metadata={
			'costs': costs
		}
		_.isUpdated=True
		PrettyPrint(_)
	
	studentsOfClasses = con.run(Select(StudentOfClass), fetch=StudentOfClass)
	PrettyPrint(studentsOfClasses)

	for _ in studentsOfClasses if studentsOfClasses else []:
		costs = []
		for i in range(0, randrange(5, 10)):
			costs.append(randrange(0, 100))
		o = con.run(
			Update(StudentOfClass).set(
				score=sum(costs)/len(costs),
				tests=costs,
				vector=[randrange(-10, 10), randrange(-10, 10), randrange(-10, 10)],
				metadata={
					'tests': costs,
					'updated': str(datetime.now()),
				},
				atUpdated=datetime.now(),
				isUpdated=True,
			).where(
				EqualTo(StudentOfClass.studentId, _.studentId),
				EqualTo(StudentOfClass.classId, _.classId),
			),
			fetch=StudentOfClass,
		)
		PrettyPrint(o)
	
	studentsOfClasses = con.run(Select(StudentOfClass), fetch=StudentOfClass)
	PrettyPrint(studentsOfClasses)
	
	for _ in studentsOfClasses if studentsOfClasses else []:
		PrettyPrint(_)
		costs = []
		for i in range(0, randrange(5, 10)):
			costs.append(randrange(0, 100))
		_.score = randrange(10, 45)/10
		_.tests = costs
		_.vector=[randrange(-10, 10), randrange(-10, 10), randrange(-10, 10)]
		_.atUpdated = datetime.now()
		PrettyPrint(_)
	
	studentsOfClasses = con.run(Select(StudentOfClass))
	PrettyPrint(studentsOfClasses)
	
	exec = Select(Student).join(
			LeftOuter(StudentOfClass, EqualTo(Student.id, StudentOfClass.studentId)),
			LeftOuter(Class, EqualTo(StudentOfClass.classId, Class.id)),
		).values(
			Alias(Student.id, 'STUDENT'),
			Alias(Student.name, 'NAME'),
			Alias(Count(StudentOfClass.score), 'COUNT'),
			Alias(Sum(StudentOfClass.score), 'SUM'),
			Alias(Average(StudentOfClass.score), 'AVG'),
			Alias(Min(StudentOfClass.atCreated), 'AT_CREATED'),
			Alias(Max(StudentOfClass.atUpdated), 'AT_UPDATED'),
		).where(
			EqualTo(Student.isDeleted, 'N')
		).group(
			Student.id,
		).having(
			GreaterEqualTo(Average(StudentOfClass.score), 3)
		).order(
			Ascend(Student.id),
			Descend(Average(StudentOfClass.score)),
			Ascend(Sum(StudentOfClass.score)),
		).limit(0, 10)

	class RowFilter(Filter):
		def __call__(self, row: Dict) -> Dict:
			return {
				'id': row['STUDENT'],
				'name': row['NAME'],
				'sum': row['SUM'],
				'avg': row['AVG'],
				'updated': max(row['AT_CREATED'].isoformat(), row['AT_UPDATED'].isoformat()),
			}
	PrettyPrint(con.run(exec, filter=RowFilter()))

	con.run(Delete(StudentOfClass).where(
		EqualTo(StudentOfClass.studentName, 'Song Hahee')
	))

	PrettyPrint(con.run(exec))
	print(Select(StatOfStudent).query)
	statOfStudent = con.run(Select(StatOfStudent))
	PrettyPrint(statOfStudent)
	
	statOfStudent = con.run(
		Select(StatOfStudent).where(
			GreaterThan(StatOfStudent.average, 3)
		)
	)
	PrettyPrint(statOfStudent)
	
	statOfClass = con.run(Select(StatOfClass))
	PrettyPrint(statOfClass)
	
	statOfClass = con.run(
		Select(StatOfClass).where(
			EqualTo(StatOfClass.count, 0)
		),
		fetch=StatOfClass,
	)
	PrettyPrint(statOfClass)

	con.run(Drop(StatOfClass))
	con.run(Drop(StatOfStudent))
	con.run(Drop(StudentOfClass))
	con.run(Drop(Class))
	con.run(Drop(Student))

	con.commit()
