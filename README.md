# Liquirizia.DataAccessObject.Implements.PostgreSQL

DataAccessObject of PostgreSQL for Liquirizia

## 예제

- [연결 및 실행 예제](sample/01.Connection.py)
- [테이블과 데이터 유형 예제](sample/02.Table.py)
- [모델링 예제](sample/03.Model.py)

### 실행자 예제

- [실행자 예제](sample/11.Insert.py)

### 표현식 및 함수 예제

- [표현식 예제](sample/21.Expression.py)

## 도커 빌드 및 실행

```shell
> docker image build --file=res/PostgreSQL.15.docker --tag=postgresql:15 .
> docker container run --name=postgresql --detach --publish=5432:5432 postgresql:15
```
