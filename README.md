# Liquirizia.DataAccessObject.Implements.PostgreSQL

DataAccessObject of PostgreSQL for Liquirizia

## 예제

- [연결 및 실행 예제](sample/Connection.py)
- [테이블과 데이터 유형 예제](sample/Table.py)
- [표현식 예제](sample/Expression.py)
- [모델링 예제](sample/Model.py)

## 도커 빌드 및 실행

```shell
> docker image build --file=res/PostgreSQL.15.docker --tag=postgresql:15 .
> docker container run --name=postgresql --detach --publish=5432:5432 postgresql:15
```
