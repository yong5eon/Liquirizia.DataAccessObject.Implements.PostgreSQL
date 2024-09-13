# -*- coding: utf-8 -*-

from Liquirizia.DataAccessObject import Helper

from Liquirizia.DataAccessObject.Errors import *
from Liquirizia.DataAccessObject.Properties.Database.Errors import *

from Liquirizia.DataAccessObject.Implements.PostgreSQL import *
from Liquirizia.DataAccessObject.Implements.PostgreSQL.Model import *
from Liquirizia.DataAccessObject.Implements.PostgreSQL.Type import *
from Liquirizia.DataAccessObject.Implements.PostgreSQL.Constraint import *
from Liquirizia.DataAccessObject.Implements.PostgreSQL.Executor import *
from Liquirizia.DataAccessObject.Implements.PostgreSQL.Executor.Filters import *
from Liquirizia.DataAccessObject.Implements.PostgreSQL.Executor.Orders import *
from Liquirizia.DataAccessObject.Implements.PostgreSQL.Executor.Joins import *
from Liquirizia.DataAccessObject.Implements.PostgreSQL.Executor.Exprs import *
from Liquirizia.DataAccessObject.Implements.PostgreSQL.Executor.Functions import *

from Liquirizia.DataModel import Model, Handler
from Liquirizia.Validator.Patterns import IsIn
from Liquirizia.Util import *

from random import randrange, sample
from datetime import datetime
from decimal import Decimal as decimal, Context as context


# table
class StudentUpdated(Handler):
	def __call__(self, model, obj, attr, value, prev):
		print('{} of {} is changed {} to {} in {}'.format(
			'{}({})'.format(attr.name, attr.key),
			'{}({})'.format(model.__name__, model.__properties__['name']),
			prev,
			value,
			obj,
		))
		changed = obj.__cursor__.run(Update(Student).set(
			**{attr.name: value}
		).where(
			IsEqualTo(Student.id, obj.id)
		))
		print(changed)
		return
@Table(
	name = 'STUDENT',
	constraints=(
		PrimaryKey(name='PK_STUDENT', cols='ID'),
		Unique(name='UK_STUDENT_CODE', cols='CODE'),
		Check(name='CHK_STUDENT_IS_DELETED', expr=In('IS_DELETED', ('Y', 'N'))),
	),
	indexes=(
		Index(name='IDX_STUDENT_IS_DELETED', colexprs='IS_DELETED'),
		Index(name='IDX_STUDENT_AT_CREATED', colexprs='AT_CREATED DESC'),
		Index(name='IDX_STUDENT_AT_UPDATED', colexprs='AT_UPDATED DESC'),
	),
	fn=StudentUpdated(),
)
class Student(Model):
	id = Integer(name='ID', seq=Sequence(name='SEQ_STUDENT', type='INTEGER'), default=NextVal('SEQ_STUDENT'))
	code = Text('CODE')
	name = Text(name='NAME')
	metadata = ByteArray(name='METADATA')
	atCreated = Timestamp(name='AT_CREATED', default=Now())
	atUpdated = Timestamp(name='AT_UPDATED', null=True)
	isDeleted = Text(name='IS_DELETED', default='N', vaps=IsIn('Y', 'N'))
	isUpdated = Bool(name='IS_UPDATED', default=False)


class ClassUpdated(Handler):
	def __call__(self, model, obj, attr, value, prev):
		print('{} of {} is changed {} to {} in {}'.format(
			'{}({})'.format(attr.name, attr.key),
			'{}({})'.format(model.__name__, model.__properties__['name']),
			prev,
			value,
			obj,
		))
		changed = obj.__cursor__.run(Update(Class).set(
			**{attr.name: value}
		).where(
			IsEqualTo(Class.id, obj.id)
		))
		print(changed)
		return
@Table(
	name='CLASS',
	constraints=(
		PrimaryKey(name='PK_CLASS', cols='ID'),
		Unique(name='UK_CLASS_CODE', cols='CODE'),
		Check(name='CHK_CLASS_IS_DELETED', expr=In('IS_DELETED', ('Y', 'N'))),
	),
	indexes=(
		Index(name='IDX_CLASS_IS_DELETED', colexprs='IS_DELETED'),
		Index(name='IDX_CLASS_AT_CREATED', colexprs='AT_CREATED DESC'),
		Index(name='IDX_CLASS_AT_UPDATED', colexprs='AT_UPDATED DESC'),
	),
	fn=ClassUpdated(),
)
class Class(Model):
	id = Integer(name='ID', seq=Sequence(name='SEQ_CLASS', type='INTEGER'), default=NextVal('SEQ_CLASS'))
	code = Text(name='CODE')
	name = Text(name='NAME')
	atCreated = Timestamp(name='AT_CREATED', default=Now())
	atUpdated = Timestamp(name='AT_UPDATED', null=True)
	isDeleted = Text(name='IS_DELETED', default='N', vaps=IsIn('Y', 'N'))
	isUpdated = Bool(name='IS_UPDATED', default=False)


class StudentClassUpdated(Handler):
	def __call__(self, model, obj, attr, value, prev):
		print('{} of {} is changed {} to {} in {}'.format(
			'{}({})'.format(attr.name, attr.key),
			'{}({})'.format(model.__name__, model.__properties__['name']),
			prev,
			value,
			obj,
		))
		changed = obj.__cursor__.run(Update(StudentOfClass).set(
			**{attr.name: value}
		).where(
			IsEqualTo(StudentOfClass.studentId, obj.studentId),
			IsEqualTo(StudentOfClass.classId, obj.classId),
		))
		print(changed)
		return
@Table(
	name='STUDENT_CLASS',
	constraints=(
		PrimaryKey(name='PK_STUDENT_CLASS', cols=('STUDENT', 'CLASS')),
		ForeignKey(name='FK_STUDENT_CLASS_STUDENT', cols='STUDENT', reference='STUDENT', referenceCols='ID'),
		ForeignKey(name='FK_STUDENT_CLASS_CLASS', cols='STUDENT', reference='CLASS', referenceCols='ID'),
	),
	indexes=(
		Index(name='IDX_STUDENT_CLASS_SCORE', colexprs='SCORE'),
		Index(name='IDX_STUDENT_CLASS_AT_CREATED', colexprs='AT_CREATED DESC'),
		Index(name='IDX_STUDENT_CLASS_AT_UPDATED', colexprs='AT_UPDATED DESC'),
	),
	fn=StudentClassUpdated(),
)
class StudentOfClass(Model):
	studentId = Integer(name='STUDENT')
	studentName = Text(name='STUDENT_NAME')
	classId = Integer(name='CLASS')
	className = Text(name='CLASS_NAME')
	score = Float(name='SCORE', null=True)
	rate = Decimal(name='RATE', precision=1, scale=3, null=True)
	tests = Array(name='TESTS', type='INTEGER', null=True)
	vector = Vector(name='POSISTION', size=3, null=True)
	metadata = JavaScriptObjectNotation(name='METADATA', null=True)
	atCreated = Timestamp(name='AT_CREATED', timezone=True, default=Now())
	atCreatedDate = Date(name='AT_CREATED_DATE', default=Now())
	atCreatedTime = Time(name='AT_CREATED_TIME', timezone=True, default=Now())
	atUpdated = Timestamp(name='AT_UPDATED', null=True)
	atUpdatedDate = Date(name='AT_UPDATED_DATE', null=True)
	atUpdatedTime = Time(name='AT_UPDATED_TIME', null=True)
	isUpdated = Bool(name='IS_UPDATED', default=False)


# View 
@View(
	name='STAT_STUDENT',
	executor=Select(Student).join(
		LeftOuter(StudentOfClass, IsEqualTo(Student.id, StudentOfClass.studentId)),
		LeftOuter(Class, IsEqualTo(StudentOfClass.classId, Class.id)),
	).where(
		IsEqualTo(Student.isDeleted, 'N')
	).groupBy(
		Student.id
	).values(
		Student.id,
		Student.name,
		Count(Class.id, 'COUNT'),
		Sum(StudentOfClass.score, 'SUM'),
		Average(StudentOfClass.score, 'AVG'),
		Student.atCreated,
		Student.atUpdated,
	).orderBy(
		Ascend(Student.id)
	)
)
class StatOfStudent(Model):
	id = Integer(name='ID')
	name = Text(name='NAME')
	count = Integer(name='COUNT')
	sum = Float(name='SUM', null=True)
	average = Float(name='AVG', null=True)
	atCreated = Timestamp(name='AT_CREATED')
	atUpdated = Timestamp(name='AT_UPDATED', null=True)


@View(
	name='STAT_CLASS',
	executor=Select(Class).join(
		LeftOuter(StudentOfClass, IsEqualTo(Class.id, StudentOfClass.classId)),
		LeftOuter(Student), IsEqualTo(StudentOfClass.studentId, Student.id)
	).where(
		IsEqualTo(Class.isDeleted, 'N')
	).groupBy(
		Class.id
	).values(
		Class.id,
		Class.name,
		Count(Student.id, 'COUNT'),
		Sum(StudentOfClass.score, 'SUM'),
		Average(StudentOfClass.score, 'AVG'),
		Class.atCreated,
		Class.atUpdated,
	).orderBy(
		Ascend(Class.id)
	)
)
class StatOfClass(Model):
	id = Integer(name='ID')
	name = Text(name='NAME')
	count = Integer(name='COUNT')
	sum = Float(name='SUM', null=True)
	average = Float(name='AVG', null=True)
	atCreated = Timestamp(name='AT_CREATED')
	atUpdated = Timestamp(name='AT_UPDATED', null=True)


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
			persistent=True,  # Is Use Connection Pool, True/False
			min=1, # Minimum Connections in Pool
			max=2, # Maximum Connections in Pool
		)
	)

	# Get Connection
	con = Helper.Get('Sample')
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
		['SU970001', 'Koo Hayoon', 'VERSION'],
		['SU970002', 'Ma Youngin', 'VERSION'],
		['SU970003', 'Kang Miran', 'VERSION'],
		['SU970004', 'Song Hahee', 'VERSION'],
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
			)
		)
		PrettyPrint(s)
		students.append(s)
	
	for _ in students:
		PrettyPrint(_)
		_.atUpdated = datetime.now()
		_.isUpdated = True
		PrettyPrint(_)
	
	students = con.run(Select(Student))
	PrettyPrint(students)

	classes = []
	for _ in CLASS:
		classes.append(con.run(
			Insert(Class).values(
				code=_[0],
				name=_[1],
			)
		))
	
	for _ in classes:
		PrettyPrint(_)
		_.atUpdated = datetime.now()
		_.isUpdated = True
		PrettyPrint(_)
	
	classes = con.run(Select(Class))
	PrettyPrint(classes)
	
	for scode, ccode in STUDENT_OF_CLASS:
		s = con.run(Get(Student).where(IsEqualTo(Student.code, scode)).to(Student))
		c = con.run(Get(Class).where(IsEqualTo(Class.code, ccode)).to(Class))
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
		)
		sc = con.run(exec)
		PrettyPrint(sc)
	
	studentsOfClasses = con.run(Select(StudentOfClass).to(StudentOfClass))
	PrettyPrint(studentsOfClasses)

	for _ in studentsOfClasses:
		PrettyPrint(_)
		costs = []
		for i in range(0, randrange(5, 10)):
			costs.append(randrange(0, 100))
		_.tests=costs
		_.metadata={
			'costs': costs
		}
		_.isUpdated=True
		PrettyPrint(_)
	
	studentsOfClasses = con.run(Select(StudentOfClass).to(StudentOfClass))
	PrettyPrint(studentsOfClasses)

	for _ in studentsOfClasses:
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
				IsEqualTo(StudentOfClass.studentId, _.studentId),
				IsEqualTo(StudentOfClass.classId, _.classId),
			)
		)
		PrettyPrint(o)
	
	studentsOfClasses = con.run(Select(StudentOfClass).to(StudentOfClass))
	PrettyPrint(studentsOfClasses)
	
	for _ in studentsOfClasses:
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
			LeftOuter(StudentOfClass, IsEqualTo(Student.id, StudentOfClass.studentId)),
			LeftOuter(Class, IsEqualTo(StudentOfClass.classId, Class.id)),
		).values(
			Alias(Student.id, 'STUDENT'),
			Alias(Student.name, 'NAME'),
			Count(StudentOfClass.score, 'COUNT'),
			Sum(StudentOfClass.score, 'SUM'),
			Average(StudentOfClass.score, 'AVG'),
			Min(StudentOfClass.atCreated, 'AT_CREATED'),
			Max(StudentOfClass.atUpdated, 'AT_UPDATED'),
		).where(
			IsEqualTo(Student.isDeleted, 'N')
		).groupBy(
			Student.id,
		).having(
			IsGreaterEqualTo(Average(StudentOfClass.score), 3)
		).orderBy(
			Ascend(Student.id),
			Descend(Average(StudentOfClass.score)),
			Ascend(Sum(StudentOfClass.score)),
		).limit(0, 10)

	PrettyPrint(con.run(exec))

	con.run(Delete(StudentOfClass).where(
		IsEqualTo(StudentOfClass.studentName, 'Song Hahee')
	))

	PrettyPrint(con.run(exec))
	print(Select(StatOfStudent).query)
	statOfStudent = con.run(Select(StatOfStudent))
	PrettyPrint(statOfStudent)
	
	statOfStudent = con.run(
		Select(StatOfStudent).where(
			IsGreaterThan(StatOfStudent.average, 3)
		)
	)
	PrettyPrint(statOfStudent)
	
	statOfClass = con.run(Select(StatOfClass))
	PrettyPrint(StatOfClass)
	
	statOfClass = con.run(
		Select(StatOfClass).where(
			IsEqualTo(StatOfClass.count, 0)
		)
	)
	PrettyPrint(statOfClass)

	con.run(Drop(StatOfClass))
	con.run(Drop(StatOfStudent))
	con.run(Drop(StudentOfClass))
	con.run(Drop(Class))
	con.run(Drop(Student))

	con.commit()
